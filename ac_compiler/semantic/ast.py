from typing import List, Optional


class Node:
    """
    A node for populating an AST.
    """

    def __init__(self, parent: Optional["Node"]):
        self.parent = parent
        self.children = list()

    def add_child(self, child: "Node"):
        self.children.append(child)

    def get_children(self) -> List["Node"]:
        return self.children


class AST:
    """
    An Abstract Syntax Tree
    """

    def __init__(self):
        self.root = Node(None)
