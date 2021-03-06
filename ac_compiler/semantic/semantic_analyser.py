from string import ascii_lowercase
from ..scanner import Tokens
from ..parser import AST, Node
from ..util import SymbolError, SemanticError
from .symbol_table import SymbolTable, DataType


COMPUTATION_NODES = [Tokens.PLUS, Tokens.MINUS]
CONSTANT_NODES = [Tokens.INUM, Tokens.FNUM]


class SemanticAnalyser:
    """
    Performs semantic (meaning) analysis on an ac program.
    Focuses (at present) on correct variable symbol usage (initialisation, reference etc.)
    """
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
        """
        Determines the most general type applicable to two nodes and ensures
        (through destructive change) that the types of both are consistent with
        one another.
        :param node1: the first node to make consistent
        :param node2: the second node to make consistent
        :return: the new (consistent) datatype the nodes now share
        """
        new_type = SemanticAnalyser.generalise(node1.datatype, node2.datatype)
        SemanticAnalyser.convert(node1, new_type)
        SemanticAnalyser.convert(node2, new_type)
        return new_type

    @staticmethod
    def generalise(type1: DataType,
                   type2: DataType) -> DataType:
        """
        Finds the most general datatype applicable to two nodes (i.e. float unless both are
        integers).
        :param type1: the first type
        :param type2: the second type
        :return: the newly found (most general) type
        """
        if type1 == DataType.FLOAT or type2 == DataType.FLOAT:
            return DataType.FLOAT
        return DataType.INT

    @staticmethod
    def convert(node: Node, type_: DataType) -> DataType:
        """
        Converts a single node to the given DataType.
        :param node: the node to convert
        :param type_: the type to convert the node to
        """
        if node.datatype == DataType.FLOAT and type_ == DataType.INT:
            raise SemanticError("Illegal type conversion")
        elif node.datatype == DataType.INT and type_ == DataType.FLOAT:
            node.type = Tokens.FNUM
            node.datatype = type_
            # node.value = float(node.value)
            return type_

    @staticmethod
    def visit_computation(node: Node) -> None:
        """
        Visits a computation node and sets its DataType to the consistent type derived from its
        two children.
        :param node: the computation node to visit
        """
        node.datatype = SemanticAnalyser.consistent(node.left(), node.right())

    @staticmethod
    def visit_assignment(node: Node) -> None:
        """
        Visits an assignment node and sets its datatype to the type of the value node being
        assigned.
        :param node: the assignment node to visit
        """
        node.datatype = SemanticAnalyser.convert(node.right(), node.left().datatype)

    @staticmethod
    def visit_reference(symbol_table: SymbolTable, node: Node) -> None:
        """
        Visits a reference node and sets its datatype to the type of the variable as listed in
        the symbol table.
        :param symbol_table: the table to refer to for lookup
        :param node: the reference node to visit
        """
        node.datatype = symbol_table.lookup(node.value)

    @staticmethod
    def visit_constant(node: Node) -> None:
        """
        Visits a constant node and sets its datatype to the relevant type for the Token (i.e.
        FLOAT for FNUM and INT for INUM).
        :param node: the constant node to visit
        """
        if node.type == Tokens.FNUM:
            node.datatype = DataType.FLOAT
        elif node.type == Tokens.INUM:
            node.datatype = DataType.INT
        else:
            raise SemanticError("Non-constant node type")

    def analyse(self) -> None:
        """
        Analyses the whole tree by calling analyse_node on the root of the AST.
        """
        self.analyse_node(self.ast.root)

    def analyse_node(self, node: Node) -> None:
        """
        Uses a stack-based approach to visit all the children of a node in post-order.
        :param node: the node to begin analysis from
        """
        children = node.get_children()
        for child in children:
            self.analyse_node(child)

        if node.type in COMPUTATION_NODES:
            SemanticAnalyser.visit_computation(node)
        elif node.type == Tokens.ASSIGN:
            SemanticAnalyser.visit_assignment(node)
        elif node.type in CONSTANT_NODES:
            SemanticAnalyser.visit_constant(node)
        elif node.type == Tokens.ID:
            SemanticAnalyser.visit_reference(self.symbol_table, node)
