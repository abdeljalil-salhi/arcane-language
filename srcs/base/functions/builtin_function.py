from .base_function import BaseFunction
from ..run_time_result import RunTimeResult
from ...errors.run_time_error import RunTimeError
from ..context import Context
from ..number import Number
from ..string import String
from ..list import List


class BuiltInFunction(BaseFunction):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def __repr__(self) -> str:
        return f"<built-in function {self.name}>"

    def execute(self, arguments) -> "RunTimeResult":
        response = RunTimeResult()
        context = self.generate_new_context()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_visit_method)

        response.register(
            self.check_and_populate_arguments(method.argument_names, arguments, context)
        )
        if response.should_return():
            return response

        return_value = response.register(method(context))
        if response.should_return():
            return response

        return response.success(return_value)

    def no_visit_method(self, _, __):
        raise Exception(f"No execute_{self.name} method defined")

    def copy(self) -> "BuiltInFunction":
        return (
            BuiltInFunction(self.name)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )

    def execute_print(self, context: "Context") -> "RunTimeResult":
        value = str(context.symbol_table.get("value"))
        print(value)
        return RunTimeResult().success(Number(len(value)))

    def execute_input(self, _: "Context") -> "RunTimeResult":
        value = input("> ")
        try:
            number = int(value)
            return RunTimeResult().success(Number(number))
        except ValueError:
            return RunTimeResult().success(String(value))

    def execute_clear(self, _: "Context") -> "RunTimeResult":
        from os import system, name

        system("cls" if name == "nt" else "clear")
        return RunTimeResult().success(Number.null)

    def execute_len(self, context: "Context") -> "RunTimeResult":
        value = context.symbol_table.get("value")

        if isinstance(value, List):
            return RunTimeResult().success(Number(len(value.elements)))
        try:
            return RunTimeResult().success(Number(len(str(value))))
        except:
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "Argument must be string, number or list",
                    context,
                )
            )

    def execute_is_number(self, context: "Context") -> "RunTimeResult":
        return RunTimeResult().success(
            Number.true
            if isinstance(context.symbol_table.get("value"), Number)
            else Number.false
        )

    def execute_is_string(self, context: "Context") -> "RunTimeResult":
        return RunTimeResult().success(
            Number.true
            if isinstance(context.symbol_table.get("value"), String)
            else Number.false
        )

    def execute_is_list(self, context: "Context") -> "RunTimeResult":
        return RunTimeResult().success(
            Number.true
            if isinstance(context.symbol_table.get("value"), List)
            else Number.false
        )

    def execute_is_function(self, context: "Context") -> "RunTimeResult":
        return RunTimeResult().success(
            Number.true
            if isinstance(context.symbol_table.get("value"), BaseFunction)
            else Number.false
        )

    def execute_append(self, context: "Context") -> "RunTimeResult":
        _list = context.symbol_table.get("list")
        value = context.symbol_table.get("value")

        if not isinstance(_list, List):
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "First argument must be list",
                    context,
                )
            )

        _list.elements.append(value)
        return RunTimeResult().success(Number(len(_list.elements)))

    def execute_pop(self, context: "Context") -> "RunTimeResult":
        _list = context.symbol_table.get("list")
        index = context.symbol_table.get("index")

        if not isinstance(_list, List):
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "First argument must be list",
                    context,
                )
            )

        if not isinstance(index, Number):
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "Second argument must be number",
                    context,
                )
            )

        try:
            element = _list.elements.pop(index.value)
        except:
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "Index out of bounds",
                    context,
                )
            )
        return RunTimeResult().success(element)

    def execute_extend(self, context: "Context") -> "RunTimeResult":
        first_list = context.symbol_table.get("first_list")
        second_list = context.symbol_table.get("second_list")

        if not isinstance(first_list, List):
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "First argument must be list",
                    context,
                )
            )

        if not isinstance(second_list, List):
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "Second argument must be list",
                    context,
                )
            )

        first_list.elements.extend(second_list.elements)
        return RunTimeResult().success(Number(len(first_list.elements)))

    def execute_run(self, context: "Context") -> "RunTimeResult":
        from ...shell import run

        file_name = context.symbol_table.get("file_name")
        if not isinstance(file_name, String):
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    "Argument must be string",
                    context,
                )
            )

        file_name = file_name.value
        try:
            with open(file_name, "r") as f:
                script = f.read()
        except Exception as e:
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    f'Failed to load file "{file_name}"\n{str(e)}',
                    context,
                )
            )

        _, error = run(file_name, script)
        if error:
            return RunTimeResult().failure(
                RunTimeError(
                    self.position_start,
                    self.position_end,
                    f'Failed to finish executing file "{file_name}"\n{error.as_string()}',
                    context,
                )
            )

        return RunTimeResult().success(Number.null)

    execute_print.argument_names = ["value"]
    execute_input.argument_names = []
    execute_clear.argument_names = []
    execute_len.argument_names = ["value"]
    execute_is_number.argument_names = ["value"]
    execute_is_string.argument_names = ["value"]
    execute_is_list.argument_names = ["value"]
    execute_is_function.argument_names = ["value"]
    execute_append.argument_names = ["list", "value"]
    execute_pop.argument_names = ["list", "index"]
    execute_extend.argument_names = ["first_list", "second_list"]
    execute_run.argument_names = ["file_name"]


BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.clear = BuiltInFunction("clear")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.is_number = BuiltInFunction("is_number")
BuiltInFunction.is_string = BuiltInFunction("is_string")
BuiltInFunction.is_list = BuiltInFunction("is_list")
BuiltInFunction.is_function = BuiltInFunction("is_function")
BuiltInFunction.append = BuiltInFunction("append")
BuiltInFunction.pop = BuiltInFunction("pop")
BuiltInFunction.extend = BuiltInFunction("extend")
BuiltInFunction.run = BuiltInFunction("run")
