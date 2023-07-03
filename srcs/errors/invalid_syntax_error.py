from .base_error import BaseError


class InvalidSyntaxError(BaseError):
    def __init__(
        self, position_start: "Position", position_end: "Position", details: str = ""
    ) -> None:
        super().__init__(position_start, position_end, "Invalid Syntax", details)
