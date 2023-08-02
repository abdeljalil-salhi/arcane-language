from .nodes.binary_operation_node import BinaryOperationNode
from ..errors.run_time_error import RunTimeError
from .run_time_result import RunTimeResult
from .value import Value
from .base_function import BaseFunction


class Function(BaseFunction):
    def __init__(
        self, name: str, body_node: "BinaryOperationNode", argument_names: list
    ) -> None:
        super().__init__(name)
        self.body_node = body_node
        self.argument_names = argument_names

    def __repr__(self) -> str:
        return f"<function {self.name}>"

    def execute(self, arguments: list["Value"]) -> "RunTimeResult":
        from ..interpreter import Interpreter

        response = RunTimeResult()
        interpreter = Interpreter()
        context = self.generate_new_context()

        response.register(
            self.check_and_populate_arguments(self.argument_names, arguments, context)
        )
        if response.error:
            return response

        value = response.register(interpreter.visit(self.body_node, context))
        if response.error:
            return response
        return response.success(value)

    def copy(self) -> "Function":
        return (
            Function(self.name, self.body_node, self.argument_names)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )
