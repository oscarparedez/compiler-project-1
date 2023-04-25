from utils import *

class Node:
    def __init__(self, id, value, return_val=None, left=None, right=None):
        self.id = id
        self.value = value
        self.return_value = return_val
        self.right = right
        self.left = left
        self.operator = value == '*' or value == '|' or value == '.'
        self.nullability = None
        self.firstpos = None
        self.lastpos = None
        self.followpos = set()