class Error:
    def __init__(
        self,
        position_start: "Position",
        position_end: "Position",
        name: str,
        details: str,
    ) -> None:
        self.position_start = position_start
        self.position_end = position_end
        self.name = name
        self.details = details

    def as_string(self) -> str:
        result = f"{self.name}: {self.details}\n"
        result += (
            f"File {self.position_start.file_name}, line {self.position_start.line + 1}"
        )
        result += "\n\n" + self.string_with_arrows(
            self.position_start.file_text, self.position_start, self.position_end
        )
        return result

    def string_with_arrows(
        self, text: str, position_start: "Position", position_end: "Position"
    ) -> str:
        result = ""
        index_start = max(text.rfind("\n", 0, position_start.index), 0)
        index_end = text.find("\n", index_start + 1)
        if index_end < 0:
            index_end = len(text)
        line_count = position_end.line - position_start.line + 1
        for i in range(line_count):
            line = text[index_start:index_end]
            col_start = position_start.column if i == 0 else 0
            col_end = position_end.column if i == line_count - 1 else len(line) - 1
            result += line + "\n"
            result += " " * col_start + "^" * (col_end - col_start)
            index_start = index_end
            index_end = text.find("\n", index_start + 1)
            if index_end < 0:
                index_end = len(text)
        return result.rstrip()


class IllegalCharacterError(Error):
    def __init__(
        self, position_start: "Position", position_end: "Position", details: str
    ) -> None:
        super().__init__(position_start, position_end, "Illegal Character", details)


class InvalidSyntaxError(Error):
    def __init__(
        self, position_start: "Position", position_end: "Position", details: str = ""
    ) -> None:
        super().__init__(position_start, position_end, "Invalid Syntax", details)


class RunTimeError(Error):
    def __init__(
        self,
        position_start: "Position",
        position_end: "Position",
        details: str = "",
        context: "Context" = None,
    ) -> None:
        super().__init__(position_start, position_end, "Runtime Error", details)
        self.context = context

    def as_string(self) -> str:
        result = self.generate_traceback()
        result += f"{self.name}: {self.details}"
        result += "\n\n" + self.string_with_arrows(
            self.position_start.file_text, self.position_start, self.position_end
        )
        return result

    def generate_traceback(self) -> str:
        result = ""
        position = self.position_start
        context = self.context
        while context:
            result = (
                f"  File {position.file_name}, line {position.line + 1}, in {context.display_name}\n"
                + result
            )
            position = context.parent_entry_position
            context = context.parent
        return "Traceback (most recent call last):\n" + result


class Position:
    def __init__(
        self, index: int, line: int, column: int, file_name: str, file_text: str
    ) -> None:
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text

    def advance(self, current_character: str = None) -> "Position":
        self.index += 1
        self.column += 1

        if current_character == "\n":
            self.line += 1
            self.column = 0

        return self

    def copy(self) -> "Position":
        return Position(
            self.index, self.line, self.column, self.file_name, self.file_text
        )


TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MUL = "MUL"
TOKEN_DIV = "DIV"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_EOF = "EOF"


class Token:
    def __init__(
        self,
        _type: str,
        value: str = None,
        position_start: "Position" = None,
        position_end: "Position" = None,
    ) -> None:
        self.type = _type
        self.value = value

        if position_start:
            self.position_start = position_start.copy()
            self.position_end = position_start.copy()
            self.position_end.advance()
        if position_end:
            self.position_end = position_end.copy()

    def __repr__(self) -> str:
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:
    def __init__(self, file_name: str, text: str) -> None:
        self.file_name = file_name
        self.text = text
        self.position = Position(-1, 0, -1, self.file_name, self.text)
        self.current_character = None

        self.advance()

    def advance(self) -> None:
        self.position.advance(self.current_character)
        self.current_character = (
            self.text[self.position.index]
            if self.position.index < len(self.text)
            else None
        )

    def make_tokens(self) -> tuple[list["Token"], Error]:
        tokens = []

        while self.current_character:
            if self.current_character in " \t":
                self.advance()
            elif self.current_character in "0123456789":
                tokens.append(self.make_number())
            elif self.current_character == "+":
                tokens.append(Token(TOKEN_PLUS, position_start=self.position))
                self.advance()
            elif self.current_character == "-":
                tokens.append(Token(TOKEN_MINUS, position_start=self.position))
                self.advance()
            elif self.current_character == "*":
                tokens.append(Token(TOKEN_MUL, position_start=self.position))
                self.advance()
            elif self.current_character == "/":
                tokens.append(Token(TOKEN_DIV, position_start=self.position))
                self.advance()
            elif self.current_character == "(":
                tokens.append(Token(TOKEN_LPAREN, position_start=self.position))
                self.advance()
            elif self.current_character == ")":
                tokens.append(Token(TOKEN_RPAREN, position_start=self.position))
                self.advance()
            else:
                position_start = self.position.copy()
                char = self.current_character
                self.advance()
                return [], IllegalCharacterError(
                    position_start, self.position, f"'{char}'"
                )

        tokens.append(Token(TOKEN_EOF, position_start=self.position))
        return tokens, None

    def make_number(self) -> "Token":
        number_string = ""
        dot_count = 0
        position_start = self.position.copy()

        while self.current_character and self.current_character in "0123456789.":
            if self.current_character == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                number_string += "."
            else:
                number_string += self.current_character
            self.advance()

        if dot_count == 0:
            return Token(TOKEN_INT, int(number_string), position_start, self.position)
        return Token(TOKEN_FLOAT, float(number_string), position_start, self.position)


