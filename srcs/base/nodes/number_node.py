from ..token import Token


class NumberNode:
    def __init__(self, token: "Token") -> None:
        self.token = token
        self.position_start = self.token.position_start
        self.position_end = self.token.position_end

    def __repr__(self) -> str:
        return f"{self.token}"
