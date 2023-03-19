from automata import *
from utils import *
from subset_construction import *
from automathon import NFA
from ExpressionTree.ExpressionTree import *

def build_automata(postfix_symbols):
        automatas_stack = []
        id_counter = 0
        for symbol in postfix_symbols:
            if symbol in ALPHABET:
                node_initial_state = str(id_counter)
                node_final_state = str(id_counter+1)
                transition = {
                    node_initial_state: {
                        symbol: {node_final_state}
                    }
                }
                states = {node_initial_state, node_final_state}
                new_automata = Automata(node_initial_state, node_final_state, str(symbol), transition, states)
                id_counter += 2
                automatas_stack.append(new_automata)
            elif symbol == '|':
                new_initial_state = str(id_counter)
                new_final_state = str(id_counter+1)
                id_counter += 2

                automata_result = or_operation(new_initial_state, new_final_state, automatas_stack[-2], automatas_stack[-1])
                automatas_stack.pop()
                automatas_stack.pop()
                automatas_stack.append(automata_result)
            elif symbol == '.':
                automata_result = concat_operation(automatas_stack[-2], automatas_stack[-1])
                automatas_stack.pop()
                automatas_stack.pop()
                automatas_stack.append(automata_result)
            elif symbol == '*':
                new_initial_state = str(id_counter)
                new_final_state = str(id_counter+1)
                id_counter += 2

                automata_result = kleene_operation(new_initial_state, new_final_state, automatas_stack[-1])
                automatas_stack.pop()
                automatas_stack.append(automata_result)
                
        automata_final = automatas_stack[-1]
        automata1 = NFA(automata_final.q_states, automata_final.sigma, automata_final.transitions, automata_final.initial_state, {automata_final.final_state})
        automata1.view("NFA")
        
        # tree = ExpressionTree(postfix_symbols)
        # root = tree.build_tree()
        # tree.print_inorder(root)
    
        subset_construction(automata_final.sigma, automata_final.transitions, automata_final.initial_state, {automata_final.final_state})  

def or_operation(new_initial_state, new_final_state, automata1, automata2):
    new_alphabet = automata1.sigma
    new_alphabet.update(automata2.sigma)
    new_transitions = {
        new_initial_state: {
            'ε': { automata1.initial_state, automata2.initial_state }
        },
        automata1.final_state: {
            'ε': {new_final_state},
        },
        automata2.final_state: {
            'ε': {new_final_state},
        }
    }
    new_transitions.update(automata1.transitions)
    new_transitions.update(automata2.transitions)
    
    new_states = set()
    new_states.update(new_initial_state)
    new_states.update(new_final_state)
    new_states.update(automata1.q_states)
    new_states.update(automata2.q_states)
    new_automata = Automata(new_initial_state, new_final_state, new_alphabet, new_transitions, new_states)

    return new_automata

def concat_operation(automata1, automata2):
        new_alphabet = automata1.sigma
        new_alphabet.update(automata2.sigma)
        new_transitions = {
            automata1.final_state: {
                'ε': {automata2.initial_state}
            }
        }
        new_transitions.update(automata1.transitions)
        new_transitions.update(automata2.transitions)
        
        new_states = set()
        new_states.update(automata1.q_states)
        new_states.update(automata2.q_states)
        new_automata = Automata(automata1.initial_state, automata2.final_state, new_alphabet, new_transitions, new_states)
        return new_automata


def kleene_operation(new_initial_state, new_final_state, automata):
    new_transitions = {
        new_initial_state: {
            'ε': {automata.initial_state, new_final_state},
        },
        automata.final_state: {
            'ε': {new_final_state, automata.initial_state}
        }
    }
    new_transitions.update(automata.transitions)
    
    new_states = set()
    new_states.update(new_initial_state)
    new_states.update(new_final_state)
    new_states.update(automata.q_states)
    new_automata = Automata(new_initial_state, new_final_state, automata.sigma, new_transitions, new_states)

    return new_automata