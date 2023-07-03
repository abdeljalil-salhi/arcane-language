from .base.context import Context
from .base.nodes.number_node import NumberNode
from .base.run_time_result import RunTimeResult
from .base.number import Number
from .base.nodes.unary_operation_node import UnaryOperationNode
from .base.nodes.binary_operation_node import BinaryOperationNode
from .base.token import (
    TOKEN_MINUS,
    TOKEN_PLUS,
    TOKEN_MUL,
    TOKEN_DIV,
    TOKEN_MOD,
    TOKEN_POW,
)
from .errors.run_time_error import RunTimeError
from .base.nodes.variable_access_node import VariableAccessNode
from .base.nodes.variable_assign_node import VariableAssignNode


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

        if error:
            return response.failure(error)
        return response.success(
            result.set_position(node.position_start, node.position_end)
        )

    def visit_VariableAccessNode(
        self, node: "VariableAccessNode", context: "Context"
    ) -> float:
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
