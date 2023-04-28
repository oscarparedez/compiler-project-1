from string import digits, ascii_lowercase, ascii_uppercase

# Extras
EPSILON = 'ε'
HASHTAG = '#'

OPERATORS = [')', '(', '?', '+', '*', '.', '|']

POSTFIX_OPERATORS = {
    ')': 5,
    '(': 4,
    '*': 3, #kleene
    '.': 2, #concat
    '|': 1, #or 
}

# ALPHABET = ascii_lowercase + ascii_uppercase + digits + EPSILON
ALPHABET = ascii_lowercase + ascii_uppercase + digits + EPSILON + HASHTAG
ALPHABET_YALEX = ascii_lowercase + ascii_uppercase + digits + EPSILON + HASHTAG + 'Ж' + 'Л' + 'Ф' + 'Ц' + '/' + '+' + '-' + 'ß' + '§' + '¤'
UNDERSCORE = ascii_uppercase + ascii_lowercase + digits + 'ß' + '§' + '¤'

def peek(stack):
    if (stack):
        return (stack[-1])
    else:
        return None