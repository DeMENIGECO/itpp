from __future__ import annotations

import sys
from pathlib import Path

try:
    from .errors import IppError
    from .interpreter import Interpreter
    from .lexer import Lexer
    from .parser import Parser
    from .repl import REPL
    from .runtime import Runtime
except ImportError:  # pragma: no cover
    from errors import IppError
    from interpreter import Interpreter
    from lexer import Lexer
    from parser import Parser
    from repl import REPL
    from runtime import Runtime


def run_file(path: str) -> None:
    code = Path(path).read_text(encoding='utf-8')
    tokens = Lexer(code).tokenize()
    statements = Parser(tokens).parse()
    Interpreter(Runtime()).interpret(statements)


def main() -> None:
    if len(sys.argv) < 2:
        REPL().run()
        return
    path = sys.argv[1]
    if path == '--repl' or path == '-r':
        REPL().run()
        return
    try:
        run_file(path)
    except IppError as exc:
        print(exc)
    except Exception as exc:
        print(f"Errore di runtime: {exc}")


if __name__ == '__main__':
    main()
