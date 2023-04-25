from utils import *
from ExpressionTree.ExpressionTree import *
from ExpressionTree.Node import *
from graphviz import Digraph

file_to_open = 'slr-1.yal'
def read_yal():
    variables = {}
    infixes = {}
    results = []
    rules = ''
    with open('yal/'+file_to_open) as f:
        lines = f.readlines()

        for line in lines:
            if "let" in line:
                key = line.split('=')[0].split("let ")[1].strip()
                val = line.split('=')[1].strip()
                
                if (len(detect_substring(variables, val)) != 0):
                    temp_val = val
                    var_names = detect_substring(variables, val)
                    for var in var_names:
                        if infixes[var][0] == '(' and infixes[var][len(infixes[var])-1] == ')':
                            temp_val = temp_val.replace(var, str(infixes[var]))
                        else:
                            temp_val = temp_val.replace(var, '(' + str(infixes[var] + ')'))
                        
                    if '[' in val and ']' in val:
                        starting_pos = 0
                        ending_pos = 0
                        while starting_pos < len(temp_val):
                            if temp_val[starting_pos] == '[':
                                ending_pos = starting_pos +1
                                while temp_val[ending_pos] != ']':
                                    ending_pos += 1
                                value_to_update = temp_val[starting_pos+1: ending_pos]
                                value_to_update = value_to_update.replace("'", '')
                                new = transform_string(value_to_update)
                                temp_val = temp_val[:starting_pos] + new + temp_val[ending_pos + 1:]
                                starting_pos = ending_pos
                            starting_pos += 1
                
                    temp_val = temp_val.replace("'.'", 'Ц')
                    
                    variables[key] = temp_val
                    infixes[key] = temp_val
                    results.append(temp_val)
                        
                    # Means variable depends on other variables
                else:
                    if "'" in val or '"' in val:
                        if "-" in val:
                            my_list = split_by_quotes(val)
                            i = 0
                            new_list = [] 
                            while i+1 < len(my_list):
                                new_list.append(str(my_list[i])+'-'+str(my_list[i+1]))
                                i+=2
                            new_infix = ''
                            for i in range(len(new_list)):
                                new_list[i] = range_to_list(new_list[i])
                                for j in range(len(new_list[i])):
                                    if j == 0:
                                        if i == 0:
                                            new_infix += ''+str(new_list[i][j])+'|'
                                        else:
                                            new_infix += str(new_list[i][j])+'|'
                                    elif j != len(new_list[i]) - 1:
                                        new_infix += str(new_list[i][j])+'|'
                                    else:
                                        new_infix += str(new_list[i][j]) + "|"
                            infixes[key] = new_infix[:-1]
                            variables[key] = new_list
                            results.append(new_infix[:-1])
                            
                        elif 'delim' in key:
                            my_list = []
                            active_char = 0
                            while active_char < len(val):
                                if val[active_char] == ' ':
                                    my_list.append(val[active_char])
                                elif val[active_char] == "\\":
                                    if val[active_char+1] == 'n':
                                        my_list.append('⌐')
                                    if val[active_char+1] == 's':
                                        my_list.append('¬')
                                    if val[active_char+1] == 't':
                                        my_list.append('■')
                                    active_char += 1
                                active_char += 1
                                
                            # Generate infix
                            new_infix = ''
                            for i in range(len(my_list)):
                                my_list[i] = str(my_list[i])
                                if i != len(my_list) - 1:
                                    new_infix += str(my_list[i])+'|'
                                else:
                                    new_infix += str(my_list[i])

                            new_infix = new_infix.replace('.', 'Ц')
                            infixes[key] = new_infix
                            variables[key] = my_list
                            results.append(new_infix)
                        else:
                            new_infix = val[2: -2]
                            new_infix = '(' + '|'.join(new_infix) + ')'
                            infixes[key] = new_infix
                            variables[key] = new_infix
                            results.append(new_infix)

                    
        # Preprocessing #1: Concatenation
        infixes_values = list(infixes.values())
        infixes_keys = list(infixes.keys())

        for i in range(len(infixes_values)):
            infixes_values[i] = get_tokens(infixes_values[i])

        # Preprocessing #2: Operate Nullable and Plus symbols
        for i in range(len(infixes_values)):
            if '?' in infixes_values[i] or '+' in infixes_values[i]:
                infixes_values[i] = str(operate_nullable_and_plus(infixes_values[i]))

    # Read rules
    with open('yal/'+file_to_open) as f:
        lines = f.readlines()
        is_rule = False
        for line in lines:
            line = line.strip()
            if line != '' and 'rule tokens' not in line and 'let ' not in line and 'if' not in line and 'else' not in line and line.split(' ', 1)[0] != '}' and line.split(' ', 1)[0] != '(*' and is_rule:
                if line[0] != '|' and line.split(' ', 1)[0] != 'return':
                    first_rule = line.split()[0]
                    # Get index of the first rule in infixes_keys
                    index_of_rule = infixes_keys.index(first_rule)
                    rules += infixes_values[index_of_rule] + '.#' + '|'
                elif line[0] == '|':
                    rule = line.split('{')[0].strip()
                    rule_value = rule.split('|')[1].strip()

                    if rule_value == "'*'" or rule_value == '"*"':
                        rule_value = 'Ж'
                    elif rule_value == "'('" or rule_value == '"("':
                        rule_value = 'Л'
                    elif rule_value == "')'" or rule_value == '")"':
                        rule_value = 'Ф'
                    elif rule_value == "'.'" or rule_value == '"."':
                        rule_value = 'Ц'
                        
                    else:
                        if (rule_value[0] == "'" and rule_value[len(rule_value)-1] == "'") or (rule_value[0] == '"' and rule_value[len(rule_value)-1] == '"'):
                            rule_value = rule_value.replace("'", '')
                            rule_value = rule_value.replace('"', '')
                            if len(rule_value) > 1:
                                new_rule_value = '('
                                for i in range(len(rule_value)):
                                    char_from_rule_value = rule_value[i]
                                    if rule_value[i] == "*":
                                        char_from_rule_value = 'Ж'
                                    elif rule_value[i] == "(":
                                        char_from_rule_value = 'Л'
                                    elif rule_value[i] == ")":
                                        char_from_rule_value = 'Ф'
                                    elif rule_value[i] == ".":
                                        char_from_rule_value = 'Ц'
                                    new_rule_value += char_from_rule_value + '.'
                                rule_value = new_rule_value[:-1] + ')'
                        else:
                            rule_value = rule_value.replace("'", '')
                            rule_value = rule_value.replace('"', '')
                    
                    if rule_value in infixes_keys:
                        # Get index of the rule in infixes_keys
                        index_of_rule = infixes_keys.index(rule_value)
                        rules += infixes_values[index_of_rule] + '.#' + '|'
                    else:
                        rules += rule_value + '.#' + '|'
                else:
                    pass
            if 'rule tokens ' in line:
                is_rule = True
                
        rules = rules[:-1]
    rules = rules.replace('s.t.r', '(' + '|'.join(UNDERSCORE) + ')')
    postfix_rules = shunting_yard(rules)
    
    dictionary = {}
    
    with open('yal/'+file_to_open) as f:
        lines = f.readlines()
        key = ''
        value = ''
        is_rule = False
        for line in lines:
            line = line.strip()
            if is_rule and line != '':
                if line[0] != '|':
                    first_string = line.split()[0]
                    if first_string in infixes_keys:
                        key = first_string
                        key = key.replace('\t', '')
                        key = key.replace("'", '')
                        if '{' in line:
                            if '}' in line:
                                dictionary[key] = line[line.index('{')+1 : line.index('}')]
                        elif '{' not in line and '}' not in line:
                            dictionary[key] = ''
                    else:
                        if '}' not in line:
                            value += line + ' '
                        else:
                            value += line[:line.index('}')].strip()
                            dictionary[key] = value
                            value = ''
                elif line[0] == '|':
                    first_string = line.split(' ')[1]
                    key = first_string
                    key = key.replace('\t', '')
                    key = key.replace("'", '')
                    
                    if '{' in line:
                        if '}' in line:
                            dictionary[key] = line[line.index('{')+1 : line.index('}')]
                        else:
                            value += line[line.index('{')+1 :].strip()
                    elif '}' in line:
                        value += line[:line.index('}')].strip()
                        dictionary[key] = value
                        value = ''
                    elif '{' not in line and '}' not in line:
                        dictionary[key] = ''
                        
                    else:
                        value += line + ' '
                            
                            
            if 'rule tokens ' in line:
                is_rule = True
    
    headers_and_trailers = {'headers': '', 'trailers': ''}
    with open('yal/'+file_to_open) as f:
        lines = f.readlines()
        is_header = True
        for line in lines:
            if is_header:
                if '(*' in line and '|' not in line:
                    if '*)' in line:
                        headers_and_trailers['headers'] += line[line.index('(*'):line.index('*)')+2] + '\n'
                    else:
                        headers_and_trailers['headers'] += line[line.index('(*'):]
                elif '*)' in line and '|' not in line:
                    headers_and_trailers['headers'] += line[:line.index('*)')+2] + '\n'
            
            else:
                if '(*' in line and '|' not in line:
                    if '*)' in line:
                        headers_and_trailers['trailers'] += line[line.index('(*'):line.index('*)')+2] + '\n'
                    else:
                        headers_and_trailers['trailers'] += line[line.index('(*'):]
                elif '*)' in line and '|' not in line:
                    headers_and_trailers['trailers'] += line[:line.index('*)')+2] + '\n'
            
            if 'let ' in line:
                is_header = False
                
                
    return_list = []

    for key in dictionary:
        value = dictionary[key]
        return_list.append(value)
                            
    return postfix_rules, return_list, dictionary, headers_and_trailers
            
