from ..value import Value
from ..context import Context
from ..symbol_table import SymbolTable
from ..run_time_result import RunTimeResult
from ...errors.run_time_error import RunTimeError


class BaseFunction(Value):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self) -> "Context":
        new_context = Context(self.name, self.context, self.position_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_arguments(
        self, argument_names: list, arguments: list["Value"]
    ) -> "RunTimeResult":
        response = RunTimeResult()
        if len(arguments) > len(argument_names):
            return response.failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    f"{len(arguments) - len(argument_names)} too many arguments passed into '{self.name}'",
                    self.context,
                )
            )

        if len(arguments) < len(argument_names):
            return response.failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    f"{len(argument_names) - len(arguments)} too few arguments passed into '{self.name}'",
                    self.context,
                )
            )
        return response.success(None)

    def populate_arguments(
        self,
        argument_names: list,
        arguments: list["Value"],
        execution_context: "Context",
    ) -> None:
        for i in range(len(arguments)):
            argument_name = argument_names[i]
            argument_value = arguments[i]
            argument_value.set_context(execution_context)
            execution_context.symbol_table.set(argument_name, argument_value)

    def check_and_populate_arguments(
        self,
        argument_names: list,
        arguments: list["Value"],
        execution_context: "Context",
    ) -> "RunTimeResult":
        response = RunTimeResult()
        response.register(self.check_arguments(argument_names, arguments))
        if response.error:
            return response
        self.populate_arguments(argument_names, arguments, execution_context)
        return response.success(None)
