class IppError(Exception):
    """Errore base del linguaggio I++."""

    def __init__(self, message: str, line: int | None = None):
        self.message = message
        self.line = line
        super().__init__(self.format_message())

    def format_message(self) -> str:
        if self.line is not None:
            return f"Errore alla riga {self.line}\n\n{self.message}"
        return self.message


class SyntaxErrorIpp(IppError):
    pass


class NameErrorIpp(IppError):
    pass


class TypeErrorIpp(IppError):
    pass


class RuntimeErrorIpp(IppError):
    pass
