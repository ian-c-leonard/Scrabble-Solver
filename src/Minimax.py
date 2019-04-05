class Minimax:
    def value(self, state, agent_id):
        util = utility(state) # we need to limit and get values for the state (agents score - others)
        if util != None:
            return util

        if agent_id == 1:
            return self.max_value(state, agent_id)
        if agent_id == -1:
            return self.min_value(state, agent_id)

    def max_value(self, state, agent_id):
        v = float('-inf')
        for move in [i for i, cell in enumerate(state) if cell == None]:
            new_state = state[:]
            new_state[move] = 1
            v = max(v, self.value(new_state, -agent_id))
        return v

    
    def min_value(self, state, agent_id):
        v = float('inf')
        for move in [i for i, cell in enumerate(state) if cell == None]:
            new_state = state[:]
            new_state[move] = -1
            v = min(v, self.value(new_state, -agent_id))
        return v
    
    
    def succ(word, index):
        return new_board