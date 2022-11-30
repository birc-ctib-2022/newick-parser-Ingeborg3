"""A Newick parser."""

from __future__ import annotations
from dataclasses import dataclass
from typing import Union, cast
import re


def tokenize(tree: str) -> list[str]:
    """
    Extract the tokens from the text representation of a tree.

    >>> tokenize("A")
    ['A']
    >>> tokenize("(A, (B, C))")
    ['(', 'A', '(', 'B', 'C', ')', ')']
    """
    return re.findall(r'[()]|\w+', tree)


@dataclass(repr=False)
class Leaf:
    """
    A leaf in a tree.

    This will just be a string for our application.
    """

    name: str

    def __str__(self) -> str:
        """Simplified text representation."""
        return self.name
    __repr__ = __str__


@dataclass(repr=False)
class Node:
    """An inner node."""

    children: list[Tree]

    def __str__(self) -> str:
        """Simplified text representation."""
        return f"({','.join(str(child) for child in self.children)})"
    __repr__ = __str__


# A tree is either a leaf or an inner node with sub-trees
Tree = Union[Leaf, Node]

class EmptyStack(Exception):
    pass

# FIXME: hvordan tegne newick tree ((A,B), C, ((D,E), F))?

class Stack(object):
    """
    Underlying data-structure is a python list.
    """
    def __init__(self):
        self.stack = []
    
    def push(self, element):
        self.stack.append(element)
    
    def get_top_element(self):
        if len(self.stack) == 0: # could also use try-except block here as on p. 552.
            raise EmptyStack()
        return self.stack[-1]
    
    def pop(self):
        if len(self.stack) == 0:
            raise EmptyStack()
        return self.stack.pop()

    def empty(self):
        return len(self.stack) == 0

    def __bool__(self): 
        return not self.empty


def parse(tree: str) -> Tree:
    """
    Parse a string into a tree.

    >>> parse("(A, (B, C))")
    (A, (B ,C)) # A, B and C are leafs. (B,C) is a subtree. (A, (B,C)) is
    a tree.
    """
    stack = Stack()
    tokens = tokenize(tree) # list of strings. 
    for token in tokens:
        if token == ')':
            # pop until ( and make (sub)tree (by making a class call to
            # Node() and give the leaf objects in a list as argument) 
            # and push the (sub)tree back onto the top of the stack.
            stack.push(token) 
            leafs =[]
            while True:
                x = stack.pop()
                if x == '(':
                    break
                elif x != ')': # if x is a leaf-object or a subtree
                    # (Node) created in line 212. 
                    leafs.append(x)
            subtree = Node(leafs)
            stack.push(tree)

        elif token == '(':
            # push onto top of the stack.
            stack.push(token)

        else: # token is a string representation of a leaf.
            # create Leaf object. Push onto the top of the stack.
            stack.push(Leaf(token))
    return stack.get_top_element()

# How to make leaf
print(Leaf('A')) # A
# how to make node
print(Node([Leaf('B'), Leaf('C')])) # (B, C)
# how to make tree
print(Node([Leaf('A'), Node([Leaf('B'), Leaf('C')])])) # (A, (B,C))
# can also just make tree from list of strings
print(Node(['A', 'B'])) # (A, B)
