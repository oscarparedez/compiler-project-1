
from tokenizer import Tokenizer

regex_options = ['ab*ab*', '(a|b)*a', 'ab*ab*', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?', 'a(ab+(ab+)?a?)+', 'a+bc']

tokenizer = Tokenizer(regex_options[3])
tokenizer.get_tokens()