from .base_error import BaseError
from ..base.position import Position


class ExpectedCharacterError(BaseError):
    def __init__(
        self, position_start: "Position", position_end: "Position", details: str
    ):
        super().__init__(position_start, position_end, "Expected Character", details)
