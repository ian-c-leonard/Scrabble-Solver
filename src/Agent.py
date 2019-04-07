import numpy as np
from collections import Counter

class Agent():
    def __init__(self, scrabble, number):
        self.game = scrabble
        self.number = number
        self.tiles = {}
        self.opponent_tiles = []
        self.out_of_moves = False
        print(f"AGENT_{self.number}: Drawing Tiles And Guessing Opponent's Tiles")
        self.draw()
        self.guess_opponent_tiles()
        self.score = 0
     
    
    def draw(self):
        '''Draw from the global game's tile bag'''
        n_missing = 7 - sum(self.tiles.values())
        old_tiles = [x for l in [[tile]*num for tile, num in self.tiles.items()] for x in l] # unpacking
        drawn_tiles = list(np.random.choice(self.game.tiles, n_missing, replace = False))
        
        for x in drawn_tiles:
            self.game.tiles.remove(x)
        
        self.tiles = Counter(old_tiles + drawn_tiles)
        
    def guess_opponent_tiles(self):
        """Guess opponent's tiles given the current distribution of tiles"""
        self.opponent_tiles = np.random.choice(self.game.tiles, 7, replace = False)
        
    def get_successors(self):
        grids = self.get_grids()
        list_of_moves = [self.get_grid_words(*grid) for grid in grids]
        moves = [move for moves in list_of_moves for move in moves if self.validate_move(*move)]
        new_boards = [(move, self.place(*move, mock = True)) for move in moves]
        
        return new_boards
    
    def get_optimal_move(self):
        # call minimax here
        pass
    
    def move(self):
        optimal_move = self.get_optimal_move()
        self.place(*optimal_move)
        self.draw()
        
    
    def get_created_word_indices(self, word, indices):
        '''Returns the indices of all newly createds from placing a word in a position'''

        size = self.game.size
        new_board = self.place(word, indices, mock = True)
        horizontal = len(set([x[0] for x in indices])) == 1 # Word is being played horizontally
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

        
        word_indices = [indices for indices in word_indices if self.game.unplayed_indices(indices)]
        return [(''.join([new_board[ind] for ind in indices]), indices) for indices in word_indices]
    
    def get_grids(self):
        board = self.game.board.copy()
        
        rows = [board[i] for i in range(self.game.size)]
        row_indices = [[(i, x) for x in range(agent.game.size)] for i in range(agent.game.size)]
        cols = [[board[x][i] for x in range(agent.game.size)] for i in range(agent.game.size)]
        col_indices = [[(x, i) for x in range(agent.game.size)] for i in range(agent.game.size)]
        
        
        return  list(zip(rows, row_indices)) + list(zip(cols, col_indices))
        
    
    def get_grid_words(self, row, indices):
        ## Getting the start and end indices
        row = list(row)
        start = [0]
        end = []
        for i in range(1, len(row) - 1):
            letter = row[i]
            if not letter and not row[i - 1]:
                start.append(i)
            if letter and not row[i - 1]:
                start.append(i)
            if letter and not row[i + 1]:
                end.append(i)
            if not letter and (((i - 1) in end) or (i - 1 == 0)) and not row[i + 1]:
                end.append(i)
        end.append(len(row) - 1)

        ## Getting all possible pairs
        pairs = [(starting_index, ending_index) for starting_index in start 
                     for ending_index in end if starting_index < ending_index]

        def filter_unneeded_pairs(pair): ## Rewrite to lambda later
            section = row[pair[0]: pair[1] + 1]
            blank_count = section.count('')
            return blank_count < len(section) and blank_count != 0

        ## Filter out pairs that have all or no blanks
        pairs = [pair for pair in pairs if filter_unneeded_pairs(pair)]

        ## Making constraints
        constraints = [(pair[0], pair[1] - pair[0] + 1, [(i - pair[0], row[i]) for i in range(pair[0], pair[1] + 1) if row[i]]) for pair in pairs]

        words_and_indices = [(self.game.satisfying_words(length, constraint), indices[start_i: start_i + length]) 
                           for start_i, length, constraint in constraints]

        words_to_indices = [(word, indices) for words, indices in words_and_indices for word in words]

        return words_to_indices
    
    
    def place(self, word, indices, mock = False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''
        
        board = self.game.board.copy() if mock else self.game.board
        
        for count, ind in enumerate(indices):
            board[ind] = word[count]
        
        if mock: # We want to actually return the board if it's a mock placemenent
            return board
        
        self.score += self.score_word(word, indices)
        
    def validate_move(self, word, indices):
        
        #Check if agent has required tiles to form a word
        required_tiles = Counter([word[i] for i, index in enumerate(indices) if word[i] != self.game.board[index]])
        
        for tile in required_tiles:
            if self.tiles[tile] < required_tiles[tile]:
                return False
            
        # Check if all created words are valid
        created_words = self.get_created_word_indices(word, indices)
        return created_words
        
        for (word, indices) in created_words:
                if not self.game.valid_word(word):
                    return False

    def score_word(self, word, indices):
        return self.game.score(word, indices)