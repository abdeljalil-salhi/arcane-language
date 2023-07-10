from ..token import Token
from ..position import Position


class ListNode:
    def __init__(
        self,
        element_nodes: list["Token"],
        position_start: "Position",
        position_end: "Position",
    ):
        self.element_nodes = element_nodes
        self.position_start = position_start
        self.position_end = position_end
