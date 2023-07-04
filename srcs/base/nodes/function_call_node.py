from .function_definition_node import FunctionDefinitionNode
from .binary_operation_node import BinaryOperationNode


class FunctionCallNode:
    def __init__(
        self,
        node_to_call: "FunctionDefinitionNode",
        arguments: list["BinaryOperationNode"],
    ) -> None:
        self.node_to_call = node_to_call
        self.arguments = arguments
        self.position_start = self.node_to_call.position_start
        if len(self.arguments) > 0:
            self.position_end = self.arguments[len(self.arguments) - 1].position_end
        else:
            self.position_end = self.node_to_call.position_end
