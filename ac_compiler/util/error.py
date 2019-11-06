

class Error(Exception):
    """Base error class for the compiler"""
    pass


class LexicalError(Error):
    """Error raised when scanning tokens fails"""
    pass


class SyntaxParsingError(Error):
    """Error raised when parsing token stream fails"""
    pass
