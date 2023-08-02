from .nodes.number_node import NumberNode
from ..errors.base_error import BaseError


class ParseResult:
    def __init__(self) -> None:
        self.error = None
        self.node = None
        self.count = 0
        self.reverse_count = 0

    def register(self, result: "ParseResult") -> "ParseResult":
        self.count += result.count
        if result.error:
            self.error = result.error
        return result.node
    
    def try_register(self, result: "ParseResult") -> "ParseResult":
        if result.error:
            self.reverse_count = result.count
            return None
        return self.register(result)

    def register_advance(self, advance: callable) -> None:
        self.count += 1
        advance()

    def success(self, node: "NumberNode") -> "ParseResult":
        self.node = node
        return self

    def failure(self, error: "BaseError") -> "ParseResult":
        if not self.error or self.count == 0:
            self.error = error
        return self
