from .position import Position
from .context import Context
from ..errors.run_time_error import RunTimeError


class Value:
    def __init__(self) -> None:
        self.set_position()
        self.set_context()

    def set_position(
        self, position_start: "Position" = None, position_end: "Position" = None
    ) -> "Value":
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context: "Context" = None) -> "Value":
        self.context = context
        return self

    def execute(self, arguments) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation()

    def copy(self) -> None:
        raise Exception("No copy method defined")

    def is_true(self) -> bool:
        return False

    def illegal_operation(self, other=None) -> "RunTimeError":
        if not other:
            other = self
        return RunTimeError(
            other.position_start,
            other.position_end,
            "Illegal operation",
            self.context,
        )

    def added_to(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def subtracted_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def multiplied_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def divided_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def moduled_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def powered_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def get_comparison_neq(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def anded_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def ored_by(self, other) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation(other)

    def notted(self) -> tuple["Value", "RunTimeError"]:
        return None, self.illegal_operation()
