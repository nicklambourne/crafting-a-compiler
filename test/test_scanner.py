from ac_compiler.scanner.scanner import Scanner


def test_scan():
    scanner = Scanner("sample.ac")
    print(scanner)
