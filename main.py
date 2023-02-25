
from tokenizer import Tokenizer

regex_options = ['a|b?+', 'a(a|b)*b', '(a|b)*a', 'ab*ab*', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?', 'a(ab+(ab+)?a?)+', 'a+bc']

tokenizer = Tokenizer(regex_options[0])
tokenizer.get_tokens()