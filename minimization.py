from automathon import DFA
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
        # print('self', type(self.transitions))
        # transitions_sample = {'q0': {'a': 'q1', 'b': 'q2'}, 'q1': {'b': 'q2', 'a': 'q3'}, 'q3': {'a': 'q1', 'b': 'q2'}, 'q4': {'c': 'q5'}}
        # self.transitions = transitions_sample
        # self.x = {'q0', 'q1', 'q2', 'q3'}
        new_transitions = {}
        repeated_states_transitions = []
        for state1 in self.x:
            if self.transitions.get(state1) != None:
                for key, val in self.transitions.get(state1).items():

                    for state2 in self.x:
                        if self.transitions.get(state2) != None:
                            for key, val in self.transitions.get(state2).items():
                                if state1 != state2 and self.transitions.get(state1) == self.transitions.get(state2):
                                    print("REPEATED!", state1, state2, self.transitions.get(state1), self.transitions.get(state2))
                                    repeated_states_transitions.append([state1, state2])
                                    self.transitions.pop(state2)

        for repeated_group_of_states in repeated_states_transitions:
            for state in self.x:
                if self.transitions.get(state) != None:
                    for key, val in self.transitions.get(state).items():
                        if val in repeated_group_of_states:
                            self.transitions.get(state)[key] = repeated_group_of_states[0]
                            
        for repeated_ones in repeated_states_transitions:
            for item in repeated_ones[1:]:
                # print(repeated_ones[1:])
                self.x.remove(item)

        # print("SELFX", self.x)

        repeated_states_acceptance = []
        for state3 in self.y:
            if self.transitions.get(state3) != None:
                for key, val in self.transitions.get(state3).items():

                    for state4 in self.y:
                        if self.transitions.get(state4) != None:
                            for key, val in self.transitions.get(state4).items():
                                if state3 != state4 and self.transitions.get(state3) == self.transitions.get(state4):
                                    # print("REPEATED!", state3, state4, self.transitions.get(state3), self.transitions.get(state4))
                                    repeated_states_acceptance.append([state3, state4])
                                    self.transitions.pop(state4)
    
        for repeated_group_of_states in repeated_states_acceptance:
            for state in self.y:
                if self.transitions.get(state) != None:
                    for key, val in self.transitions.get(state).items():
                        if val in repeated_group_of_states:
                            self.transitions.get(state)[key] = repeated_group_of_states[0]

        for repeated_ones in repeated_states_acceptance:
            for item in repeated_ones[1:]:
                # print(repeated_ones[1:])
                self.y.remove(item)

    def generate_automata(self):
        automata = DFA(self.x | self.y, self.sigma, self.transitions, 'q0', self.final_states)
        automata.view("DFA MINIMIZED")
        
            