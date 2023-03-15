from utils import *
from ExpressionTree.Node import *

class ExpressionTree:
    def __init__(self, postfix):
        self.root = None
        self.postfix = postfix
    
    def build_tree(self):
        nodes = []
        node_id = 1
        for symbol in self.postfix:
            isOperator = symbol == '*' or symbol == '|' or symbol == '.'
            if not isOperator:
                nodes.append(Node(node_id, symbol))
            else:
                if symbol == '*':
                    right = None
                else:
                    right = nodes.pop()
                left = nodes.pop()
                new_node = Node(node_id, symbol, left, right)
                nodes.append(new_node)
            node_id += 1
        root = nodes.pop()
        self.root = root
        return self.root
    
    # A function to do inorder tree traversal
    def print_inorder(self, root):
    
        if root:
            # First recursive on left child
            self.print_inorder(root.left)
    
            # then print the data of node
            print(root.value),
    
            # now recursive on right child
            self.print_inorder(root.right)
        
    