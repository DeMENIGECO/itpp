from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .errors import SyntaxErrorIpp
from .lexer import Token


@dataclass
class ASTNode:
    line: int


@dataclass
class PrintNode(ASTNode):
    value: ASTNode


@dataclass
class AssignNode(ASTNode):
    name: str
    value: ASTNode


@dataclass
class VarNode(ASTNode):
    name: str


@dataclass
class LiteralNode(ASTNode):
    value: object


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode


@dataclass
class IfNode(ASTNode):
    condition: ASTNode
    then_body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)


@dataclass
class WhileNode(ASTNode):
    condition: ASTNode
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class RepeatNode(ASTNode):
    count: ASTNode
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class ForEachNode(ASTNode):
    var_name: str
    iterable: ASTNode
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class FunctionDefNode(ASTNode):
    name: str
    params: List[str]
    body: List[ASTNode] = field(default_factory=list)


@dataclass
class CallNode(ASTNode):
    name: str
    args: List[ASTNode] = field(default_factory=list)


@dataclass
class ReturnNode(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class InputNode(ASTNode):
    prompt: ASTNode
    target: str


@dataclass
class ListNode(ASTNode):
    items: List[ASTNode] = field(default_factory=list)


@dataclass
class IndexNode(ASTNode):
    target: ASTNode
    index: ASTNode


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def parse(self) -> List[ASTNode]:
        statements: List[ASTNode] = []
        while not self._match('EOF'):
            if self._peek().type in {'\n', ';'}:
                self.pos += 1
                continue
            statements.append(self._statement())
        return statements

    def _statement(self) -> ASTNode:
        token = self._peek()
        if token.type == 'STAMPA':
            self._advance()
            value = self._expression()
            return PrintNode(token.line, value)
        if token.type == 'SIA':
            return self._assignment()
        if token.type == 'SE':
            return self._if_statement()
        if token.type == 'RIPETI':
            return self._repeat_statement()
        if token.type == 'MENTRE':
            return self._while_statement()
        if token.type == 'PER':
            return self._for_each_statement()
        if token.type == 'DEFINISCI':
            return self._function_definition()
        if token.type == 'RESTITUISCI':
            self._advance()
            value = self._expression() if not self._match('EOF') and self._peek().type != 'FINE' else None
            return ReturnNode(token.line, value)
        if token.type == 'CHIEDI':
            return self._input_statement()
        if token.type == 'CHIAMA':
            return self._call_statement()
        if token.type == 'AGGIUNGI':
            return self._add_statement()
        if token.type == 'RIMUOVI':
            return self._remove_statement()
        raise SyntaxErrorIpp(f"Istruzione non riconosciuta: {token.value}", token.line)

    def _assignment(self) -> ASTNode:
        self._advance()  # sia
        name = self._expect('IDENT').value
        self._expect('UGUALE')
        self._expect('A')
        value = self._expression()
        return AssignNode(self._peek().line, name, value)

    def _if_statement(self) -> ASTNode:
        token = self._advance()
        condition = self._expression()
        self._expect('ALLORA')
        then_body: List[ASTNode] = []
        else_body: List[ASTNode] = []
        while self._peek().type not in {'FINE', 'ALTRIMENTI', 'EOF'}:
            then_body.append(self._statement())
        if self._peek().type == 'ALTRIMENTI':
            self._advance()
            while self._peek().type not in {'FINE', 'EOF'}:
                else_body.append(self._statement())
        if self._peek().type == 'FINE':
            self._advance()
        return IfNode(token.line, condition, then_body, else_body)

    def _repeat_statement(self) -> ASTNode:
        token = self._advance()
        count = self._expression()
        self._expect('VOLTE')
        body: List[ASTNode] = []
        while self._peek().type not in {'FINE', 'EOF'}:
            body.append(self._statement())
        if self._peek().type == 'FINE':
            self._advance()
        return RepeatNode(token.line, count, body)

    def _while_statement(self) -> ASTNode:
        token = self._advance()
        condition = self._expression()
        body: List[ASTNode] = []
        while self._peek().type not in {'FINE', 'EOF'}:
            body.append(self._statement())
        if self._peek().type == 'FINE':
            self._advance()
        return WhileNode(token.line, condition, body)

    def _for_each_statement(self) -> ASTNode:
        self._advance()  # per
        self._expect('OGNI')
        self._expect('ELEMENTO')
        self._expect('IN')
        iterable = self._expression()
        body: List[ASTNode] = []
        while self._peek().type not in {'FINE', 'EOF'}:
            body.append(self._statement())
        if self._peek().type == 'FINE':
            self._advance()
        return ForEachNode(self._peek().line, 'elemento', iterable, body)

    def _function_definition(self) -> ASTNode:
        self._advance()
        self._expect('FUNZIONE')
        name = self._expect('IDENT').value
        params: List[str] = []
        if self._match('CON'):
            while self._match('PARAMETRO'):
                params.append(self._expect('IDENT').value)
        body: List[ASTNode] = []
        while self._peek().type not in {'FINE', 'EOF'}:
            body.append(self._statement())
        if self._peek().type == 'FINE':
            self._advance()
        return FunctionDefNode(self._peek().line, name, params, body)

    def _input_statement(self) -> ASTNode:
        token = self._advance()
        prompt = self._expression()
        self._expect('E')
        self._expect('SALVA')
        self._expect('IN')
        target = self._expect('IDENT').value
        return InputNode(token.line, prompt, target)

    def _call_statement(self) -> ASTNode:
        token = self._advance()
        name = self._expect('IDENT').value
        self._expect('CON')
        args: List[ASTNode] = []
        if not self._match(')'):
            args.append(self._expression())
        return CallNode(token.line, name, args)

    def _add_statement(self) -> ASTNode:
        token = self._advance()
        value = self._expression()
        self._expect('A')
        target = self._expression()
        return CallNode(token.line, 'aggiungi', [value, target])

    def _remove_statement(self) -> ASTNode:
        token = self._advance()
        value = self._expression()
        self._expect('DA')
        target = self._expression()
        return CallNode(token.line, 'rimuovi', [value, target])

    def _expression(self) -> ASTNode:
        return self._comparison()

    def _comparison(self) -> ASTNode:
        node = self._additive()
        if self._peek().type == 'È':
            self._advance()
            if self._peek().type in {'MAGGIORE', 'MINORE', 'UGUALE', 'DIVERSO', 'ALMENO', 'ALMASSIMO'}:
                op = self._advance().type
                if self._peek().type in {'DI', 'DA'}:
                    self._advance()
                right = self._additive()
                return BinaryOpNode(node.line, node, op, right)
        while self._peek().type in {'MAGGIORE', 'MINORE', 'UGUALE', 'DIVERSO', 'ALMENO', 'ALMASSIMO'}:
            op = self._advance().type
            if self._peek().type in {'DI', 'DA'}:
                self._advance()
            right = self._additive()
            node = BinaryOpNode(node.line, node, op, right)
        return node

    def _additive(self) -> ASTNode:
        node = self._multiplicative()
        while self._peek().type in {'PIU', 'MENO', '+', '-'}:
            op = self._advance().type
            if op in {'+', '-'}:
                op = 'PIU' if op == '+' else 'MENO'
            right = self._multiplicative()
            node = BinaryOpNode(node.line, node, op, right)
        return node

    def _multiplicative(self) -> ASTNode:
        node = self._unary()
        while self._peek().type in {'PER', 'DIVISO', 'MODULO', '*', '/', '%'}:
            op = self._advance().type
            if op in {'*', '/'}:
                op = 'PER' if op == '*' else 'DIVISO'
            elif op == '%':
                op = 'MODULO'
            right = self._unary()
            node = BinaryOpNode(node.line, node, op, right)
        return node

    def _unary(self) -> ASTNode:
        if self._peek().type == 'NON':
            self._advance()
            return UnaryOpNode(self._peek().line, 'non', self._unary())
        return self._primary()

    def _primary(self) -> ASTNode:
        token = self._peek()
        if token.type == 'NUMBER':
            self._advance()
            return LiteralNode(token.line, token.value)
        if token.type == 'STRING':
            self._advance()
            return LiteralNode(token.line, token.value)
        if token.type == 'BOOLEAN':
            self._advance()
            return LiteralNode(token.line, token.value == 'vero')
        if token.type == 'NULLO':
            self._advance()
            return LiteralNode(token.line, None)
        if token.type == 'IDENT':
            self._advance()
            if self._match('('):
                args: List[ASTNode] = []
                if not self._match(')'):
                    args.append(self._expression())
                    while self._match(','):
                        args.append(self._expression())
                    self._expect(')')
                return CallNode(token.line, token.value, args)
            return VarNode(token.line, token.value)
        if token.type == '[':
            self._advance()
            items: List[ASTNode] = []
            if not self._match(']'):
                items.append(self._expression())
                while self._match(','):
                    items.append(self._expression())
                self._expect(']')
            return ListNode(token.line, items)
        if token.type == '(':
            self._advance()
            expr = self._expression()
            self._expect(')')
            return expr
        raise SyntaxErrorIpp(f"Espressione non prevista: {token.value}", token.line)

    def _expect(self, token_type: str) -> Token:
        token = self._peek()
        if token.type != token_type:
            raise SyntaxErrorIpp(f"Mi aspettavo '{token_type}'.", token.line)
        return self._advance()

    def _match(self, token_type: str) -> bool:
        if self._peek().type == token_type:
            self._advance()
            return True
        return False

    def _peek(self) -> Token:
        return self.tokens[self.pos]

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        self.pos += 1
        return token


@dataclass
class UnaryOpNode(ASTNode):
    op: str
    operand: ASTNode
