from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .base.context import Context
from .base.token import Token
from .errors.base_error import BaseError


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
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
