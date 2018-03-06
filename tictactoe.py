import os


class Game:
    def __init__(self):
        size = self.get_valid_size()
        total_spots = size**2
        self.size = size
        self.x_turn = True
        self.player_x_name = self.get_player_name_input('x')
        self.player_o_name = self.get_player_name_input('o')
        self.who = 'x'
        self.winner_exists = False
        self.moves = [' '] * total_spots
        self.moves_left = total_spots
        self.player_x_moves = [None] * total_spots
        self.player_o_moves = [None] * total_spots

    @staticmethod
    def print_cat():
        print('tie game, nice try!')
        print('  A_A')
        print(' (-.-)')
        print('  |-|')
        print(' /   \ ')
        print('|     |   __')
        print('|  || |  |  \__')
        print(' \_||_/_/')

    @staticmethod
    def print_board(size, moves):
        os.system('clear')
        print('Tic-tac-toe\n')

        print('  ', end='')
        for j in range(size):
            print(' {}  '.format(j), end='')
        print()

        for i in range(size):
            # Row
            print('{} '.format(i), end='')
            for j in range(size):
                # Columns
                if j < size - 1:
                    print(' {} |'.format(moves[i * size + j]), end='')
                else:
                    print(' {} '.format(moves[i * size + j]), end='')
            print()
            if i < size - 1:
                print('  ', end='')
                print('---+' * (size-1), end='')
                print('---')

    @staticmethod
    def print_winner(player_name):
        print('{} wins\ncongratulations!'.format(player_name))
        # Art by Joan Stark
        print("                      . : .")
        print("      __________    '.  :  .'")
        print("     /         /\__.__'.:.'  .")
        print("     \_________\/  .  .':'.  .")
        print("                    .'  :  '.")
        print("jgs                   ' : '")

    @staticmethod
    def _winning_row_exists(board_width, player_moves):
        for i in range(0, board_width ** 2, board_width):
            if player_moves[i: i + board_width].count(True) == board_width:
                return True
        return False

    @staticmethod
    def _winning_col_exists(board_width, player_moves):
        # for every column
        for j in range(board_width):
            # check all rows
            found = 0
            for i in range(board_width):
                start_of_row = i * board_width
                if player_moves[start_of_row + j]:
                    found += 1
            if found == board_width:
                return True

    @staticmethod
    def _winning_diagonal_exists(board_width, player_moves):
        found = 0
        for i in range(board_width):
            if player_moves[i*board_width + i]:
                found += 1
        if found == board_width:
            return True

        # check other diagonal
        found = 0
        for i in range(board_width):
            start_of_row = i * board_width
            column_position = board_width - 1 - i
            if player_moves[start_of_row + column_position]:
                found += 1
        return found == board_width

    @staticmethod
    def get_valid_size():
        while True:
            try:
                size = int(input('Input size between 2 and 10: '))
            except ValueError:
                print('enter an integer')
                continue
            if 2 > size or size > 10:
                print('size is out of range')
                continue
            return size

    @staticmethod
    def get_player_name_input(symbol):
        while True:
            name = input('Player {} name: '.format(symbol))
            if 2 > len(name) > 10:
                print('wrong size name')
                continue
            return name.capitalize()

    def get_player_name(self):
        return self.player_x_name if self.x_turn else self.player_o_name

    def is_winner(self, player_moves):
        board_width = self.size
        if self._winning_row_exists(board_width, player_moves):
            return True
        if self._winning_col_exists(board_width, player_moves):
            return True
        return self._winning_diagonal_exists(board_width, player_moves)

    def draw_board(self):
        player_x_moves = self.player_x_moves
        player_o_moves = self.player_o_moves
        moves = self.moves

        os.system('clear')

        for i in range(len(moves)):
            if player_x_moves[i] and player_o_moves[i]:
                # Should never happen
                raise Exception('both players on same spot')
            if player_x_moves[i]:
                moves[i] = 'x'
            if player_o_moves[i]:
                moves[i] = 'o'

        self.print_board(self.size, moves)

    def get_valid_move(self):
        size = self.size
        player_name = self.get_player_name()
        print("Turn: '{}' - {}'s move".format(self.who, player_name))
        while True:
            try:
                row, col = [abs(int(n)) for n in input('Input row & column: ')]
            except ValueError:
                print('enter two single digit integers')
                continue
            if row >= size:
                print('row is out of range')
                continue
            if col >= size:
                print('col is out of range')
                continue
            move = row * size + col
            if self.player_x_moves[move] or self.player_o_moves[move]:
                print('place is already taken on board')
                continue
            return move

    def make_move(self, move):

        player_moves = self.player_x_moves if self.x_turn else self.player_o_moves

        player_moves[move] = True

        if self.is_winner(player_moves):
            self.winner_exists = True

    def set_who(self):
        self.who = 'x' if self.x_turn else 'o'

    def play_game(self):
        self.draw_board()

        while self.moves_left and not self.winner_exists:
            self.set_who()

            # move happens
            move = self.get_valid_move()
            self.make_move(move)

            self.draw_board()

            if self.winner_exists:
                self.print_winner(self.get_player_name())

            # change turns
            self.x_turn = not self.x_turn
            self.moves_left -= 1

        if not self.winner_exists:
             self.print_cat()

if __name__ == '__main__':
    game = Game()
    game.play_game()
