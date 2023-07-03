from .position import Position

TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"

TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MUL = "MUL"
TOKEN_DIV = "DIV"
TOKEN_MOD = "MOD"
TOKEN_POW = "POW"

TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"

TOKEN_EOF = "EOF"


class Token:
    def __init__(
        self,
        _type: str,
        value: str = None,
        position_start: "Position" = None,
        position_end: "Position" = None,
    ) -> None:
        self.type = _type
        self.value = value

        if position_start:
            self.position_start = position_start.copy()
            self.position_end = position_start.copy()
            self.position_end.advance()
        if position_end:
            self.position_end = position_end.copy()

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
