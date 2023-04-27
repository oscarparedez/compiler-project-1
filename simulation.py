from utils import *

def calculate_move(origin_states, symbol, transitions):
    move = set()
    for state in origin_states:
        if transitions.get(state) == None:
            move.update()
        else:
            for key in transitions.get(state):
                if key == symbol and transitions.get(state).get(key) != set():
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
    s = calculate_e_closure(initial_state, transitions)
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

def DFA_accepts_R(string, initial_state, final_states, transitions, t_states, final_states_ids, final_states_dict):
    final_states_dict = list(final_states_dict.values())
    s = initial_state
    tokens = []
    prev_s = ''
    while (len(string) != 0):
        c = string[0]
        s = transitions.get(s, {}).get(c, None)
        if s is None:
            get_all_ids = t_states.get(prev_s)
            counter = 0
            for i in get_all_ids:
                for j in final_states_ids:
                    if i == j and counter == 0:
                        matching_id = final_states_ids.index(i)
                        counter += 1
            tokens.append(final_states_dict[matching_id])
            s = initial_state
        else:
            prev_s = s
            string = string[1:]
    get_all_ids = t_states.get(prev_s)
    counter = 0
    for i in get_all_ids:
        for j in final_states_ids:
            if i == j and counter == 0:
                matching_id = final_states_ids.index(i)
                counter += 1

    tokens.append(final_states_dict[matching_id])
    return tokens