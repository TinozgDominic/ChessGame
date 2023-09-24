# Piece
class Piece():
    def __init__(self, piece):
        self.piece = piece
        self.color, self.type = piece
        self.sign = 1 if self.color == "w" else - 1 
        self.value = 0

# Pawn
class Pawn(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.enpassant = False
        self.enpassant_square = []
        self.value = 1.0 * self.sign
        self.occupied_value = 1.0
    
    def get_move(self, boardstate, coord):
        r, c = coord
        enemy_color = "b" if boardstate.white_turn else "w"
        direction = - 1 if (boardstate.white_under and self.color == "w") or (not boardstate.white_under and self.color == "b")  else + 1 # - 1 is moving up, + 1 is moving down
        moveset = []

        # Move up 1 or 2 square(S)
        if boardstate.board[r + 1 * direction][c].piece == "--": 
            moveset.append([r + 1 * direction, c])
            if (r == 6 or r == 1) and r + 2 * direction >= 0 and r + 2 * direction <= 7:
                if boardstate.board[r + 2 * direction][c].piece == "--":
                    moveset.append([r + 2 * direction, c])
        # Capture
        if c >= 1: # Capture left
            if boardstate.board[r + 1 * direction][c - 1].color == enemy_color:
                moveset.append([r + 1 * direction, c - 1])
        if c <= 6: # Capture right
            if boardstate.board[r + 1 * direction][c + 1].color == enemy_color:
                moveset.append([r + 1 * direction, c + 1])
        # En passant
        if self.enpassant == True:
            moveset.append(self.enpassant_square)
        return moveset

    def get_occupied(self, boardstate, coord):
        r, c = coord
        direction = - 1 if (boardstate.white_under and self.color == "w") or (not boardstate.white_under and self.color == "b")  else + 1 # - 1 is moving up, + 1 is moving down
        occupied = []

        # Capture
        if c >= 1: # Capture left
            occupied.append([r + 1 * direction, c - 1])
        if c <= 6: # Capture right
            occupied.append([r + 1 * direction, c + 1])
        
        return occupied


# Bishop
class Bishop(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.value = 3.5 * self.sign
        self.occupied_value = 3.5

    def get_move(self, boardstate, coord):
        r, c = coord
        enemy_color = "b" if boardstate.white_turn else "w"
        moveset = []

        direction = [[- 1, - 1], 
                     [- 1, + 1], 
                     [+ 1, - 1], 
                     [+ 1, + 1]]
        
        for dir in direction:
            for i in range(1, 8):
                row = r + i * dir[0]
                col = c + i * dir[1]
                if  row < 0 or row > 7 or col < 0 or col > 7:
                    break
                else:
                    if boardstate.board[row][col].piece == "--":
                        moveset.append([row, col])
                    elif boardstate.board[row][col].color == enemy_color:
                        moveset.append([row, col])
                        break
                    else:
                        break

        return moveset

    def get_occupied(self, boardstate, coord):
        r, c = coord
        occupied = []

        direction = [[- 1, - 1], 
                     [- 1, + 1], 
                     [+ 1, - 1], 
                     [+ 1, + 1]]
        
        for dir in direction:
            for i in range(1, 8):
                row = r + i * dir[0]
                col = c + i * dir[1]
                if  row < 0 or row > 7 or col < 0 or col > 7:
                    break
                else:
                    if boardstate.board[row][col].piece == "--":
                        occupied.append([row, col])
                    else:
                        occupied.append([row, col])
                        break
        
        return occupied

# Knight
class Knight(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.value = 3.0 * self.sign
        self.occupied_value = 3.0
    
    def get_move(self, boardstate, coord):
        r, c = coord
        ally_color = "w" if boardstate.white_turn else "b"
        moveset = []
        direction =[[- 2, + 1],
                    [- 1, + 2],
                    [+ 1, + 2],
                    [+ 2, + 1],
                    [+ 2, - 1],
                    [+ 1, - 2],
                    [- 1, - 2],
                    [- 2, - 1]]
        
        for dir in direction:
            row = r + dir[0]
            col = c + dir[1]
            if  row >= 0 and row <= 7 and col >= 0 and col <= 7:
                if boardstate.board[row][col].color != ally_color:
                    moveset.append([row, col])

        return moveset

    def get_occupied(self, boardstate, coord):
        r, c = coord
        occupied = []

        direction =[[- 2, + 1],
                    [- 1, + 2],
                    [+ 1, + 2],
                    [+ 2, + 1],
                    [+ 2, - 1],
                    [+ 1, - 2],
                    [- 1, - 2],
                    [- 2, - 1]]
        
        for dir in direction:
            row = r + dir[0]
            col = c + dir[1]
            if  row >= 0 and row <= 7 and col >= 0 and col <= 7:
                occupied.append([row, col])
        
        return occupied

# Rook
class Rook(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.value = 5.0 * self.sign
        self.castle_right = True
        self.occupied_value = 5.0

    def get_move(self, boardstate, coord):
        r, c = coord
        enemy_color = "b" if boardstate.white_turn else "w"
        moveset = []

        direction = [[- 1, + 0], 
                     [+ 1, + 0], 
                     [+ 0, - 1], 
                     [+ 0, + 1]]
        
        for dir in direction:
            for i in range(1, 8):
                row = r + i * dir[0]
                col = c + i * dir[1]
                if  row < 0 or row > 7 or col < 0 or col > 7:
                    break
                else:
                    if boardstate.board[row][col].piece == "--":
                        moveset.append([row, col])
                    elif boardstate.board[row][col].color == enemy_color:
                        moveset.append([row, col])
                        break
                    else:
                        break
        
        return moveset

    def get_occupied(self, boardstate, coord):
        r, c = coord
        occupied = []

        direction = [[- 1, + 0], 
                     [+ 1, + 0], 
                     [+ 0, - 1], 
                     [+ 0, + 1]]
        
        for dir in direction:
            for i in range(1, 8):
                row = r + i * dir[0]
                col = c + i * dir[1]
                if  row < 0 or row > 7 or col < 0 or col > 7:
                    break
                else:
                    if boardstate.board[row][col].piece == "--":
                        occupied.append([row, col])
                    else:
                        occupied.append([row, col])
                        break
        
        return occupied
    
# Queen
class Queen(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.value = 9.0 * self.sign
        self.occupied_value = 0.5
    
    def get_move(self, boardstate, coord):
        r, c = coord
        enemy_color = "b" if boardstate.white_turn else "w"
        moveset = []

        direction = [[- 1, + 0], 
                     [+ 1, + 0], 
                     [+ 0, - 1], 
                     [+ 0, + 1],
                     [- 1, - 1], 
                     [- 1, + 1], 
                     [+ 1, - 1], 
                     [+ 1, + 1]]
        
        for dir in direction:
            for i in range(1, 8):
                row = r + i * dir[0]
                col = c + i * dir[1]
                if  row < 0 or row > 7 or col < 0 or col > 7:
                    break
                else:
                    if boardstate.board[row][col].piece == "--":
                        moveset.append([row, col])
                    elif boardstate.board[row][col].color == enemy_color:
                        moveset.append([row, col])
                        break
                    else:
                        break
        
        return moveset

    def get_occupied(self, boardstate, coord):
        r, c = coord
        occupied = []

        direction = [[- 1, + 0], 
                     [+ 1, + 0], 
                     [+ 0, - 1], 
                     [+ 0, + 1],
                     [- 1, - 1], 
                     [- 1, + 1], 
                     [+ 1, - 1], 
                     [+ 1, + 1]]
        
        for dir in direction:
            for i in range(1, 8):
                row = r + i * dir[0]
                col = c + i * dir[1]
                if  row < 0 or row > 7 or col < 0 or col > 7:
                    break
                else:
                    if boardstate.board[row][col].piece == "--":
                        occupied.append([row, col])
                    else:
                        occupied.append([row, col])
                        break
        
        return occupied

# King
class King(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.value = 40.0 * self.sign
        self.castle_right = True
        self.is_check = False
        self.occupied_value = 0.5
    
    def get_move(self, boardstate, coord):
        r, c = coord
        ally_color = "w" if boardstate.white_turn else "b"
        moveset = []

        direction = [[- 1, + 0], 
                     [+ 1, + 0], 
                     [+ 0, - 1], 
                     [+ 0, + 1],
                     [- 1, - 1], 
                     [- 1, + 1], 
                     [+ 1, - 1], 
                     [+ 1, + 1]]
        
        for dir in direction:
            row = r + dir[0]
            col = c + dir[1]
            if  row >= 0 and row <= 7 and col >= 0 and col <= 7:
                if boardstate.board[row][col].color != ally_color:
                    moveset.append([row, col])

        # Castle
        if self.castle_right and not self.is_check:
            if boardstate.white_under:
                # Short
                # Check the rook is available
                if boardstate.board[r][c + 3].piece == ally_color + "r":
                    if boardstate.board[r][c + 3].castle_right == True:
                        # Check the next 2 squares are empty and not occupied
                        if boardstate.board[r][c + 1].piece == "--" and boardstate.board[r][c + 2].piece == "--":
                            if boardstate.white_turn:
                                if boardstate.black_occupied[r][c + 1] == 0 and boardstate.black_occupied[r][c + 2] == 0:
                                    moveset.append([r, c + 2])
                            else:
                                if boardstate.white_occupied[r][c + 1] == 0 and boardstate.white_occupied[r][c + 2] == 0:
                                    moveset.append([r, c + 2])
                # Long
                # Check the rook is available
                if boardstate.board[r][c - 4].piece == ally_color + "r":
                    if boardstate.board[r][c - 4].castle_right == True:
                        # Check the next 2 squares are empty and not occupied
                        if boardstate.board[r][c - 1].piece == "--" and boardstate.board[r][c - 2].piece == "--":
                            if boardstate.white_turn:
                                if boardstate.black_occupied[r][c - 1] == 0 and boardstate.black_occupied[r][c - 2] == 0:
                                    moveset.append([r, c - 2])
                            else:
                                if boardstate.white_occupied[r][c - 1] == 0 and boardstate.white_occupied[r][c - 2] == 0:
                                    moveset.append([r, c - 2])
            else:
                # Short
                # Check the rook is available
                if boardstate.board[r][c - 3].piece == ally_color + "r":
                    if boardstate.board[r][c - 3].castle_right == True:
                        # Check the next 2 squares are empty and not occupied
                        if boardstate.board[r][c - 1].piece == "--" and boardstate.board[r][c - 2].piece == "--":
                            if boardstate.white_turn:
                                if boardstate.black_occupied[r][c - 1] == 0 and boardstate.black_occupied[r][c - 2] == 0:
                                    moveset.append([r, c - 2])
                            else:
                                if boardstate.white_occupied[r][c - 1] == 0 and boardstate.white_occupied[r][c - 2] == 0:
                                    moveset.append([r, c - 2])
                # Long
                # Check the rook is available
                if boardstate.board[r][c + 4].piece == ally_color + "r":
                    if boardstate.board[r][c + 4].castle_right == True:
                        # Check the next 2 squares are empty and not occupied
                        if boardstate.board[r][c + 1].piece == "--" and boardstate.board[r][c + 2].piece == "--":
                            if boardstate.white_turn:
                                if boardstate.black_occupied[r][c + 1] == 0 and boardstate.black_occupied[r][c + 2] == 0:
                                    moveset.append([r, c + 2])
                            else:
                                if boardstate.white_occupied[r][c + 1] == 0 and boardstate.white_occupied[r][c + 2] == 0:
                                    moveset.append([r, c + 2])

        return moveset

    def get_occupied(self, boardstate, coord):
        r, c = coord
        occupied = []

        direction = [[- 1, + 0], 
                     [+ 1, + 0], 
                     [+ 0, - 1], 
                     [+ 0, + 1],
                     [- 1, - 1], 
                     [- 1, + 1], 
                     [+ 1, - 1], 
                     [+ 1, + 1]]
        
        for dir in direction:
            row = r + dir[0]
            col = c + dir[1]
            if  row >= 0 and row <= 7 and col >= 0 and col <= 7:
                occupied.append([row, col])
        
        return occupied

# Empty
class Empty(Piece):
    def __init__(self, piece):
        super().__init__(piece)
        self.castle_right = True

    def get_move(self, boardstate, coord):
        return []
    def get_occupied(self, boardstate, coord):
        return []