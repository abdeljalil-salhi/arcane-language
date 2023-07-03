from ..token import Token


class VariableAccessNode:
    def __init__(self, token: "Token") -> None:
        self.variable_name_token = token
        self.position_start = self.variable_name_token.position_start
        self.position_end = self.variable_name_token.position_end
