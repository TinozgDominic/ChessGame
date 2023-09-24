import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from copy import deepcopy
from collections import Counter
from src.pieces import Empty, Pawn, Knight, Bishop, Rook, Queen, King
import random

# Board
class BoardState():
    def __init__(self, white_under = True):
        self.previous = []
        self.white_under = white_under
        self.board = self.get_board()
        if not self.white_under:
            self.flip_board()
            self.white_under = False
        
        self.white_turn = True

        self.white_occupied, self.black_occupied = [], []
        self.get_occupied()
       
        self.game_over = False
        self.gamestate = 0

        self.log = []
        self.get_log()
        
    def get_board(self):
        board = [["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
                 ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                 ["--", "--", "--", "--", "--", "--", "--", "--"],
                 ["--", "--", "--", "--", "--", "--", "--", "--"],
                 ["--", "--", "--", "--", "--", "--", "--", "--"],
                 ["--", "--", "--", "--", "--", "--", "--", "--"],
                 ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                 ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        piece_maker = {"p": Pawn, "b": Bishop, "n": Knight, "r": Rook, "q": Queen, "k": King, "-": Empty}
        for r in range(8):
            for c in range(8):
                board[r][c] = piece_maker[board[r][c][1]](board[r][c])
        return board
    
    def get_occupied(self):
        white_occupied = [[0 for r in range(8)] for c in range(8)]
        black_occupied = [[0 for r in range(8)] for c in range(8)]
        for r in range(8):
            for c in range(8):
                occupied = self.board[r][c].get_occupied(self, [r, c])
                for occ in occupied:
                    row, col = occ
                    if self.board[r][c].color == "b":
                        black_occupied[row][col] = max(black_occupied[row][col], self.board[r][c].occupied_value)
                    elif self.board[r][c].color == "w":
                        white_occupied[row][col] = max(white_occupied[row][col], self.board[r][c].occupied_value)

        self.white_occupied = white_occupied
        self.black_occupied = black_occupied

    def get_valid_move(self, coord):
        moveset = self.get_move(coord)

        for i in range(len(moveset) - 1, - 1, - 1):
            test_state = deepcopy(self)
            test_state.make_move(coord = coord, destination = moveset[i])

            # Find the King coordinate
            for r in range(8):
                for c in range(8):
                    if test_state.white_turn:
                        if test_state.board[r][c].piece == "bk":
                            if test_state.board[r][c].is_check:
                                moveset.pop(i)
                                break
                    else:
                        if test_state.board[r][c].piece == "wk":
                            if test_state.board[r][c].is_check:
                                moveset.pop(i)
                                break

        return moveset

    def get_all_valid_move(self):
        move_list = []
        for r in range(8):
            for c in range(8):
                moveset = self.get_valid_move([r, c])
                for move in moveset:
                    move_list.append([[r, c], move])
        return move_list

    def get_move(self, coord):
        r, c = coord

        if (self.white_turn and self.board[r][c].color == "w") or (not self.white_turn and self.board[r][c].color == "b"):
            return self.board[r][c].get_move(self, coord)
        else:
            return []

    def make_move(self, coord, destination, display = None):
        r, c = coord
        r_des, c_des = destination

        # Pawn special
        if self.board[r][c].type == "p":
            # Enpassant
            if self.board[r][c].enpassant_square == destination:
                self.board[r][c_des] = Empty("--")
            # Promote
            elif r_des == 0 or r_des == 7:
                if display == None:
                    self.board[r][c] = Queen(self.board[r][c].color + "q")
                else:
                    promote_piece = display.promotion(self.board[r][c].color, destination)
                    promote_maker = {"q": Queen, "r": Rook, "b": Bishop, "n": Knight}
                    self.board[r][c] = promote_maker[promote_piece](self.board[r][c].color + promote_piece)

        # King special
        elif self.board[r][c].type == "k" and abs(c - c_des) == 2:
            is_short = True if (c_des > c and self.white_under) or (c_des < c and not self.white_under) else False
            if is_short:
                rook_square = c + 3 * (c_des - c) // 2
                self.board[r][(c + c_des) // 2] = self.board[r][rook_square]
                self.board[r][(c + c_des) // 2].castle_right = False
                self.board[r][rook_square] = Empty("--")
            else:
                rook_square = c + 4 * (c_des - c) // 2
                self.board[r][(c + c_des) // 2] = self.board[r][rook_square]
                self.board[r][(c + c_des) // 2].castle_right = False
                self.board[r][rook_square] = Empty("--")
            self.board[r][c].value = self.board[r][c].sign * 40.5

        self.board[r_des][c_des] = self.board[r][c]
        self.board[r][c] = Empty("--")
        
        # Set status after making move
        # Reset the enpassant
        for row in range(8):
            for col in range(8):
                if self.board[row][col].type == "p":
                    self.board[row][col].enpassant = False
                    self.board[row][col].enpassant_square = []
        # Set the enpassant
        if self.board[r_des][c_des].type == "p" and abs(r - r_des) == 2:
            # Enable the enpassant
            if c_des >= 1: # Left pawn
                if self.board[r_des][c_des].color != self.board[r_des][c_des - 1].color and self.board[r_des][c_des - 1].type == "p":
                    self.board[r_des][c_des - 1].enpassant = True
                    self.board[r_des][c_des - 1].enpassant_square = [(r + r_des) // 2, c]
                if c_des <= 6: # Right pawn
                    if self.board[r_des][c_des].color != self.board[r_des][c_des + 1].color and self.board[r_des][c_des + 1].type == "p":
                        self.board[r_des][c_des + 1].enpassant = True
                        self.board[r_des][c_des + 1].enpassant_square = [(r + r_des) // 2, c]
        # Update Castle right
        elif self.board[r_des][c_des].type == "r" or self.board[r_des][c_des].type == "k":
            self.board[r_des][c_des].castle_right = False

        self.white_turn = not self.white_turn
        self.get_occupied()
        self.get_check()
        self.get_log()
    
    def flip_board(self):
        new_board = deepcopy(self.board)
        for r in range(8):
            for c in range(8):
                if self.board[r][c].type == "p":
                    if self.board[r][c].enpassant_square != []:
                        r_e, c_e = self.board[r][c].enpassant_square
                        self.board[r][c].enpassant_square = [7 - r_e, 7 - c_e]
                new_board[7 - r][7 - c] = self.board[r][c]
        self.board = new_board
        self.white_under = not self.white_under
        if self.previous != []:
            r, c = self.previous[0]
            r_des, c_des = self.previous[1]
            self.previous = [[7 - r, 7 - c], [7 - r_des, 7 - c_des]]

    def get_check(self):
        # Find the King coordinate
        for r in range(8):
            for c in range(8):
                if self.board[r][c].piece == "bk":
                        self.board[r][c].is_check = True if self.white_occupied[r][c] != 0 else False
                if self.board[r][c].piece == "wk":
                    self.board[r][c].is_check = True if self.black_occupied[r][c] != 0 else False

    def get_gamestate(self):
        # Repitition
        counts = Counter(self.log)
        if any(count >= 3 for count in counts.values()):
            self.game_over = True
            self.gamestate = 0
        # Checkmate, Staltemate
        moveable = False
        white_king = []
        black_king = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c].piece == "wk":
                    white_king = [r, c]
                if self.board[r][c].piece == "bk":
                    black_king = [r, c]

                moveset = self.get_valid_move([r, c])
                if len(moveset) != 0:
                    moveable = True
                    break
        if not moveable:
            self.game_over = True
            if self.white_turn and self.board[white_king[0]][white_king[1]].is_check:
                self.gamestate = -1
            elif not self.white_turn and self.board[black_king[0]][black_king[1]].is_check:
                self.gamestate = 1
            else:
                self.gamestate = 0
        else: 
            self.game_over = False

    def get_board_value(self):
        if self.game_over:
            return self.gamestate * 40.0
        board_value = 0
        black_occupied = 0
        white_occupied = 0
        for r in range(8):
            for c in range(8):
                board_value += self.board[r][c].value
                black_occupied += self.black_occupied[r][c]
                white_occupied += self.white_occupied[r][c]
        return round(board_value + (white_occupied - black_occupied) * random.uniform(0.01, 0.02), 2)
        
    def get_log(self):
        board = ""
        for r in range(8):
            for c in range(8):
                board += self.board[r][c].piece
        self.log.append(board)


    
