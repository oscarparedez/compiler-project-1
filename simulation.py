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

def DFA_accepts_R(string, initial_state, final_states, transitions):
    i = 0
    s = initial_state
    while (i < len(string) and s != None):
        c = string[i]
        s = transitions.get(s, {}).get(c, None)
        i += 1
    if s in final_states:
        return True
    else:
        return False