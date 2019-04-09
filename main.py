import argparse
from src.View import View
from src.Scrabble import Scrabble
from src.Agent import Agent
from src.Minimax import Minimax

# Parsing command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-s', dest='size', type=int)
parser.add_argument('-b', dest='blanks', action='store_true')
results = parser.parse_args()

if not results.size:
    results.size = 15

# Setting up the game with two players
state = Scrabble(blanks=results.blanks, size=results.size)
state.add_agent(0, Agent())
state.add_agent(1, Agent())

# Play
agents = state.agents.keys()
while not state.is_over():
    for agent in agents:
        state.draw(agent)
        best_move = Minimax(agent).get_best_word(state, agent, 1)
        state.place(best_move)