class NumberNode:
    def __init__(self, token: "Token") -> None:
        self.token = token
        self.position_start = self.token.position_start
        self.position_end = self.token.position_end

    def __repr__(self) -> str:
        return f"{self.token}"


class UnaryOperationNode:
    def __init__(self, operator_token: "Token", node: "NumberNode") -> None:
        self.operator_token = operator_token
        self.node = node
        self.position_start = self.operator_token.position_start
        self.position_end = self.node.position_end

    def __repr__(self) -> str:
        return f"({self.operator_token}, {self.node})"


class BinaryOperationNode:
    def __init__(
        self, left_node: "NumberNode", operator_token: "Token", right_node: "NumberNode"
    ) -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
        self.position_start = self.left_node.position_start
        self.position_end = self.right_node.position_end

    def __repr__(self) -> str:
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"


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

    def failure(self, error: "Error") -> "ParseResult":
        self.error = error
        return self


class Parser:
    def __init__(self, tokens: list["Token"]) -> None:
        self.tokens = tokens
        self.token_index = -1

        self.advance()

    def advance(self) -> None:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self) -> "BinaryOperationNode":
        response = self.expr()
        if not response.error and self.current_token.type != TOKEN_EOF:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '+', '-', '*', or '/'",
                )
            )
        return response

    def factor(self) -> "NumberNode":
        response = ParseResult()
        token = self.current_token

        if token.type in (TOKEN_PLUS, TOKEN_MINUS):
            response.register(self.advance())
            factor = response.register(self.factor())
            if response.error:
                return response
            return response.success(UnaryOperationNode(token, factor))

        elif token.type in (TOKEN_INT, TOKEN_FLOAT):
            response.register(self.advance())
            return response.success(NumberNode(token))

        elif token.type == TOKEN_LPAREN:
            response.register(self.advance())
            expr = response.register(self.expr())
            if response.error:
                return response
            if self.current_token.type == TOKEN_RPAREN:
                response.register(self.advance())
                return response.success(expr)
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected ')'",
                )
            )

        return response.failure(
            InvalidSyntaxError(
                token.position_start, token.position_end, "Expected int or float"
            )
        )

    def term(self) -> "BinaryOperationNode":
        return self.binary_operation(self.factor, (TOKEN_MUL, TOKEN_DIV))

    def expr(self) -> "BinaryOperationNode":
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS))

    def binary_operation(
        self, function, operation_tokens: list["Token"]
    ) -> "BinaryOperationNode":
        response = ParseResult()
        left_node = response.register(function())
        if response.error:
            return response
        while self.current_token.type in operation_tokens:
            operator_token = self.current_token
            response.register(self.advance())
            right_node = response.register(function())
            if response.error:
                return response
            left_node = BinaryOperationNode(left_node, operator_token, right_node)
        return response.success(left_node)


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

    def failure(self, error: "Error") -> "RunTimeResult":
        self.error = error
        return self


class Number:
    def __init__(self, value: int | float) -> None:
        self.value = value

        self.set_position()
        self.set_context()

    def __repr__(self) -> str:
        return f"{self.value}"

    def set_position(
        self, position_start: "Position" = None, position_end: "Position" = None
    ) -> "Number":
        self.position_start = position_start
        self.position_end = position_end
        return self

    def set_context(self, context: "Context" = None) -> "Number":
        self.context = context
        return self

    def added_to(self, other: "Number") -> tuple["Number", Error]:
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtracted_by(self, other: "Number") -> tuple["Number", Error]:
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other: "Number") -> tuple["Number", Error]:
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divided_by(self, other: "Number") -> tuple["Number", Error]:
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.position_start,
                    other.position_end,
                    "Division by zero",
                    self.context,
                )
            return Number(self.value / other.value).set_context(self.context), None


class Context:
    def __init__(
        self,
        display_name: str,
        parent: "Context" = None,
        parent_entry_position: int = None,
    ) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position = parent_entry_position


class Interpreter:
    def __init__(self) -> None:
        pass

    def visit(self, node, context: "Context") -> float:
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: "Context") -> None:
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node: "NumberNode", context: "Context") -> float:
        return RunTimeResult().success(
            Number(node.token.value)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )

    def visit_UnaryOperationNode(
        self, node: "UnaryOperationNode", context: "Context"
    ) -> float:
        response = RunTimeResult()
        number = response.register(self.visit(node.node, context))
        if response.error:
            return response

        error = None
        if node.operator_token.type == TOKEN_MINUS:
            number, error = number.multiplied_by(Number(-1))

        if error:
            return response.failure(error)
        return response.success(
            number.set_position(node.position_start, node.position_end)
        )

    def visit_BinaryOperationNode(
        self, node: "BinaryOperationNode", context: "Context"
    ) -> float:
        response = RunTimeResult()
        left_node = response.register(self.visit(node.left_node, context))
        if response.error:
            return response
        right_node = response.register(self.visit(node.right_node, context))
        if response.error:
            return response

        if node.operator_token.type == TOKEN_PLUS:
            result, error = left_node.added_to(right_node)
        elif node.operator_token.type == TOKEN_MINUS:
            result, error = left_node.subtracted_by(right_node)
        elif node.operator_token.type == TOKEN_MUL:
            result, error = left_node.multiplied_by(right_node)
        elif node.operator_token.type == TOKEN_DIV:
            result, error = left_node.divided_by(right_node)

        if error:
            return response.failure(error)
        return response.success(
            result.set_position(node.position_start, node.position_end)
        )


def run(file_name: str, text: str) -> tuple[list["Token"], Error]:
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return [], error

    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return [], ast.error

    interpreter = Interpreter()
    context = Context("<program>")
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
