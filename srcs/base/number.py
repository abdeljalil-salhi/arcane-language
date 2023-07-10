from ..base.position import Position
from ..errors.run_time_error import RunTimeError
from .context import Context
from .value import Value


class Number(Value):
    def __init__(self, value: float) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def set_position(
        self, position_start: "Position" = None, position_end: "Position" = None
    ) -> "Number":
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context: "Context" = None) -> "Number":
        self.context = context
        return self

    def copy(self) -> "Number":
        return (
            Number(self.value)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )

    def is_true(self) -> bool:
        return self.value != 0

    def added_to(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def subtracted_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def multiplied_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def divided_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )
            return Number(self.value / other.value).set_context(self.context), None
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def moduled_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )
            return Number(self.value % other.value).set_context(self.context), None
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def powered_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(self.context), None
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def get_comparison_eq(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value == other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def get_comparison_neq(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value != other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def get_comparison_lt(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value < other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def get_comparison_lte(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value <= other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def get_comparison_gt(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value > other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def get_comparison_gte(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value >= other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def anded_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value and other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def ored_by(self, other: "Number") -> tuple["Number", "RunTimeError"]:
        if isinstance(other, Number):
            return (
                Number(int(self.value or other.value)).set_context(self.context),
                None,
            )
        return None, Value.illegal_operation(self.position_start, self.position_end)

    def notted(self) -> tuple["Number", "RunTimeError"]:
        return Number(int(not self.value)).set_context(self.context), None


Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
