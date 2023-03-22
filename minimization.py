from automathon import DFA
from simulation import *
class Minimization:
    def __init__(self, states, sigma, transitions, initial_state, final_states, type):
        self.states = states
        # self.states.add(initial_state)
        self.sigma = sigma
        self.transitions = transitions
        self.final_transitions = {}
        self.initial_state = initial_state
        self.final_states = final_states
        self.type = type
        
    def states_partition(self):
        self.x = self.states - self.final_states
        self.y = self.states & self.final_states

    def transitions_partition(self):
        # print("SELF.TRANSITIONS", self.transitions)
        # print("TRANSITONS", self.transitions)
        for acceptance_state in self.y:
            # print("transition final", acceptance_state, self.transitions.get(acceptance_state))
            # self.transitions.pop(acceptance_state)
            # print("ACCEPTANCE", acceptance_state)
            if (self.transitions.get(acceptance_state) != None):
                # print("ACCEPTANCE", acceptance_state, self.transitions.get(acceptance_state))
                self.final_transitions[acceptance_state] = self.transitions.pop(acceptance_state)
                # self.final_transitions[acceptance_state] = self.transitions.get(acceptance_state, {})
        # print("SELF.TRANSITIONS22222", self.transitions, self.final_transitions)
        
        


        
    def verify_identical_transitions(self):
        # print("HERE", self.x, self.y)
        repeated_states_transitions = []
        for state1 in self.x:
            if self.transitions.get(state1) != None:
                for key, val in self.transitions.get(state1).items():
                    for state2 in self.x:
                        if self.transitions.get(state2) != None:
                            for key, val in self.transitions.get(state2).items():
                                if state1 != state2 and self.transitions.get(state1) == self.transitions.get(state2):
                                    # print("REPEATED!", state1, state2, self.transitions.get(state1), self.transitions.get(state2))
                                    
                                    if len(repeated_states_transitions) == 0:
                                        repeated_states_transitions.append([state1, state2])
                                    else:
                                        for repeated_states_groups in repeated_states_transitions:
                                            if state2 not in repeated_states_groups:
                                                print("EHRE 2")
                                                repeated_states_transitions.append([state1, state2])
                                    self.transitions.pop(state2)
                          
        for repeated_group_of_states in repeated_states_transitions:
            for state in self.x:
                if self.transitions.get(state) != None:
                    for key, val in self.transitions.get(state).items():
                        if val in repeated_group_of_states:
                            self.transitions.get(state)[key] = repeated_group_of_states[0]

        # print("REPEATED ONES", repeated_states_transitions)
        for repeated_ones in repeated_states_transitions:
            for item in repeated_ones:
                # print("ITEM", item)
                if len(repeated_ones) != 1:
                    
                    self.x.remove(repeated_ones[-1])
                    self.states.remove(repeated_ones[-1])
                    repeated_ones.pop()
        
        # print("NEW REPEATED ONES", repeated_states_transitions, self.transitions)

        ##############################################

        # print("START(NG)2", self.final_transitions)
        repeated_states_acceptance = []
        # print("FINAL STATES ARRAY ATM", repeated_states_acceptance)
        for state5 in self.y:
            for state6 in self.y:
                if state5 != state6 and self.final_transitions.get(state5) == None and self.final_transitions.get(state6) == None:
                    # print("ENTERS XXX", state5, self.final_transitions.get(state5))
                    # print("ENTERS YYY", state6, self.final_transitions.get(state6))
                    if len(repeated_states_acceptance) == 0:
                        repeated_states_acceptance.append([state5, state6])
                    else:
                        for repeated_states_groups in repeated_states_acceptance:
                            if state6 not in repeated_states_groups:
                                # print("EHRE 2")
                                repeated_states_acceptance.append([state5, state6])
        for state3 in self.y:
            if self.final_transitions.get(state3) != None:
                for key, val in self.final_transitions.get(state3).items():
                    for state4 in self.y:
                        if self.final_transitions.get(state4) != None:
                            for key, val in self.final_transitions.get(state4).items():
                                if state3 != state4 and self.final_transitions.get(state3) == self.final_transitions.get(state4):
                                    # print("REPEATED!", state3, state4, self.final_transitions.get(state3), self.final_transitions.get(state4))
                                    
                                    if len(repeated_states_acceptance) == 0:
                                        repeated_states_acceptance.append([state3, state4])
                                    else:
                                        for repeated_states_groups in repeated_states_acceptance:
                                            if state4 not in repeated_states_groups:
                                                # print("EHRE 2")
                                                repeated_states_acceptance.append([state3, state4])
                                    self.final_transitions.pop(state4)
        
                    # self.final_transitions.pop(state6)   

        # print("REPEATED IN HERE", repeated_states_acceptance)    
    
        for repeated_group_of_states in repeated_states_acceptance:
            for state in self.y:
                if self.final_transitions.get(state) != None:
                    for key, val in self.final_transitions.get(state).items():
                        if val in repeated_group_of_states:
                            self.final_transitions.get(state)[key] = repeated_group_of_states[0]
            
            for state2 in self.x:
                for key, val in self.transitions.get(state2).items():
                    if val in repeated_group_of_states:
                        self.transitions.get(state2)[key] = repeated_group_of_states[0]

        # print("REPEATED ONES", repeated_states_acceptance)
        for repeated_ones in repeated_states_acceptance:
            for item in repeated_ones:
                # print("ITEM", item)
                if len(repeated_ones) != 1:
                    
                    self.y.remove(repeated_ones[-1])
                    self.final_states.remove(repeated_ones[-1])
                    repeated_ones.pop()
        
        # print("START(NG2", self.x, self.y)


    def generate_automata(self):
        automata = DFA(self.x | self.y, self.sigma, self.transitions | self.final_transitions, 'q0', self.final_states)
        automata.view("DFA MINIMIZED "+self.type)

    def simulate(self):
        accepts = DFA_accepts_R('abbbbbbbbbb', 'q0', self.final_states, self.transitions | self.final_transitions)
        print("ACCEPTA MINIMIZACION "+self.type, accepts)
        
            