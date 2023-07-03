from .base.token import Token
from .base.constants.tokens import *
from .base.nodes.binary_operation_node import BinaryOperationNode
from .errors.invalid_syntax_error import InvalidSyntaxError
from .base.parse_result import ParseResult
from .base.nodes.number_node import NumberNode
from .base.nodes.unary_operation_node import UnaryOperationNode
from .base.nodes.variable_access_node import VariableAccessNode
from .base.nodes.variable_assign_node import VariableAssignNode


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
                    "Expected '+', '-', '*', or '/', '^', '%', '==', '!=', '<', '<=', '>', '>=', 'and' or 'or'",
                )
            )
        return response

    def atom(self) -> "NumberNode":
        response = ParseResult()
        token = self.current_token

        if token.type in (TOKEN_INT, TOKEN_FLOAT):
            response.register_advance(self.advance)
            return response.success(NumberNode(token))

        elif token.type == TOKEN_IDENTIFIER:
            response.register_advance(self.advance)
            return response.success(VariableAccessNode(token))

        elif token.type == TOKEN_LPAREN:
            response.register_advance(self.advance)
            expr = response.register(self.expr())
            if response.error:
                return response
            if self.current_token.type == TOKEN_RPAREN:
                response.register_advance(self.advance)
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
                token.position_start,
                token.position_end,
                "Expected int, float, identifier, '+', '-' or '('",
            )
        )

    def power(self) -> "BinaryOperationNode":
        return self.binary_operation(self.atom, (TOKEN_POW,), self.factor)

    def factor(self) -> "NumberNode":
        response = ParseResult()
        token = self.current_token

        if token.type in (TOKEN_PLUS, TOKEN_MINUS):
            response.register_advance(self.advance)
            factor = response.register(self.factor())
            if response.error:
                return response
            return response.success(UnaryOperationNode(token, factor))

        return self.power()

    def term(self) -> "BinaryOperationNode":
        return self.binary_operation(self.factor, (TOKEN_MUL, TOKEN_DIV, TOKEN_MOD))

    def comp_expr(self) -> "BinaryOperationNode":
        response = ParseResult()

        if self.current_token.matches(TOKEN_KEYWORD, "not"):
            operator_token = self.current_token
            response.register_advance(self.advance)
            node = response.register(self.comp_expr())
            if response.error:
                return response
            return response.success(UnaryOperationNode(operator_token, node))

        node = response.register(
            self.binary_operation(
                self.arith_expr,
                (
                    TOKEN_EEQ,
                    TOKEN_NEQ,
                    TOKEN_LT,
                    TOKEN_LTE,
                    TOKEN_GT,
                    TOKEN_GTE,
                ),
            )
        )
        if response.error:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected int, float, identifier, '+', '-', '(' or 'not'",
                )
            )
        return response.success(node)

    def arith_expr(self) -> "BinaryOperationNode":
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS))

    def expr(self) -> "BinaryOperationNode":
        response = ParseResult()

        if self.current_token.matches(TOKEN_KEYWORD, "auto"):
            response.register_advance(self.advance)
            if self.current_token.type != TOKEN_IDENTIFIER:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier",
                    )
                )
            identifier = self.current_token
            response.register_advance(self.advance)
            if self.current_token.type != TOKEN_EQ:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected '='",
                    )
                )
            response.register_advance(self.advance)
            expr = response.register(self.expr())
            if response.error:
                return response
            return response.success(VariableAssignNode(identifier, expr))

        node = response.register(
            self.binary_operation(
                self.comp_expr, ((TOKEN_KEYWORD, "and"), (TOKEN_KEYWORD, "or"))
            )
        )
        if response.error:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'auto', int, float, identifier, '+', '-', '(' or 'not'",
                )
            )
        return response.success(node)

    def binary_operation(
        self, function_first, operation_tokens: any, function_second=None
    ) -> "BinaryOperationNode":
        if function_second is None:
            function_second = function_first

        response = ParseResult()
        left_node = response.register(function_first())
        if response.error:
            return response
        while (
            self.current_token.type in operation_tokens
            or (
                self.current_token.type,
                self.current_token.value,
            )
            in operation_tokens
        ):
            operator_token = self.current_token
            response.register_advance(self.advance)
            right_node = response.register(function_second())
            if response.error:
                return response
            left_node = BinaryOperationNode(left_node, operator_token, right_node)
        return response.success(left_node)
