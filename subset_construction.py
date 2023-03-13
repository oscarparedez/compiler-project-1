from utils import *
    
def subset_construction(q_states, sigma, transitions, initial_state, final_state):
    t_states_array = []
    zero_e_closure = calculate_e_closure(initial_state, transitions)
    t_states_array.append(zero_e_closure)
    # test = calculate_move(zero_e_closure, 'a', transitions)
    print("TRANSITIONJS", transitions)
    
    expression_matches = False
    i = 0
    while (not expression_matches):
        for t in t_states_array:
            print("-----------------------")
            print("T STATES ARRAY", t_states_array)
            for symbol in sigma:
                result = calculate_e_closure2(calculate_move(t, symbol, transitions), transitions)
                if result in t_states_array:
                    expression_matches = True
                else:
                    t_states_array.append(result)
            print("-----------------------")
    print(t_states_array)
    
def calculate_move(origin_states, symbol, transitions):
    move = set()
    for state in origin_states:
        for key in transitions.get(state):
            if key == symbol:
                move.update(transitions.get(state).get(key))
                for child_state in transitions.get(state).get(key):
                    # print("CHILD STATE", child_state)
                    for child_key in transitions.get(child_state):
                        if child_key == symbol:
                            move.update(transitions.get(child_state).get(child_key))
    print("MOVE", origin_states, symbol, move)
    return move

def calculate_e_closure(origin_states, transitions):
    # print("TRANSITIONS", transitions)
    closures = set()
    for state in origin_states:
        states_set = set()
        states_set.update(state)
        for key in transitions.get(state):
            if key == EPSILON:
                states_set.update(transitions.get(state).get(key))
                for child_state in transitions.get(state).get(key):
                    for child_key in transitions.get(child_state):
                        if child_key == EPSILON:
                            states_set.update(transitions.get(child_state).get(child_key))
        closures.update(states_set)
    
    print("CLOSURES", origin_states, 'EPSILON', closures)
    return closures

def calculate_e_closure2(origin_states, transitions):
    # print("TRANSITIONS", transitions)
    closures = set()
    for state in origin_states:
        closures.update(state)
        child_states = closures
        while len(child_states) != 0:
            print("CHILD STATES!", child_states)
            for child_state in list(child_states):
                next_states = set()
                for key in transitions.get(child_state):
                    if key == EPSILON:
                        next_states.update(transitions.get(state).get(key))
                        closures.update(transitions.get(state).get(key))
                # print("NEXT STATES", next_states)
                child_states = next_states - closures
                print("SUBSTRACXTION", next_states, closures, child_states)
                # print("NEXT STATES", next_states)
    print("CLOSURES", closures)