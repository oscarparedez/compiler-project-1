
from tokenizer import Tokenizer

regex_options = ['(a|b)*abb', '0?(1?)?0*', '(a*|b*)c', '(b|b)*abb(a|b)*', '(a|ε)b(a+)c?', '(a|b)*a(a|b)(a|b)', 'a(a?b*|c+)b|baa']

tokenizer = Tokenizer(regex_options[0])
tokenizer.get_tokens()