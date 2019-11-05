from typing import List
from re import match
from .tokens import Token, Tokens


class Scanner:
    def __init__(self, file: str):
        self.file = file
        self.tokens = list()

    def scan(self) -> List[Token]:
        with open(self.file, "r") as file:
            contents = file.read()
            length = len(contents)
            index = 0
            while index < length:
                while match(Tokens.BLANK.value, contents[index]):
                    index += 1
                if index == length:
                    self.tokens.append(Tokens.END)

