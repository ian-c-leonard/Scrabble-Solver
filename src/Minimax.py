PAS = 'pass'
INF = float('inf')

class Minimax():
    def __init__(self, max_who):
        self.max_who = max_who

    def value(self, state, agent_id, depth):
        if state.is_over() or depth == 0:
            return self.evaluation_function(state, agent_id)

        if agent_id == self.max_who:
            return self.max_value(state, agent_id, depth)[0]

        return self.min_value(state, agent_id, depth)[0]

    def max_or_min_value(self, state, agent_id, depth, fn, initial_value):
        v = (initial_value, PAS)
        for action in state.get_legal_actions(agent_id):
            v = fn([v, (self.value(state.generate_successor(agent_id, action), (agent_id + 1) % state.get_num_agents(), depth - 1), action)], key=lambda pair: pair[0])
        return v

    def evaluation_function(self, state, agent_id): # TODO do it live (one liner)
        evauation = 0
        for _id in state.agents.keys():
            if _id == agent_id:
                evauation += state.agents[_id].score
            else:
                evauation -= state.agents[_id].score
        return evauation

    def max_value(self, state, agent_id, depth):
        return self.max_or_min_value(state, agent_id, depth, max, -INF)

    def min_value(self, state, agent_id, depth):
        return self.max_or_min_value(state, agent_id, depth, min, INF)

    def get_best_word(self, state, agent_id, depth):
        return self.max_value(state, agent_id, depth * state.get_num_agents())[1] # TODO get depth value right
