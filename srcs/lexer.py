from .base.position import Position
from .base.token import (
    Token,
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_MUL,
    TOKEN_DIV,
    TOKEN_LPAREN,
    TOKEN_RPAREN,
    TOKEN_EOF,
    TOKEN_INT,
    TOKEN_FLOAT,
)
from .errors.base_error import BaseError
from .errors.illegal_character_error import IllegalCharacterError


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

    def make_tokens(self) -> tuple[list["Token"], BaseError]:
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
