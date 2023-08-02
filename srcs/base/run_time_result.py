from ..errors.base_error import BaseError
from .number import Number
from .value import Value


class RunTimeResult:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.value = None
        self.error = None
        self.return_value = None
        self.continue_loop = False
        self.break_loop = False

    def register(self, result: "RunTimeResult") -> "RunTimeResult":
        if result.error:
            self.error = result.error
        self.return_value = result.return_value
        self.continue_loop = result.continue_loop
        self.break_loop = result.break_loop
        return result.value

    def success(self, value: "Number") -> "RunTimeResult":
        self.reset()
        self.value = value
        return self

    def success_return(self, value: "Value") -> "RunTimeResult":
        self.reset()
        self.return_value = value
        return self

    def success_continue(self) -> "RunTimeResult":
        self.reset()
        self.continue_loop = True
        return self

    def success_break(self) -> "RunTimeResult":
        self.reset()
        self.break_loop = True
        return self

    def failure(self, error: "BaseError") -> "RunTimeResult":
        self.reset()
        self.error = error
        return self

    def should_return(self) -> bool:
        return self.error or self.return_value or self.continue_loop or self.break_loop
