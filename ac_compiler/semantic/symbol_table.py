from typing import Union
from ..util import SymbolError


class SymbolTable:
    def __init__(self):
        self.symbols = dict()

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
