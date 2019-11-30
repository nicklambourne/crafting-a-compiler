from ..parser.ast import Node


class CodeGenerator:
    """
    Generates code for the dc language from an AST of the ac language.
    """
    def __init__(self):
        self.stack = list()
        self.register = dict()
        self.precision = 0

    def visit_assignment(self, node: Node):
        self.codegen(node.right())
        self.emit("s")
        self.emit(f"{node.left().value}")  # emit ID
        self.emit("0 k")

    def visit_computation(self, node: Node):
        self.codegen(node.left())
        self.codegen(node.right())
        self.emit(node.value)

    def visit_reference(self):
        pass

    def visit_print(self):
        pass

    def visit_convert(self):
        pass

    def visit_constant(self):
        pass

    def codegen(self, node: Node):
        pass

    def emit(self, code: str):
        pass