def transform_string(s):
    result = '(' + '|'.join(s) + ')'
    return result     
        

def split_by_quotes(string):
    substrings = []
    i = 0
    while i < len(string):
        if string[i] == "'":
            j = i + 1
            while j < len(string):
                if string[j] == "'":
                    new_string = string[i+1:j]
                    if new_string == '\\n':
                        substrings.append('⌐')
                    elif new_string == '\\t':
                        substrings.append('■')
                    elif new_string == '\\s':
                        substrings.append('¬')
                    else:
                        substrings.append(new_string)

                    i = j + 1
                    break
                j += 1
        else:
            i += 1
    return substrings                            
                
def char_to_ascii(char):
    return ord(char)

def range_to_list(s):
    result = []
    start = ord(s[0])
    end = ord(s[2])

    for i in range(start, end+1):
        result.append(chr(i))

    return result

def detect_substring(dictionary, s):
    substrings = []
    for i in range(len(s)):
        for j in range(i+1, len(s)+1):
            substring = s[i:j]
            for dict_key in dictionary.keys():
                if substring == dict_key and substring not in substrings:
                    substrings.append(substring)
    return sorted(substrings, key=len, reverse=True)

def operate_nullable_and_plus(infix_string):
    token_length = len(infix_string)
    i = 0
    while i < token_length:
        start_pos = None
        end_pos = None

        # Operate all ? and +
        # eliminate operation that uses ? and replace it by its equivalent (a? = a | E)
        # eliminate operation that uses + and replace it by its equivalent (a+ = a.a*)
        if (infix_string[i] == '?' or infix_string[i] == '+'):
            if (infix_string[i - 1] in ALPHABET):
                start_pos = i - 1
                end_pos = i
                if infix_string[i] == '?':
                    infix_string = infix_string.replace(infix_string[start_pos: end_pos + 1], '(' + infix_string[start_pos] + '|ε)')
                else:
                    infix_string = infix_string.replace(infix_string[start_pos: end_pos + 1], '(' + infix_string[start_pos] + '.' + infix_string[start_pos] + '*)')
                token_length = len(infix_string)
            
            elif (infix_string[i - 1] == ')'):
                open_parenthesis_finder = i - 1
                while (infix_string[open_parenthesis_finder] != '('):
                    open_parenthesis_finder -= 1
                start_pos = open_parenthesis_finder
                end_pos = i
                term = infix_string[start_pos : end_pos]
                if infix_string[i] == '?':
                    infix_string = infix_string.replace(infix_string[start_pos: end_pos + 1], '(' + term + '|ε)')
                else:
                    infix_string = infix_string.replace(infix_string[start_pos: end_pos + 1], '(' + term + '.' + term + '*)')
                token_length = len(infix_string)

        i += 1
    return str(infix_string)

