from ..position import Position


class ReturnNode:
    def __init__(
        self, to_return, position_start: "Position", position_end: "Position" = None
    ):
        self.to_return = to_return
        self.position_start = position_start
        self.position_end = position_end
