from ..base.value import Value
from ..errors.run_time_error import RunTimeError
from .value import Value
from .number import Number


class String(Value):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __repr__(self) -> str:
        return f'"{self.value}"'

    def added_to(self, other: "String") -> tuple["String", "RunTimeError"]:
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def multiplied_by(self, other: "String") -> tuple["String", "RunTimeError"]:
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)

    def is_true(self) -> bool:
        return len(self.value) > 0

    def copy(self) -> "String":
        return (
            String(self.value)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )
