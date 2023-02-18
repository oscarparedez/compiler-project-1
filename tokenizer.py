from regex import *

class Tokenizer:
    def __init__(self, expression):
        self.expression = list(expression)
        self.active_index = 0
        self.active_char = self.expression[self.active_index]
        self.tokens = []
        self.string = expression

        self.get_tokens()

    def next_char(self):
        try:
            self.active_index += 1
            self.active_char = self.expression[self.active_index]
        except Exception:
            self.active_char = None

    def get_tokens(self):
        while self.active_index < len(self.expression):
            if (self.active_char not in ALPHABET and self.active_char not in OPERATORS.keys()):
                raise Exception("Unsupported chars")

            if (self.active_char in ALPHABET):
                if self.active_index > 0 and (self.tokens[len(self.tokens) - 1] in ALPHABET or self.tokens[len(self.tokens) - 1] == ')' or self.tokens[len(self.tokens) - 1] == '?' or self.tokens[len(self.tokens) - 1] == '*' or self.tokens[len(self.tokens) - 1] == '+'):
                    self.tokens.append('.')
                self.tokens.append(self.active_char)
                
            elif (self.active_char in OPERATORS.keys()):
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
        return self.tokens

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
