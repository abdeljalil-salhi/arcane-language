from .base_function import BaseFunction
from ..run_time_result import RunTimeResult


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
        if response.error:
            return response

        return_value = response.register(method(context))
        if response.error:
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
