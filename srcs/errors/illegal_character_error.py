from .base_error import BaseError


class IllegalCharacterError(BaseError):
    def __init__(
        self, position_start: "Position", position_end: "Position", details: str
    ) -> None:
        super().__init__(position_start, position_end, "Illegal Character", details)
