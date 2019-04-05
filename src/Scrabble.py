import numpy as np
from random import shuffle
from src.constants import WORDS
from lexpy.dawg import DAWG
from src.Agent import Agent
from collections import defaultdict

class Scrabble():
    def __init__(self, size=15, multipliers=None, blanks=False):
        print('Initializing Scrabble...')
        assert size % 2, 'Board length must be odd.'
        self.agent = 0  # The agent's turn
        self.turn = 1  # What turn we're on
        self.words = WORDS  # List of Scrabble words
        self.size = size  # Size of the board
        self.center = (size // 2, size // 2)
        self.board = np.array([''] * size ** 2, dtype=object).reshape(size, size)
        # self.multipliers = multipliers if multipliers else self._default_multipliers()
        self.counted_words = np.zeros((size, size), dtype=int)
        self.tiles = ['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 + ['F'] * 2 + \
                     ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] * 1 + ['K'] * 1 + ['L'] * 4 + \
                     ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] * 1 + ['R'] * 6 + \
                     ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X'] * 1 + \
                     ['Y'] * 2 + ['Z'] * 1 + (['BLANK'] * 2 if blanks else [])
        shuffle(self.tiles)
        self.score_map = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
                          'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
                          'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                          'Y': 4, 'Z': 10, 'BLANK': 0}
        print('Optimizing Word Dictionary...')
        #self.dawg = self._optimize_scrabble_words()  # Optimize Scrabble words with a lookup dictionary
        self.word_sets = self._build_word_sets()
        print('Done')

    def _optimize_scrabble_words(self):
        '''Initializes a Trie of all possible Scrabble words for optimized lookups.'''
        dawg = DAWG()
        dawg.add_all(WORDS)

        return dawg
    
    def _build_word_sets(self):
        word_sets = defaultdict(lambda: defaultdict(set()))
        letters = set(self.tiles)
        
        sets = {length: {(i, l): {w for w in self.words if len(w) == length and len(w) > i  and w[i] == l} 
                             for i in range(length) for l in letters}
                    for length in range(2, self.size + 1)}
        
        word_sets.update(sets)
        
        return word_sets

    def satisfying_words(self, length, constrains):
        '''Given a length and a list of constraints (e.g. (5, [(1, 'A'), ... , (12, 'Z')])), 
           return the set of words of a given length which satisfy all of the constraints'''
        sets = [self.word_sets[length][c] for c in constrains]
        
        return set.intersection(*sets)
    
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

        quadrant = [x[:self.size // 2 + 1] for x in quadrant][:self.size // 2 + 1] # Trim down to board size

        quadrant = quadrant + quadrant[len(quadrant) - 2::-1]
        multipliers = [y + y[::-1][1:] for y in quadrant]
        return np.array(multipliers, dtype=object).reshape(self.size, self.size)

    def get_agent_rack(self, agent):
        return agent.tiles

    def is_over(self):
        out_of_words = not self.tiles and any([not agent.tiles for agent in self.agents])

        out_of_possible_moves = any([agent.out_of_moves for agent in self.agents])

        if out_of_words or out_of_plays:
            return True

        return False

    def unplayed_indices(self, indices):
        return not all([self.counted_words[index] for index in indices])

    def valid_word(self, word):
        return word in self.dawg

    def place(self, word, indices, mock=False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''

        board = self.board.copy() if mock else self.board

        for count, ind in enumerate(indices):
            board[ind] = word[count]

        if mock:  # We want to actually return the board if it's a mock placement
            return board

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