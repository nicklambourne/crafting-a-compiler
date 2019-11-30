from typing import List
from ..parser.ast import AST, Node
from ..scanner.tokens import Tokens
from ..semantic import COMPUTATION_NODES, CONSTANT_NODES


class CodeGenerator:
    """
    Generates code for the dc language from an AST of the ac language.
    """
    def __init__(self, ast: AST):
        self.ast = ast
        self.generated = list()

    def visit_assignment(self, node: Node) -> None:
        """
        Visits an assignment node and emits dc code for that assignment
        :param node: the assignment node to visit and emit dc code for
        """
        self.codegen(node.right())
        self.emit("s")
        self.emit(f"{node.left().value}")  # emit ID
        self.emit("0 k")

    def visit_computation(self, node: Node) -> None:
        """
        Visits a computation node and emits dc code for that computation
        :param node: the computation node to visit and emit dc code for
        """
        self.codegen(node.left())
        self.codegen(node.right())
        self.emit("+" if node.type == Tokens.PLUS else "-")

    def visit_reference(self, node: Node) -> None:
        """
        Visits a reference node and emits the ID of that node
        :param node: the reference node to visit and emit dc code for
        """
        self.emit("l")
        self.emit(node.value)

    def visit_print(self, node: Node) -> None:
        """
        Visits a print node and emits the value of the symbol referenced in that node
        :param node: the print node to visit and emit dc code for
        """
        self.emit("l")
        self.emit(node.value)
        self.emit("p")
        self.emit("si")

    def visit_convert(self, node: Node) -> None:
        """
        Visits a convert node, emit the value of child, and emit dc code to change the
        precision level to five decimal places.
        :param node: the convert node to visit and emit dc code for
        """
        self.emit(node.child().value)
        self.emit("5 k")

    def visit_constant(self, node: Node) -> None:
        """
        Visits a constant node and emits its value in dc code.
        :param node: the constant node to visit and emit dc code for
        """
        self.emit(node.value)

    def codegen(self, node: Node) -> None:
        """
        Generates dc code by calling the relevant visitor method for the given node.
        :param node: the node to generate dc code for.
        """
        for child in node.children:
            self.codegen(child)

        if node.type == Tokens.ASSIGN:
            self.visit_assignment(node)
        elif node.type in COMPUTATION_NODES:
            self.visit_computation(node)
        elif node.type == Tokens.ID:
            self.visit_reference(node)
        elif node.type == Tokens.PRINT:
            self.visit_print(node)
        elif node.type == Tokens.CONVERT:
            self.visit_convert(node)
        elif node.type in CONSTANT_NODES:
            self.visit_constant(node)

    def emit(self, code: str) -> None:
        """
        Append generated code to the list of produced code.
        :param code: the code string to append to the list of generated code
        """
        self.generated.append(code)

    def generate(self) -> List[str]:
        """
        Generate dc code from the AST produced by the parser
        :return: the list of generated dc code statements
        """
        self.codegen(self.ast.root)
        return self.generated
