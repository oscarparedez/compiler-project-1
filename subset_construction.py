from utils import *
from automata import *
from automathon import DFA

    
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

    automata = DFA(states_stack, sigma, transitions_stack, 'q0', final_states_stack)
    automata.view("DFA")

    accepts = NFA_accepts_R("aabbbbbba", initial_state, final_state, transitions)
    print("IS STRING ACCEPTED BY NFA?", accepts)
    
def calculate_move(origin_states, symbol, transitions):
    move = set()
    for state in origin_states:
        if transitions.get(state) == None:
            move.update()
        else:
            for key in transitions.get(state):
                if key == symbol:
                    if transitions.get(state).get(key) != set():
                        move.update(transitions.get(state).get(key))
    return move

def calculate_e_closure(origin_states, transitions):
    closures = set()
    for state in origin_states:
        closures.update({state})
        child_states = transitions.get(state , {}).get(EPSILON, {})
        while len(child_states) != 0:
            if child_states != {}:
                closures.update(child_states)
            next_states = set()
            for state in child_states:
                if state != None:
                    next_states.update(transitions.get(state, {}).get(EPSILON, {}))
            child_states = next_states - closures
    return closures

def NFA_accepts_R(string, initial_state, final_states, transitions):
    s = calculate_e_closure({initial_state}, transitions)
    i = 0
    while (i < len(string)):
        c = string[i]
        move = calculate_move(s, c, transitions)
        s = calculate_e_closure(move, transitions)
        i += 1
    for state in final_states:
        if state in s:
            return True
    
    return False
    