from .base.token import Token
from .base.constants.tokens import *
from .base.nodes.binary_operation_node import BinaryOperationNode
from .errors.invalid_syntax_error import InvalidSyntaxError
from .base.parse_result import ParseResult
from .base.nodes.number_node import NumberNode
from .base.nodes.string_node import StringNode
from .base.nodes.unary_operation_node import UnaryOperationNode
from .base.nodes.variable_access_node import VariableAccessNode
from .base.nodes.variable_assign_node import VariableAssignNode
from .base.nodes.if_node import IfNode
from .base.nodes.for_node import ForNode
from .base.nodes.while_node import WhileNode
from .base.nodes.function_definition_node import FunctionDefinitionNode
from .base.nodes.function_call_node import FunctionCallNode
from .base.nodes.list_node import ListNode
from .base.nodes.return_node import ReturnNode
from .base.nodes.continue_node import ContinueNode
from .base.nodes.break_node import BreakNode


class Parser:
    def __init__(self, tokens: list["Token"]) -> None:
        self.tokens = tokens
        self.token_index = -1
        self.current_token: "Token" = None

        self.advance()

    def advance(self) -> "Token":
        self.token_index += 1
        self.update_current_token()
        return self.current_token

    def reverse(self, count: int = 1) -> "Token":
        self.token_index -= count
        self.update_current_token()
        return self.current_token

    def update_current_token(self) -> None:
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def parse(self) -> "BinaryOperationNode":
        response = self.statements()
        if not response.error and self.current_token.type != TOKEN_EOF:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '+', '-', '*', or '/', '^', '%', '==', '!=', '<', '<=', '>', '>=', '{KEYWORD_AND}' or '{KEYWORD_OR}'",
                )
            )
        return response

    def call(self) -> "NumberNode":
        response = ParseResult()
        atom: "NumberNode" = response.register(self.atom())
        if response.error:
            return response

        if self.current_token.type == TOKEN_LPAREN:
            response.register_advance(self.advance)
            argument_nodes: list["BinaryOperationNode"] = []

            if self.current_token.type == TOKEN_RPAREN:
                response.register_advance(self.advance)
            else:
                argument_nodes.append(response.register(self.expr()))
                if response.error:
                    return response.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            f"Expected ')', '{KEYWORD_VARIABLE}', int, float, identifier, '+', '-', '(', '[' or 'not'",
                        )
                    )

                while self.current_token.type == TOKEN_COMMA:
                    response.register_advance(self.advance)
                    argument_nodes.append(response.register(self.expr()))
                    if response.error:
                        return response

                if self.current_token.type != TOKEN_RPAREN:
                    return response.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            f"Expected ',' or ')'",
                        )
                    )
                response.register_advance(self.advance)
            return response.success(FunctionCallNode(atom, argument_nodes))
        return response.success(atom)

    def atom(self) -> "NumberNode":
        response = ParseResult()
        token = self.current_token

        if token.type in (TOKEN_INT, TOKEN_FLOAT):
            response.register_advance(self.advance)
            return response.success(NumberNode(token))

        elif token.type == TOKEN_STRING:
            response.register_advance(self.advance)
            return response.success(StringNode(token))

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

        elif token.type == TOKEN_LSQUARE:
            list_expr = response.register(self.list_expr())
            if response.error:
                return response
            return response.success(list_expr)

        elif token.matches(TOKEN_KEYWORD, "if"):
            if_expr = response.register(self.if_expr())
            if response.error:
                return response
            return response.success(if_expr)

        elif token.matches(TOKEN_KEYWORD, "for"):
            for_expr = response.register(self.for_expr())
            if response.error:
                return response
            return response.success(for_expr)

        elif token.matches(TOKEN_KEYWORD, "while"):
            while_expr = response.register(self.while_expr())
            if response.error:
                return response
            return response.success(while_expr)

        elif token.matches(TOKEN_KEYWORD, KEYWORD_FUNCTION):
            func_def = response.register(self.func_def())
            if response.error:
                return response
            return response.success(func_def)

        return response.failure(
            InvalidSyntaxError(
                token.position_start,
                token.position_end,
                f"Expected int, float, identifier, '+', '-', '(', '[', 'if', 'for', 'while', or '{KEYWORD_FUNCTION}'",
            )
        )

    def power(self) -> "BinaryOperationNode":
        return self.binary_operation(self.call, (TOKEN_POW,), self.factor)

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
                    "Expected int, float, identifier, '+', '-', '(', '[' or 'not'",
                )
            )
        return response.success(node)

    def arith_expr(self) -> "BinaryOperationNode":
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS))

    def list_expr(self) -> "ListNode":
        response = ParseResult()
        element_nodes = []
        position_start = self.current_token.position_start.copy()

        if self.current_token.type != TOKEN_LSQUARE:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '['",
                )
            )
        response.register_advance(self.advance)

        if self.current_token.type == TOKEN_RSQUARE:
            response.register_advance(self.advance)
        else:
            element_nodes.append(response.register(self.expr()))
            if response.error:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        f"Expected ']', 'if', 'for', 'while', '{KEYWORD_FUNCTION}', int, float, identifier, '+', '-', '(', '[' or 'not'",
                    )
                )

            while self.current_token.type == TOKEN_COMMA:
                response.register_advance(self.advance)
                element_nodes.append(response.register(self.expr()))
                if response.error:
                    return response

            if self.current_token.type != TOKEN_RSQUARE:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ',' or ']'",
                    )
                )
            response.register_advance(self.advance)

        return response.success(
            ListNode(
                element_nodes, position_start, self.current_token.position_end.copy()
            )
        )

    def if_expr(self) -> "BinaryOperationNode":
        response = ParseResult()
        all_cases = response.register(self.condition_expr("if"))
        if response.error:
            return response

        cases, else_case = all_cases
        return response.success(IfNode(cases, else_case))

    def elif_expr(self) -> "BinaryOperationNode":
        return self.condition_expr("elif")

    def else_expr(self) -> "BinaryOperationNode":
        response = ParseResult()
        else_case = None

        if self.current_token.matches(TOKEN_KEYWORD, "else"):
            response.register_advance(self.advance)

            if self.current_token.type == TOKEN_NEWLINE:
                response.register_advance(self.advance)
                statements = response.register(self.statements())
                if response.error:
                    return response
                else_case = (statements, True)

                if self.current_token.matches(TOKEN_KEYWORD, "end"):
                    response.register_advance(self.advance)
                else:
                    return response.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            f"Expected 'end'",
                        )
                    )
            else:
                expr = response.register(self.statement())
                if response.error:
                    return response
                else_case = (expr, False)

        return response.success(else_case)

    def condition_expr(self, case_keyword: str) -> "BinaryOperationNode":
        response = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(TOKEN_KEYWORD, case_keyword):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '{case_keyword}'",
                )
            )
        response.register_advance(self.advance)
        condition = response.register(self.expr())
        if response.error:
            return response

        if not self.current_token.matches(TOKEN_KEYWORD, KEYWORD_THEN):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '{KEYWORD_THEN}'",
                )
            )
        response.register_advance(self.advance)

        if self.current_token.type == TOKEN_NEWLINE:
            response.register_advance(self.advance)
            statements = response.register(self.statements())
            if response.error:
                return response
            cases.append((condition, statements, True))

            if self.current_token.matches(TOKEN_KEYWORD, "end"):
                response.register_advance(self.advance)
            else:
                all_cases = response.register(self.secondary_condition_expr())
                if response.error:
                    return response
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = response.register(self.statement())
            if response.error:
                return response
            cases.append((condition, expr, False))

            all_cases = response.register(self.secondary_condition_expr())
            if response.error:
                return response
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return response.success((cases, else_case))

    def secondary_condition_expr(self) -> "BinaryOperationNode":
        response = ParseResult()
        cases = []
        else_case = None

        if self.current_token.matches(TOKEN_KEYWORD, "elif"):
            all_cases = response.register(self.elif_expr())
            if response.error:
                return response
            cases, else_case = all_cases
        else:
            else_case = response.register(self.else_expr())
            if response.error:
                return response

        return response.success((cases, else_case))

    def for_expr(self) -> "BinaryOperationNode":
        response = ParseResult()

        if not self.current_token.matches(TOKEN_KEYWORD, "for"):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'for'",
                )
            )
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

        start_value = response.register(self.expr())
        if response.error:
            return response

        if not self.current_token.matches(TOKEN_KEYWORD, "to"):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'to'",
                )
            )
        response.register_advance(self.advance)

        end_value = response.register(self.expr())
        if response.error:
            return response

        if self.current_token.matches(TOKEN_KEYWORD, "increment"):
            response.register_advance(self.advance)
            increment_value = response.register(self.expr())
            if response.error:
                return response
        elif self.current_token.matches(TOKEN_KEYWORD, "decrement"):
            response.register_advance(self.advance)
            increment_value: "NumberNode" = response.register(self.expr())
            if response.error:
                return response
            increment_value.token.value *= -1
        else:
            increment_value = None

        if not self.current_token.matches(TOKEN_KEYWORD, KEYWORD_THEN):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '{KEYWORD_THEN}'",
                )
            )
        response.register_advance(self.advance)

        if self.current_token.type == TOKEN_NEWLINE:
            response.register_advance(self.advance)
            body = response.register(self.statements())
            if response.error:
                return response

            if not self.current_token.matches(TOKEN_KEYWORD, "end"):
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected 'end'",
                    )
                )
            response.register_advance(self.advance)

            return response.success(
                ForNode(identifier, start_value, end_value, increment_value, body, True)
            )

        body = response.register(self.statement())
        if response.error:
            return response

        return response.success(
            ForNode(identifier, start_value, end_value, increment_value, body, False)
        )

    def while_expr(self) -> "BinaryOperationNode":
        response = ParseResult()

        if not self.current_token.matches(TOKEN_KEYWORD, "while"):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'while'",
                )
            )
        response.register_advance(self.advance)

        condition = response.register(self.expr())
        if response.error:
            return response

        if not self.current_token.matches(TOKEN_KEYWORD, KEYWORD_THEN):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '{KEYWORD_THEN}'",
                )
            )
        response.register_advance(self.advance)

        if self.current_token.type == TOKEN_NEWLINE:
            response.register_advance(self.advance)
            body = response.register(self.statements())
            if response.error:
                return response

            if not self.current_token.matches(TOKEN_KEYWORD, "end"):
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected 'end'",
                    )
                )
            response.register_advance(self.advance)

            return response.success(WhileNode(condition, body, True))

        body = response.register(self.statement())
        if response.error:
            return response

        return response.success(WhileNode(condition, body, False))

    def statements(self) -> "ListNode":
        response = ParseResult()
        statements = []
        position_start = self.current_token.position_start.copy()

        while self.current_token.type == TOKEN_NEWLINE:
            response.register_advance(self.advance)

        statement = response.register(self.statement())
        if response.error:
            return response
        statements.append(statement)

        more_statements = True
        while True:
            newline_count = 0
            while self.current_token.type == TOKEN_NEWLINE:
                response.register_advance(self.advance)
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            if not more_statements:
                break
            statement = response.try_register(self.statement())
            if not statement:
                self.reverse(response.reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return response.success(
            ListNode(
                statements, position_start, self.current_token.position_start.copy()
            )
        )

    def statement(self) -> "BinaryOperationNode":
        response = ParseResult()
        position_start = self.current_token.position_start.copy()

        if self.current_token.matches(TOKEN_KEYWORD, "return"):
            response.register_advance(self.advance)

            expr = response.try_register(self.expr())
            if not expr:
                self.reverse(response.reverse_count)
            return response.success(
                ReturnNode(
                    expr, position_start, self.current_token.position_start.copy()
                )
            )

        if self.current_token.matches(TOKEN_KEYWORD, "continue"):
            response.register_advance(self.advance)

            return response.success(
                ContinueNode(position_start, self.current_token.position_start.copy())
            )

        if self.current_token.matches(TOKEN_KEYWORD, "break"):
            response.register_advance(self.advance)

            return response.success(
                BreakNode(position_start, self.current_token.position_start.copy())
            )

        expr = response.register(self.expr())
        if response.error:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected 'return', 'continue', 'break', 'if', 'for', 'while', '{KEYWORD_FUNCTION}', int, float, identifier, '+', '-', '(', '[' or 'not'",
                )
            )

        return response.success(expr)

    def expr(self) -> "BinaryOperationNode":
        response = ParseResult()

        if self.current_token.matches(TOKEN_KEYWORD, KEYWORD_VARIABLE):
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
                self.comp_expr,
                ((TOKEN_KEYWORD, KEYWORD_AND), (TOKEN_KEYWORD, KEYWORD_OR)),
            )
        )
        if response.error:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '{KEYWORD_VARIABLE}', 'if', 'for', 'while', '{KEYWORD_FUNCTION}', int, float, identifier, '+', '-', '(', '[' or 'not'",
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

    def func_def(self):
        response = ParseResult()

        if not self.current_token.matches(TOKEN_KEYWORD, KEYWORD_FUNCTION):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    f"Expected '{KEYWORD_FUNCTION}'",
                )
            )
        response.register_advance(self.advance)

        if self.current_token.type == TOKEN_IDENTIFIER:
            identifier_token = self.current_token
            response.register_advance(self.advance)
            if self.current_token.type != TOKEN_LPAREN:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected '('",
                    )
                )
        else:
            identifier_token = None
            if self.current_token.type != TOKEN_LPAREN:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier or '('",
                    )
                )
        response.register_advance(self.advance)

        argument_name_tokens = []
        if self.current_token.type == TOKEN_IDENTIFIER:
            argument_name_tokens.append(self.current_token)
            response.register_advance(self.advance)
            while self.current_token.type == TOKEN_COMMA:
                response.register_advance(self.advance)
                if self.current_token.type != TOKEN_IDENTIFIER:
                    return response.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            "Expected identifier",
                        )
                    )
                argument_name_tokens.append(self.current_token)
                response.register_advance(self.advance)
            if self.current_token.type != TOKEN_RPAREN:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected ',' or ')'",
                    )
                )
        else:
            if self.current_token.type != TOKEN_RPAREN:
                return response.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier or ')'",
                    )
                )
        response.register_advance(self.advance)

        if self.current_token.type == TOKEN_ARROW:
            response.register_advance(self.advance)

            node_to_return: "BinaryOperationNode" = response.register(self.expr())
            if response.error:
                return response

            return response.success(
                FunctionDefinitionNode(
                    identifier_token, argument_name_tokens, node_to_return, True
                )
            )

        if self.current_token.type != TOKEN_NEWLINE:
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected '=>' or new line",
                )
            )
        response.register_advance(self.advance)

        body = response.register(self.statements())
        if response.error:
            return response

        if not self.current_token.matches(TOKEN_KEYWORD, "end"):
            return response.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'end'",
                )
            )
        response.register_advance(self.advance)

        return response.success(
            FunctionDefinitionNode(identifier_token, argument_name_tokens, body, False)
        )
