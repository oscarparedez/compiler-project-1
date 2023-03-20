from utils import *
from automata import *
from automathon import DFA
from simulation import *

    
def subset_construction(sigma, transitions, initial_state, final_state):
    zero_e_closure = calculate_e_closure({initial_state}, transitions)

    t_states = {'q0': zero_e_closure}
    d_states_array = [zero_e_closure]
    d_states = [zero_e_closure]

    id_counter = 1

    transitions_stack = {}
    states_stack = set()
    final_states_stack = set()

    if EPSILON in sigma:
        sigma.remove(EPSILON)

    while (len(d_states) > 0):
        t = d_states.pop()
        for symbol in sigma:
            move_calculation = calculate_move(t, symbol, transitions)
            u = calculate_e_closure(move_calculation, transitions)
            if u != set():
                if (u not in d_states_array):
                    d_states.append(u)
                    t_states['q'+str(id_counter)] = u
                    d_states_array.append(u)
                    states_stack.update({'q'+str(id_counter)})
                    id_counter += 1

                t_key = ''
                for key, value in t_states.items():
                    if value == t:
                        t_key = key

                u_key = ''
                for key, value in t_states.items():
                    if value == u:
                        u_key = key
                            
                new_transitions = {
                    t_key: {
                        symbol : u_key
                    }
                }

                if transitions_stack.get(t_key) == None:
                    transitions_stack.update(new_transitions)
                else:
                    transitions_stack.get(t_key)[symbol] = u_key
                    
    for u in d_states_array:
        if final_state.issubset(u):
            for key, value in t_states.items():
                if value == u:
                    final_states_stack.update({key})

    initial = 'q0'
    automata = DFA(states_stack, sigma, transitions_stack, initial, final_states_stack)
    automata.view("DFA FROM SUBSETS")
    return initial, final_states_stack, transitions_stack


    