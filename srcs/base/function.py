from .nodes.binary_operation_node import BinaryOperationNode
from .context import Context
from ..errors.run_time_error import RunTimeError
from .symbol_table import SymbolTable
from .run_time_result import RunTimeResult
from .value import Value


class Function(Value):
    def __init__(
        self, name: str, body_node: "BinaryOperationNode", argument_names: list
    ) -> None:
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.argument_names = argument_names

    def __repr__(self) -> str:
        return f"<function {self.name}>"

    def execute(self, arguments: list["Value"]) -> tuple["Value", "RunTimeError"]:
        from ..interpreter import Interpreter

        response = RunTimeResult()
        interpreter = Interpreter()
        context = Context(self.name, self.context, self.position_start)
        context.symbol_table = SymbolTable(context.parent.symbol_table)

        if len(arguments) > len(self.argument_names):
            return response.failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    f"{len(arguments) - len(self.argument_names)} too many arguments passed into '{self.name}'",
                    context,
                )
            )

        if len(arguments) < len(self.argument_names):
            return response.failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    f"{len(self.argument_names) - len(arguments)} too few arguments passed into '{self.name}'",
                    context,
                )
            )

        for i in range(len(arguments)):
            argument_name = self.argument_names[i]
            argument_value = arguments[i]
            argument_value.set_context(context)
            context.symbol_table.set(argument_name, argument_value)

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
