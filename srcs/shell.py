from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .base.context import Context
from .base.token import Token
from .errors.base_error import BaseError
from .base.symbol_table import SymbolTable
from .base.number import Number
from .base.functions.builtin_function import BuiltInFunction

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("PI", Number.PI)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("get_return", BuiltInFunction.get_return)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("is_number", BuiltInFunction.is_number)
global_symbol_table.set("is_string", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_function", BuiltInFunction.is_function)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)


def run(file_name: str, text: str) -> tuple[list["Token"], BaseError]:
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
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
