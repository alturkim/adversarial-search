import math
from adversarial_game import Node
import time

depth = 0
max_depth = 1


def min_value(game, node, alpha, beta):
    global depth
    if game.current_state.current_player is game.player_min:
        depth += 1

    is_terminal, winner = game.terminal_test(node.state)
    is_cutoff = game.cutoff_test(node.state, depth, max_depth)
    if not is_terminal and is_cutoff:
        return game.evaluation_function(node.state), node.action, alpha
    if is_terminal:
        return game.utility(winner), node.action, alpha
    v = math.inf
    v_dict = {v: [[None, (None, None), (None, None)]]}
    list_of_list_of_actions = game.get_possible_actions(node.state)
    examined_nodes = 0
    local_copy_depth = depth
    for list_of_actions in list_of_list_of_actions:
        examined_nodes += 1
        piece_idx = list_of_actions[0][0]
        source = list_of_actions[0][2]
        destination = list_of_actions[-1][3]
        return_of_max_value = max_value(game, Node(state=game.result(node.state, piece_idx, source, destination),
                                                   parent=node, action=list_of_actions), alpha, beta)
        beta = min(return_of_max_value[0], beta)
        v = min(v, return_of_max_value[0])
        v_dict[v] = list_of_actions
        if v <= alpha:
            return v, v_dict[v], alpha
        beta = min(beta, v)
        depth = local_copy_depth
    return v, v_dict[v], alpha


def max_value(game, node, alpha, beta):
    global depth
    if game.current_state.current_player is game.player_max:
        depth += 1
    is_terminal, winner = game.terminal_test(node.state)
    is_cutoff = game.cutoff_test(node.state, depth, max_depth)
    if not is_terminal and is_cutoff:
        return game.evaluation_function(node.state), node.action, beta
    if is_terminal:
        return game.utility(winner), node.action, beta
    v = -math.inf
    v_dict = {v: [[None, (None, None), (None, None)]]}
    list_of_list_of_actions = game.get_possible_actions(node.state)
    examined_nodes = 0
    local_copy_depth = depth
    for list_of_actions in list_of_list_of_actions:
        examined_nodes += 1
        piece_idx = list_of_actions[0][0]
        source = list_of_actions[0][2]
        destination = list_of_actions[-1][3]
        return_of_min_value = min_value(game, Node(state=game.result(node.state, piece_idx, source, destination),
                                                   parent=node, action=list_of_actions), alpha, beta)
        alpha = max(return_of_min_value[0], alpha)
        v = max(v, return_of_min_value[0])
        v_dict[v] = list_of_actions
        if v >= beta:
            return v, v_dict[v], beta
        alpha = max(alpha, v)
        depth = local_copy_depth
    return v, v_dict[v], beta


def alpha_beta_search(game, node, iteration):
    global depth, max_depth
    depth = 0
    # if max_depth < 4:
    # if iteration%200 == 0 and max_depth <4:
    #     max_depth += 0.01
    #     print(max_depth)
    # print('max_depth', max_depth)
    if game.current_state.current_player is game.player_max:
        v, list_of_actions, _ = max_value(game, node, -math.inf, math.inf)
        return v, list_of_actions
    else:
        v, list_of_actions, _ = min_value(game, node, -math.inf, math.inf)
        return v, list_of_actions
