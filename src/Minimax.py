import numpy as np

PAS = 'pass'

class Minimax():
    def __init__(self, max_who, rules):
        self.max_who = max_who
        self.rules = rules

    def value(self, state, agent_id, depth, alpha, beta):
        if state.is_over() or depth == 0:
            return self.evaluation_function(state, agent_id)

        if agent_id == self.max_who:
            return self.max_value(state, agent_id, depth, alpha, beta)[0]

        return self.min_value(state, agent_id, depth, alpha, beta)[0]

    def max_value(self, state, agent_id, depth, alpha, beta):
        max_eval = (-np.inf, PAS)
        for action in state.get_legal_moves(agent_id, self.rules):
            _eval = (self.value(state.generate_successor(agent_id, action[0], action[1], self.rules), (agent_id + 1) % state.get_num_agents(), depth - 1, alpha, beta), action)
            max_eval = max([max_eval, _eval], key=lambda pair: pair[0])
            alpha = max([alpha, _eval], key=lambda pair: pair[0])
            if beta[0] <= alpha[0]:
                break
        return max_eval

    def min_value(self, state, agent_id, depth, alpha, beta):
        min_eval = (np.inf, PAS)
        for action in state.get_legal_moves(agent_id, self.rules):
            _eval = (self.value(state.generate_successor(agent_id, action[0], action[1], self.rules), (agent_id + 1) % state.get_num_agents(), depth - 1, alpha, beta), action)
            min_eval = min([min_eval, _eval], key=lambda pair: pair[0])
            beta = min([beta, _eval], key=lambda pair: pair[0])
            if beta[0] <= alpha[0]:
                break
        return min_eval

    def evaluation_function(self, state, agent_id):
        evauation = 0
        for _id in state.agents.keys():
            if _id == agent_id:
                evauation += state.agents[_id].score
            else:
                evauation -= state.agents[_id].score
        return evauation

    def get_best_word(self, state, agent_id, depth):
        return self.max_value(state, agent_id, depth * state.get_num_agents(), (-np.inf, PAS), (np.inf, PAS))[1]
