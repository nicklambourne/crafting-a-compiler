from string import ascii_lowercase
from ..scanner import Tokens
from ..parser import AST
from ..util import SymbolError
from .symbol_table import SymbolTable


class SemanticAnalyser:
    def __init__(self, ast: AST):
        self.ast = ast
        self.symbol_table = SymbolTable()

    def populate_symbol_table(self) -> SymbolTable:
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
                    symbol_table.enter(top.value.value, float)
                if top.type == Tokens.INTDCL:
                    symbol_table.enter(top.value.value, int)
            elif top.type == Tokens.ID:
                _ = symbol_table.lookup(top.value)  # Value unused here (more checks to come)

        return symbol_table
