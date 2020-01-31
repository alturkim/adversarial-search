from utility import JumpDestination
import copy
import random
import math

all_cells = []
for i in range(0, 16):
    for j in range(0, 16):
        all_cells.append((i,j))

black_camp_cells_list = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
                    (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                    (0, 2), (1, 2), (2, 2), (3, 2),
                    (0, 3), (1, 3), (2, 3),
                    (0, 4), (1, 4)]

white_camp_cells_list = [(14, 11), (15, 11),
                    (13, 12), (14, 12), (15, 12),
                    (12, 13), (13, 13), (14, 13), (15, 13),
                    (11, 14), (12, 14), (13, 14), (14, 14), (15, 14),
                    (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)]
########################  0   1   2   3   4   5   6   7   8   9   A   B   C   D   E   F
evaluation_map_black = [[  1,  1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1], #0
                        [  1,  4,  2,  2,  2,  2,  2, -1, -1, -1, -1, -1, -1, -1, -1, -1], #1
                        [  1,  3,  8,  4,  4,  4,  4, -1, -1, -1, -1, -1, -1, -1, -1, -1], #2
                        [  1,  3,  4, 52, 40, 30, 20, 10, -1, -1, -1, -1, -1, -1, -1, -1], #3
                        [  1,  3,  6, 40, 54, 50, 40, 30, -1, -1, -1, -1, -1, -1, -1, -1], #4
                        [ -1,  4,  6, 50, 53, 56, 57, 53, 40, 40, 30, 30,  1,  1, 10, -1], #5
                        [ -1,  6,  8, 50, 53, 55, 58, 50, 50, 50, 40, 40, 10, 10, 20, -1], #6
                        [ -1,  8, 10, 48, 51, 55, 57, 60, 50, 50, 50, 50, 20, 20, 30, -1], #7
                        [ -1, -1, -1, 46, 40, 55, 57, 59, 62, 60, 60, 60, 30, 30, 40, -1], #8
                        [ -1, -1, -1, -1, 40, 40, 57, 59, 61, 64, 60, 60, 40, 40, 50, -1], #9
                        [ -1, -1, -1, -1, -1, -1, 40, 59, 61, 63, 66, 60, 50, 50, 60, -1], #A
                        [ -1, -1, -1, -1, -1, -1, -1, 40, 61, 63, 65, 68, 60, 60, 80, 80], #B
                        [ -1, -1, -1, -1, -1, -1, -1, -1, 40, 40, 14, 67, 70, 80, 80, 80], #C
                        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, 16, 80, 80, 80, 80], #D
                        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, 80, 80, 80, 80, 80], #E
                        [ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 14, 80, 80, 80, 80, 80]] #F

