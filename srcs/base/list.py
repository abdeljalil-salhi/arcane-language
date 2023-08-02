from .value import Value
from .number import Number
from ..errors.run_time_error import RunTimeError


class List(Value):
    def __init__(self, elements: list["Value"]):
        super().__init__()
        self.elements = elements

    def copy(self) -> "List":
        return (
            List(self.elements)
            .set_context(self.context)
            .set_position(self.position_start, self.position_end)
        )

    def __repr__(self) -> str:
        return f"[{', '.join([repr(x) for x in self.elements])}]"

    def added_to(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subtracted_by(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RunTimeError(
                    other.position_start,
                    other.position_end,
                    "Index out of bounds",
                    self.context,
                )
        return None, RunTimeError(
            other.position_start,
            other.position_end,
            "Cannot subtract list by non-number; index must be a number",
            self.context,
        )

    def multiplied_by(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        return None, RunTimeError(
            other.position_start,
            other.position_end,
            "Cannot concatenate list with non-list",
            self.context,
        )

    def divided_by(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RunTimeError(
                    other.position_start,
                    other.position_end,
                    "Index out of bounds",
                    self.context,
                )
        return None, RunTimeError(
            other.position_start,
            other.position_end,
            "Cannot divide list by non-number; index must be a number",
            self.context,
        )
