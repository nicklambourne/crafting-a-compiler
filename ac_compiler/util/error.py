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
                expected_value = f"{', '.join([expected_.type for expected_ in expected])}"
            else:
                expected_value = expected.type
            super().__init__(f"Expected {expected_value}, Got: {actual.type}")
        else:
            super().__init__()