def shunting_yard(exp):
        i = 0
        output = ''
        operator_stack = []
        while i < len(exp):
            symbol = exp[i]
            symbol_is_not_operator = symbol != '*' and symbol != '|' and symbol != '.' and symbol != '(' and symbol != ')'
            if (symbol_is_not_operator):
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
    
        postfix_string = output
        
        return postfix_string

def get_tokens(expression):
    active_index = 0
    tokens = []
    while active_index < len(expression):
        if (expression[active_index] in ALPHABET):
            if active_index > 0 and (tokens[len(tokens) - 1] in ALPHABET or tokens[len(tokens) - 1] == ')' or tokens[len(tokens) - 1] == '?' or tokens[len(tokens) - 1] == '*' or tokens[len(tokens) - 1] == '+'):
                tokens.append('.')
            tokens.append(expression[active_index])
        elif expression[active_index] == ' ':
            tokens.append('¬')
        elif (expression[active_index]) == '\\':
            if expression[active_index+1] == 'n':
                tokens.append('⌐')
            elif expression[active_index+1] == 't':
                tokens.append('■')
            active_index += 1
        elif (expression[active_index]) == "'" and (expression[active_index+2]) == "'":
            tokens.append(expression[active_index + 1])
            active_index += 2
        elif (expression[active_index] in OPERATORS):
            if expression[active_index] == '(':
                if active_index > 0 and tokens[len(tokens) - 1] != '(' and tokens[len(tokens) - 1] != '|':
                    tokens.append('.')
                tokens.append('(')
            elif expression[active_index] == ')':
                tokens.append(')')
            elif expression[active_index] == '*':
                tokens.append('*')
            elif expression[active_index] == '?':
                tokens.append('?')
            elif expression[active_index] == '+':
                tokens.append('+')
            elif expression[active_index] == '|':
                tokens.append('|')
        else:
            tokens.append(expression[active_index])
        
        active_index += 1
    
    result = "".join(tokens)

    return result

def build_tree(postfix, return_values):
    final_states_id = []
    nodes = []
    node_id = 1
    for symbol in postfix:
        is_operator = symbol == '*' or symbol == '|' or symbol == '.'
        if not is_operator:
            if symbol == EPSILON:
                nodes.append(Node(None, symbol))
            elif symbol == HASHTAG:
                return_val = return_values.pop()
                final_states_id.append(node_id)
                nodes.append(Node(node_id, symbol, return_val))
                node_id += 1
            else:
                nodes.append(Node(node_id, symbol))
                node_id += 1
        else:
            if symbol == '*':
                right = None
            else:
                right = nodes.pop()
            left = nodes.pop()
            new_node = Node(None, symbol, None, left, right)
            nodes.append(new_node)
    root = nodes.pop()
    return root, final_states_id

def render(root):
    digraph = Digraph()

    def add_node(node):
        digraph.node(str(id(node)), str(node.value))
        if node.left:
            digraph.edge(str(id(node)), str(id(node.left)), label='L')
            add_node(node.left)
        if node.right:
            digraph.edge(str(id(node)), str(id(node.right)), label='R')
            add_node(node.right)

    add_node(root)

    digraph.render(file_to_open+'.pdf', view=False)