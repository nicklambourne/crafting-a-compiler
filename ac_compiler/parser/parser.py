from typing import List, Optional
from ..scanner import Token, Tokens
from ..util import SyntaxParsingError


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0
        self.length = len(tokens)

    def peek(self) -> Optional[Token]:
        if self.index < self.length:
            return self.tokens[self.index]
        else:
            return None

    def advance(self) -> Optional[Token]:
        if self.index < self.length:
            self.index += 1
            return self.tokens[self.index]
        else:
            return None

    def parse(self):
        pass

    def match(self, type_: Tokens):
        pass

    def parse_value(self):
        pass

    def parse_expression(self):
        pass

    def parse_statement(self):
        if self.peek().type == Tokens.ID:
            self.match(Tokens.ID)
            self.match(Tokens.ASSIGN)
            self.parse_value()
            self.parse_expression()
        elif self.peek().type == Tokens.PRINT:
            self.match(Tokens.PRINT)
            self.match(Tokens.ID)
        else:
            raise SyntaxParsingError

    def parse_statements(self):
        if self.peek() == Tokens.ID or self.peek() == Tokens.PRINT:
            self.parse_statement()
            self.parse_statements()
        elif self.peek() == Tokens.END:
            pass
        else:
            raise SyntaxParsingError

