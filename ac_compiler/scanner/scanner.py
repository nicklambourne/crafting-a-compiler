from typing import List, Optional, Tuple
from re import match
from .tokens import Token, Tokens
from ..util.error import LexicalError


class Scanner:
    def __init__(self, file: str):
        self.file = file
        self.index = 0

        with open(self.file, "r") as file:
            self.content = file.read()
            self.length = len(self.content)

        self.tokens = self.scan()

    def scan(self) -> List[Token]:
        tokens = list()

        while self.index < self.length:
            token, index = self.match_token()
            tokens.append(token)
            index += 1
            print(self.content[self.index])
            print(token)

        return tokens

    def match_token(self) -> Tuple[Optional[Token], int]:
        while match(Tokens.BLANK.value, self.content[self.index]):
            self.index += 1

        if match(r"[0-9]", self.content[self.index]):
            return self.scan_digits()

        if self.index == self.length:
            return Token(Tokens.End), self.index

        for token in Tokens:
            print(token)
            if match(token.value, self.content[self.index]):
                if token == Tokens.ID:
                    return Token(Tokens.ID, self.content[self.index]), self.index

        raise LexicalError

    def scan_digits(self) -> Tuple[Token, int]:
        value = ""
        while self.index < self.length and match(r"[0-9]", self.content[self.index]):
            value += self.content[self.index]
            self.index += 1

        if self.index < self.length and self.content[self.index] != ".":
            type_ = Tokens.INUM
            value = int(value)
        else:
            type_ = Tokens.FNUM
            value += self.content[self.index]
            while self.index < self.length and match(r"[0-9]", self.content[self.index]):
                value += self.content[self.index]
                self.index += 1
            value = float(value)
        return Token(type_, value), self.index
