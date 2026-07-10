from __future__ import annotations

from typing import Any, Dict, List, Optional

from .errors import NameErrorIpp
from .parser import FunctionDefNode


class Runtime:
    def __init__(self):
        self.globals: Dict[str, Any] = {}
        self.functions: Dict[str, FunctionDefNode] = {}
        self.scopes: List[Dict[str, Any]] = [self.globals]

    def push_scope(self) -> None:
        self.scopes.append({})

    def pop_scope(self) -> None:
        if len(self.scopes) > 1:
            self.scopes.pop()

    def set_variable(self, name: str, value: Any) -> None:
        self.scopes[-1][name] = value

    def get_variable(self, name: str):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameErrorIpp(f'Variabile "{name}" non definita.')

    def set_function(self, name: str, func: FunctionDefNode) -> None:
        self.functions[name] = func

    def get_function(self, name: str) -> Optional[FunctionDefNode]:
        return self.functions.get(name)
