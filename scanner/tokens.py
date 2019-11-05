from enum import Enum


class Tokens(Enum):
    FLOATDCL = "f"
    INTDCL = "i"
    PRINT = "p"
    ID = r"[a-e|g-h|j-o|q-z]"
    ASSIGN = "="
    PLUS = r"\+"
    MINUS = "-"
    INUM = "[0-9]+"
    FNUM = r"[0-9]+\.[0-9]+"
    BLANK = "[ ]+"
    END = r"\$"


class Token:
    def __init__(self, type_: Tokens, context: dict):
        self.type = type_
        self.context = context
