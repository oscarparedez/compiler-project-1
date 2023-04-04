from utils import *
from ExpressionTree.ExpressionTree import *
from ExpressionTree.Node import *

def read_yal():
    with open('yal/slr-2.yal') as f:
        lines = f.readlines()
        variables = {}
        infixes = {}
        results = []
        rules = ''
        for line in lines:
            if "let" in line:
                key = line.split('=')[0].split("let ")[1].strip()
                val = line.split('=')[1].strip()
                
                if (len(detect_substring(variables, val)) != 0):
                    temp_val = val
                    var_names = detect_substring(variables, val)
                    # print("FOUND THESE", val, var_names)
                    for var in var_names:
                        # print("HERE FOUND", var, infixes[var])
                        temp_val = temp_val.replace(var, '('+str(infixes[var])+')')
                        # variables[key] = temp_val
                        # infixes[key] = temp_val
                        # results.append(temp_val)
                        
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
                                
                    variables[key] = temp_val
                    infixes[key] = temp_val
                    results.append(temp_val)
                        
                    # Means variable depends on other variables
                else:
                    if "'" in val or '"' in val:
                        if "-" in val:
                            # print("VAL!", val)
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
                                    if j != len(new_list[i]) - 1:
                                        new_infix += str(new_list[i][j])+'|'
                                    else:
                                        new_infix += str(new_list[i][j])
                                if i != len(new_list) - 1:
                                    new_infix += '|'
                                    
                            # print("SUMMARY", new_infix, new_list)
                            
                            infixes[key] = new_infix
                            variables[key] = new_list
                            results.append(new_infix)
                            
                        elif 'delim' in key:
                            my_list = []
                            active_char = 0
                            while active_char < len(val):
                                if val[active_char] == ' ':
                                    my_list.append(val[active_char])
                                elif val[active_char] == "\\":
                                    if val[active_char+1] == 'n':
                                        my_list.append(r"\n")
                                    if val[active_char+1] == 's':
                                        my_list.append(' ')
                                    if val[active_char+1] == 't':
                                        my_list.append(r"\t")
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
                                    
                            infixes[key] = new_infix
                            variables[key] = my_list
                            results.append(new_infix)
                            
            elif line.startswith('    '):
                first_rule = line.split()[0]
                rules += infixes[first_rule]
            elif line.startswith('  | '):
                rule = line.split('{')[0].strip()
                rule_declaration = rule.split('|')[1].strip().replace("'", '')
                # print("RULE DECL", rule_declaration)
                    
                                        
 
                       
        # print("NEW VARS", variables)
        # print("RESULTS", results)
        infixes_values = list(infixes.values())
        for i in range(len(infixes_values)):
            if '?' in infixes_values[i] or '+' in infixes_values[i]:
                infixes_values[i] = str(operate_nullable_and_plus(infixes_values[i]))
                # print("THIS ENTERED THE CONDITION", infixes_values[i])
        
        # Concatenate based on rules
        print("INFIXES", infixes)

        # postfixes_values = []
        # for i in range(len(infixes_values)):      
        #     postfixes_values.append(shunting_yard(infixes_values[i]))
        #     print("NEW INFIX", infixes_values[i])
            
            
        # for i in range(len(postfixes_values)):
        #     print("POSTFIX: ", postfixes_values[i])
            # print(print_postorder(generate_tree(postfixes_values[i])))
            
def transform_string(s):
    """
    This function takes a string with one or more characters and transforms it
    to a string with the characters separated by a pipe symbol and enclosed in
    parentheses.
    """
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
                        substrings.append(r"\n")
                    elif new_string == '\\t':
                        substrings.append(r"\t")
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
                    # print("ENTERS HERE????", infix_string[start_pos: end_pos + 1])
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

        if (symbol in ALPHABET):
            output += symbol
        elif symbol == '\\':
            if exp[i+1] == 'n':
                output += r"\n"
            elif exp[i+1] == 't':
                output += r"\t"
            elif exp[i+1] == 's':
                output += ' '
            i += 1
        elif symbol == ' ':
            output += ' '
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
    # print("INFIX: ", exp)
    # print("POSTFIX: ", postfix_string)
    
    return postfix_string

def generate_tree(postfix):
    nodes = []
    node_id = 0
    pos_counter = 0
    while pos_counter < len(postfix):
        is_operator = postfix[pos_counter] == '*' or postfix[pos_counter] == '|' or postfix[pos_counter] == '.'
        if not is_operator:
            if postfix[pos_counter] == EPSILON:
                nodes.append(Node(None, postfix[pos_counter]))
            else:
                if postfix[pos_counter] == '\\':
                    if postfix[pos_counter+1] == 'n':
                        nodes.append(Node(node_id, "ASCII 10"))
                        pos_counter += 1
                        
                    elif postfix[pos_counter+1] == 't':
                        nodes.append(Node(node_id, "ASCII 9"))
                        pos_counter += 1
                elif postfix[pos_counter] == ' ':
                    nodes.append(Node(node_id, "ASCII 32"))
                else:
                    nodes.append(Node(node_id, postfix[pos_counter]))
                node_id += 1
        else:
            if postfix[pos_counter] == '*':
                right = None
            else:
                right = nodes.pop()
            left = nodes.pop()
            new_node = Node(None, postfix[pos_counter], left, right)
            nodes.append(new_node)
        pos_counter += 1
    root = nodes.pop()
    return root

def print_postorder(root):

    if root:
        # First recursive on left child
        print_postorder(root.left)
        
        # now recursive on right child
        print_postorder(root.right)

        # then print the data of node
        print("---", root.value),