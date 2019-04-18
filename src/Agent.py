from collections import Counter
class Agent():
    def __init__(self):
        self.tiles = Counter()
        self.opponent_tiles = []
        self.score = 0
        self.out_of_moves = False
