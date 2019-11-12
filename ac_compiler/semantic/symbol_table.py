from typing import Dict, Union
from ..util import SymbolError


class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Union[int, float]] = dict()

    def lookup(self, name: str) -> Union[int, float]:
        value = self.symbols.get(name, None)
        if value:
            return value
        else:
            raise SymbolError(f"No symbol found matching {name}")

    def enter(self, name: str, type_: Union[int, float]):
        if self.symbols.get(name, None) is None:
            self.symbols[name] = type_
        else:
            raise SymbolError(f"Duplicate declaration of symbol {name}")

    def __repr__(self):
        return f"<Symbol Table: {len(self.symbols.keys())} entries>"

    def __str__(self):
        entries = "\n".join([str(key) + str(value) for key, value in self.symbols.items()])
        return f"<Symbol Table:\n{entries}>"