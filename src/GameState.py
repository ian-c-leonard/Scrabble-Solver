import numpy as np
from random import shuffle
from collections import Counter
from src.Scrabble import ScrabbleRules

class GameState:

    def __init__(self, blanks = False, size = 15, scrabble_rules = None):
        if scrabble_rules == None:
            self.scrabble_rules = ScrabbleRules(size, blanks)
        else:
            self.scrabble_rules = scrabble_rules
        self.agents = {}
        self.size = size
        self.num_agents = 0
        self.board = np.array([''] * size ** 2, dtype=object).reshape(size, size)
        self.bag = ['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 + ['F'] * 2 + \
                     ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] * 1 + ['K'] * 1 + ['L'] * 4 + \
                     ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] * 1 + ['R'] * 6 + \
                     ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X'] * 1 + \
                     ['Y'] * 2 + ['Z'] * 1 + (['BLANK'] * 2 if blanks else [])
        shuffle(self.bag)

    def add_agent(self, agent_id, agent):
        self.agents[agent_id] = agent
        self.num_agents += 1

    def get_num_agents(self):
        return self.num_agents

    def get_agent_rack(self, agent):
        return agent.tiles

    def is_over(self):
        out_of_words = not self.bag and any([not agent.tiles for agent in self.agents])

        out_of_possible_moves = any([agent.out_of_moves for agent in self.agents])

        if out_of_words or out_of_possible_moves:
            return True

        return False

    def draw(self, agent_id): # TODO need to draw the tiles in the order they are
        '''Draw from the global game's tile bag'''
        agent = self.agents[agent_id]
        n_missing = 7 - sum(agent.tiles.values())
        old_tiles = [x for l in [[tile]*num for tile, num in agent.tiles.items()] for x in l] # unpacking
        drawn_tiles = list(np.random.choice(self.bag, n_missing, replace = False))

        for x in drawn_tiles:
            self.bag.remove(x)

        agent.tiles = Counter(old_tiles + drawn_tiles)

    def get_legal_moves(self, agent_id):

        return self.scrabble_rules.change_me_daddy(agent_id, self)


        # board = self.board.copy()
        # grids = self.scrabble_rules.get_grids(board)
        # list_of_moves = [self.scrabble_rules.get_grid_words(*grid) for grid in grids]
        # moves = [move for moves in list_of_moves for move in moves if self.scrabble_rules.validate_move(*move, agent = self.agents[agent_id], board = self.board)]
        # # new_boards = [(move, self.place(*move, mock = True, agent_id = agent_id)) for move in moves]

        # return moves

    def place(self, word, indices, agent_id, mock = False):
        '''Place a word in a location on the board.
           You can mock placements and return the would-be board state'''

        board = self.board.copy() if mock else self.board

        for count, ind in enumerate(indices):
            board[ind] = word[count]

        if mock: # We want to actually return the board if it's a mock placemenent
            return board

        agent = self.agents[agent_id]
        agent.score += self.scrabble_rules.word_score(word, indices)
