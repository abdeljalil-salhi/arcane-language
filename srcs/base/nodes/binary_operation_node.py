from .number_node import NumberNode
from ..token import Token


class BinaryOperationNode:
    def __init__(
        self, left_node: "NumberNode", operator_token: "Token", right_node: "NumberNode"
    ) -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        self.position_start = self.left_node.position_start
        self.position_end = self.right_node.position_end

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"
