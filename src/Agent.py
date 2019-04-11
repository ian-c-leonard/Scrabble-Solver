import numpy as np
from collections import Counter

class Agent():
    def __init__(self):
        self.tiles = {}
        self.opponent_tiles = []
        self.out_of_moves = False
        # print(f"AGENT_{self.number}: Drawing Tiles And Guessing Opponent's Tiles")
        # self.draw()
        # self.guess_opponent_tiles()
        self.score = 0

    def guess_opponent_tiles(self):
        """Guess opponent's tiles given the current distribution of tiles"""
        self.opponent_tiles = np.random.choice(self.game.tiles, 7, replace = False)
