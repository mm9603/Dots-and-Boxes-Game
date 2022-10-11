import random
import statistics

class Game:
    def __init__(self, boxes_per_row):
        self.boxes_per_row = boxes_per_row
        self.total_boxes = boxes_per_row ** 2

        # List representing the game board.
        # Each position can contain one of the following values:
        # -1 - implies that the box has not been filled.
        #  0 - implies that the box has been filled by player 1.
        #  1 - implies that the box has been filled by player 2.
        self.board = [-1] * boxes_per_row ** 2

        # Keeps track of each player's score.
        # Postion 0 contains player 1's points while
        # position 1 contains player 2's points.
        self.score = [0, 0]

        # Adjacency matrix for the board (because
        # this matrix is symmetrical, only the upper right half is used).
        # Represented as a n x n list of lists, where n is the number of
        # dots per row on the board. Each postion (i, j) can contain
        # one of the following values:
        #
        #  0 - implies that a move cannot be made between dots i and j
        #      because they are not adjacent.
        #  1 - implies that a move can be made between dots i and j.
        #  2 - mplies that a move had already been made between dots i and j.
        self.am = []

        
        n = boxes_per_row + 1
        v = n ** 2

        # Number of dots per row/column on board.
        self.dots_per_row = n

        # Total number of dots on the board.
        self.total_dots = v

        # Keeps track of which moves are available
        # for random_play() to make.
        self.valid_moves = []

        # This constructs the adjacency matrix
        # and the list of valid moves.
        for i in range(v):
            r = [] # new row in adjacency matrix.
            for j in range(v):
                if (j == i + 1 and i % n != n - 1) or j == i + n:
                    # Adds a 1 in the position (i, j) in the adjacency matrix
                    # to represent that dots i and j are adjacent.
                    r.append(1)
                    # Adds the move between dots i and j to the list of valid moves.
                    self.valid_moves.append( (i, j) )
                else:
                    # Adds a 0 in the position (i, j) in the adjacency matrix
                    # to represent that dots i and j are not adjacent.
                    r.append(0)
            self.am.append(r)

    def move(self, player, input):
        '''Takes in a string of two space-seperated integers representing
        two dots between which a move is meant to be made. Returns an integer
        representing the outcome of attempting to make the move. Each integer
        represents the following:

         0 - Input resulted in a valid move but a point was not made.
         1 - Input resulted in a valid move and a point was made.
        -1 - Input was not formatted properly so no move was made.
        -2 - Input designated a move between dots which were already connected
             so no move was made.
        -3 - Input designated a move between dots which were not adjacent
             so no move was made.
        '''

        # Attempts to read input into variables a and b,
        # each representing a dot. If input is formatted
        # incorrectly, returns -1.
        try:
            a, b = input.split()
            a = int(a)
            b = int(b)
        except:
            return -1

        # Because only the upper-right half of the adjacency
        # matrix is being used, each position must be referenced
        # by (i, j) where j is greater than i.
        if a > b:
            i = b
            j = a
        else:
            i = a
            j = b

        # Checks to see if a move can be made between i and j.
        if self.am[i][j] == 1:
            # Marks dots i and j as connected.
            self.am[i][j] = 2

            # Removes the move between i and j from the list of valid moves.
            self.valid_moves.remove( (i,j) )

            # Calls check_for_box() to see if connecting i and j has closed a box.
            if self.check_for_box(player, i, j):
                return 1 # Returns 1 if a box was closed.

            return 0 # Returns 0 if no box was closed.

        # Checks to see if i and j are already connected.
        elif self.am[i][j] == 2:
            return -2

        # Executes if i and j are not adjacent.
        else:
            return -3

    def check_for_box(self, player, a, b):
        '''Checks each box on the board to determine whether or not
        one or two boxes have been closed by making a connection
        between dots a and b. If one or two new boxes have been formed,
        the score of whichever player closed the box/boxes in increased and
        True is returned. Otherwise, returns false.'''

        # Indicates whether or not a new box was formed by connecting a and b.
        box_was_formed = False

        for i in range(self.total_dots):
            for j in range(self.total_dots):
                # Each of the following variable declarations establishes
                # a dot which is a corner of a box that has potentially been closed.
                upper_left_dot = i 
                upper_right_dot = j
                lower_left_dot = j + self.dots_per_row - 1
                lower_right_dot = j + self.dots_per_row

                try:
                    # First checks to see whether or not a and b
                    # belong to the box being checked and are non-diagonally adjacent.
                    # Then, checks to see if all sides of the box have been closed.
                    if  (((upper_left_dot == a and upper_right_dot == b) or
                        (upper_left_dot == a and lower_left_dot == b) or
                        (upper_right_dot == a and lower_right_dot == b) or
                        (lower_left_dot == a and lower_right_dot == b)) and
                        self.am[upper_left_dot][upper_right_dot] == 2 and
                        self.am[upper_left_dot][lower_left_dot] == 2 and
                        self.am[upper_right_dot][lower_right_dot] == 2 and
                        self.am[lower_left_dot][lower_right_dot] == 2):
                            # Marks where on the board the player scored a point.
                            self.board[j - j // self.dots_per_row - 1] = player

                            # Increases the score of the player who scored a point.
                            self.score[player] += 1

                            box_was_formed = True

                except IndexError:
                    # Not every dot has a box to its lower right (i.e. dots in the
                    # last column and/or last row of the board).
                    # Whenever this is the case, trying to find corners of
                    # such a box will result in an IndexError being thrown. These
                    # dots are ignored.
                    pass
        
        return box_was_formed

    def _get_horizontal_dash(self, i, j):
        '''Used for formatting when displaying the board.
        Checks the adjacency matrix for a connection beween dots i and j,
        returning a horizontal dash if the connection exists and a space if it
        does not.'''
        if self.am[i][j] == 2:
            return '-'
        return ' '

    def _get_vertical_dash(self, i, j):
        '''Used for formatting when displaying the board.
        Checks the adjacency matrix for a connection beween dots i and j,
        returning a vertical dash if the connection exists and a space if it
        does not.'''
        if self.am[i][j] == 2:
            return '|'
        return ' '

    def _get_box_value(self, i, j):
        '''Used for formatting when displaying the board.
        Gets the value of the tile in the ith row and jth column of the board
        and translates it to A for 0 and B for 1.'''
        n = self.dots_per_row
        a = i * n + j - n - i

        x = self.board[a]

        if x == 0:
            return 'A'
        elif x == 1:
            return 'B'
        return ' '


    def draw_board(self):
        '''Returns a string representing the board and the current score for each player.'''

        n = self.dots_per_row # Condenses varaible name for readability

        output = ' 0'
        # Adds the first row of dots to the board's string representation
        for j in range(1, n):
            output += ' {} {}'.format(self._get_horizontal_dash(j - 1, j), j)
        # Adds the remaining rows of dotsto the board's string representation,
        # as well as the row of boxes.
        for i in range(1, n):
            output += '\n {}'.format(self._get_vertical_dash(i * n - n, i * n))
            for j in range(1, n):
                output += ' {} {}'.format(self._get_box_value(i, j),
                    self._get_vertical_dash((i * n - n) + j, i * n + j))
            output += '\n{:2d}'.format(i * n)
            for j in range(1, n):
                output += ' {}{:2d}'.format(self._get_horizontal_dash(i * n + j - 1, i * n + j), i * n + j)

        output += '\n'

        output += 'Score is A:{} and B:{}\n'.format(*self.score)

        return output

    def _get_player_name(self, x):
        '''Returns the letter representation of player (0 is A, 1 is B).'''
        if x == 0:
            return 'A'
        elif x == 1:
            return 'B'

    def random_play(self, player):
        '''Uses random number generation to determine which move to make.'''

        # Selects a move at random from valid_moves.
        x = random.randint(0, len(self.valid_moves) - 1)
        move = self.valid_moves[x]

        # Converts the move to a formatted string which can be interpretted by
        # move function.
        move = str(move[0]) + ' ' + str(move[1])

        return self.move(player, move)

    
    def play_with_output(self, starting_player):
        '''Plays a game, pitting Winning Player against Random Player.
        The starting_player variable should be 0 if Winning Player is meant to go
        first and 1 if Random Player is meant to go first. Returns a play-by-play
        of the game as a formatted string.'''

        winning_player = WinningPlayer(self)

        active_player = starting_player

        output = 'Player {} goes first!\n'.format(self._get_player_name(active_player))

        output += self.draw_board()

        # Continues playing until all possible points have been scored.
        while sum(self.score) < self.total_boxes:

            # It is winning player's turn.
            if active_player == 0:
                output += "Player A's turn!\n"
                winning_player_move = winning_player.determine_next_move(self)
                result = self.move(active_player, winning_player_move)

                # If no point was scored, switches active player to the other player
                if result == 0:
                    if active_player == 1:
                        active_player = 0
                    else:
                        active_player = 1
                output += self.draw_board()
            # It is random player's turn.
            else:
                output += "Player B's turn!\n"
                result = self.random_play(active_player)

                # If no point was scored, switches active player to the other player
                if result == 0:
                    if active_player == 1:
                        active_player = 0
                    else:
                        active_player = 1
                output += self.draw_board()

        output += 'Game is over, all boxes have been filled\n'
        if self.score[0] > self.score[1]:
            output += 'Player A wins!'
        elif self.score[1] > self.score[0]:
            output += 'Player B wins!'
        else:
           output += "It's a tie!"

        return output

    def play_game_without_output(self):
        '''Plays a game, pitting Winning Player against Random Player.
        The starting_player is selected at random. Data regarding the outcome of
        the game is returned once the game is finished.'''

        # Player A is Winning Player.
        winning_player = WinningPlayer(self)

        # The starting player is chosen at random.
        active_player = random.randint(0, 1)

        # Keeps track of the number of rounds played.
        rounds = 0

        # Continues playing until all possible points have been scored.
        while sum(self.score) < self.total_boxes:
            rounds += 1

            # It is winning player's turn.
            if active_player == 0:
                winning_player_move = winning_player.determine_next_move(self)
                result = self.move(active_player, winning_player_move)

                # If no point was scored, switches active player to the other player
                if result == 0:
                    if active_player == 1:
                        active_player = 0
                    else:
                        active_player = 1

            # It is random player's turn.
            else:
                result = self.random_play(active_player)

                # If no point was scored, switches active player to the other player
                if result == 0:
                    if active_player == 1:
                        active_player = 0
                    else:
                        active_player = 1

        # Returns data regarding the outcome of the game.
        # The last member in the returned tuple is a 0 if
        # Winning Player won, a 1 if Random Player won
        # and a 2 if it was a tie.
        if self.score[0] > self.score[1]:
            return rounds, self.score[0], self.score[1], 0
        elif self.score[1] > self.score[0]:
            return rounds, self.score[0], self.score[1], 1
        else:
            return rounds, self.score[0], self.score[1], 2

class WinningPlayer:
    '''Class designed to store all relevant information about a game in order for
    Winning Player to perform such that their odds of winning are significantly higher
    than Random Player's. Also provides a function which returns the best possible
    move given the current condition of the board.'''

    def __init__(self, game):
        '''Using the game which is about to played, sets up an ordered list of
        moves which should be made in order, and makes a list of every box on the board
        (see Box class).'''

        # A list of moves which WinningPlayer is meant to make in order.
        # Doing so establishes the longest possible chain of boxes for the board.
        self.ordered_moves = []

        # Keeps track of how each box should be treated, i.e. under what condtions
        # should Winning Player close the box.
        self.boxes = []

        # Indicates whether or not the next move to be made is consecutive,
        # i.e. if a point was just scored.
        self.consecutive_move = False

        # The number of the last box closed by this player. Used to determine if adjacent
        # box can be closed on a consecutive move.
        self.last_closed_box = None

        # The number of the box which, when closed, started a chain of consecutive moves.
        # Must be stored so that the chain can be closed on both sides if possible.
        self.start_of_chain = None

        # Direction the chain is being traversed. False for backwards, True for forwards.
        self.chain_traversal_direction = None

        n = game.dots_per_row

        # Establishes a run of moves along the top row of dots
        # from left to right.
        for i in range(n-1):
            self.ordered_moves.append( (i, i+1) )

        # Establishes a move between the top right dot on the board
        # and the dot underneath it.
        self.ordered_moves.append( (n-1, 2*n - 1) )

        # Keeps track of the number of the left-most
        # dot in each row for the following iteration.
        offset = 0

        # Sets up ordered_moves.
        while True:
            offset += n

            # Establishes a run of moves along a row of dots starting at
            # offset from right to left, excluding the first and last possible moves.
            for i in range(offset + n - 2, offset + 1, -1):
                self.ordered_moves.append( (i-1, i) )

            # Halts iteration if there is no row underneath the row.
            if offset + n > game.total_dots - 1:
                break

            # Establishes a move from the left-most dot in the row to the
            # left-most dot in the row above it.            
            self.ordered_moves.append( (offset-n, offset) )

            # Establishes a move from the left-most dot in the row to the
            # left-most dot in the row underneath it.
            self.ordered_moves.append( (offset, offset+n) )

            offset += n

            # Establishes a run of moves along a row of dots starting at
            # offset from left to right, excluding the first and last possible moves.
            for i in range(offset, offset + n - 2):
                self.ordered_moves.append( (i, i+1) )

            # Halts iteration if there is no row underneath the row.
            if offset + 2*n -1 > game.total_dots - 1:
                break

            # Establishes a move from the right-most dot in the row to the
            # right-most dot in the row above it.     
            self.ordered_moves.append( (offset - 1, offset + n - 1) )

            # Establishes a move from the right-most dot in the row to the
            # right-most dot in the row underneath it. 
            self.ordered_moves.append( (offset + n - 1, offset + 2*n - 1) )

        # Establishes the last move necessary to complete a chain covering
        # the entire board.
        self.ordered_moves.append( (2*n -2, 2*n -1) )

        # Establishes directions for how each box on the board should be treated.
        for i in range(game.total_dots):
            # Dots along the right side and bottom of the board do not have a box to their
            # lower right.
            if i % n == n-1 or i >= n*(n-1):
                pass
            # Upper right box.
            elif i == n - 2:
                self.boxes.append(Box( ((i, i+1), (i+1, i+n+1)), ((i, i+n), (i+n, i+n+1)) ))
            
            # Any box along the left side of the board which is the bottom of a curve in the chain.
            elif i % (n*2) == n:
                self.boxes.append(Box( ((i, i+n), (i+n, i+n+1)), ( (i, i+1), (i+1, i+n+1)) ))
            
            # Any box along the right side of the board which is the top of a curve in the chain.
            elif i % (n*2) == 2*n - 2:
                self.boxes.append(Box( ((i, i+1), (i+1, i+n+1)), ((i, i+n), (i+n, i+n+1)) ))

            # Any box along the left side of the board which is the top of a curve in the chain.
            elif i % (n*2) == 0:
                self.boxes.append(Box( ((i, i+1), (i, i+n)), ((i+1, i+n+1), (i+n, i+n+1)) ))

            # Any box along the right side of the board which is the bottom of a curve in the chain.
            elif i % (n*2) == n - 2:
                self.boxes.append(Box( ((i+1, i+n+1), (i+n, i+n+1)), ((i, i+1), (i, i+n)) ))

            # Any box that is not in the left-most or right-most column on the board.
            else:
                self.boxes.append(Box( ((i, i+1), (i+n, i+n+1)), ((i, i+n), (i+1, i+n+1)) ))

    def determine_next_move(self, game):
        '''Analyzes the current condition of the board and determines
        the best possible move for Winning Player to make.'''

        # Keeps track of the best next move.
        next_move = None

        # Remove all moves from ordered_moves which are no longer valid.
        new_ordered_moves = []
        for move in self.ordered_moves:
            if move in game.valid_moves:
                new_ordered_moves.append(move)

        self.ordered_moves = new_ordered_moves

        # Marks any newly setup boxes as setup,
        # as well as any newly closable boxes as closable.
        for box in self.boxes:
            box.check_if_set_up(game.am)
            if box.check_if_closable(game.am):
                # If the box is closable, marks closing the box as the next move.
                next_move = box.final_move
                self.last_closed_box = self.boxes.index(box)
                self.start_of_chain = self.boxes.index(box)
                self.chain_traversal_direction = False

        # Executed if this one of a chain of consecutive moves
        if self.consecutive_move:
            # Chain is being traveresed backwards
            if self.chain_traversal_direction == False:
                # Either there is no next box in this direction or the next box is not closable.
                if self.last_closed_box == 0 or not self.boxes[self.last_closed_box - 1].closable:
                    # Begin traversing forwards from the start of the chain.
                    self.chain_traversal_direction = True

                    # Either there is no next box in this direction or the next box is not closable.
                    if self.start_of_chain == game.total_boxes - 1 or not self.boxes[self.start_of_chain + 1].closable:
                        # Marks the chain of consecutive moves as over.
                        self.consecutive_move = False
                    else:
                        # Marks closing the next box in this direction as the next move.
                        next_move = self.boxes[self.start_of_chain + 1].final_move
                        # Marks this box as the last closed box.
                        self.last_closed_box = self.start_of_chain + 1

                # The next box in this direction is closable
                else:
                    # Marks closing the next box in this direction as the next move.
                    next_move = self.boxes[self.last_closed_box - 1].final_move
                    # Marks this box as the last closed box.
                    self.last_closed_box = self.last_closed_box - 1
            else:
                # Either there is no next box in this direction or the next box is not closable.
                if self.last_closed_box == game.total_boxes - 1 or not self.boxes[self.last_closed_box + 1].closable:
                        # Marks the chain of consecutive moves as over.
                        self.consecutive_move = False
                else:
                    # Marks closing the next box in this direction as the next move.
                    next_move = self.boxes[self.last_closed_box + 1].final_move
                    # Marks this box as the last closed box.
                    self.last_closed_box = self.last_closed_box + 1

        # Executed if a next move has not yet been determines
        if not next_move:
            # If no box is closable, marks the top-most move from ordered_moves
            # as the next move and removes it from ordered_moves.
            if self.ordered_moves:
                next_move = self.ordered_moves.pop(0)
            else:
                # If no next move has been determined yet, select whatever move is available.
                # This seems to occur at the end of a game.
                next_move = game.valid_moves[0]

        # Converts next_move to a formatted string which can be
        # interpretted by Game.move().
        next_move_str = '{} {}'.format(*next_move)

        return next_move_str

class Box:
    '''Class used to store and modify information relevant to Winnning Player
    about a box on the board.'''

    def __init__(self, setup_moves, closing_moves):
        '''Takes two tuples, each containing a pair of tuples which each contains
        a pair of dots. Uses this data to establish under what conditions the box should be closed
        by Winning Player.'''

        # The two moves which should be made in order to set the box up for
        # Random Player to make it closable.
        self.setup_moves = setup_moves

        # Two moves, either of which must be made after Random Player
        # has made the box closable.
        self.closing_moves = closing_moves

        # Whether or not the box has been setup to become closable.
        self.setup = False

        # Whether or not the box is closable (i.e. three of sides are connected).
        self.closable = False

        # This value is set after the box becomes closable. Indicates
        # the move which needs to be made in order to close the box.
        self.final_move = None

        # Indicates whether or not the box is closed. If this value is
        # set to True, check_if_set_up() or check_if_closable() will both
        # return False.
        self.closed = False

    def check_if_set_up(self, am):
        '''Checks to see if a box is setup to become closable, first by
        checking to see whether setup or closed is True, then
        by checking the board to see if both setup moves have been made. If they
        have, setup is set to True'''

        # Checks to see if the box is already considered setup or has already been closed.
        if self.setup or self.closed:
            return
        
        sm = self.setup_moves # Condenses variable name for readability

        # If both setup moves have been made, sets setup to True.
        if am[sm[0][0]][sm[0][1]] == 2 and am[sm[1][0]][sm[1][1]] == 2:
            self.setup = True

    def check_if_closable(self, am):
        '''Checks to see if a box closable, first by
        checking to see whether closable or closed is True, and then
        by checking the board to see if both setup moves have been made
        and one of either closing moves has already been made. If they
        have been, closable is set to True. Returns True if the box is closable,
        and False otherwise.'''

        # Checks to see if the box is already considered closable or has already been closed.
        if self.closable or self.closed:
            return False

        cm = self.closing_moves # Condenses variable name for readability

        # First checks to see if both setup moves have been made.
        if self.setup:
            if am[cm[0][0]][cm[0][1]] == 2:
                # If the first closing move has been made,
                # closable is set to true, final_move is set
                # to the second closing move and True is returned.
                self.closable = True
                self.final_move = cm[1]
                return True
            elif am[cm[1][0]][cm[1][1]] == 2:
                # If the second closing move has been made,
                # closable is set to true, final_move is set
                # to the first closing move and True is returned.
                self.closable = True
                self.final_move = cm[0]
                return True

        return False

    def close_box(self):
        '''Used to set the box as closed.'''
        self.closed = True
        self.setup = False
        self.closable = False

def main():
    answer = input('Enter how many boxes per row you would like to play with on the board: ')

    # Repeatedly prompts the user until valid input is entered.
    while True:
        try:
            boxes_per_row = int(answer)
            game = Game(boxes_per_row)
            break
        except:
            print('Invalid input, please try again.')
            answer = input('Enter how many boxes per row you would like to play with on the board: ')

    answer = input('Enter a random seed integer: ')

    # Repeatedly prompts the user until valid input is entered.
    while True:
        try:
            seed = int(answer)
            random.seed(seed)
            break
        except:
            print('Invalid input, please try again.')
            answer = input('Enter a random seed integer: ')
    
    answer = input('Enter a number of rounds to play: ')

    # Repeatedly prompts the user until valid input is entered.
    while True:
        try:
            rounds = int(answer)
            break
        except:
            print('Invalid input, please try again.')
            answer = input('Enter a number of rounds to play: ')
            

    # Winning player goes first
    output = game.play_with_output(0)
    output += '\n\n\n\n\n'

    game = Game(boxes_per_row)
    # Losing player goes first
    output += game.play_with_output(1)

    fp = open('single_play.txt', 'w')
    fp.write(output)
    fp.close()

    results = []
    wins = [0, 0, 0]

    # Plays the game the number of designated times,
    # recording the results each time.
    for _ in range(rounds):
        game = Game(boxes_per_row)
        result = game.play_game_without_output()
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
Winning Player average: {}
Random Player average: {}
Winning Player median: {}
Random Player median: {}
Winning Player highest score: {}
Random Player highest score: {}
Winning Player lowest score: {}
Random Player lowest score: {}
Winning Player total wins: {}
Random Player total wins: {}
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


    print(output)



if __name__ == '__main__':
    main()
            
