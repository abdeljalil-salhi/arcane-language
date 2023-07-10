from .value import Value
from .number import Number
from ..errors.run_time_error import RunTimeError


class List(Value):
    def __init__(self, elements: list["Value"]):
        super().__init__()
        self.elements = elements

    def copy(self) -> "List":
        return (
            List(self.elements[:])
            .set_context(self.context)
            .set_pos(self.pos_start, self.pos_end)
        )
    
    def __repr__(self) -> str:
        return f"[{', '.join([str(x) for x in self.elements])}]"

    def added_to(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subtracted_by(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        if isinstance(other, List):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Element at this index could not be removed from list because index is out of bounds",
                    self.context,
                )
        return None, RunTimeError(
            other.pos_start,
            other.pos_end,
            "Cannot subtract list by non-list",
            self.context,
        )

    def multiplied_by(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        return None, RunTimeError(
            other.pos_start,
            other.pos_end,
            "Cannot multiply list by non-list",
            self.context,
        )

    def divided_by(self, other: "Value") -> tuple["Value", "RunTimeError"]:
        if isinstance(other, Number):
            try:
                return self.elements[other.value], None
            except:
                return None, RunTimeError(
                    other.pos_start,
                    other.pos_end,
                    "Element at this index could not be retrieved from list because index is out of bounds",
                    self.context,
                )
        return None, RunTimeError(
            other.pos_start,
            other.pos_end,
            "Cannot divide list by non-list",
            self.context,
        )
