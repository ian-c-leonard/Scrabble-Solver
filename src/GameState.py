from random import shuffle

class GamesState:

    def __init__(self, blanks=False):
        self.agents = {}
        self.num_agents = 0
        self.tiles = ['A'] * 9 + ['B'] * 2 + ['C'] * 2 + ['D'] * 4 + ['E'] * 12 + ['F'] * 2 + \
                     ['G'] * 3 + ['H'] * 2 + ['I'] * 9 + ['J'] * 1 + ['K'] * 1 + ['L'] * 4 + \
                     ['M'] * 2 + ['N'] * 6 + ['O'] * 8 + ['P'] * 2 + ['Q'] * 1 + ['R'] * 6 + \
                     ['S'] * 4 + ['T'] * 6 + ['U'] * 4 + ['V'] * 2 + ['W'] * 2 + ['X'] * 1 + \
                     ['Y'] * 2 + ['Z'] * 1 + (['BLANK'] * 2 if blanks else [])
        shuffle(self.tiles)

    def add_agent(self, agent_id, agent):
        self.agents[agent_id] = agent
        self.num_agents += 1

    def get_num_agents(self):
        return self.num_agents
