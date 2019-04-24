PAS = 'pass'
INF = float('inf')

class Expectimax:
    def __init__(self, max_who, rules):
        self.max_who = max_who
        self.rules = rules

    def value(self, state, agent_id, depth):
        if state.is_over() or depth <= 0:
            return self.evaluation_function(state, agent_id)

        if agent_id == self.max_who:
            return self.max_value(state, agent_id, depth)[0]

        return self.exp_value(state, agent_id, depth)[0]

    def max_value(self, state, agent_id, depth):
        max_eval = (-INF, PAS)
        for action in state.get_legal_moves(agent_id, self.rules):
            _eval = (self.value(state.generate_successor(agent_id, action[0], action[1], self.rules), (agent_id + 1) % state.get_num_agents(), depth - 1), action)
            max_eval = max([max_eval, _eval], key=lambda pair: pair[0])
        return max_eval

    def exp_value(self, state, agent_id, depth):
        exp_eval = (0, PAS)
        moves = state.get_legal_moves(agent_id, self.rules)
        for action in moves:
            p = len(moves)
            avg = (float(self.value(state.generate_successor(agent_id, action[0], action[1], self.rules), (agent_id + 1) % state.get_num_agents(), depth - 1)) / float(p))
            exp_eval = (exp_eval[0] + avg, action)
        return exp_eval

    def evaluation_function(self, state, agent_id):
        evauation = 0
        for _id in state.agents.keys():
            if _id == agent_id:
                evauation += state.agents[_id].score
            else:
                evauation -= state.agents[_id].score
        return evauation

    def get_best_word(self, state, agent_id, depth):
        return self.max_value(state, agent_id, depth * state.get_num_agents())[1]
