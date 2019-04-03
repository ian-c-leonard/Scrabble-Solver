import numpy as np
from collections import Counter

class Agent():
    def __init__(self, scrabble, number):
        self.game = scrabble
        self.number = number
        self.tiles = []
        self.opponent_tiles = []
        self.out_of_moves = False
        # print(f"AGENT_{self.number}: Drawing Tiles And Guessing Opponent's Tiles")
        # print "test"
        self.draw()
        self.guess_opponent_tiles()

    def draw(self):
        """Draw from the global game's tile bag"""
        n_missing = 7 - len(self.tiles)

        for _ in range(n_missing):
            self.tiles.append(self.game.tiles.pop())

    def guess_opponent_tiles(self):
        """Guess opponent's tiles given the current distribution of tiles"""
        self.opponent_tiles = np.random.choice(self.game.tiles, 7, replace=False)

    def move(self):
        pass

    def get_created_word_indices(self, word, indices):
        '''Returns the indices of all newly createds from placing a word in a position'''

        size = self.game.size
        new_board = self.place(word, indices, mock=True)
        horizontal = len(set([x[0] for x in indices])) == 1  # Word is being played horizontally
        word_indices = []

        if horizontal:
            row = indices[0][0]

            # Get all vertical words created
            for _, j in indices:
                col = [(x, j) for x in range(size)]
                longest_indices = []
                created = False

                for index in col:
                    if index in indices:  # The letter was just placed
                        created = True

                    if not new_board[index] and not created:
                        longest_indices = []

                    if new_board[index]:
                        longest_indices.append(index)

                    elif created:
                        if len(longest_indices) > 1:
                            word_indices.append(longest_indices)
                        break

            # Get all horizontal words created
            curr_row = [(row, x) for x in range(size)]
            longest_indices = []
            created = False

            for index in curr_row:
                if index in indices:  # The letter was just placed
                    created = True

                if not new_board[index] and not created:
                    longest_indices = []

                if new_board[index]:
                    longest_indices.append(index)

                elif created:
                    word_indices.append(longest_indices)
                    break

        else:
            col = indices[0][1]

            # Get all horizontal words created
            for i, _ in indices:
                row = [(i, x) for x in range(size)]
                longest_indices = []
                created = False

                for index in row:
                    if index in indices:  # The letter was just placed
                        created = True

                    if not new_board[index] and not created:
                        longest_indices = []

                    if new_board[index]:
                        longest_indices.append(index)

                    elif created:
                        if len(longest_indices) > 1:
                            word_indices.append(longest_indices)
                        break

            # Get the vertical word created
            curr_col = [(x, col) for x in range(size)]
            longest_indices = []
            created = False

            for index in curr_col:
                if index in indices:  # The letter was just placed
                    created = True

                if not new_board[index] and not created:
                    longest_indices = []

                if new_board[index]:
                    longest_indices.append(index)

                elif created:
                    word_indices.append(longest_indices)
                    break

        word_indices = [indices for indices in word_indices if self.unplayed_indices(indices)]

        print(word_indices)
        return [{''.join([new_board[ind] for ind in indices]): indices} for indices in word_indices]

    def get_grids(self):
        board = self.game.board.copy()
        rows = [board[i] for i in range(self.game.size)]
        cols = [board[:][i] for i in range(self.game.size)]

        return rows + cols

    def grid_optimizer(self, letters, grid, indices):
        ## Rework grid_optimizer to take in a max_length grid (i.e. 12) and then find the largest word that CAN fit in said grid
        ## i.e. [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] --> CATS ( potentially)

        # Deduce a list of words which fit in the given grid with letter constraints
        search_string = '*' + ''.join([x if x else '?' for x in grid]).strip('?') + '*'

        result = self.game.dawg.search(search_string)

        counter = Counter(letters + [x for x in grid if x])

        playable_words = [word for word in result if
                          all([counter[letter] >= sum([1 for x in word if x == letter]) for letter in word])]

        max_word = (None, -np.inf)
        for word in playable_words:

            for start, index in enumerate(indices):
                if all([grid[ind + start] == word[ind] for ind in range(len(word)) if grid[ind + start].isalnum()]):
                    start_ind = start
                    break

            score = self.score(word, indices[start: start + len(word)])
            if score > max_word[1]:
                max_word = (word, score)

        # Return max score of playable words with givin indices
        return max_word[0]

    def place(self, word, indices, mock=False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''

        board = self.game.board.copy() if mock else self.game.board

        for count, ind in enumerate(indices):
            board[ind] = word[count]

        if mock:  # We want to actually return the board if it's a mock placemenent
            return board
