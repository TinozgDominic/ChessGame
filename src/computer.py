from copy import deepcopy
import random
import time
import multiprocessing

random.seed(time.time())

class Computer():
    def __init__(self, depth = 3, num_processes = 16):
        self.depth = depth
        self.num_processes = num_processes
    
    def make_move(self, boardstate, depth):
        move_list = boardstate.get_all_valid_move()

        maximizing = True if boardstate.white_turn else False
        values = []

        # Use multiprocessing to evaluate moves in parallel
        with multiprocessing.Pool(processes=self.num_processes) as pool:
            values = pool.map(self.evaluate_move_parallel, [(boardstate, move, depth) for move in move_list])

        if values == []:
            return [[], []]
        else:
            smart_movelist = []
            if maximizing:
                max_values = max(values)
                for i in range(len(move_list)): 
                    if values[i] == max_values:
                        smart_movelist.append(move_list[i])
            else:
                min_values = min(values)
                for i in range(len(move_list)): 
                    if values[i] == min_values:
                        smart_movelist.append(move_list[i])
            
            return random.choice(smart_movelist)

    def evaluate_move_parallel(self, args):
        boardstate, move, depth = args
        current_boardstate = deepcopy(boardstate)
        current_boardstate.make_move(coord = move[0], destination = move[1], display = None)
        current_boardstate.get_gamestate()
        if current_boardstate.game_over:
            return current_boardstate.gamestate * 40.0
        if depth == 1:
            value = current_boardstate.get_board_value()
        else:
            value = self.evaluate_move(current_boardstate, depth - 1)
        del current_boardstate
        return value

    def evaluate_move(self, boardstate, depth):
        # Get move list
        move_list = boardstate.get_all_valid_move()

        # Make move and evaluate values
        values = []

        for move in move_list:
            current_boardstate = deepcopy(boardstate)
            current_boardstate.make_move(coord = move[0], destination = move[1], display = None)
            current_boardstate.get_gamestate()
            if depth == 1:
                values.append(current_boardstate.get_board_value())
            else:
                values.append(self.evaluate_move(current_boardstate, depth - 1))
            del current_boardstate

        # Check the gamestate
        boardstate.get_gamestate()
        if boardstate.game_over:
            values.append(boardstate.gamestate * 40.0)

        maximizing = True if boardstate.white_turn else False

        if maximizing:
            board_value = max(values)
        else:
            board_value = min(values)

        return board_value
