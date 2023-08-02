from ..position import Position


class BreakNode:
    def __init__(self, position_start: "Position", position_end: "Position" = None):
        self.position_start = position_start
        self.position_end = position_end
