from ac_compiler.parser import Parser
from ac_compiler.scanner import Scanner
from ac_compiler.semantic import SemanticAnalyser
from ac_compiler.generator import CodeGenerator


def test_semantic():
    scanner = Scanner("sample.ac")
    parser = Parser(scanner.tokens)
    parser.parse()
    analyser = SemanticAnalyser(ast=parser.ast)
    analyser.populate_symbol_table()
    print(analyser.symbol_table)
    analyser.analyse()
    generator = CodeGenerator(ast=analyser.ast)
    _ = generator.generate()
