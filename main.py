
from tokenizer import Tokenizer

regex_options = ['ab*ab*', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?']

tokenizer = Tokenizer(regex_options[1])
tokenizer.get_tokens()