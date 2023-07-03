from .position import Position
from .constants.tokens import *


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

    def matches(self, _type: str, value: str) -> bool:
        return self.type == _type and self.value == value
