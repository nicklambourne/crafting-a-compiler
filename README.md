# Crafting a Compiler

This repository contains my work produced following along with the 2010 (language agnostic) edition of [Crafting a Compiler](https://books.google.com.au/books/about/Crafting_a_Compiler.html?id=G4Y_AQAAIAAJ&source=kp_book_description&redir_esc=y) by Fischer, Cytron & LeBlanc.

I have undertaken this work as preparation for my upcoming internship at [Canva](https://canva.com). While I would not typically use Python for a project with such potential for complexity and scope, this decision provides the best possible preparation for the work I'll undertake during my internship. It also provides the opportunity to experiment with more more sophisticated Python language features like meta-programming.

There's nothing particularly revolutionary about this code, so if anything takes your fancy feel free to use it as you please. All of the code in this repository is covered by the permissive [BSD-3 open source licence](https://opensource.org/licenses/BSD-3-Clause).

## Content

### ac (Adding Calculator) Compiler

- Scanner [[link]](./ac_compiler/scanner/scanner.py)
- Parser [[link]](./ac_compiler/parser/parser.py)
- Semantic Analysis [[link]](./ac_compiler/semantic/semantic_analyser.py)
- Code Generator (ac -> dc) [[link]](./ac_compiler/generator/generator.py)

Simple [pytest](https://docs.pytest.org/en/latest/) integration tests have been included [here](./test).

The only dependency for this project is `pytest`.
