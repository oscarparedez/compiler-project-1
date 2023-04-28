from utils import *
from ExpressionTree.Node import *
from automathon import DFA

class ExpressionTree:
    def __init__(self, postfix, final_states):
        self.root = None
        self.postfix = postfix
        self.final_states = final_states
    
    def build_tree(self):
        nodes = []
        node_id = 1
        for symbol in self.postfix:
            is_operator = symbol == '*' or symbol == '|' or symbol == '.'
            if not is_operator:
                if symbol == EPSILON:
                    nodes.append(Node(None, symbol))
                else:
                    nodes.append(Node(node_id, symbol))
                    node_id += 1
            else:
                if symbol == '*':
                    right = None
                else:
                    right = nodes.pop()
                left = nodes.pop()
                new_node = Node(None, symbol, left, right)
                nodes.append(new_node)
        root = nodes.pop()
        self.root = root
        return self.root
    
    # A function to do inorder tree traversal
    def print_postorder(self, root):
    
        if root:
            # First recursive on left child
            self.print_postorder(root.left)
            
            # now recursive on right child
            self.print_postorder(root.right)
    
            # then print the data of node
            print("---", root.value),
            
    def nullable(self, root):
        if root:
            # First recursive on left child
            self.nullable(root.left)
    
            # now recursive on right child
            self.nullable(root.right)
            
            # then print the data of node
            if root.id is not None:
                root.nullability = False
            elif root.value == EPSILON:
                root.nullability = True
            elif root.value == '*':
                root.nullability = True
            elif root.value == '|':
                if root.left.nullability or root.right.nullability:
                    root.nullability = True
                else:
                    root.nullability = False
            elif root.value == '.':
                if root.left.nullability and root.right.nullability:
                    root.nullability = True
                else:
                    root.nullability = False
            
    def firstpos(self, root):
        if root:
            # First recursive on left child
            self.firstpos(root.left)
    
            # now recursive on right child
            self.firstpos(root.right)
            
            # then print the data of node
            if root.id is not None:
                root.firstpos = {root.id}
            elif root.value == EPSILON:
                root.firstpos = set()
            elif root.value == '*':
                root.firstpos = root.left.firstpos
            elif root.value == '|':
                root.firstpos = root.left.firstpos | root.right.firstpos 
            elif root.value == '.':
                if root.left.nullability:
                    root.firstpos = root.left.firstpos | root.right.firstpos 
                else:
                    root.firstpos = root.left.firstpos
    
    def lastpos(self, root):
        if root:
            # First recursive on left child
            self.lastpos(root.left)
    
            # now recursive on right child
            self.lastpos(root.right)
            
            # then calculate lastpos
            if root.id is not None:
                root.lastpos = {root.id}
            elif root.value == EPSILON:
                root.lastpos = set()
            elif root.value == '*':
                root.lastpos = root.left.lastpos
            elif root.value == '|':
                root.lastpos = root.left.lastpos | root.right.lastpos 
            elif root.value == '.':
                if root.right.nullability:
                    root.lastpos = root.left.lastpos | root.right.lastpos 
                else:
                    root.lastpos = root.right.lastpos
                    
    def get_children_from_node(self, root, nodes_array):
        if root.left:
            nodes_array.append(root.left)
            self.get_children_from_node(root.left, nodes_array)
        if root.right:
            nodes_array.append(root.right)
            self.get_children_from_node(root.right, nodes_array)
        
        return nodes_array
                 
    def followpos(self, root):
        if root:
            # First recursive on left child
            self.followpos(root.left)
    
            # now recursive on right child
            self.followpos(root.right)

            # then calculate followpos
            if root.value == '#' or root == None or \
                (root.value != '*' and root.value != '.'):
                return
            
            elif root.value == '*':
                children_nodes = []
                child_nodes_array = self.get_children_from_node(root, children_nodes)
                root_last_pos = root.lastpos
                root_first_pos = root.firstpos
                for node in root_last_pos:
                    for child_node in child_nodes_array:
                        if child_node.id == node:
                            child_node.followpos.update(root_first_pos)
            elif root.value == '.':
                children_nodes = []
                child_nodes_array = self.get_children_from_node(root, children_nodes)
                left_child_last_pos = root.left.lastpos
                right_child_first_pos = root.right.firstpos # se le updatea
                for node in left_child_last_pos:
                    for child_node in child_nodes_array:
                        if child_node.id == node:
                            child_node.followpos.update(right_child_first_pos)
                    
    def generate_transitions(self, root):
        sigma = ''
        for character in self.postfix:
            if character != '.' and character != '*' and character != '|' and character != '#' and character not in sigma:
                sigma += character
                
        with open('input.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace(' ', 'ß')
                line = line.replace('\n', 'ß')
                line = line.replace('   ', '§')
                line = line.replace('*', 'Ж')
                line = line.replace('(', 'Л')
                line = line.replace(')', 'Ф')
                line = line.replace('.', 'Ц')
                for char in line:
                    if  char not in sigma:
                        raise Exception('Input File not supported. ',  char, 'not defined in yal file.')
        
        s0 = root.firstpos 
        s0_children_nodes = []
        root_children_array = self.get_children_from_node(root, s0_children_nodes)
        s0_nodes = []
        for node in s0:
            for child_node in root_children_array:
                    s0_nodes.append(child_node)
        
        t_states = {'q0': s0}
        d_states = [s0]
        d_states_array = [s0]
        state_counter = 1

        transitions_stack = {}
        states_stack = set()
        states_stack.update({'q0'})
        final_states_stack = set()
        
        if '#' in sigma:
            sigma.remove('#')
        
        while len(d_states) > 0:
            s = d_states.pop()
            for symbol in sigma:
                u = set()
                for p in s:
                    for child_node in s0_children_nodes:
                        if child_node.id == p and child_node.value == symbol:
                            u.update(child_node.followpos)
                if u not in d_states_array and u != set():
                    d_states_array.append(u)
                    d_states.append(u)
                    t_states['q'+str(state_counter)] = u
                    states_stack.update({'q'+str(state_counter)})
                    state_counter += 1
                    
                s_key = ''
                for key, value in t_states.items():
                    if value == s:
                        s_key = key

                u_key = ''
                for key, value in t_states.items():
                    if value == u:
                        u_key = key
                        
                new_transitions = {
                    s_key: {
                        symbol : u_key
                    }
                }
                if u_key != '':
                    if transitions_stack.get(s_key) == None:
                        transitions_stack.update(new_transitions)
                    else:
                        transitions_stack.get(s_key)[symbol] = u_key
    
        # final_state_id = {root.right.id}
        # print("FINALSTATES", self.final_states)
        # print("DSTATES", t_states.items())
    
                    
        for u in d_states_array:
            for final_state in self.final_states:
                if final_state in u:
                    for key, value in t_states.items():
                        if value == u:
                            final_states_stack.update({key})
        
        automata = DFA(states_stack, sigma, transitions_stack, 'q0', final_states_stack)
        automata.view("DFA DIRECT - YALEX")
        
        return (states_stack, sigma, transitions_stack, 'q0', final_states_stack, t_states, self.final_states)
            
            

        
