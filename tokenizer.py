from utils import *
from automata import *
from transition import *
import random
from automathon import NFA

class Tokenizer:
    def __init__(self, expression):
        self.expression = list(expression)
        self.active_index = 0
        self.active_char = self.expression[self.active_index]
        self.tokens = []
        self.string = expression
        self.postfix_string = ''

    def next_char(self):
        try:
            self.active_index += 1
            self.active_char = self.expression[self.active_index]
        except Exception:
            self.active_char = None

    def get_tokens(self):
        while self.active_index < len(self.expression):
            if (self.active_char not in ALPHABET and self.active_char not in OPERATORS):
                raise Exception("Unsupported chars")

            if (self.active_char in ALPHABET):
                if self.active_index > 0 and (self.tokens[len(self.tokens) - 1] in ALPHABET or self.tokens[len(self.tokens) - 1] == ')' or self.tokens[len(self.tokens) - 1] == '?' or self.tokens[len(self.tokens) - 1] == '*' or self.tokens[len(self.tokens) - 1] == '+'):
                    self.tokens.append('.')
                self.tokens.append(self.active_char)
                
            elif (self.active_char in OPERATORS):
                if self.active_char == '(':
                    if self.active_index > 0 and self.tokens[len(self.tokens) - 1] != '(':
                        self.tokens.append('.')
                    self.tokens.append('(')
                elif self.active_char == ')':
                    self.tokens.append(')')
                elif self.active_char == '*':
                    self.tokens.append('*')
                elif self.active_char == '?':
                    self.tokens.append('?')
                elif self.active_char == '+':
                    self.tokens.append('+')
                elif self.active_char == '|':
                    self.tokens.append('|')
            
            self.next_char()
        
        self.string = "".join(self.tokens)

        if '?' in self.string or '+' in self.string:
            self.reduce()
        
        postfix_symbols = self.shunting_yard(self.string)

        self.build_automata(postfix_symbols)
                

    def reduce(self):
        token_length = len(self.string)
        i = 0
        while i < token_length:
            start_pos = None
            end_pos = None

            # Operate all ? and +
            if (self.string[i] == '?' or self.string[i] == '+'):
                if (self.string[i - 1] in ALPHABET):
                    start_pos = i - 1
                    end_pos = i
                    if self.string[i] == '?':
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], self.string[start_pos] + "|ε")
                    else:
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], self.string[start_pos] + "." + self.string[start_pos] + "*")
                    # eliminate operation that uses ? and replace it by its equivalent (a? = a | E)
                    token_length = len(self.string)
                
                elif (self.string[i - 1] == ')'):
                    open_parenthesis_finder = i - 1
                    while (self.string[open_parenthesis_finder] != '('):
                        open_parenthesis_finder -= 1
                    start_pos = open_parenthesis_finder
                    end_pos = i
                    term = self.string[start_pos : end_pos]
                    if self.string[i] == '?':
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], term + "|ε")
                    else:
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], term + "." + term + "*")
                    token_length = len(self.string)

            i += 1

    def shunting_yard(self, exp):
        i = 0
        output = ''
        operator_stack = []
        while i < len(exp):
            symbol = exp[i]

            if (symbol in ALPHABET):
                output += symbol
            elif symbol == '*' or symbol == '|' or symbol == '.':
                symbol_has_higher_precedence = False
                while not symbol_has_higher_precedence and len(operator_stack) > 0:
                    last_symbol_precedence = POSTFIX_OPERATORS.get(operator_stack[-1])
                    current_symbol_precedence = POSTFIX_OPERATORS.get(symbol)
                    if last_symbol_precedence >= current_symbol_precedence and last_symbol_precedence != 4:
                        output += operator_stack.pop()
                    else:
                        symbol_has_higher_precedence = True
                operator_stack.append(symbol)
            elif symbol == '(':
                operator_stack.append(symbol)
            elif symbol == ')':
                found_left_parenthesis = False
                while not found_left_parenthesis:
                    while len(operator_stack) > 0 and operator_stack[-1] != '(':
                        output += operator_stack.pop()
                    found_left_parenthesis = True
                # print(operator_stack)
                    if len(operator_stack) > 0:
                        operator_stack.pop()

            i += 1
        
        while len(operator_stack) != 0:
            output += operator_stack.pop()   
    
        self.postfix_string = output
        print("INFIX: ", self.string)
        print("POSTFIX: ", self.postfix_string)
        
        return self.postfix_string

    def build_automata(self, postfix_symbols):
        automata_final = Automata('', '', '')
        automatas_stack = [] #ab|
        id_counter = 1
        for symbol in postfix_symbols:
            if symbol in ALPHABET:
                node_initial_state = id_counter
                node_final_state = id_counter+1
                new_automata = Automata(str(node_initial_state), str(node_final_state), str(symbol))

                if id_counter == 1:
                    automata_final = new_automata
                id_counter += 2
                automatas_stack.append(new_automata)
            elif symbol == '|':
                new_initial_state = id_counter
                new_final_state = id_counter+1
                id_counter += 2

                automata_result, new_transitions = automata_final.or_operation(str(new_initial_state), str(new_final_state), automatas_stack[-2], automatas_stack[-1])
                automatas_stack.pop()
                automatas_stack.pop()
                automata_final.set_automata(automata_result, new_transitions)
            elif symbol == '.':
                automata_result, new_transitions = automata_final.concat_operation(automatas_stack[-2], automatas_stack[-1])
                automatas_stack.pop()
                automatas_stack.pop()
                automata_final.set_automata(automata_result, new_transitions)
            elif symbol == '*':
                new_initial_state = id_counter
                new_final_state = id_counter+1
                id_counter += 2

                automata_result, new_transitions = automata_final.kleene_operation(str(new_initial_state), str(new_final_state), automata_final)
                automata_final.set_automata(automata_result, new_transitions)

        automata1 = NFA(automata_final.Qstates, automata_final.sigma, automata_final.transitions, str(automata_final.initial_state), set(automata_final.final_state))
        automata1.view("NFA")



        

        