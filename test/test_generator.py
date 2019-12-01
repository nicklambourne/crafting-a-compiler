from ac_compiler.parser import Parser
from ac_compiler.scanner import Scanner
from ac_compiler.semantic import SemanticAnalyser
from ac_compiler.generator import CodeGenerator


def test_generator():
    scanner = Scanner("sample.ac")
    parser = Parser(scanner.tokens)
    parser.parse()
    analyser = SemanticAnalyser(ast=parser.ast)
    analyser.populate_symbol_table()
    print(str(analyser.symbol_table) + "\n")
    analyser.analyse()
    generator = CodeGenerator(ast=analyser.ast)
    dc_code = generator.generate()
    for statement in dc_code:
        print(statement)
