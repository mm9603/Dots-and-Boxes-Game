import random
import statistics

class Game:
    def __init__(self, tiles_per_row):
        self.tiles_per_row = tiles_per_row
        self.total_tiles = tiles_per_row ** 2

        # adjacency matrix for the board (because
        # this matrix is symmetric, only the upper right half is used.)
        self.am = []

        n = tiles_per_row + 1
        v = n ** 2

        self.vertices_per_row = n
        self.total_vertices = v

        self.valid_moves = []

        for i in range(v):
            r = [] # new row
            for j in range(v):
                if j == i + 1 and i % n != n - 1:
                    r.append(1)
                    self.valid_moves.append( (i, j) )
                elif j == i + n:
                    r.append(1)
                    self.valid_moves.append( (i, j) )
                else:
                    r.append(0)
            self.am.append(r)

        self.board = [-1] * tiles_per_row ** 2
        self.score = [0, 0]

    def move(self, player, input):
        '''Takes in a string of two vertices between which a move is meant
        to be made and either returns an integer representative of an error
        or records and move and determines if any points were scored.'''
        try:
            a, b = input.split()
            a = int(a)
            b = int(b)
        except:
            return -1
        if a > b:
            i = b
            j = a
        else:
            i = a
            j = b

        if self.am[i][j] == 1:
            self.am[i][j] = 2
            self.valid_moves.remove( (i,j) )
            if self.check_for_box(player, i, j):
                return 1
            return 0
        elif self.am[i][j] == 2:
            return -2
        else:
            return -3

    def check_for_box(self, player, a, b):
        '''Checks the board to determine whether or not
        one or two new boxes have been formed. Increases the
        score of whichever player formed the new box/boxes.'''
        
        am = self.am
        n = self.vertices_per_row
        v = self.total_vertices

        flag = False

        for i in range(v):
            for j in range(v):
                ul = i
                ur = j
                ll = j + n - 1
                lr = j + n

                try:
                    if  (((ul == a and ur == b) or
                        (ul == a and ll == b) or
                        (ur == a and lr == b) or
                        (ll == a and lr == b)) and
                        am[ul][ur] == 2 and
                        am[ul][ll] == 2 and
                        am[ur][lr] == 2 and
                        am[ll][lr] == 2):
                            self.board[j - j // n - 1] = player
                            self.score[player] += 1
                            flag = True
                except IndexError:
                    pass
        
        return flag

    def _get_horizontal_dash(self, i, j):
        '''Returns a horizontal dash if there is a connection
        between vertices i and j.'''
        if self.am[i][j] == 2:
            return '-'
        return ' '

    def _get_vertical_dash(self, i, j):
        '''Returns a vertical dash if there is a connection
        between vertices i and j.'''
        if self.am[i][j] == 2:
            return '|'
        return ' '

    def _get_tile_value(self, i, j):
        '''Private function used to translate the data structure's
        recording of a player (0 or 1) into the letter representing that player
        (A or B)'''
        n = self.vertices_per_row
        a = i * n + j - n - i

        x = self.board[a]

        if x == 0:
            return 'A'
        elif x == 1:
            return 'B'
        return ' '


    def draw_board(self):
        '''Returns a string representing the board and the current score for each player.'''
        n = self.vertices_per_row

        output = ' 0'
        for j in range(1, n):
            output += ' {} {}'.format(self._get_horizontal_dash(j - 1, j), j)
        for i in range(1, n):
            output += '\n {}'.format(self._get_vertical_dash(i * n - n, i * n))
            for j in range(1, n):
                output += ' {} {}'.format(self._get_tile_value(i, j),
                    self._get_vertical_dash((i * n - n) + j, i * n + j))
            output += '\n{:2d}'.format(i * n)
            for j in range(1, n):
                output += ' {}{:2d}'.format(self._get_horizontal_dash(i * n + j - 1, i * n + j), i * n + j)

        output += '\n'

        output += 'Score is A:{} and B:{}'.format(*self.score)

        return output

    def _get_player_name(self, x):
        '''Returns the letter representation of player (0 is A, 1 is B).'''
        if x == 0:
            return 'A'
        elif x == 1:
            return 'B'

    def play_game_with_output_and_input(self):
        '''Allows two users to play the game with ouput being printed.'''
        active_player = random.randint(0, 1)

        print('Player {} goes first!\n'.format(self._get_player_name(active_player)))

        print(self.draw_board())

        while sum(self.score) < self.total_tiles:

            while True:
                move = input("Player {}'s turn: ".format(self._get_player_name(active_player)))
                result = self.move(active_player, move)
                if result == 0:
                    print(self.draw_board())
                    if active_player == 1:
                        active_player = 0
                    else:
                        active_player = 1
                    break
                elif result == 1:
                    print(self.draw_board())
                    break
                elif result == -1:
                    print('Invalid input format, please try again.\n')
                elif result == -2:
                    print('A move cannot be made between these dots: they are already connected\n')
                elif result == -3:
                    print('A move cannot be made between these dots: they are not adjacent\n')

        print('Game is over, all tiles have been filled')
        if self.score[0] > self.score[1]:
            print('Player A wins!')
        elif self.score[1] > self.score[0]:
            print('Player B wins!')
        else:
            print("It's a tie!")

    def play_game_with_output_no_input(self):
        '''Plays the game without actual players, with each move being
        determined by random number generation. Outputs the results to a file.'''
        active_player = random.randint(0, 1)

        output = 'Player {} goes first!\n'.format(self._get_player_name(active_player))

        output += self.draw_board()

        while sum(self.score) < self.total_tiles:

            result = self.random_play(active_player)
            if result == 0:
                if active_player == 1:
                    active_player = 0
                else:
                    active_player = 1
            output += self.draw_board()

        output += 'Game is over, all tiles have been filled\n'
        if self.score[0] > self.score[1]:
            output += 'Player A wins!'
        elif self.score[1] > self.score[0]:
            output += 'Player B wins!'
        else:
           output += "It's a tie!"

        fp = open('single_play.txt', 'w')
        fp.write(output)
        fp.close()

    def random_play(self, player):
        '''Uses random number generation to determine which move to make.'''
        x = random.randint(0, len(self.valid_moves) - 1)

        move = self.valid_moves[x]
        move = str(move[0]) + ' ' + str(move[1])

        return self.move(player, move)

    def play_game_with_no_output_no_input(self):
        '''Plays the game without actual players, with each move being
        determined by random number generation. Returns data about the game.'''
        active_player = random.randint(0, 1)

        rounds = 0

        while sum(self.score) < self.total_tiles:
            rounds += 1

            result = self.random_play(active_player)
            if result == 0:
                if active_player == 1:
                    active_player = 0
                else:
                    active_player = 1

        if self.score[0] > self.score[1]:
            return rounds, self.score[0], self.score[1], 0
        elif self.score[1] > self.score[0]:
            return rounds, self.score[0], self.score[1], 1
        else:
            return rounds, self.score[0], self.score[1], 2
        


        

def main():
    answer = input('Enter how many tiles per row you would like to play with on the board: ')

    while True:
        try:
            tiles_per_row = int(answer)
            game = Game(tiles_per_row)
            break
        except:
            print('Invalid input, please try again.')
            answer = input('Enter how many tiles per row you would like to play with on the board: ')

    answer = input('Enter a random seed integer: ')

    while True:
        try:
            seed = int(answer)
            random.seed(seed)
            break
        except:
            print('Invalid input, please try again.')
            answer = input('Enter a random seed integer: ')
    
    answer = input('Enter a number of rounds to play: ')

    while True:
        try:
            rounds = int(answer)
            break
        except:
            print('Invalid input, please try again.')
            answer = input('Enter a number of rounds to play: ')

    game.play_game_with_output_no_input()

    results = []
    wins = [0, 0, 0]

    for _ in range(rounds):
        game = Game(tiles_per_row)
        result = game.play_game_with_no_output_no_input()
        results.append(result)
        wins[result[3]] += 1

    total_rounds = sum([i[0] for i in results])

    avg_1 = statistics.mean([i[1] for i in results])
    avg_2 =  statistics.mean([i[2] for i in results])

    med_1 = statistics.median([i[1] for i in results])
    med_2 =  statistics.median([i[2] for i in results])

    max_1 = max([i[1] for i in results])
    max_2 = max([i[2] for i in results])

    min_1 = min([i[1] for i in results])
    min_2 = min([i[2] for i in results])

    output = '''
Total number of rounds played: {}
Player 1 average: {}
Player 2 average: {}
Player 1 median: {}
Player 2 median: {}
Player 1 highest score: {}
Player 2 highest score: {}
Player 1 lowest score: {}
Player 2 lowest score: {}
Player 1 total wins: {}
Player 2 total wins: {}
Ties: {}
'''.format(
    total_rounds,
    avg_1,
    avg_2,
    med_1,
    med_2,
    max_1,
    max_2,
    min_1,
    min_2,
    wins[0],
    wins[1],
    wins[2]
)
    fp = open('multiple_play.txt', 'w')
    fp.write(output)
    fp.close()



if __name__ == '__main__':
    main()
            






