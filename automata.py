class Automata:
    def __init__(self, initial_state, final_state, sigma, transitions, states):
        self.sigma = set()
        self.q_states = states
        self.initial_state = initial_state
        self.final_state = final_state
        self.sigma.update(sigma)
        self.transitions = transitions
