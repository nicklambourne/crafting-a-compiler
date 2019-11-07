from typing import List, Optional
from ..scanner import Token, Tokens
from ..util import SyntaxParsingError


class Parser:
    """
    Recursive-descent parser based on the grammar for the ac language.
    """

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
        self.parse_program()

    def expect(self, expected: Tokens):
        token = self.advance()
        if token.type == expected:
            pass
        else:
            raise SyntaxParsingError(expected, token)

    def parse_program(self):
        expected = [Tokens.FLOATDCL, Tokens.INTDCL, Tokens.ID, Tokens.PRINT,
                    Tokens.END]
        if self.peek() in expected:
            self.parse_declarations()
            self.parse_statements()
            self.expect(Tokens.END)
        else:
            raise SyntaxParsingError(expected, self.peek())

    def parse_declarations(self):
        expected_declarations = [Tokens.FLOATDCL, Tokens.INTDCL]
        expected_lambdas = [Tokens.ID, Tokens.PRINT, Tokens.END]
        union_expected = expected_declarations + expected_lambdas

        if self.peek() not in union_expected:
            raise SyntaxParsingError(union_expected, self.peek())

        if self.peek() in expected_declarations:
            self.parse_declaration()
            self.parse_declarations()
        elif self.peek() in expected_lambdas:
            pass

    def parse_declaration(self):
        if self.peek() == Tokens.FLOATDCL:
            self.expect(Tokens.FLOATDCL)
            self.expect(Tokens.ID)
        elif self.peek() == Tokens.INTDCL:
            self.expect(Tokens.INTDCL)
            self.expect(Tokens.ID)
        else:
            raise SyntaxParsingError([Tokens.FLOATDCL, Tokens.INTDCL],
                                     self.peek())

    def parse_statements(self):
        if self.peek() == Tokens.ID or self.peek() == Tokens.PRINT:
            self.parse_statement()
            self.parse_statements()
        elif self.peek() == Tokens.END:
            pass
        else:
            raise SyntaxParsingError

    def parse_statement(self):
        if self.peek().type == Tokens.ID:
            self.expect(Tokens.ID)
            self.expect(Tokens.ASSIGN)
            self.parse_value()
            self.parse_expression()
        elif self.peek().type == Tokens.PRINT:
            self.expect(Tokens.PRINT)
            self.expect(Tokens.ID)
        else:
            raise SyntaxParsingError

    def parse_value(self):
        if self.peek() == Tokens.ID:
            self.expect(Tokens.ID)
        elif self.peek() == Tokens.INUM:
            self.expect(Tokens.INUM)
        elif self.peek() == Tokens.FNUM:
            self.expect(Tokens.FNUM)
        else:
            raise SyntaxParsingError([Tokens.ID, Tokens.FNUM, Tokens.INUM],
                                     self.peek())

    def parse_expression(self):
        if self.peek() == Tokens.PLUS:
            self.expect(Tokens.PLUS)
            self.parse_value()
            self.parse_expression()
        elif self.peek() == Tokens.MINUS:
            self.expect(Tokens.MINUS)
            self.parse_value()
            self.parse_expression()
        elif self.peek() in [Tokens.ID, Tokens.PRINT, Tokens.END]:
            pass
        else:
            raise SyntaxParsingError([Tokens.PLUS, Tokens.MINUS, Tokens.ID,
                                      Tokens.PRINT, Tokens.END],
                                     self.peek())
