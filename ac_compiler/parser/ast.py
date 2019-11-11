from typing import List, Union, Optional
from ..scanner import Tokens


class Node:
    """
    A node for populating an AST.
    """

    def __init__(self, parent: Optional["Node"],
                 type_: Optional[Tokens] = None,
                 value: Optional[Union[str, float, int]] = None):
        self.parent = parent
        self.children = list()
        self.type = type_
        self.value = value

    def add_child(self,
                  type_: Optional[Tokens] = None,
                  value: Optional[Union[str, float, int]] = None):
        child = Node(self.parent, type_, value)
        self.children.append(child)
        return child

    def add_child_node(self,
                       node: "Node"):
        self.children.append(node)

    def get_children(self) -> List["Node"]:
        return self.children

    def get(self, index: int) -> "Node":
        if index < len(self.children):
            return self.children[index]
        else:
            raise IndexError(f"Index {index} not available in {len(self.children)} "
                             f"children")

    def __str__(self):
        return f"<Node {', '.join([child.type for child in self.children])}>"


class AST:
    """
    An Abstract Syntax Tree
    """

    def __init__(self):
        self.root = Node(None)
