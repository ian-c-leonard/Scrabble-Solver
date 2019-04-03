
from View import View
from Scrabble import Scrabble
from Agent import Agent

if __name__ == '__main__':
    game = Scrabble()
    agent = Agent(game, 1)
    view = View(game, 1)

    view.visualize_rack()
