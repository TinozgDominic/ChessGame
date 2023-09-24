import pygame as pg
pg.init()

class Display():
    def __init__(self, width = 560, height = 700):
        self.width = width
        self. height = height
        self.dimension = (self.width, self. height)
        self.square_size = width // 8

        self.screen = pg.display.set_mode(self.dimension)
        self.background_color = pg.Color(50, 50, 50)
        self.screen.fill(self.background_color)

        self.colors = [(238, 238, 210),(118, 150, 86)]

        self.images = {}
        self.load_images()
        self.current_value = 0.0

    def load_images(self):
        pieces=['wp','wr','wn','wb','wq','wk','bp','br','bn','bb','bq','bk']
        for i in pieces:
            self.images[i] = pg.transform.scale(pg.image.load('.pack/' + i + '.png'), (self.square_size, self.square_size))
        self.images["player"] = pg.transform.scale(pg.image.load('.pack/player.png'), (self.square_size * 7 // 10, self.square_size * 7 // 10))
        self.images["computer"] = pg.transform.scale(pg.image.load('.pack/computer.png'), (self.square_size * 7 // 10, self.square_size * 7 // 10))
    
    def draw_board(self):
        for r in range(8):
            for c in range(8):
                color = self.colors[(r + c) % 2]
                pg.draw.rect(self.screen, color, pg.Rect(c * self.square_size, (r + 1) * self.square_size, self.square_size, self.square_size))

    def draw_piece(self, board):
        for r in range(8):
            for c in range(8):
                piece = board[r][c].piece
                if piece != "--":
                    self.screen.blit(self.images[piece], pg.Rect(c * self.square_size, (r + 1) * self.square_size, self.square_size, self.square_size))

    def draw_state(self, boardstate, white, black):
        self.screen.fill(self.background_color)
        self.draw_player(boardstate, white, black)
        self.draw_board()
        self.draw_piece(boardstate.board)
        self.draw_coordinate(boardstate)
        self.draw_board_value(boardstate)
        
        pg.display.flip()

    def draw_moveable(self, board, coord, moveset):
        # Highlight the chosen piece
        r, c = coord
        color = pg.Color(250, 200, 152)
        pg.draw.circle(self.screen, color, (c * self.square_size + self.square_size // 2, (r + 1) * self.square_size + self.square_size // 2), self.square_size // 12)
        # Highlight the moveset
        for move in moveset:
            r, c = move
            if board[r][c].piece == "--":
                color = pg.Color(159, 192, 222)
            else:
                color = pg.Color(255, 179, 71)
            pg.draw.circle(self.screen, color, (c * self.square_size + self.square_size // 2, (r + 1) * self.square_size + self.square_size // 2), self.square_size // 12)
        pg.display.flip()
    
    def draw_previous(self, coord, destination):
        color = pg.Color(208, 94, 79)
        for sq in [coord, destination]:
            r, c = sq
            pg.draw.circle(self.screen, color, (c * self.square_size + self.square_size // 2, (r + 1) * self.square_size + self.square_size // 2), self.square_size // 16)
        pg.display.flip()

    def promotion(self, color, destination):
        r, c = destination
        r = 4 if r != 0 else 0

        promote_background = (238, 238, 210)
        pg.draw.rect(self.screen, promote_background, pg.Rect(c * self.square_size, (r + 1)  * self.square_size, self.square_size, 4 * self.square_size))
        pg.draw.lines(self.screen, (0, 0, 0), True, [[c * self.square_size, (r + 1)  * self.square_size], [(c + 1) * self.square_size, (r + 1)  * self.square_size], [(c + 1) * self.square_size, (r + 5)  * self.square_size], [c * self.square_size, (r + 5)  * self.square_size]])
        for (i , type) in enumerate(["q", "r", "b", "n"]):
            self.screen.blit(self.images[color + type], pg.Rect(c * self.square_size, (r + i + 1) * self.square_size, self.square_size, self.square_size))
        pg.display.flip()
        
        promoting = True
        promote_piece = ""
        while promoting:
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    promoting = False
                    pg.quit()

                elif e.type == pg.MOUSEBUTTONDOWN:
                    location = pg.mouse.get_pos()
                    col = location[0] // self.square_size
                    row = location[1] // self.square_size - 1

                    if col == c and row - r >= 0 and row - r <= 3:
                        promote_piece = ["q", "r", "b", "n"][row - r]
                        promoting = False
        
        return promote_piece
    
    def draw_coordinate(self, boardstate):
        font = pg.font.SysFont(name = "calibri", size = 18, bold = True)
        if boardstate.white_under:
            numbers = ["8", "7", "6", "5", "4", "3", "2", "1"]
            chars   = ["a", "b", "c", "d", "e", "f", "g", "h"]
        else:
            numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
            chars   = ["h", "g", "f", "e", "d", "c", "b", "a"]
        # Draw numbers
        for i, num in enumerate(numbers):
            color = self.colors[(i + 1) % 2]
            text = font.render(num, 0, color)
            self.screen.blit(text, (int(self.square_size * 0.05), int((i + 1 + 0.05) * self.square_size)))   
        
        # Draw characters
        for i, char in enumerate(chars):
            color = self.colors[i % 2]
            text = font.render(char, 0, color)
            self.screen.blit(text, (int((i + 0.85) * self.square_size), int((8 + 0.7) * self.square_size)))   
        
    def draw_gamestate(self, boarstate):
        if boarstate.gamestate == 1:
            text = "White win!"
            color = (248, 248, 248)
            background_color = (86, 83, 82)
        elif boarstate.gamestate == -1:
            text = "Black win!"
            color = (86, 83, 82)
            background_color = (248, 248, 248)
        else:
            text = "Draw!"
            color = (140, 138, 137)
            background_color = (194, 193, 193)

        font = pg.font.SysFont('calibri', 30, True, False)
        text = font.render(text, 0, color)
        location = pg.Rect(0, 0, self.width, self.height).move((self.width - text.get_width()) / 2, (self.height - text.get_height()) / 2)
        pg.draw.rect(self.screen, background_color, pg.Rect((self.width - text.get_width()) / 2, (self.height - text.get_height()) / 2, text.get_width(), text.get_height()))
        self.screen.blit(text, location)  

        pg.display.flip()
    
    def draw_board_value(self, boardstate):
        value = boardstate.get_board_value()

        font = pg.font.SysFont('calibri', 18, True, False)
        text = font.render(str(value), 0, (248, 248, 248))
        location = pg.Rect(0, 9.1 * self.square_size, self.width, self.square_size // 8).move((self.width - text.get_width()) / 2, (self.square_size // 8 - text.get_height()) / 2)
        self.screen.blit(text, location) 

        value_min = -40.0
        value_max = 40.0
        for v in [self.current_value + (value - self.current_value) / 10 * i for i in range(10)]:
            pg.draw.rect(self.screen, (86, 83, 82), pg.Rect(0, 0.8 * self.square_size, self.width, self.square_size // 8))
            pg.draw.rect(self.screen, (248, 248, 248), pg.Rect(0, 0.8 * self.square_size, (v - value_min) * self.width // (value_max - value_min), self.square_size // 8))
            pg.display.flip()
        self.current_value = value
    
    def draw_player(self, boardstate, white, black):
        white_image = self.images["player"] if white == "Player" else self.images["computer"]
        black_image = self.images["player"] if black == "Player" else self.images["computer"]

        upper_image, lower_image, upper_text, lower_text = [black_image, white_image, black, white] if boardstate.white_under else [white_image, black_image, white, black]

        player_size = self.square_size * 7 // 10

        pg.draw.rect(self.screen, (238, 238, 210), pg.Rect(0, 0, player_size, player_size))
        self.screen.blit(upper_image, pg.Rect(0, 0, player_size, player_size))
        pg.draw.rect(self.screen, (238, 238, 210), pg.Rect(0, self.height - player_size, player_size, player_size))
        self.screen.blit(lower_image, pg.Rect(0, self.height - player_size, player_size, player_size))
         
        font = pg.font.SysFont('calibri', 18, True, False)

        text = font.render(upper_text + " noob", 0, (248, 248, 248))
        self.screen.blit(text, (self.square_size, player_size // 2 - text.get_height() // 2)) 

        text = font.render(lower_text + " noob", 0, (248, 248, 248))
        self.screen.blit(text, (self.square_size, self.height - player_size // 2 - text.get_height() // 2)) 