evaluation_map_white = [[80, 80, 80, 80, 80, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [80, 80, 80, 80, 80, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [80, 80, 80, 80, 16, 14, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
       [80, 80, 80, 70, 67, 14, 40, 40, -1, -1, -1, -1, -1, -1, -1, -1],
       [80, 80, 60, 69, 68, 65, 63, 61, 40, -1, -1, -1, -1, -1, -1, -1],
       [-1, 60, 50, 50, 67, 66, 63, 61, 59, 40, -1, -1, -1, -1, -1, -1],
       [-1, 50, 40, 40, 66, 65, 64, 61, 59, 57, 40, -1, -1, -1, -1, -1],
       [-1, 40, 30, 30, 60, 65, 63, 62, 59, 57, 55, 40, 46, -1, -1, -1],
       [-1, 30, 20, 20, 50, 50, 63, 61, 60, 57, 55, 51, 48, -1, -1, -1],
       [-1, 20, 10, 10, 40, 40, 50, 50, 59, 58, 55, 53, 50,  8, -1, -1],
       [-1, 10,  1,  1, 30, 30, 40, 40, 53, 57, 56, 53, 50,  6, -1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, 51, 54, 55, 54, 50,  6,  2, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, 51, 53, 54, 52, 52,  4,  2, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  4,  1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  1,  1, -1],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]




black_camp_cells = dict()
white_camp_cells = dict()
for cell in all_cells:
    black_camp_cells[cell] = False
    white_camp_cells[cell] = False
for cell in black_camp_cells_list:
    black_camp_cells[cell] = True
for cell in white_camp_cells_list:
    white_camp_cells[cell] = True


class State:
    def __init__(self, board, current_player, other_player):
        self.board = board
        self.current_player = current_player
        self.other_player = other_player

    def __str__(self):
        output = '\n   0 1 2 3 4 5 6 7 8 9 A B C D E F\n'
        for i, row in enumerate(self.board):
            output += str(i) + '  ' if i < 10 else str(i) + ' '
            for ch in row:
                output += ch + ' '
            output += '\n'
        output += '\nCurrent Player: {}'.format(self.current_player)
        return output

    def update_board(self, set_empty, set_full, color):
        self.board[set_empty[1]][set_empty[0]] = '.'
        self.board[set_full[1]][set_full[0]] = color[0]


class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def __str__(self):
        return 'State: {}, Parent: {}, Action: {}\n'.format(self.state, self.parent, self.action)


class Piece:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return 'Piece:{}, @ ({},{})'.format(self.color, self.x, self.y)


class Player:
    def __init__(self, color, pieces, camp):
        self.color = color
        self.pieces = pieces
        self.camp = camp

    def __str__(self):
        return 'Player:{}'.format(self.color)

    def move(self, piece_idx, destination):
        # remember that x is col and y is row
        self.pieces[piece_idx].x = destination[0]
        self.pieces[piece_idx].y = destination[1]


class Game:
    def __init__(self, init_state, player_max, player_min, basic_actions_for_black, jump_actions_for_black,
                 basic_actions_for_white, jump_actions_for_white):
        self.init_state = init_state
        self.current_state = init_state
        self.player_max = player_max
        self.player_min = player_min
        self.basic_actions_for_black = basic_actions_for_black
        self.jump_actions_for_black = jump_actions_for_black
        self.basic_actions_for_white = basic_actions_for_white
        self.jump_actions_for_white = jump_actions_for_white

    def __str__(self):
        return 'State:{}\nMax:{}\n'.format(self.current_state, self.player_max)

    def cutoff_test(self, state, depth, depth_limit=5):
        if depth > depth_limit:  # or self.terminal_test(state)[0]
            return True
        else:
            return False

    def evaluation_function(self, state):
        current_player_pieces_in_other_camp = 0
        other_player_pieces_in_current_camp = 0
        current_player_pieces_beyond_each_diagonal = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                                                      16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0}
        other_player_pieces_beyond_each_diagonal = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0,
                                                    16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0}

        if state.current_player.color == 'BLACK':
            for piece in state.current_player.pieces:
                temp = piece.x + piece.y
                if 6 <= temp <= 24:
                    current_player_pieces_beyond_each_diagonal[temp] = current_player_pieces_beyond_each_diagonal[
                                                                           temp] + 1

                if state.other_player.camp[(piece.x, piece.y) ]:
                    current_player_pieces_in_other_camp += 1

            for piece in state.other_player.pieces:
                temp = piece.x + piece.y
                if 6 <= temp <= 24:
                    other_player_pieces_beyond_each_diagonal[30 - temp] = current_player_pieces_beyond_each_diagonal[
                                                                              30 - temp] + 1

                if state.current_player.camp[(piece.x, piece.y)]:
                    other_player_pieces_in_current_camp += 1

        else:
            for piece in state.current_player.pieces:
                temp = piece.x + piece.y
                if 6 <= temp <= 24:
                    if abs(piece.x - piece.y) <= 2:
                        current_player_pieces_beyond_each_diagonal[30 - temp] = current_player_pieces_beyond_each_diagonal[
                                                                                30 - temp] + 5
                    else:
                        current_player_pieces_beyond_each_diagonal[30 - temp] = \
                        current_player_pieces_beyond_each_diagonal[
                            30 - temp] + 1

            if state.other_player.camp[(piece.x, piece.y)]:
                current_player_pieces_in_other_camp += 1

            for piece in state.other_player.pieces:
                temp = piece.x + piece.y
                if 6 <= temp <= 24:
                    if abs(piece.x - piece.y) <= 2:
                        other_player_pieces_beyond_each_diagonal[temp] = other_player_pieces_beyond_each_diagonal[
                                                                         temp] + 5
                    else:
                        other_player_pieces_beyond_each_diagonal[temp] = other_player_pieces_beyond_each_diagonal[
                                                                         temp] + 1
                if state.current_player.camp[(piece.x, piece.y)]:
                    other_player_pieces_in_current_camp += 1

        diagonals_utility = 0
        for key, value in current_player_pieces_beyond_each_diagonal.items():
            weight = 2 * (key - 6)
            diagonals_utility += (weight * value)

        other_diagonals_utility = 0
        for key, value in other_player_pieces_beyond_each_diagonal.items():
            weight = (2 * (key - 6))
            other_diagonals_utility += (weight * value)

        if current_player_pieces_in_other_camp > 0:
            total_eval = (1 * current_player_pieces_in_other_camp) \
                         - (1 * other_player_pieces_in_current_camp) \
                         + (100 * diagonals_utility) \
                         - (100 * other_diagonals_utility)
        else:
            total_eval = (1000 * current_player_pieces_in_other_camp) \
                         - (1000 * other_player_pieces_in_current_camp) \
                         + (10 * diagonals_utility) \
                         - (10 * other_diagonals_utility)
        if self.player_max.color == state.current_player.color:
            return 1 * total_eval
        else:
            return -1 * total_eval
    '''


    def evaluation_function(self, state):
        total_eval = 0
        if state.current_player.color == 'BLACK':
            for piece in state.current_player.pieces:
                total_eval += evaluation_map_black[piece.y][piece.x]

            # for piece in state.other_player.pieces:

        else:
            for piece in state.current_player.pieces:
                total_eval += evaluation_map_white[piece.y][piece.x]
            # for piece in state.other_player.pieces:

        # print(total_eval)
        if self.player_max.color == state.current_player.color:
            return total_eval
        else:
            return -1 * total_eval
    '''
    def terminal_test(self, state):
        whites_in_white_camp = 0
        black_in_black_camp = 0
        no_empty_white_cells = True
        no_empty_black_cells = True
        if state.current_player.color == 'BLACK':
            for cell in white_camp_cells:
                content = state.board[cell[1]][cell[0]]
                if content == '.':
                    no_empty_white_cells = False
                    break
                if content.upper() == 'W':
                    whites_in_white_camp += 1
            if whites_in_white_camp < 19 and no_empty_white_cells:
                return True, 'BLACK'
        else:
            for cell in black_camp_cells:
                content = state.board[cell[1]][cell[0]]
                if content == '.':
                    no_empty_black_cells = False
                    break
                if content.upper() == 'B':
                    black_in_black_camp += 1
            if black_in_black_camp < 19 and no_empty_black_cells:
                return True, 'WHITE'

        return False, 'NON-TERMINAL'

    def transition_fn(self, state, source, single_action):
        def n_jump_effect(state, destination_x, destination_y):
            if destination_y - 1 < 0:
                return None
            if state.board[destination_y - 1][destination_x] == '.':
                return None
            return destination_x, destination_y - 2

        def ne_jump_effect(state, destination_x, destination_y):
            if destination_y - 1 < 0 or destination_x + 1 > 15:
                return None
            if state.board[destination_y - 1][destination_x + 1] == '.':
                return None
            return destination_x + 2, destination_y - 2

        def e_jump_effect(state, destination_x, destination_y):
            if destination_x + 1 > 15:
                return None
            if state.board[destination_y][destination_x + 1] == '.':
                return None
            return destination_x + 2, destination_y

        def se_jump_effect(state, destination_x, destination_y):
            if destination_y + 1 > 15 or destination_x + 1 > 15:
                return None
            if state.board[destination_y + 1][destination_x + 1] == '.':
                return None
            return destination_x + 2, destination_y + 2

        def s_jump_effect(state, destination_x, destination_y):
            if destination_y + 1 > 15:
                return None
            if state.board[destination_y + 1][destination_x] == '.':
                return None
            return destination_x, destination_y + 2

        def sw_jump_effect(state, destination_x, destination_y):
            if destination_y + 1 > 15 or destination_x - 1 < 0:
                return None
            if state.board[destination_y + 1][destination_x - 1] == '.':
                return None
            return destination_x - 2, destination_y + 2

        def w_jump_effect(state, destination_x, destination_y):
            if destination_x - 1 < 0:
                return None
            if state.board[destination_y][destination_x - 1] == '.':
                return None
            return destination_x - 2, destination_y

        def nw_jump_effect(state, destination_x, destination_y):
            if destination_y - 1 < 0 or destination_x - 1 < 0:
                return None
            if state.board[destination_y - 1][destination_x - 1] == '.':
                return None
            return destination_x - 2, destination_y - 2

        # it does not matter which action list to in transition_fn
        basic_actions_list = self.basic_actions_for_black
        jump_actions_list = self.jump_actions_for_black

        destination_x, destination_y = source

        if single_action in basic_actions_list:
            single_actions_effect_dict = {
                'E': (lambda destination_x, destination_y: (destination_x + 1, destination_y)),
                'W': (lambda destination_x, destination_y: (destination_x - 1, destination_y)),
                'N': (lambda destination_x, destination_y: (destination_x, destination_y - 1)),
                'S': (lambda destination_x, destination_y: (destination_x, destination_y + 1)),
                'NE': (lambda destination_x, destination_y: (destination_x + 1, destination_y - 1)),
                'SE': (lambda destination_x, destination_y: (destination_x + 1, destination_y + 1)),
                'SW': (lambda destination_x, destination_y: (destination_x - 1, destination_y + 1)),
                'NW': (lambda destination_x, destination_y: (destination_x - 1, destination_y - 1))
            }

            effect_function = single_actions_effect_dict[single_action]
            destination_x, destination_y = effect_function(destination_x, destination_y)

        elif single_action in jump_actions_list:
            jump_actions_effect_dict = {
                'SE_JUMP': se_jump_effect,
                'S_JUMP': s_jump_effect,
                'E_JUMP': e_jump_effect,
                'SW_JUMP': sw_jump_effect,
                'W_JUMP': w_jump_effect,
                'NE_JUMP': ne_jump_effect,
                'NW_JUMP': nw_jump_effect,
                'N_JUMP': n_jump_effect
            }
            effect_function = jump_actions_effect_dict[single_action]
            output = effect_function(state, destination_x, destination_y)
            if output is None:
                return None
            else:
                destination_x, destination_y = output

        # check if the action is possible
        if 0 <= destination_x <= 15 and 0 <= destination_y <= 15:
            if state.board[destination_y][destination_x] != '.':
                return None
            # moving a piece from outside the camp to inside the camp is illegal
            elif not state.current_player.camp[source] and state.current_player.camp[(destination_x, destination_y)]:
                return None
            else:
                return destination_x, destination_y
        else:
            return None

    def pieces_still_in_camp_of_current_player(self, state):
        still_in_camp = []
        for piece_idx, piece in enumerate(state.current_player.pieces):
            if state.current_player.camp[(piece.x, piece.y)]:
                still_in_camp.append(piece_idx)
        return still_in_camp

    def in_to_out_opposite_camp(self, state, piece, destination):
        if state.current_player.color == 'BLACK':
            check = white_camp_cells
        else:
            check = black_camp_cells

        if check[(piece.x, piece.y)] and not check[destination]:
            return True
        else:
            return False

    def get_possible_actions(self, state):
        first_of_rest = True
        possible_actions = []
        jump_destinations = []
        inside_to_outside = []
        further_from_corner = []
        closer_to_other_corner = []
        leading_to_oppoisite_camp = []

        player_color = state.current_player.color
        if player_color == 'BLACK':
            basic_actions_list = self.basic_actions_for_black
            jump_actions_list = self.jump_actions_for_black
        elif player_color == 'WHITE':
            basic_actions_list = self.basic_actions_for_white
            jump_actions_list = self.jump_actions_for_white
        else:
            return None

        still_in_camp_idxs = self.pieces_still_in_camp_of_current_player(state)
        if len(still_in_camp_idxs) > 0:
            movable_idxs = still_in_camp_idxs
        else:
            movable_idxs = [i for i in range(19)]

        rest_of_idxs = [i for i in range(19) if i not in movable_idxs]
        # random.shuffle(movable_idxs)
        # random.shuffle(rest_of_idxs)
        for piece_idx, piece in zip(movable_idxs + rest_of_idxs,
                                    [state.current_player.pieces[i] for i in movable_idxs + rest_of_idxs]):
            if piece_idx in rest_of_idxs:
                if first_of_rest:
                    first_of_rest = False
                    if len(inside_to_outside) > 0 or len(further_from_corner) > 0:
                        break

            # for each piece, clear the previously visited list and initialize it with the original position.
            been_there = [(piece.x, piece.y)]

            for action in jump_actions_list:
                destination = self.transition_fn(state, (piece.x, piece.y), action)
                if destination is not None:

                    possible_action = [piece_idx, action, (piece.x, piece.y), destination]
                    if not self.in_to_out_opposite_camp(state, piece, destination):
                        possible_actions.append([possible_action])

                        if state.current_player.camp[(piece.x, piece.y)] and not state.current_player.camp[destination]:
                            inside_to_outside.append([possible_action])
                        elif self.is_further_from_corner(state, piece, destination):
                            further_from_corner.append([possible_action])
                        if self.is_closer_to_opposite_corner(state, piece, destination):
                            closer_to_other_corner.append([possible_action])
                        if self.lead_to_opposite_camp(state, piece, destination):
                            leading_to_oppoisite_camp.append([possible_action])

                        jump_destinations.append(
                            JumpDestination(destination=destination, jump_series=[possible_action]))
                        been_there.append(destination)

            while len(jump_destinations) > 0:
                exploring = jump_destinations[0]
                for action_again in jump_actions_list:
                    destination = self.transition_fn(state, source=exploring.destination, single_action=action_again)
                    if destination is not None and destination not in been_there:
                        if not self.in_to_out_opposite_camp(state, piece, destination):
                            copy_of_jump_series = copy.deepcopy(exploring.jump_series)
                            copy_of_jump_series.append([piece_idx, action_again, exploring.destination, destination])
                            possible_action = copy_of_jump_series
                            possible_actions.append(possible_action)
                            if state.current_player.camp[(piece.x, piece.y)] \
                                    and not state.current_player.camp[destination]:
                                inside_to_outside.append(possible_action)
                            elif self.is_further_from_corner(state, piece, destination):
                                further_from_corner.append(possible_action)
                            if self.is_closer_to_opposite_corner(state, piece, destination):
                                closer_to_other_corner.append(possible_action)
                            if self.lead_to_opposite_camp(state, piece, destination):
                                leading_to_oppoisite_camp.append(possible_action)

                            jump_destinations.append(
                                JumpDestination(destination=destination, jump_series=possible_action))
                            been_there.append(destination)
                jump_destinations.remove(exploring)

            # possible_basic_actions
            for action in basic_actions_list:
                destination = self.transition_fn(state, (piece.x, piece.y), action)
                if destination is not None:
                    if not self.in_to_out_opposite_camp(state, piece, destination):
                        possible_action = [piece_idx, action, (piece.x, piece.y), destination]
                        possible_actions.append([possible_action])
                        if state.current_player.camp[(piece.x, piece.y)] and not state.current_player.camp[destination]:
                            inside_to_outside.append([possible_action])
                        elif self.is_further_from_corner(state, piece, destination):
                            further_from_corner.append([possible_action])
                        if self.is_closer_to_opposite_corner(state, piece, destination):
                            closer_to_other_corner.append([possible_action])
                        if self.lead_to_opposite_camp(state, piece, destination):
                            leading_to_oppoisite_camp.append([possible_action])

            # random.shuffle(closer_to_other_corner)
            # random.shuffle(leading_to_oppoisite_camp)
            # random.shuffle(possible_actions)
            # random.shuffle(inside_to_outside)
            # random.shuffle(further_from_corner)

        if len(inside_to_outside):
            return inside_to_outside
        # elif 0 < len(inside_to_outside) <= 19:
        #     return inside_to_outside
        elif len(movable_idxs) < 19 and len(further_from_corner) > 0:
            return further_from_corner
        # elif len(leading_to_oppoisite_camp) > 0:
        #     return leading_to_oppoisite_camp
        # elif len(closer_to_other_corner) > 0:
        #     return closer_to_other_corner
        elif len(further_from_corner):
            return further_from_corner
        # elif 0 < len(further_from_corner) <= 19:
        #     return further_from_corner
        else:
            return possible_actions

    def is_further_from_corner(self, state, piece, destination):
        if state.current_player.color == 'BLACK':
            if destination[0] >= piece.x and destination[1] >= piece.y:
                return True
            else:
                return False
        else:
            if destination[0] <= piece.x and destination[1] <= piece.y:
                return True
            else:
                return False

    def is_closer_to_opposite_corner(self, state, piece, destination):
        if state.current_player.color == 'BLACK':
            if destination[0] > piece.x and destination[1] > piece.y:
                return True
            else:
                return False
        else:
            if destination[0] < piece.x and destination[1] < piece.y:
                return True
            else:
                return False

    def lead_to_opposite_camp(self, state, piece, destination):
        if state.current_player.color == 'BLACK':
            if (piece.x, piece.y) not in white_camp_cells and destination in white_camp_cells:
                return True
            else:
                return False
        else:
            if (piece.x, piece.y) not in black_camp_cells and destination in black_camp_cells:
                return True
            else:
                return False

    def utility(self, winner):
        if not (self.player_max.color == winner):
            return -1 * math.inf
        else:
            return math.inf

    def result(self, state, piece_idx, source, destination):
        resulting_state = copy.deepcopy(state)
        resulting_state.current_player.move(piece_idx, destination)
        resulting_state.update_board(set_empty=source, set_full=destination, color=state.current_player.color)
        resulting_state.current_player, resulting_state.other_player = resulting_state.other_player, resulting_state.current_player
        return resulting_state

    def apply_action(self, piece_idx, source, destination):
        self.current_state.update_board(set_empty=source, set_full=destination,
                                        color=self.current_state.current_player.color)
        self.current_state.current_player.move(piece_idx, destination)
        self.current_state.current_player, self.current_state.other_player = self.current_state.other_player, \
                                                                             self.current_state.current_player
