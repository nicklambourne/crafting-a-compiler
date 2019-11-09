from typing import List, Union
from ..scanner.tokens import Token, Tokens


class Error(Exception):
    """Base error class for the compiler"""
    pass


class LexicalError(Error):
    """Error raised when scanning tokens fails"""
    pass


class SyntaxParsingError(Error):
    """Error raised when parsing token stream fails"""
    def __init__(self,
                 expected: Union[Tokens, List[Tokens]] = None,
                 actual: Token = None,
                 message: str = None):
        if message:
            super().__init__(message)
        elif expected and actual:
            if type(expected) == list:
                expected_value = f"{', '.join([expected_.name for expected_ in expected])}"
            else:
                expected_value = expected.name
            super().__init__(f"Expected {expected_value}, "
                             f"Got: {actual.type.name} ({actual.value})")
        else:
            super().__init__()


class SymbolError(Error):
    def __init__(self, message: str):
        super().__init__(message)
