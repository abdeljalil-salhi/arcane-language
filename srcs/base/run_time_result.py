from ..errors.base_error import BaseError
from .number import Number


class RunTimeResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, result: "RunTimeResult") -> "RunTimeResult":
        if result.error:
            self.error = result.error
        return result.value

    def success(self, value: "Number") -> "RunTimeResult":
        self.value = value
        return self

    def failure(self, error: "BaseError") -> "RunTimeResult":
        self.error = error
        return self
