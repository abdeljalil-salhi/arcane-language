from .number_node import NumberNode
from ..token import Token


class UnaryOperationNode:
    def __init__(self, operator_token: "Token", node: "NumberNode") -> None:
        self.operator_token = operator_token
        self.node = node
        self.position_start = self.operator_token.position_start
        self.position_end = self.node.position_end

    def __repr__(self) -> str:
        return f"({self.operator_token}, {self.node})"
