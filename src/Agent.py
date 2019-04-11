import numpy as np
from collections import Counter
class Agent():
    def __init__(self):
        self.tiles = Counter()
        self.opponent_tiles = []
        self.score = 0
