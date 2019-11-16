from __future__ import annotations
from typing import List, Union, Optional
from ..scanner import Tokens


class Node:
    """
    A node for populating an AST.
    """

    def __init__(self, parent: Optional[Node],
                 type_: Optional[Tokens] = None,
                 value: Optional[Union[str, float, int]] = None):
        self.parent = parent
        self.children = list()
        self.type = type_
        self.value = value
        self.datatype = None

    def add_child(self,
                  type_: Optional[Tokens] = None,
                  value: Optional[Union[str, float, int]] = None):
        child = Node(self, type_, value)
        self.children.append(child)
        return child

    def add_child_node(self, node: Node):
        node.parent = self
        self.children.append(node)

    def get_children(self) -> List[Node]:
        return self.children

    def get(self, index: int) -> Node:
        if index < len(self.children):
            return self.children[index]
        else:
            raise IndexError(f"Index {index} not available in {len(self.children)} "
                             f"children")

    def left(self) -> Node:
        if len(self.children) == 2:
            return self.children[0]
        else:
            raise IndexError(f"Could not get left with {len(self.children)} children")

    def right(self) -> Node:
        if len(self.children) == 2:
            return self.children[1]
        else:
            raise IndexError(f"Could not get left with {len(self.children)} children")

    def __repr__(self):
        if self.children:
            children = " - " + ", ".join([str(child.type) for child in self.children])
        else:
            children = ""

        type_ = self.type if self.type else Tokens.NONE
        return f"<Node {type_}{children}>"

    def __str__(self):
        return str(self.__repr__())


class AST:
    """
    An Abstract Syntax Tree (of Nodes)
    """

    def __init__(self):
        self.root = Node(None)
        self.children = self.root.children

    def children(self) -> List[Node]:
        return self.children
