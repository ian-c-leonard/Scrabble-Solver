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

print(game.tiles)
print(agent.tiles)
agent.tiles = agent.tiles[1:3]

print(agent.tiles)
agent.draw()

print(agent.tiles)
print(game.tiles)