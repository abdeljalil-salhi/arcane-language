from ..position import Position


class ContinueNode:
    def __init__(self, position_start: "Position", position_end: "Position" = None):
        self.position_start = position_start
        self.position_end = position_end
