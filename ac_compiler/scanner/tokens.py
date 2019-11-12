from enum import Enum
from typing import Optional, Union


class Tokens(Enum):
    """
    The various terminal values that comprise the ac language, mapped to the
    regex pattern that identifies them.
    """
    FLOATDCL = "f"
    INTDCL = "i"
    PRINT = "p"
    ID = r"[a-e|g-h|j-o|q-z]"
    ASSIGN = "="
    PLUS = r"\+"
    MINUS = "-"
    INUM = "[0-9]+"
    FNUM = r"[0-9]+\.[0-9]+"
    BLANK = r" +"
    END = r"\$"
    NONE = ""


class Token:
    """
    A common token for the ac language, consisting of a type (see Tokens) and a value
    where appropriate (e.g. integer value for an INUM token).
    """
    def __init__(self, type_: Tokens, value: Optional[Union[int, float, str]] = None):
        self.type = type_
        self.value = value

    def __str__(self) -> str:
        return f"<{self.type.name}: {self.value}>"
