from utils import *
    
def subset_construction(sigma, transitions, initial_state):
    t_states_array = []
    zero_e_closure = calculate_e_closure(initial_state, transitions)
    t_states_array.append(zero_e_closure)
    
    expression_matches = False
    while (not expression_matches):
        for t in t_states_array:
            for symbol in sigma:
                move_calculation = calculate_move(t, symbol, transitions)
                result = calculate_e_closure(move_calculation, transitions)
                if result in t_states_array:
                    expression_matches = True
                else:
                    t_states_array.append(result)
    print("SUBCONJUNTOS: ", t_states_array)
    
def calculate_move(origin_states, symbol, transitions):
    move = set()
    for state in origin_states:
        for key in transitions.get(state):
            if key == symbol:
                move.update(transitions.get(state).get(key))
                for child_state in transitions.get(state).get(key):
                    child_states = transitions.get(child_state)
                    if child_states != None:
                        for child_key in child_states:
                            if child_key == symbol:
                                move.update(transitions.get(child_state).get(child_key))
    return move

def calculate_e_closure(origin_states, transitions):
    closures = set()
    for state in origin_states:
        closures.update(state)
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