import argparse
from src.View import View
from src.Scrabble import Scrabble
from src.Agent import Agent



parser = argparse.ArgumentParser()

parser.add_argument('-p', dest='port', type=int)
parser.add_argument('-b', action='store_true')
results = parser.parse_args()

game = Scrabble(blanks=results.b)
agent = Agent(game, 1)
view = View(game, 1)

agent.place('BIN', [(7, 7), (7, 8), (7, 9)])


print(game.seeded_tiles)
