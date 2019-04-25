import argparse
from src.View import View
from src.Scrabble import ScrabbleRules
from src.GameState import GameState
from src.Agent import Agent
from src.Minimax import Minimax
import time

# Parsing command line arguments
parser = argparse.ArgumentParser()

parser.add_argument('-s', dest='size', type=int)
parser.add_argument('-b', dest='blanks', action='store_true')
results = parser.parse_args()

if not results.size:
    results.size = 15

rules = ScrabbleRules(blanks = results.blanks, size = results.size)
state = GameState(blanks = results.blanks, size = results.size)
view = View()

agent_0 = Agent()
agent_1 = Agent()
state.add_agent(0, agent_0)
state.add_agent(1, agent_1)
state.place('A', [(3, 3)], 0, rules)

# Play
agents = [0, 1]

try:
    while True:
        for agent in agents:
            state.draw(agent)
            best_move = Minimax(agent, rules).get_best_word(state, agent, 1)
            print(f'Agent #{agent} played: {best_move[0]}')
            print(best_move)
            state.place(*best_move, agent, rules)
            if state.is_over():
                print('DOINE BOI')
                break
            print(view.visualize_board(state.board))
except:
     print('Game Over.')
     print(f'Agent #0 with score: {state.agents[0].score}')
     print(f'Agent #1 with score: {state.agents[1].score}')
     print(f'Agent #{max(state.agents, key = lambda x: state.agents[x].score)} wins!')
