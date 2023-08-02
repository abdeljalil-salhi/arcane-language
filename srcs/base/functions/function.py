from ..nodes.binary_operation_node import BinaryOperationNode
from ..run_time_result import RunTimeResult
from ..value import Value
from .base_function import BaseFunction
from ..number import Number


class Function(BaseFunction):
    def __init__(
        self,
        name: str,
        body_node: "BinaryOperationNode",
        argument_names: list,
        is_automatic_return: bool = False,
    ) -> None:
        super().__init__(name)
        self.body_node = body_node
        self.argument_names = argument_names
        self.is_automatic_return = is_automatic_return

    def __repr__(self) -> str:
        return f"<function {self.name}>"

    def execute(self, arguments: list["Value"]) -> "RunTimeResult":
        from ...interpreter import Interpreter

        response = RunTimeResult()
        interpreter = Interpreter()
        context = self.generate_new_context()

        response.register(
            self.check_and_populate_arguments(self.argument_names, arguments, context)
        )
        if response.should_return():
            return response

        value = response.register(interpreter.visit(self.body_node, context))
        if response.should_return() and response.return_value is None:
            return response
        return response.success(
            (value if self.is_automatic_return else None)
            or response.return_value
            or Number.null
        )

    def copy(self) -> "Function":
        return (
            Function(
                self.name, self.body_node, self.argument_names, self.is_automatic_return
            )
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )
