import graphviz

def read_yal(file_to_open):
    found_production = False
    tokens = []
    productions = {}
    active_production_variable = ''
    with open('yalp/'+file_to_open) as f:
        lines = f.readlines()
        for line in lines:
            if line != '' and '/*' not in line and '*/' not in line:
                if '%token ' in line:
                    for token_value in line[7:-1].split(' '):
                        tokens.append(token_value)
                if ':' in line:
                    active_production_variable = line.split(':')[0]
                    productions[active_production_variable] = []
                    found_production = True
                elif '| ' in line:
                    active_production_value = line.split('| ')[1]
                    active_production_value = active_production_value.split('\n')[0]
                    productions[active_production_variable].append(active_production_value.strip().split(' '))
                elif found_production and line != '\n' and ';' not in line:
                        productions[active_production_variable].append(line.strip().split(' '))
                        found_production = False

    return tokens, productions

def closure(itemset, productions):
    marked = []

    while len(itemset) > 0:
        current = itemset.pop(0)
        marked.append(current)

        next_term = None
        mark_next = False
        for i in current:
            if mark_next:
                mark_next = False
                next_term = i
            if i == '∙':
                mark_next = True
        
        if next_term and next_term in productions: #Si existe y es no terminal
            for production in productions[next_term]:
                item = tuple([next_term, '∙'] + [j for j in production])
                if item not in marked and item not in itemset:
                    itemset.append(item)

    return marked

def shift_right(item, symbol):
    shifted = []
    
    shift_next = False
    shift_happened = False
    for i in item:
        if i == '∙':
            shift_next = True
        elif shift_next:
            shift_next = False
            if  i == symbol:
                shift_happened = True
                shifted.append(i)
                shifted.append('∙')
            else:
                return None
        else:
            shifted.append(i)
    if shift_happened:
        return tuple(shifted)
    else:
        return None

def goto(itemset, symbol, productions):
    shifted_production = []
    for i in itemset:
        shift = shift_right(i, symbol)
        if shift:
            shifted_production.append(shift)
    return closure(shifted_production, productions)

def build_automata(tokens, productions):
    first_production = list(productions.keys())[0]
    augmented_first_production = first_production + "'"
    productions[augmented_first_production] = [first_production]
    productions_pieces = [closure([(augmented_first_production, '∙', first_production)], productions)]
    # print("productions_pieces", productions_pieces)

    symbols = []

    for i in productions.keys():
        symbols.append(i)

    symbols += tokens
    
    start = productions_pieces[0]
    transitions = []
    states = []
    
    while len(productions_pieces) > 0:
        current = productions_pieces.pop(0)
        states.append(current)

        for i in symbols:
            state = goto(current, i, productions)

            if len(state) > 0:
                transitions.append((current, i, state))
                if state not in states and state not in productions_pieces:
                    productions_pieces.append(state)
    
    final_states = []
    for i in states:
        for j in i:
            if j == (augmented_first_production, first_production, '∙'):
                final_states.append(i)

    return start, states, final_states, transitions

def render_automata(states, transitions, filename):
    dot = graphviz.Digraph('Automata')

    dot.node(name='Accept', label='Accept', shape='plaintext') 
    count = 0
    for state in states:
        stateName = 'q'+str(count)
        count += 1
        
        label = '<<TABLE><TR><TD>'+stateName+'</TD></TR>'

        for item in state:
            line = item[0] + '  →  '
            for i in range(1, len(item)):
                line += ' ' + item[i] + ' '
            label+= '<TR><TD>'+line+'</TD></TR>'
        label+= '</TABLE>>'

        dot.node(name=stateName, label=label, shape='none') 

        if state in accept:
            dot.edge(stateName, 'Accept')
        
    for transition in transitions:
        dot.edge('q'+str(states.index(transition[0])),
                 'q'+str(states.index(transition[2])), 
                 label=transition[1])

    dot.render(filename, view=True)



file_to_open = 'slr-1.yalp'
tokens, productions = read_yal(file_to_open)
start, states, accept, transitions = build_automata(tokens=tokens, productions=productions)
render_automata(states, transitions, file_to_open)

file_to_open = 'slr-2.yalp'
tokens, productions = read_yal(file_to_open)
start, states, accept, transitions = build_automata(tokens=tokens, productions=productions)
render_automata(states, transitions, file_to_open)

file_to_open = 'slr-3.yalp'
tokens, productions = read_yal(file_to_open)
start, states, accept, transitions = build_automata(tokens=tokens, productions=productions)
render_automata(states, transitions, file_to_open)

file_to_open = 'slr-4.yalp'
tokens, productions = read_yal(file_to_open)
start, states, accept, transitions = build_automata(tokens=tokens, productions=productions)
render_automata(states, transitions, file_to_open)