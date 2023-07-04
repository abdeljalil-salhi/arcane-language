from ..token import Token
from .binary_operation_node import BinaryOperationNode


class FunctionDefinitionNode:
    def __init__(
        self, token: "Token", arguments: list, body: "BinaryOperationNode"
    ) -> None:
        self.token = token
        self.arguments = arguments
        self.body = body
        if self.token:
            self.position_start = self.token.position_start
        elif len(self.arguments) > 0:
            self.position_start = self.arguments[0].position_start
        else:
            self.position_start = self.body[0].position_start
        self.position_end = self.body.position_end
