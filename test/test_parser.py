from ac_compiler.parser import Parser
from ac_compiler.scanner import Scanner


def test_parser():
    scanner = Scanner("sample.ac")
    parser = Parser(scanner.tokens)
    parser.parse()
    print(parser)
