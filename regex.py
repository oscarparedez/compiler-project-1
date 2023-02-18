from string import digits, ascii_lowercase, ascii_uppercase

# Extras
EPSILON = 'ε'
END_SYMBOL = '#'

OPERATORS = {
    ')': 1, 
    '(': 2,
    '?': 3, #null
    '+': 4, #plus
    '*': 5, #kleene
    '|': 6, #or
    '.': 7, #conc
}

ALPHABET = ascii_lowercase + ascii_uppercase + digits + '.' + EPSILON