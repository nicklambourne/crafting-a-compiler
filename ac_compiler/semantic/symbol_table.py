from enum import Enum
from typing import Dict
from ..util import SymbolError


class DataType(Enum):
    """
    The possible data types for the ac language.
    """
    INT = int
    FLOAT = float


class SymbolTable:
    """
    Collection mapping symbols (variable names) to DataTypes.
    Valid symbols are the lowercase letters excluding {f, i, p}.
    """
    def __init__(self):
        self.symbols: Dict[str, DataType] = dict()

    def lookup(self, name: str) -> DataType:
        """
        Get the DataType assigned to the provided variable name.
        :param name: the symbol to lookup
        :return: the DataType associated with that symbol
        """
        value = self.symbols.get(name, None)
        if value:
            return value
        else:
            raise SymbolError(f"No symbol found matching {name}")

    def enter(self, name: str, type_: DataType):
        """
        Add the new symbol identified by name to the symbol table with the given DataType.
        :param name: the name identifying the new symbol (unused symbol from the set of capital
                     letters excluding f, i & p)
        :param type_: the DataType to assign
        :return:
        """
        if self.symbols.get(name, None) is None:
            self.symbols[name] = type_
        else:
            raise SymbolError(f"Duplicate declaration of symbol {name}")

    def __repr__(self):
        return f"<Symbol Table: {len(self.symbols.keys())} entries>"

    def __str__(self):
        entries = "\n".join([f"{str(key)} {str(value)}" for key, value in self.symbols.items()])
        return f"<Symbol Table:\n{entries}>"