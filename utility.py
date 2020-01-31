def read_input_file():
    with open('input.txt') as file:
        input_dict = dict()
        lines = file.readlines()
        input_dict['type'] = lines[0].strip().upper()
        input_dict['color'] = lines[1].strip().upper()
        input_dict['total_time'] = float(lines[2].strip())
        board_string = lines[3:]
        board = []
        for row in board_string:
            board.append(list(row.strip().upper()))
        input_dict['board'] = board
        return input_dict


class JumpDestination:
    def __init__(self, destination, jump_series):
        self.destination = destination
        self.jump_series = jump_series

    def __str__(self):
        return '{}, {}'.format(self.destination, self.jump_series)
