from utils import *
import random
from automathon import NFA
from thompson import build_automata

class Tokenizer:
    def __init__(self, expression):
        expression_no_spaces = expression.replace(' ', '')
        self.expression = list(expression_no_spaces)
        self.active_index = 0
        self.active_char = self.expression[self.active_index]
        self.tokens = []
        self.string = expression
        self.postfix_string = ''
        
        self.check_for_errors(expression)

    def next_char(self):
        try:
            self.active_index += 1
            self.active_char = self.expression[self.active_index]
        except Exception:
            self.active_char = None
            
    def check_for_errors(self, expression):
        # check parentheses
        left_parenthesis_count = expression.count('(')
        right_parenthesis_count = expression.count(')')
        if (left_parenthesis_count > right_parenthesis_count):
            raise Exception('There is one left parenthesis without a match')
        if (left_parenthesis_count < right_parenthesis_count):
            raise Exception('There is one right parenthesis without a match')
        
        if expression[0] == '|':
            raise Exception('OR operator needs a symbol to its left')
        if expression[0] == '*':
            raise Exception('KLEENE operator needs a symbol to its left')
        if expression[0] == '+':
            raise Exception('PLUS operator needs a symbol to its left')
        if expression[0] == '?':
            raise Exception('NULLABLE operator needs a symbol to its left')
        
        for i in range(len(expression)):
            if expression[i] == '|':
                if i == len(expression) - 1:
                    raise Exception('OR operator cannot be the last symbol of the expression')
                elif (expression[i+1] not in ALPHABET and(expression[i+1] == ')' or expression[i+1] == '*' or expression[i+1] == '|' or expression[i+1] == '.')):
                    raise Exception('OR operator needs a valid value to its right')
        

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
                    if self.active_index > 0 and self.tokens[len(self.tokens) - 1] != '(' and self.tokens[len(self.tokens) - 1] != '|':
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

        if '?' in self.string or '+' in self.string or '*' in self.string:
            self.reduce_stacked_operators()
        if '?' in self.string or '+' in self.string:
            self.operate_nullable_and_plus()
        
        postfix_symbols = self.shunting_yard(self.string)
        
        return postfix_symbols

    def reduce_stacked_operators(self):
        token_length = len(self.string)
        i = 0
        while i < token_length:

            # Reduce stacked * into one
            if self.string[i] == '*':
                plus_counter = 1
                is_plus = True
                j = i + 1
                while is_plus and j < token_length:
                    if (self.string[j] == '*'):
                        plus_counter += 1
                    else:
                        is_plus = False
                    j+=1
                self.string = self.string.replace(self.string[i: i + plus_counter], "*")
                token_length = len(self.string)

            #Reduce stacked + into one 
            elif self.string[i] == '+':
                plus_counter = 1
                is_plus = True
                j = i + 1
                while is_plus and j < token_length:
                    if (self.string[j] == '+'):
                        plus_counter += 1
                    else:
                        is_plus = False
                    j+=1
                self.string = self.string.replace(self.string[i: i + plus_counter], "+")
                token_length = len(self.string)

            #Reduce stacked ? into one    
            elif self.string[i] == '?':
                plus_counter = 1
                is_plus = True
                j = i + 1
                while is_plus and j < token_length:
                    if (self.string[j] == '?'):
                        plus_counter += 1
                    else:
                        is_plus = False
                    j+=1
                self.string = self.string.replace(self.string[i: i + plus_counter], "?")
                token_length = len(self.string)  
            
            i += 1 
                

    def operate_nullable_and_plus(self):
        token_length = len(self.string)
        i = 0
        while i < token_length:
            start_pos = None
            end_pos = None

            # Operate all ? and +
            # eliminate operation that uses ? and replace it by its equivalent (a? = a | E)
            # eliminate operation that uses + and replace it by its equivalent (a+ = a.a*)
            if (self.string[i] == '?' or self.string[i] == '+'):
                if (self.string[i - 1] in ALPHABET):
                    start_pos = i - 1
                    end_pos = i
                    if self.string[i] == '?':
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], "(" + self.string[start_pos] + "|ε)")
                    else:
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], "(" + self.string[start_pos] + "." + self.string[start_pos] + "*)")
                    token_length = len(self.string)
                
                elif (self.string[i - 1] == ')'):
                    open_parenthesis_finder = i - 1
                    while (self.string[open_parenthesis_finder] != '('):
                        open_parenthesis_finder -= 1
                    start_pos = open_parenthesis_finder
                    end_pos = i
                    term = self.string[start_pos : end_pos]
                    if self.string[i] == '?':
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], "(" + term + "|ε)")
                    else:
                        self.string = self.string.replace(self.string[start_pos: end_pos + 1], "(" + term + "." + term + "*)")
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
                while len(operator_stack) != 0 and (peek(operator_stack) != '(') and (POSTFIX_OPERATORS.get(peek(operator_stack)) >= POSTFIX_OPERATORS.get(symbol)):
                    output += operator_stack.pop()
                operator_stack.append(symbol)
            elif symbol == '(':
                operator_stack.append(symbol)
            elif symbol == ')':
                found_left_parenthesis = False
                while not found_left_parenthesis:
                    while len(operator_stack) > 0 and operator_stack[-1] != '(':
                        output += operator_stack.pop()
                    found_left_parenthesis = True
                    if len(operator_stack) > 0:
                        operator_stack.pop()

            i += 1
        
        while len(operator_stack) != 0:
            output += operator_stack.pop()   
    
        self.postfix_string = output
        print("INFIX: ", self.string)
        print("POSTFIX: ", self.postfix_string)
        
        return self.postfix_string