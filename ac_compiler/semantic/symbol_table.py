from enum import Enum
from typing import Dict, Union
from ..util import SymbolError


class DataType(Enum):
    INT = int
    FLOAT = float


class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, DataType] = dict()

    def lookup(self, name: str) -> DataType:
        value = self.symbols.get(name, None)
        if value:
            return value
        else:
            raise SymbolError(f"No symbol found matching {name}")

    def enter(self, name: str, type_: DataType):
        if self.symbols.get(name, None) is None:
            self.symbols[name] = type_
        else:
            raise SymbolError(f"Duplicate declaration of symbol {name}")

    def __repr__(self):
        return f"<Symbol Table: {len(self.symbols.keys())} entries>"

    def __str__(self):
        entries = "\n".join([f"{str(key)} {str(value)}" for key, value in self.symbols.items()])
        return f"<Symbol Table:\n{entries}>"