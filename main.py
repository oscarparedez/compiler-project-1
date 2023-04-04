
from tokenizer import Tokenizer
from thompson import *
from subset_construction import *
from ExpressionTree.ExpressionTree import *
from utils import *
from minimization import *
from simulation import *
from read_yal import *

regex_options = ['((a|b|c).(a|b|c)*)', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?', '(a|b)*a(a|b)(a|b)', 'a(a?b*|c+)b|baa']
simulation_string = "acccccb"
    
tokenizer = Tokenizer(regex_options[0])
postfix = tokenizer.get_tokens()
sigma, transitions, initial_state, final_states = build_automata(postfix)
accepts_nfa = NFA_accepts_R(simulation_string, initial_state, final_states, transitions)

# tree = ExpressionTree(postfix)
# root = tree.build_tree()
# tree.print_postorder(root)
# print("ACEPTA NFA", accepts_nfa)

states_subsets, sigma_subsets, initial, final_states_stack, transitions_stack = subset_construction(sigma, transitions, initial_state, final_states)
acepts_dfa_from_subsets = DFA_accepts_R(simulation_string, initial, final_states_stack, transitions_stack)
# print("ACEPTA DFA DE SUBCONJUNTOS", acepts_dfa_from_subsets)


# minimization_dfa_subsets = Minimization(states_subsets, sigma_subsets, transitions_stack, initial, final_states_stack, 'subsets')
# minimization_dfa_subsets.states_partition()
# minimization_dfa_subsets.transitions_partition()
# minimization_dfa_subsets.verify_identical_transitions()
# minimization_dfa_subsets.generate_automata()
# minimization_dfa_subsets.simulate()

# tree = ExpressionTree(postfix)
# root = tree.build_tree()
# tree.nullable(root)
# tree.firstpos(root)
# tree.lastpos(root)
# tree.followpos(root)
# states_stack, sigma, transitions_stack, initial_state, final_states_stack = tree.generate_transitions(root, sigma)
# accepts_dfa = DFA_accepts_R(simulation_string, initial_state, final_states_stack, transitions_stack)
# # print("ACEPTA DFA DIRECTO", accepts_dfa)

# minimization_dfa = Minimization(states_stack, sigma, transitions_stack, initial_state, final_states_stack, 'direct')
# minimization_dfa.states_partition()
# minimization_dfa.transitions_partition()
# minimization_dfa.verify_identical_transitions()
# minimization_dfa.generate_automata()
# minimization_dfa.simulate()


read_yal()