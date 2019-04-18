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
state.place('A', [(2, 2)], 0, rules)

# state.draw(0)
# state.draw(1)


# print(state.board)

# minimax_0 = Minimax(0, rules)

# best_move = minimax_0.get_best_word(state, 0, 1)

# print(best_move)

# Setting up the game with two players

# rules = ScrabbleRules(blanks = results.blanks, size = results.size)
# state = GameState(blanks = results.blanks, size = results.size)

# agent_0 = Agent()
# agent_1 = Agent()
# state.add_agent(0, agent_0)
# state.add_agent(1, agent_1)

# state.draw(0)
# state.place('ARK', [(3, 2), (3, 3), (3, 4)], 0, rules)
# state.draw(1)

# move = state.get_legal_moves(1, rules)[10]
# new_state = state.generate_successor(1, move[0], move[1], rules)

# print(state.board)
# print(state.agents[1].score)
# print(new_state.board)
# print(new_state.agents[1].score)
# print(state.board)
# print(state.agents[1].score)


# new_state = state.generate_successor(0, 0, 0)

# print('COPY')
# copy_state = state.generate_successor(0, 1, 1)

# print(copy_state.board)




# Play
agents = [0, 1]
try:
    while True:
        for agent in agents:
            state.draw(agent)
            best_move = Minimax(agent, rules).get_best_word(state, agent, 1)
            print(f'Agent #{agent} played: {best_move[0]}')
            state.place(best_move[0], best_move[1], agent, rules)
            if state.is_over():
                print('DOINE BOI')
                break
            #print(state.board)
            print(view.visualize_board(state.board))
            #print("test")

            # time.sleep(2)
except:
    print('Game Over.')
    print(f'Agent #0 with score: {state.agents[0].score}')
    print(f'Agent #1 with score: {state.agents[1].score}')
    print(f'Agent #{max(state.agents, key = lambda x: state.agents[x].score)} wins!')

