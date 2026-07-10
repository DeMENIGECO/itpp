from __future__ import annotations

from typing import Any, List, Optional

from .errors import NameErrorIpp, RuntimeErrorIpp, SyntaxErrorIpp, TypeErrorIpp
from .parser import ASTNode, AssignNode, BinaryOpNode, CallNode, ForEachNode, FunctionDefNode, IfNode, InputNode, ListNode, LiteralNode, PrintNode, RepeatNode, ReturnNode, UnaryOpNode, VarNode, WhileNode
from .runtime import Runtime
from .utils import as_number, is_number, random_int, to_string


class Interpreter:
    def __init__(self, runtime: Optional[Runtime] = None):
        self.runtime = runtime or Runtime()

    def interpret(self, statements: List[ASTNode]) -> List[Any]:
        results: List[Any] = []
        for statement in statements:
            result = self._execute(statement)
            if result is not None:
                results.append(result)
        return results

    def _execute(self, node: ASTNode) -> Any:
        if isinstance(node, PrintNode):
            value = self._evaluate(node.value)
            print(to_string(value))
            return value
        if isinstance(node, AssignNode):
            value = self._evaluate(node.value)
            self.runtime.set_variable(node.name, value)
            return value
        if isinstance(node, VarNode):
            return self.runtime.get_variable(node.name)
        if isinstance(node, LiteralNode):
            return node.value
        if isinstance(node, BinaryOpNode):
            return self._evaluate_binary(node)
        if isinstance(node, UnaryOpNode):
            return self._evaluate_unary(node)
        if isinstance(node, IfNode):
            condition = self._evaluate(node.condition)
            if condition:
                return self._execute_block(node.then_body)
            return self._execute_block(node.else_body)
        if isinstance(node, RepeatNode):
            count = int(self._evaluate(node.count))
            for _ in range(count):
                self._execute_block(node.body)
            return None
        if isinstance(node, WhileNode):
            while bool(self._evaluate(node.condition)):
                self._execute_block(node.body)
            return None
        if isinstance(node, ForEachNode):
            iterable = self._evaluate(node.iterable)
            for item in iterable:
                self.runtime.push_scope()
                self.runtime.set_variable(node.var_name, item)
                self._execute_block(node.body)
                self.runtime.pop_scope()
            return None
        if isinstance(node, FunctionDefNode):
            self.runtime.set_function(node.name, node)
            return None
        if isinstance(node, CallNode):
            return self._call_function(node)
        if isinstance(node, ReturnNode):
            return self._evaluate(node.value) if node.value else None
        if isinstance(node, InputNode):
            prompt = to_string(self._evaluate(node.prompt))
            value = input(prompt)
            self.runtime.set_variable(node.target, value)
            return value
        if isinstance(node, ListNode):
            return [self._evaluate(item) for item in node.items]
        return None

    def _execute_block(self, statements: List[ASTNode]) -> Any:
        self.runtime.push_scope()
        try:
            result = None
            for statement in statements:
                result = self._execute(statement)
                if isinstance(statement, ReturnNode):
                    return result
            return result
        finally:
            self.runtime.pop_scope()

    def _evaluate(self, node: ASTNode) -> Any:
        return self._execute(node)

    def _evaluate_binary(self, node: BinaryOpNode) -> Any:
        left = self._evaluate(node.left)
        right = self._evaluate(node.right)
        op = node.op
        if op == 'PIU':
            if is_number(left) and is_number(right):
                return left + right
            return str(left) + str(right)
        if op == 'MENO':
            return left - right
        if op == 'PER':
            return left * right
        if op == 'DIVISO':
            return left / right
        if op == 'MODULO':
            return left % right
        if op == 'E':
            return bool(left) and bool(right)
        if op == 'OPPURE':
            return bool(left) or bool(right)
        if op == 'MAGGIORE':
            return left > right
        if op == 'MINORE':
            return left < right
        if op == 'UGUALE':
            return left == right
        if op == 'DIVERSO':
            return left != right
        if op == 'ALMENO':
            return left >= right
        if op == 'ALMASSIMO':
            return left <= right
        raise RuntimeErrorIpp(f"Operatore non supportato: {op}")

    def _evaluate_unary(self, node: UnaryOpNode) -> Any:
        operand = self._evaluate(node.operand)
        if node.op == 'non':
            return not bool(operand)
        raise RuntimeErrorIpp(f"Operatore unario non supportato: {node.op}")

    def _call_function(self, node: CallNode) -> Any:
        func = self.runtime.get_function(node.name)
        if func is None:
            if node.name == 'stampa':
                value = self._evaluate(node.args[0]) if node.args else None
                print(to_string(value))
                return value
            if node.name == 'leggi':
                return input()
            if node.name == 'lunghezza':
                return len(self._evaluate(node.args[0]))
            if node.name == 'numero':
                return as_number(self._evaluate(node.args[0]))
            if node.name == 'testo':
                return to_string(self._evaluate(node.args[0]))
            if node.name == 'aggiungi':
                target = self._evaluate(node.args[1])
                target.append(self._evaluate(node.args[0]))
                return target
            if node.name == 'rimuovi':
                target = self._evaluate(node.args[1])
                target.remove(self._evaluate(node.args[0]))
                return target
            if node.name == 'tipo':
                return type(self._evaluate(node.args[0])).__name__
            if node.name == 'casuale':
                return random_int(int(self._evaluate(node.args[0])), int(self._evaluate(node.args[1])))
            if node.name == 'arrotonda':
                return round(float(self._evaluate(node.args[0])), int(self._evaluate(node.args[1])))
            raise NameErrorIpp(f"Funzione non definita: {node.name}")
        self.runtime.push_scope()
        for name, arg in zip(func.params, [self._evaluate(arg) for arg in node.args]):
            self.runtime.set_variable(name, arg)
        try:
            result = self._execute_block(func.body)
        finally:
            self.runtime.pop_scope()
        return result


class FunctionCallError(RuntimeErrorIpp):
    pass
