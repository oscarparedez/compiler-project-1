
from tokenizer import Tokenizer
from thompson import *
from subset_construction import *
from ExpressionTree.ExpressionTree import *
from utils import *
from minimization import *
from simulation import *

regex_options = ['ab*ab*', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?', '(a|b)*a(a|b)(a|b)', 'a(a?b*|c+)b|baa']
simulation_string = "abbbbbbbbbbbbbbbbbbbabccccccccccccc"
    
tokenizer = Tokenizer(regex_options[5])
postfix = tokenizer.get_tokens()
sigma, transitions, initial_state, final_states = build_automata(postfix)
accepts_nfa = NFA_accepts_R(simulation_string, initial_state, final_states, transitions)
print("ACEPTA NFA", accepts_nfa)

initial, final_states_stack, transitions_stack = subset_construction(sigma, transitions, initial_state, final_states)
acepts_dfa_from_subsets = DFA_accepts_R(simulation_string, initial, final_states_stack, transitions_stack)
print("ACEPTA DFA DE SUBCONJUNTOS", acepts_dfa_from_subsets)    

tree = ExpressionTree(postfix)
root = tree.build_tree()
tree.nullable(root)
tree.firstpos(root)
tree.lastpos(root)
tree.followpos(root)
states_stack, sigma, transitions_stack, initial_state, final_states_stack = tree.generate_transitions(root, sigma)
accepts_dfa = DFA_accepts_R(simulation_string, initial_state, final_states_stack, transitions_stack)
print("ACEPTA DFA DIRECTO", accepts_dfa)

minimization_dfa = Minimization(states_stack, sigma, transitions_stack, initial_state, final_states_stack)
minimization_dfa.states_partition()
minimization_dfa.verify_identical_transitions()