from .base_error import BaseError
from ..base.position import Position
from ..base.context import Context


class RunTimeError(BaseError):
    def __init__(
        self,
        position_start: "Position",
        position_end: "Position",
        details: str = "",
        context: "Context" = None,
    ) -> None:
        super().__init__(position_start, position_end, "Runtime Error", details)
        self.context = context

    def as_string(self) -> str:
        result = self.generate_traceback()
        result += f"{self.name}: {self.details}"
        result += "\n\n" + self.string_with_arrows(
            self.position_start.file_text, self.position_start, self.position_end
        )
        return result

    def generate_traceback(self) -> str:
        result = ""
        position = self.position_start
        context = self.context
        while context:
            result = (
                f"  File {position.file_name}, line {position.line + 1}, in {context.display_name}\n"
                + result
            )
            position = context.parent_entry_position
            context = context.parent
        return "Traceback (most recent call last):\n" + result
