
from tokenizer import Tokenizer

regex_options = ['ab*ab*', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?', '(a|b)*a(a|b)(a|b)', 'a(a?b*|c+)b|baa']

tokenizer = Tokenizer(regex_options[6])
tokenizer.get_tokens()