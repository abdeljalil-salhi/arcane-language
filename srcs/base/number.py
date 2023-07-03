from ..base.position import Position
from ..errors.base_error import BaseError
from ..errors.run_time_error import RunTimeError
from .context import Context


class Number:
    def __init__(self, value: int | float) -> None:
        self.value = value

        self.set_position()
        self.set_context()

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

    def added_to(self, other: "Number") -> tuple["Number", BaseError]:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtracted_by(self, other: "Number") -> tuple["Number", BaseError]:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other: "Number") -> tuple["Number", BaseError]:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other: "Number") -> tuple["Number", BaseError]:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )
            return Number(self.value / other.value).set_context(self.context), None
