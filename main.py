import argparse
from src.View import View
from src.Scrabble import Scrabble
from src.Agent import Agent



parser = argparse.ArgumentParser()

parser.add_argument('-s', dest='size', type=int)
parser.add_argument('-b', dest='blanks', action='store_true')
results = parser.parse_args()

if not results.size:
    results.size = 15

game = Scrabble(blanks=results.blanks, size=results.size)
agent = Agent(game, 1)
view = View(game, 1)

print(game.board)

print(game.tiles)
print(agent.tiles)
agent.tiles = agent.tiles[1:3]

print(agent.tiles)
agent.draw()

print(agent.tiles)
print(game.tiles)