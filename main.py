import numpy as np
from constants import WORDS
from lexpy.dawg import DAWG
from collections import Counter

class Scrabble():
    def __init__(self, size = 15, multipliers = None):
        assert size % 2, 'Board length must be odd.'
        self.agent = 0 # The agent's turn
        self.turn = 1 # What turn we're on
        self.words = WORDS # List of Scrabble words
        self.size = size # Size of the board
        self.center = (size // 2, size // 2)
        self.board = np.array(['']*size**2, dtype = object).reshape(size, size)
        self.multipliers = multipliers if multipliers else self._default_multipliers()
        self.counted_words = np.zeros((size, size), dtype = int)
        self.tiles  = ['A']*9 + ['B']*2 + ['C']*2 + ['D']*4 + ['E']*12 + ['F']*2 + \
                      ['G']*3 + ['H']*2 + ['I']*9 + ['J']*1 + ['K']*1 + ['L']*4 + \
                      ['M']*2 + ['N']*6 + ['O']*8 + ['P']*2 + ['Q']*1 + ['R']*6 + \
                      ['S']*4 + ['T']*6 + ['U']*4 + ['V']*2 + ['W']*2 + ['X']*1 + \
                      ['Y']*2 + ['Z']*1 + ['BLANK']*2
        self.score_map = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
                       'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 
                       'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 
                       'Y': 4, 'Z': 10, 'BLANK': 0}
        self.dawg = self._optimize_scrabble_words() # Optimize Scrabble words with a lookup dictionary
        
    def _optimize_scrabble_words(self):
        '''Initializes a Trie of all possible Scrabble words for optimized lookups.'''
        dawg = DAWG()

        dawg.add_all(WORDS)
    
        return dawg
    
            
    def _default_multipliers(self):
        quadrant = \
        [['3W', '', '', '2L', '', '', '', '3W'],
        ['', '2W', '', '', '', '3L', '', ''],
        ['', '', '2W', '', '', '', '2L', ''],
        ['2L', '', '', '2W', '', '', '', '2L'],
        ['', '', '', '', '2W', '', '', ''],
        ['', '3L', '', '', '', '3L', '', ''],
        ['', '', '2L', '', '', '', '2L', ''],
        ['3W', '', '', '2L', '', '', '', '2W']]

        quadrant = quadrant + quadrant[len(quadrant)-2::-1]
        multipliers = [y + y[::-1][1:] for y in quadrant]
        return np.array(multipliers, dtype = object).reshape(self.size, self.size)
    
            
        
    def unplayed_indices(self, indices):
        return not all([self.counted_words[index] for index in indices])
    
    
    def valid_word(self, word):
        return word in self.dawg
    
        
    def place(self, word, indices, mock = False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''
        
        board = self.board.copy() if mock else self.board
        
        for count, ind in enumerate(indices):
            board[ind] = word[count]
        
        if mock: # We want to actually return the board if it's a mock placemenent
            return board

    
    def get_created_word_indices(self, word, indices):
        '''Returns the indices of all newly createds from placing a word in a position'''

        new_board = self.place(word, indices, mock = True)
        horizontal = len(set([x[0] for x in indices])) == 1 # Word is being played horizontally
        word_indices = []

        if horizontal:
            row = indices[0][0]

            # Get all vertical words created
            for _, j in indices:
                col = [(x, j) for x in range(self.size)]
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
            curr_row = [(row, x) for x in range(self.size)]
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
                row = [(i, x) for x in range(self.size)]
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
            curr_col = [(x, col) for x in range(self.size)]
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
        
    
    def is_valid_placement(self, word, indices):
        '''Checks if placing a word here would be a valid placement.'''
        
        if self.turn == 1:
            if not self.center in indices:
                return False
        
        else:
            # Overlapping letters must be the same and at least one letter must overlapp
            for count, ind in enumerate(indices):
                if self.board[ind] == word[count]:
                    break

                return False            

            created_words = self.get_created_word_indices(word, indices)

            for word in created_words.keys():
                if not self.valid_word(word):
                    return False
            
        return True
    
    
    def placement_score(self, word, indices):
        '''Returns the score of a word being placed and a specified index'''
        
        # Check word is long enough
        assert self.valid_word(word) > 1, 'Not a long enough word, dumbass.'
        
        # Check word is placed in a valid location
        assert all([board[ind] == word[ind] or not board[ind] for ind in indices]), 'Not a valid move, dumbass.'
        
        created_indices = self.get_created_word_indices(word, indices)
        assert all([self.valid_word(x) for x in created_indices]), 'You created invalid words, dumbass.'
        
        multipliers = [multipliers[ind] for ind in created_indices if multipliers[ind]]
        
        
    
    
    def grid_optimizer(self, letters, grid, indices):
        ## Rework grid_optimizer to take in a max_length grid (i.e. 12) and then find the largest word that CAN fit in said grid
        ## i.e. [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] --> CATS ( potentially)

        # Deduce a list of words which fit in the given grid with letter constraints
        search_string = '*' + ''.join([x if x else '?' for x in grid]).strip('?') + '*'

        result = self.dawg.search(search_string)

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


    # Word, Indices --> Score
    def score(self, word, indices):
        '''Returns the score of a word at a given index'''
        
        base_word_score = [self.score_map[letter] for letter in word]
        board_scores = [self.multipliers[ind] for ind in indices]
        
        word_multiplier = 1
        
        for ind, score in enumerate(board_scores):
            if score == '3W':
                word_multiplier *= 3
                continue
            
            if score == '2W':
                word_multiplier *= 2
                continue
                
            if score == '3L':
                base_word_score[ind] *= 3
                continue
                
            if score == '2L':
                base_word_score[ind] *= 2
                continue
            
        return sum(base_word_score) * word_multiplier
