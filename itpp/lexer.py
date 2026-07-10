from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    value: object
    line: int


class Lexer:
    KEYWORDS = {
        'stampa': 'STAMPA',
        'mostra': 'STAMPA',
        'sia': 'SIA',
        'uguale': 'UGUALE',
        'a': 'A',
        'se': 'SE',
        'allora': 'ALLORA',
        'altrimenti': 'ALTRIMENTI',
        'fine': 'FINE',
        'ripeti': 'RIPETI',
        'volte': 'VOLTE',
        'finché': 'MENTRE',
        'è': 'È',
        'maggiore': 'MAGGIORE',
        'minore': 'MINORE',
        'diverso': 'DIVERSO',
        'da': 'DA',
        'almeno': 'ALMENO',
        'al massimo': 'ALMASSIMO',
        'per': 'PER',
        'ogni': 'OGNI',
        'elemento': 'ELEMENTO',
        'in': 'IN',
        'aggiungi': 'AGGIUNGI',
        'rimuovi': 'RIMUOVI',
        'lunghezza': 'LUNGHEZZA',
        'definisci': 'DEFINISCI',
        'funzione': 'FUNZIONE',
        'chiama': 'CHIAMA',
        'con': 'CON',
        'parametro': 'PARAMETRO',
        'parametri': 'PARAMETRO',
        'restituisci': 'RESTITUISCI',
        'chiedi': 'CHIEDI',
        'salva': 'SALVA',
        'vero': 'BOOLEAN',
        'falso': 'BOOLEAN',
        'nullo': 'NULLO',
        'più': 'PIU',
        'meno': 'MENO',
        'diviso': 'DIVISO',
        'modulo': 'MODULO',
        'e': 'E',
        'oppure': 'OPPURE',
        'non': 'NON',
        'di': 'DI',
    }

    PHRASES = sorted(KEYWORDS.keys(), key=len, reverse=True)

    def __init__(self, text: str):
        self.text = text
        self.tokens: List[Token] = []
        self.pos = 0
        self.line = 1

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if ch.isspace():
                if ch == '\n':
                    self.line += 1
                self.pos += 1
                continue
            if ch == '#':
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1
                continue
            if ch == '/' and self.pos + 1 < len(self.text) and self.text[self.pos + 1] == '/':
                while self.pos < len(self.text) and self.text[self.pos] != '\n':
                    self.pos += 1
                continue
            if ch in '(),[]:':
                self.tokens.append(Token(ch, ch, self.line))
                self.pos += 1
                continue
            if ch in '+-*/%':
                self.tokens.append(Token(ch, ch, self.line))
                self.pos += 1
                continue
            if ch in '"\'':
                self.tokens.append(self._read_string())
                continue
            if ch.isdigit() or (ch == '.' and self.pos + 1 < len(self.text) and self.text[self.pos + 1].isdigit()):
                self.tokens.append(self._read_number())
                continue
            if ch.isalpha() or ch == 'è':
                self.tokens.append(self._read_word())
                continue
            raise ValueError(f"Carattere non previsto: {ch} alla riga {self.line}")
        self.tokens.append(Token('EOF', None, self.line))
        return self.tokens

    def _read_string(self) -> Token:
        quote = self.text[self.pos]
        self.pos += 1
        value_chars = []
        while self.pos < len(self.text) and self.text[self.pos] != quote:
            value_chars.append(self.text[self.pos])
            self.pos += 1
        self.pos += 1
        return Token('STRING', ''.join(value_chars), self.line)

    def _read_number(self) -> Token:
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == '.'):
            self.pos += 1
        value = self.text[start:self.pos]
        if '.' in value:
            return Token('NUMBER', float(value), self.line)
        return Token('NUMBER', int(value), self.line)

    def _read_word(self) -> Token:
        for phrase in self.PHRASES:
            if self.text[self.pos:self.pos + len(phrase)].lower() == phrase:
                next_char = self.text[self.pos + len(phrase):self.pos + len(phrase) + 1]
                if next_char.isalnum() or next_char in 'èàùìò':
                    continue
                self.pos += len(phrase)
                return Token(self.KEYWORDS[phrase], phrase, self.line)
        start = self.pos
        while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] in 'èàùìò'):
            self.pos += 1
        word = self.text[start:self.pos].lower()
        if word in self.KEYWORDS:
            return Token(self.KEYWORDS[word], word, self.line)
        return Token('IDENT', word, self.line)
