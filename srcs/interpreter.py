from .base.context import Context
from .base.nodes.number_node import NumberNode
from .base.run_time_result import RunTimeResult
from .base.number import Number
from .base.nodes.unary_operation_node import UnaryOperationNode
from .base.nodes.binary_operation_node import BinaryOperationNode
from .base.constants.tokens import *
from .errors.run_time_error import RunTimeError
from .base.nodes.variable_access_node import VariableAccessNode
from .base.nodes.variable_assign_node import VariableAssignNode
from .base.nodes.if_node import IfNode
from .base.nodes.for_node import ForNode
from .base.nodes.while_node import WhileNode
from .base.nodes.function_definition_node import FunctionDefinitionNode
from .base.nodes.function_call_node import FunctionCallNode
from .base.function import Function
from .base.nodes.string_node import StringNode
from .base.string import String
from .base.nodes.list_node import ListNode
from .base.list import List


class Interpreter:
    def __init__(self) -> None:
        pass

    def visit(self, node, context: "Context") -> "Number":
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context: "Context") -> None:
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_NumberNode(self, node: "NumberNode", context: "Context") -> "Number":
        return RunTimeResult().success(
            Number(node.token.value)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )

    def visit_StringNode(self, node: "StringNode", context: "Context") -> "String":
        return RunTimeResult().success(
            String(node.token.value)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )

    def visit_ListNode(self, node: "ListNode", context: "Context") -> "List":
        response = RunTimeResult()
        elements = []
        for element_node in node.element_nodes:
            elements.append(response.register(self.visit(element_node, context)))
            if response.error:
                return response
        return response.success(
            List(elements)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )

    def visit_UnaryOperationNode(
        self, node: "UnaryOperationNode", context: "Context"
    ) -> "Number":
        response = RunTimeResult()
        number = response.register(self.visit(node.node, context))
        if response.error:
            return response

        error = None
        if node.operator_token.type == TOKEN_MINUS:
            number, error = number.multiplied_by(Number(-1))
        elif node.operator_token.matches(TOKEN_KEYWORD, "not"):
            number, error = number.notted()

        if error:
            return response.failure(error)
        return response.success(
            number.set_position(node.position_start, node.position_end)
        )

    def visit_BinaryOperationNode(
        self, node: "BinaryOperationNode", context: "Context"
    ) -> "Number":
        response = RunTimeResult()
        left_node: "Number" = response.register(self.visit(node.left_node, context))
        if response.error:
            return response
        right_node: "Number" = response.register(self.visit(node.right_node, context))
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
        elif node.operator_token.type == TOKEN_MOD:
            result, error = left_node.moduled_by(right_node)
        elif node.operator_token.type == TOKEN_POW:
            result, error = left_node.powered_by(right_node)
        elif node.operator_token.type == TOKEN_EEQ:
            result, error = left_node.get_comparison_eq(right_node)
        elif node.operator_token.type == TOKEN_NEQ:
            result, error = left_node.get_comparison_neq(right_node)
        elif node.operator_token.type == TOKEN_LT:
            result, error = left_node.get_comparison_lt(right_node)
        elif node.operator_token.type == TOKEN_LTE:
            result, error = left_node.get_comparison_lte(right_node)
        elif node.operator_token.type == TOKEN_GT:
            result, error = left_node.get_comparison_gt(right_node)
        elif node.operator_token.type == TOKEN_GTE:
            result, error = left_node.get_comparison_gte(right_node)
        elif node.operator_token.matches(TOKEN_KEYWORD, KEYWORD_AND):
            result, error = left_node.anded_by(right_node)
        elif node.operator_token.matches(TOKEN_KEYWORD, KEYWORD_OR):
            result, error = left_node.ored_by(right_node)

        if error:
            return response.failure(error)
        return response.success(
            result.set_position(node.position_start, node.position_end)
        )

    def visit_VariableAccessNode(
        self, node: "VariableAccessNode", context: "Context"
    ) -> "RunTimeResult":
        response = RunTimeResult()
        variable_name = node.variable_name_token.value
        value = context.symbol_table.get(variable_name)
        if not value:
            return response.failure(
                RunTimeError(
                    node.position_start,
                    node.position_end,
                    f"'{variable_name}' is not defined",
                    context,
                )
            )
        value = value.copy().set_position(node.position_start, node.position_end)
        return response.success(value)

    def visit_VariableAssignNode(
        self, node: "VariableAssignNode", context: "Context"
    ) -> float:
        response = RunTimeResult()
        variable_name = node.variable_name_token.value
        value = response.register(self.visit(node.value_node, context))
        if response.error:
            return response
        context.symbol_table.set(variable_name, value)
        return response.success(value)

    def visit_IfNode(self, node: "IfNode", context: "Context") -> "RunTimeResult":
        response = RunTimeResult()

        for condition, expr in node.cases:
            condition_value = response.register(self.visit(condition, context))
            if response.error:
                return response
            if condition_value.is_true():
                expr_value = response.register(self.visit(expr, context))
                if response.error:
                    return response
                return response.success(expr_value)

        if node.else_case:
            else_value = response.register(self.visit(node.else_case, context))
            if response.error:
                return response
            return response.success(else_value)

        return response.success(None)

    def visit_ForNode(self, node: "ForNode", context: "Context") -> "RunTimeResult":
        response = RunTimeResult()
        elements = []

        start_value: "Number" = response.register(self.visit(node.start_value, context))
        if response.error:
            return response

        end_value: "Number" = response.register(self.visit(node.end_value, context))
        if response.error:
            return response

        if node.increment_value:
            increment_value: "Number" = response.register(
                self.visit(node.increment_value, context)
            )
            if response.error:
                return response
        else:
            increment_value = Number(1)

        i = start_value.value

        if increment_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.token.value, Number(i))
            i += increment_value.value

            elements.append(response.register(self.visit(node.body, context)))
            if response.error:
                return response

        return response.success(
            List(elements)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )

    def visit_WhileNode(self, node: "WhileNode", context: "Context") -> "RunTimeResult":
        response = RunTimeResult()
        elements = []

        while True:
            condition: "Number" = response.register(self.visit(node.condition, context))
            if response.error:
                return response

            if not condition.is_true():
                break

            elements.append(response.register(self.visit(node.body, context)))
            if response.error:
                return response

        return response.success(
            List(elements)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )

    def visit_FunctionDefinitionNode(
        self, node: "FunctionDefinitionNode", context: "Context"
    ) -> "RunTimeResult":
        response = RunTimeResult()
        function_name = node.token.value if node.token else None
        function_body = node.body
        function_arguments = [argument.value for argument in node.arguments]
        function_value = (
            Function(function_name, function_body, function_arguments)
            .set_context(context)
            .set_position(node.position_start, node.position_end)
        )
        if node.token:
            context.symbol_table.set(function_name, function_value)
        return response.success(function_value)

    def visit_FunctionCallNode(
        self, node: "FunctionCallNode", context: "Context"
    ) -> "RunTimeResult":
        response = RunTimeResult()
        arguments = []
        value_to_call: "Function" = response.register(
            self.visit(node.node_to_call, context)
        )
        if response.error:
            return response
        value_to_call = value_to_call.copy().set_position(
            node.position_start, node.position_end
        )
        for argument_node in node.arguments:
            arguments.append(response.register(self.visit(argument_node, context)))
            if response.error:
                return response
        return_value = response.register(value_to_call.execute(arguments))
        if response.error:
            return response
        return response.success(return_value)
