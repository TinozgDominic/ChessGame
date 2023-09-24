from src.boardstate import BoardState
from src.display import Display
from src.computer import Computer

from copy import deepcopy

import pygame as pg
pg.init()


def main():
    boardstate = BoardState()
    display = Display()
    computer = Computer(depth = 2)

    white = "Player"
    black = "Player"
    
    display.draw_state(boardstate, white, black)
    

    running = True
    coord = []
    destination = []
    moveset = []
    movelog = [deepcopy(boardstate)]

    while running:
        if boardstate.game_over:
            display.draw_gamestate(boardstate)

        if ((white == "Computer" and boardstate.white_turn) or (black == "Computer" and not boardstate.white_turn)) and not boardstate.game_over:
            coord, destination = computer.make_move(boardstate, computer.depth)
            if coord != [] and destination != []:
                boardstate.make_move(coord = coord, destination = destination, display = None)
                boardstate.get_gamestate()

                boardstate.previous = [deepcopy(coord), deepcopy(destination)]
                movelog.append(deepcopy(boardstate))
                display.draw_state(boardstate, white, black)

            if boardstate.previous != []:
                display.draw_previous(boardstate.previous[0], boardstate.previous[1])
        
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()

            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0] // display.square_size
                row = location[1] // display.square_size - 1

                if row >= 0 and row <= 7 and col >= 0 and col <= 7:
                    if not boardstate.game_over and ((white == "Player" and boardstate.white_turn) or (black == "Player" and not boardstate.white_turn)):
                        if coord == [row, col]:
                            coord = []
                            display.draw_state(boardstate, white, black)
                        elif coord == []:
                            turn = "w" if boardstate.white_turn else "b"
                            chose = boardstate.board[row][col].color
                            if turn == chose:
                                coord = [row, col]
                                moveset = boardstate.get_valid_move(coord)
                                display.draw_moveable(boardstate.board, coord, moveset)
                        else:
                            destination = [row, col]

                            if destination in moveset:
                                boardstate.make_move(coord = coord, destination = destination, display = display)
                                boardstate.get_gamestate()
                                boardstate.previous = [deepcopy(coord), deepcopy(destination)]
                                movelog.append(deepcopy(boardstate))
                                
                            coord = []
                            destination = []
                            moveset = []
                            display.draw_state(boardstate, white, black)
                        if boardstate.previous != []:
                            display.draw_previous(boardstate.previous[0], boardstate.previous[1])

                elif col == 0 and row == -1:
                    if boardstate.white_under:
                        if black == "Computer":
                            black = "Player"
                        else:
                            black = "Computer"
                            white = "Player"
                    else:
                        if white == "Computer":
                            white = "Player"
                        else:
                            white = "Computer"
                            black = "Player"
                    coord = []
                    destination = []
                    moveset = []
                    display.draw_state(boardstate, white, black)
                    if boardstate.previous != []:
                        display.draw_previous(boardstate.previous[0], boardstate.previous[1])

                elif col == 0 and row == 8:
                    if boardstate.white_under:
                        if white == "Computer":
                            white = "Player"
                        else:
                            white = "Computer"
                            black = "Player"
                    else:
                        if black == "Computer":
                            black = "Player"
                        else:
                            black = "Computer"
                            white = "Player"
                    coord = []
                    destination = []
                    moveset = []
                    display.draw_state(boardstate, white, black)

                    if boardstate.previous != []:
                        display.draw_previous(boardstate.previous[0], boardstate.previous[1])

 
            elif e.type == pg.KEYDOWN:
                key = e.key
                if key == pg.K_z:
                    undo_time = 2 if ("Player" in black + white and "Computer" in black + white) else 1
                    for u in range(undo_time):
                        if len(movelog) > 1:
                            boardstate = deepcopy(movelog.pop(-1))
                        else:
                            boardstate = deepcopy(movelog[0])
                        coord = []
                        destination = []
                        moveset = []
                        display.draw_state(boardstate, white, black)
                        if boardstate.previous != []:
                            display.draw_previous(boardstate.previous[0], boardstate.previous[1])
                elif key == pg.K_r:
                    boardstate = BoardState()
                    movelog = [deepcopy(boardstate)]
                    coord = []
                    destination = []
                    moveset = []
                    display.draw_state(boardstate, white, black)
                    if boardstate.previous != []:
                        display.draw_previous(boardstate.previous[0], boardstate.previous[1])
                elif key == pg.K_f:
                    coord = []
                    destination = []
                    moveset = []
                    boardstate.flip_board()
                    display.draw_state(boardstate, white, black)
                    if boardstate.previous != []:
                        display.draw_previous(boardstate.previous[0], boardstate.previous[1])

     

if __name__ == "__main__":
    main()