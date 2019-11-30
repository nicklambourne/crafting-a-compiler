from ..parser.ast import AST, Node
from ..scanner.tokens import Tokens
from ..semantic import COMPUTATION_NODES, CONSTANT_NODES


class CodeGenerator:
    """
    Generates code for the dc language from an AST of the ac language.
    """
    def __init__(self):
        self.generated = list()

    def visit_assignment(self, node: Node) -> None:
        self.codegen(node.right())
        self.emit("s")
        self.emit(f"{node.left().value}")  # emit ID
        self.emit("0 k")

    def visit_computation(self, node: Node) -> None:
        self.codegen(node.left())
        self.codegen(node.right())
        self.emit("+" if node.type == Tokens.PLUS else "-")

    def visit_reference(self, node: Node) -> None:
        self.emit("l")
        self.emit(node.value)

    def visit_print(self, node: Node) -> None:
        self.emit("l")
        self.emit(node.value)
        self.emit("p")
        self.emit("si")

    def visit_convert(self, node: Node) -> None:
        self.emit(node.child().value)
        self.emit("5 k")

    def visit_constant(self, node: Node) -> None:
        self.emit(node.value)

    def codegen(self, node: Node):
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
        self.generated.append(code)

    def generate(self, ast: AST) -> None:
        self.codegen(ast.root)
