from ..token import Token
from .binary_operation_node import BinaryOperationNode


class ForNode:
    def __init__(
        self,
        token: "Token",
        start_value: "BinaryOperationNode",
        end_value: "BinaryOperationNode",
        increment_value: "BinaryOperationNode",
        body: "BinaryOperationNode",
        is_null: bool = False,
    ):
        self.token = token
        self.start_value = start_value
        self.end_value = end_value
        self.increment_value = increment_value
        self.body = body
        self.position_start = self.token.position_start
        self.position_end = self.body.position_end
        self.is_null = is_null
