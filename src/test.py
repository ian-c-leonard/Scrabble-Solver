from src.Agent import Agent
from src.Scrabble import Scrabble
from src.Minimax import Minimax


state = Scrabble()

state.add_agent(0, Agent())
state.add_agent(1, Agent())

minimax_0 = Minimax(0)
minimax_1 = Minimax(1)

best_move_agent_0 = minimax_0.get_best_word(state, 0, 1)

state.place(best_move_agent_0)

best_move_agent_1 = minimax_1.get_best_word(state, 1, 1)

state.place(best_move_agent_1)

# ...
