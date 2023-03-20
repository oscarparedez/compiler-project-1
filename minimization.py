class Minimization:
    def __init__(self, states, sigma, transitions, initial_state, final_states):
        self.states = states
        self.sigma = sigma
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        
    def states_partition(self):
        self.x = self.states - self.final_states
        self.y = self.states & self.final_states
        
    def verify_identical_transitions(self):
        new_transitions = {}
        for state in self.x:
            # print("TRANSITIOJNS", self.transitions.get(state))
            for key, val in self.transitions.get(state).items(): 
                new_transition = {}
                new_transition.update({
                    state: {
                        key: val
                    }
                })
                if new_transitions.get(state) == None:
                    new_transitions.update(new_transition)
                else:
                    new_transitions.get(state)[key] = val
                
        print("new", new_transitions)
        print("old", self.transitions)
        
            