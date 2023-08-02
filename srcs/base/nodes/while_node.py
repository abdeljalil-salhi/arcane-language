from .binary_operation_node import BinaryOperationNode


class WhileNode:
    def __init__(
        self,
        condition: "BinaryOperationNode",
        body: "BinaryOperationNode",
        is_null: bool = False,
    ) -> None:
        self.condition = condition
        self.body = body
        self.position_start = self.condition.position_start
        self.position_end = self.body.position_end
        self.is_null = is_null
