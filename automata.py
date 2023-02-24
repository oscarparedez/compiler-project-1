class Automata:
    def __init__(self, initial_state, final_state, sigma):
        self.sigma = set()
        self.Qstates = set()
        self.initial_state = initial_state
        self.final_state = final_state
        self.sigma.update(sigma)
        self.Qstates.update(initial_state)
        self.Qstates.update(final_state)

        if (isinstance(sigma, str)):
            self.transitions = {
                initial_state: {
                    sigma: final_state
                }
            }

    # def create_automata(self):
    #     self.transitions.update(
    #         {
    #             self.initial_state: 
    #                 {list(self.sigma)[0]: self.final_state}
    #         }
    #         # {'origin': self.initial_state, 'destination': self.final_state, 'value': self.sigma}
    #     )
    #     self.Qstates.update(self.initial_state)
    #     self.Qstates.update(self.final_state)

    def set_automata(self, automata, new_transitions):
        self.transitions.update(new_transitions)
        self.Qstates.update(str(automata.initial_state))
        self.Qstates.update(str(automata.final_state))
        self.initial_state = automata.initial_state
        self.final_state = automata.final_state

    
    def or_operation(self, new_initial_state, new_final_state, automata1, automata2):
        new_alphabet = automata1.sigma
        new_alphabet.update(automata2.sigma)
        new_automata = Automata(new_initial_state, new_final_state, new_alphabet)
        new_transitions = { 
            new_initial_state: {
                'ε': { automata1.initial_state, automata2.initial_state }
            },
            automata1.final_state: {
                'ε': new_final_state,
            },
            automata2.final_state: {
                'ε': new_final_state,
            }
        }
        new_transitions.update(automata2.transitions)

        return new_automata, new_transitions
    
    def concat_operation(self, automata1, automata2):
        new_alphabet = automata1.sigma
        new_alphabet.update(automata2.sigma)
        new_transitions = {
            automata1.final_state: {
                'ε': automata2.initial_state
            }
        }
        new_transitions.update(automata2.transitions)

        new_automata = Automata(automata1.initial_state, automata2.final_state, new_alphabet)
        return new_automata, new_transitions

    def kleene_operation(self, initial_state, final_state, automata):
        new_automata = Automata(initial_state, final_state, automata.sigma)
        new_transitions = {
            initial_state: {
                'ε': {automata.initial_state, final_state},
            },
            automata.final_state: {
                'ε': {final_state, automata.initial_state}
            }
        }

        return new_automata, new_transitions

