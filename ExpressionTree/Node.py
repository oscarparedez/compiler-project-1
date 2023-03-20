from utils import *

class Node:
    def __init__(self, id, value, left=None, right=None):
        self.id = id
        self.value = value
        self.right = right
        self.left = left
        self.operator = value == '*' or value == '|' or value == '.'
        self.nullability = None
        self.firstpos = None
        self.lastpos = None
        self.followpos = set()