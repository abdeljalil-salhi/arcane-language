from ..token import Token
from .binary_operation_node import BinaryOperationNode


class VariableAssignNode:
    def __init__(self, token: "Token", value_node: "BinaryOperationNode") -> None:
        self.variable_name_token = token
        self.value_node = value_node
        self.position_start = self.variable_name_token.position_start
        self.position_end = self.value_node.position_end
