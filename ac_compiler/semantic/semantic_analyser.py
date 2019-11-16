from string import ascii_lowercase
from ..scanner import Tokens
from ..parser import AST, Node
from ..util import SymbolError, SemanticError
from .symbol_table import SymbolTable, DataType


class SemanticAnalyser:
    def __init__(self, ast: AST):
        self.ast = ast
        self.symbol_table = SymbolTable()

    def populate_symbol_table(self) -> SymbolTable:
        """
        Traverses through the AST and populates the symbol table, checking for double
        assignment and
        :return: the populated symbol table
        """
        symbol_table = self.symbol_table
        stack = list()
        stack.append(self.ast.root)
        while stack:
            top = stack.pop(0)
            stack.extend(top.children)
            if top.type in [Tokens.FLOATDCL, Tokens.INTDCL]:
                if len(top.value.value) != 1 or top.value.value not in ascii_lowercase:
                    raise SymbolError(f"{top.value} is an invalid identifier.")
                if top.type == Tokens.FLOATDCL:
                    symbol_table.enter(top.value.value, DataType.FLOAT)
                if top.type == Tokens.INTDCL:
                    symbol_table.enter(top.value.value, DataType.INT)
            elif top.type == Tokens.ID:
                _ = symbol_table.lookup(top.value)  # Value unused here (more checks to come)

        return symbol_table

    @staticmethod
    def consistent(node1: Node, node2: Node) -> DataType:
        new_type = SemanticAnalyser.generalise(node1.datatype, node2.datatype)
        SemanticAnalyser.convert(node1, new_type)
        SemanticAnalyser.convert(node2, new_type)
        return new_type

    @staticmethod
    def generalise(type1: DataType,
                   type2: DataType) -> DataType:
        if type1 == DataType.FLOAT or type2 == DataType.FLOAT:
            return DataType.FLOAT
        return DataType.INT

    @staticmethod
    def convert(node: Node, type_: DataType):
        if node.datatype == DataType.FLOAT and type_ == DataType.INT:
            raise SemanticError("Illegal type conversion")
        elif node.datatype == DataType.INT and type_ == DataType.FLOAT:
            node.type = Tokens.FNUM
            node.datatype = type_
            node.value = float(node.value)

    @staticmethod
    def visit_computation(node: Node):
        node.datatype = SemanticAnalyser.consistent(node.left(), node.right())

    @staticmethod
    def visit_assignment(node: Node):
        node.datatype = SemanticAnalyser.convert(node.right(), node.left().datatype)

    def visit_reference(self, node: Node):
        node.datatype = self.symbol_table.lookup(node.value)

    @staticmethod
    def visit_constant(node: Node):
        if node.type == Tokens.FNUM:
            node.datatype = DataType.FLOAT
        elif node.type == Tokens.INUM:
            node.datatype = DataType.INT
        else:
            raise SemanticError("Non-constant node type")
