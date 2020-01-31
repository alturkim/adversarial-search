from utility import read_input_file
from adversarial_game import Player, Piece, Game, State, Node
from algorithms import alpha_beta_search
import copy
import time

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

black_camp_cells = dict()
white_camp_cells = dict()
for cell in all_cells:
    black_camp_cells[cell] = False
    white_camp_cells[cell] = False
for cell in black_camp_cells_list:
    black_camp_cells[cell] = True
for cell in white_camp_cells_list:
    white_camp_cells[cell] = True


if __name__ == '__main__':
    input_dict = read_input_file()
    if input_dict['type'] == 'GAME':
        black_pieces = []
        white_pieces = []
        for i in range(16):
            for j in range(16):
                if input_dict['board'][i][j].upper() == 'B':
                    black_pieces.append(Piece(x=j, y=i, color='BLACK'))
                elif input_dict['board'][i][j].upper() == 'W':
                    white_pieces.append(Piece(x=j, y=i, color='WHITE'))
        if input_dict['color'] == 'BLACK':
            player_max = Player('BLACK', black_pieces, camp=black_camp_cells)
            player_min = Player('WHITE', white_pieces, camp=white_camp_cells)
        else:
            player_max = Player('WHITE', white_pieces, camp=white_camp_cells)
            player_min = Player('BLACK', black_pieces, camp=black_camp_cells)

        initial_state = State(board=input_dict['board'], current_player=player_max, other_player=player_min)

        basic_actions_for_black = ['SE', 'S', 'E', 'SW', 'W', 'NE', 'NW', 'N']
        jump_actions_for_black = ['SE_JUMP', 'S_JUMP', 'E_JUMP', 'SW_JUMP', 'W_JUMP', 'NE_JUMP', 'NW_JUMP', 'N_JUMP']

        basic_actions_for_white = ['NW', 'N', 'W', 'NE', 'E', 'SW', 'SE', 'S']
        jump_actions_for_white = ['NW_JUMP', 'N_JUMP', 'W_JUMP', 'NE_JUMP', 'E_JUMP', 'SW_JUMP', 'SE_JUMP', 'S_JUMP']

        game = Game(init_state=initial_state, player_max=player_max, player_min=player_min,
                    basic_actions_for_black=basic_actions_for_black, jump_actions_for_black=jump_actions_for_black,
                    basic_actions_for_white=basic_actions_for_white, jump_actions_for_white=jump_actions_for_white)



        total_t = 0
        for i in range(1, 10000):

            print(game)
            is_terminal, winner = game.terminal_test(game.current_state)
            if is_terminal:
                print(winner)
                print('required iterations=', i)
                print('required time= ', total_t)
                break
            game_copy = copy.deepcopy(game)
            st = time.time()
            recommended_action = alpha_beta_search(game=game_copy,
                                                   node=Node(state=game.current_state, parent=None, action=None),
                                                   iteration=i)
            outputs = ''
            for output in recommended_action[1]:
                if output[1].find('J') >= 0:
                    outputs += 'J '
                else:
                    outputs += str(output[1]) + ' '
                outputs += str(output[2][0]) + ',' + str(output[2][1]) + ' '
                outputs += str(output[3][0]) + ',' + str(output[3][1])
                outputs += '\n'

            et = time.time()
            t = et - st
            total_t += t

            game.apply_action(recommended_action[1][0][0], source=recommended_action[1][0][2],
                              destination=recommended_action[1][-1][3])

