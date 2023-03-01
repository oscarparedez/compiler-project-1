from string import digits, ascii_lowercase, ascii_uppercase

# Extras
EPSILON = 'ε'
HASH = '#'

OPERATORS = [')', '(', '?', '+', '*', '|', '.']

POSTFIX_OPERATORS = {
    ')': 5,
    '(': 4,
    '*': 3, #kleene
    '.': 2, #or
    '|': 1, #conc 
}

ALPHABET = ascii_lowercase + ascii_uppercase + digits + EPSILON