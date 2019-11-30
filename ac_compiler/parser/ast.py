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
                  value: Optional[Union[str, float, int]] = None) -> Node:
        """
        Adds a child by taking a type and value and constructing a new node before adding that new
        node to the children of the current node.
        :param type_: the Tokens type of the new Node
        :param value:
        :return: the newly added child node
        """
        child = Node(self, type_, value)
        self.children.append(child)
        return child

    def add_child_node(self, node: Node) -> None:
        """
        Adds a pre-prepared node as a child of the current node.
        :param node: the node object to add to self.children
        """
        node.parent = self
        self.children.append(node)

    def get_children(self) -> List[Node]:
        """
        Convenience function for accessing the top-level children of the node.
        :return: the list of children of self
        """
        return self.children

    def get(self, index: int) -> Node:
        """
        Gets the child node indicated by index
        :param index: the index of the child node to get
        :return: the child node instance at the specified index
        """
        if index < len(self.children):
            return self.children[index]
        else:
            raise IndexError(f"Index {index} not available in {len(self.children)} "
                             f"children")

    def left(self) -> Node:
        """
        Returns the left (first) child of a node with two children.
        N.B. Will error if the given node does not have two children exactly.
        :return: the left child node
        """
        if len(self.children) == 2:
            return self.children[0]
        else:
            raise IndexError(f"Could not get left with {len(self.children)} children")

    def right(self) -> Node:
        """
        Returns the right (second) child of a node with two children.
        N.B. Will error if the given node does not have two children exactly.
        :return: the right child node
        """
        if len(self.children) == 2:
            return self.children[1]
        else:
            raise IndexError(f"Could not get left with {len(self.children)} children")

    def child(self) -> Node:
        """
        Returns the only child of a node with two children.
        N.B. Will error if the given node does not have one child exactly.
        :return: the only child node
        """
        if len(self.children) == 1:
            return self.children[0]
        else:
            raise IndexError(f"Could not get child with {len(self.children)} children")

    def __repr__(self) -> str:
        if self.children:
            children = " - " + ", ".join([str(child.type) for child in self.children])
        else:
            children = ""

        type_ = self.type if self.type else Tokens.NONE
        return f"<Node {type_}{children}>"

    def __str__(self) -> str:
        return str(self.__repr__())


class AST:
    """
    An Abstract Syntax Tree (of Nodes)
    """
    def __init__(self):
        self.root = Node(None)
        self.children = self.root.children

    def children(self) -> List[Node]:
        """
        Convenience function for accessing the top-level children of the node.
        :return: the list of children of the root node
        """
        return self.children
