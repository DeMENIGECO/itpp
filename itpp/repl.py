from __future__ import annotations

import os
from typing import List

try:
    import readline  # type: ignore
except ImportError:  # pragma: no cover
    readline = None

from .errors import IppError
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser
from .runtime import Runtime


class REPL:
    def __init__(self):
        self.runtime = Runtime()
        self.interpreter = Interpreter(self.runtime)
        self.history: List[str] = []
        self._history_file = os.path.expanduser('~/.itpp_history')
        self._load_history()

    def _load_history(self) -> None:
        if readline is None:
            return
        try:
            readline.read_history_file(self._history_file)
        except FileNotFoundError:
            return

    def _save_history(self) -> None:
        if readline is None:
            return
        try:
            readline.write_history_file(self._history_file)
        except OSError:
            pass

    def _read_multiline(self) -> str:
        first = input('>> ').rstrip('\n')
        if first.strip().lower() == 'esci':
            return 'esci'
        lines = [first]
        if self._should_continue(lines):
            while True:
                next_line = input('... ').rstrip('\n')
                if next_line.strip().lower() == 'esci':
                    return 'esci'
                lines.append(next_line)
                if not self._should_continue(lines):
                    break
        return '\n'.join(lines)

    def _should_continue(self, lines: List[str]) -> bool:
        text = '\n'.join(line.strip() for line in lines if line.strip())
        if not text:
            return False
        lower = text.lower()
        if any(lower.startswith(prefix) for prefix in ['se ', 'ripeti ', 'finché ', 'definisci ', 'per ogni ']):
            return 'fine' not in lower
        return False

    def run(self) -> None:
        print("I++ 1.0")
        print('Scrivi "esci" per terminare.')
        while True:
            try:
                command = self._read_multiline()
            except EOFError:
                print('Arrivederci.')
                self._save_history()
                break
            if command.strip().lower() == 'esci':
                print('Arrivederci.')
                self._save_history()
                break
            self.history.append(command)
            if readline is not None:
                readline.add_history(command)
            try:
                tokens = Lexer(command).tokenize()
                statements = Parser(tokens).parse()
                self.interpreter.interpret(statements)
            except IppError as exc:
                print(exc)
            except Exception as exc:
                print(f"Errore di runtime: {exc}")
