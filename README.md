# Parsing Newick trees

The [Newick tree file format](https://en.wikipedia.org/wiki/Newick_format) represents trees in a text with nested parentheses. You can specify branch lengths and similar annotations, but here we will just assume that a tree is either a simple alpha-numeric string, which we consider a leaf, or it is a list of comma-separated trees surrounded by parentheses. Something like this:

```python
tree = '(A, (B, C))'
```

In this exercise, we will parse such trees and build a tree of them, represented with classes for leaves and inner nodes:

```python
@dataclass
class Leaf:
    """
    A leaf in a tree.

    This will just be a string for our application.
    """

    name: str


@dataclass
class Node:
    """An inner node."""

    children: list[Tree]


# A tree is either a leaf or an inner node with sub-trees
Tree = Union[Leaf, Node]
```

Dealing directly with raw text when you want to parse something is usually a bad idea. The first step you always do is that you translate the text into a list of “tokens”, i.e., a list of the meaningful parts of the string. While it isn’t completely safe, you can use this function for the exercise:

```python
import re
def tokenize(tree: str) -> list[str]:
    return re.findall(r'[()]|\w+', tree)
```

It turns the string `(A,(B,C))` into `['(', 'A', '(', 'B', 'C', ')', ')']`.

Here is the idea for parsing the tree:
1. Whenever you see a token that isn’t `)`, push it on the stack.
2. If you see a token that is neither `(` or `)` it must be a leaf, so create a leaf and push it to the stack.
3. When you see `)`, iteratively pop trees from the stack and collect them in a list. When you reach the first `(` you stop popping, you create the new tree, and you push it on the stack.

**Exercise:** Implement a Newick parser based on this idea.

**Exercise:** If you take the tree `((A,B),C,((D,E),F))`, in which order will your algorithm created `Leaf`s and `Node`s?
