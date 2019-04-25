import copy
import numpy as np
from random import shuffle
from collections import Counter
from src.constants import WORDS
from lexpy.dawg import DAWG
from src.Agent import Agent
from collections import defaultdict
from src.word_sets import WORD_SETS
from src.dictionary import DICTIONARY

class ScrabbleRules():
    def __init__(self, size=15, multipliers=None, blanks=False, dirty = False): # TODO bad words
        print('Initializing Scrabble...')
        assert size % 2, 'Board length must be odd.'
        self.agent = 0  # The agent's turn
        self.turn = 1  # What turn we're on
        self.words = WORDS  # List of Scrabble words
        self.size = size  # Size of the board
        self.center = (size // 2, size // 2)
        # self.board = np.array([''] * size ** 2, dtype=object).reshape(size, size)
        self.multipliers = multipliers if multipliers else self._default_multipliers()
        self.score_map = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4,
                          'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3,
                          'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
                          'Y': 4, 'Z': 10, 'BLANK': 0}
        self.dawg = self._optimize_scrabble_words()  # Optimize Scrabble words with a lookup dictionary
        self.dictionary = DICTIONARY
        self.word_sets = WORD_SETS or self._build_word_sets()

    def _optimize_scrabble_words(self):
        '''Initializes a Trie of all possible Scrabble words for optimized lookups.'''
        print('Optimizing Word Dictionary...')
        dawg = DAWG()
        dawg.add_all(WORDS)
        print('Done Optimizing.')
        return dawg


    def _build_word_sets(self):
        print('Organizing Word Sets...')
        word_sets = defaultdict(lambda: defaultdict(set()))
        letters = set(self.tiles)

        sets = {length: {(i, l): sorted({w for w in self.words if len(w) == length and len(w) > i  and w[i] == l},
                                            lambda x: -self.dictionary[x])
                             for i in range(length) for l in letters}
                    for length in range(2, self.size + 1)}

        word_sets.update(sets)
        print('Done Organizing.')
        return word_sets

    def satisfying_words(self, length, constrains):
        '''Given a length and a list of constraints (e.g. (5, [(1, 'A'), ... , (12, 'Z')])),
           return the set of words of a given length which satisfy all of the constraints'''
        sets = [self.word_sets[length][c] for c in constrains]
        return set.intersection(*sets)

    def get_row_words(self, row, indices):
        ## Getting the start and end indices
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

        words_and_indices = [(self.satisfying_words(length, constraint), indices[start_i: start_i + length])
                           for start_i, length, constraint in constraints]

        words_to_indices = {word: indices for words, indices in words_and_indices for word in words}

        return words_to_indices

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

    def get_grids(self, board):
        rows = [board[i] for i in range(self.size)]
        row_indices = [[(i, x) for x in range(self.size)] for i in range(self.size)]
        cols = [[board[x][i] for x in range(self.size)] for i in range(self.size)]
        col_indices = [[(x, i) for x in range(self.size)] for i in range(self.size)]

        return  list(zip(rows, row_indices)) + list(zip(cols, col_indices))

    def validate_move(self, word, indices, agent_id, state): # this will need to take in game state

        agent = state.agents[agent_id]
        #Check if agent has required tiles to form a word
        required_tiles = Counter([word[i] for i, index in enumerate(indices) if word[i] != state.board[index]])

        for tile in required_tiles:
            if agent.tiles[tile] < required_tiles[tile]:
                return False

        # Check if all created words are valid
        created_words = self.get_created_word_indices(word, indices, agent_id = agent_id, state = state)
        # return created_words

        for (word, indices) in created_words:
                if not self.valid_word(word):
                    return False

        return True

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

        words_and_indices = [(self.satisfying_words(length, constraint), indices[start_i: start_i + length])
                           for start_i, length, constraint in constraints]

        words_to_indices = [(word, indices) for words, indices in words_and_indices for word in words]

        return words_to_indices

    def get_created_word_indices(self, word, indices, agent_id, state):
        '''Returns the indices of all newly createds from placing a word in a position'''

        size = self.size
        new_board = state.place(word, indices, agent_id = agent_id, scrabble_rules = self, mock = True)
        hor_grids = [((x, max(indices, key = lambda x: x[1])[1]), [(x, y) for y in range(size)])
                     for x in set([i[0] for i in indices])]
        ver_grids = [((max(indices, key = lambda x: x[0])[0], y),  [(x, y) for x in range(size)])
                     for y in set([i[1] for i in indices])]

        # I am so sorry to whoever has to read this nested, nested, nested listcomp. Buet we needed to make this fast tho...
        affected_indices = [grid[min(ind for ind, board_ind  in enumerate(grid)
                                 if all([new_board[test_ind] for test_ind in grid[ind: grid.index(max_played_ind) + 1]])):
                                 max(ind for ind, board_ind  in enumerate(grid)
                                     if all([new_board[test_ind] for test_ind in grid[grid.index(max_played_ind): ind + 1]])) + 1]
                            for max_played_ind, grid in hor_grids + ver_grids]

        word_indices = [indices for indices in affected_indices if state.unplayed_indices(indices) if len(indices) > 1]
        return [(''.join([new_board[ind] for ind in indices]), indices) for indices in word_indices]

    def change_me_daddy(self, agent_id, state):
        board = state.board.copy()
        grids = self.get_grids(board)
        list_of_moves = [self.get_grid_words(*grid) for grid in grids]
        moves = [move for moves in list_of_moves for move in moves if self.validate_move(*move, agent_id, state = state)]

        return moves

    def valid_word(self, word):
        return word.upper() in self.words

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
    def word_score(self, word, indices, gamestate):
        '''Returns the score of a word at a given index'''
        base_word_score = [self.score_map[letter] for letter in word]
        board_scores = [self.multipliers[ind] for ind in indices if not gamestate.counted_indices[ind]]

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