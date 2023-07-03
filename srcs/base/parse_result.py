from .nodes.number_node import NumberNode
from ..errors.base_error import BaseError


class ParseResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None

    def register(self, result: "ParseResult") -> "ParseResult":
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node
        return result

    def success(self, node: "NumberNode") -> "ParseResult":
        self.node = node
        return self

    def failure(self, error: "BaseError") -> "ParseResult":
        self.error = error
        return self
