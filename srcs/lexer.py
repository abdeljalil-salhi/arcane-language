from .base.position import Position
from .base.token import Token
from .base.constants.tokens import *
from .errors.base_error import BaseError
from .errors.illegal_character_error import IllegalCharacterError
from .errors.expected_character_error import ExpectedCharacterError


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
            elif self.current_character in NUMERIC:
                tokens.append(self.make_number())
            elif self.current_character in ALPHABETIC:
                tokens.append(self.make_identifier())
            elif self.current_character == '"':
                tokens.append(self.make_string())
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
            elif self.current_character == "%":
                tokens.append(Token(TOKEN_MOD, position_start=self.position))
                self.advance()
            elif self.current_character == "^":
                tokens.append(Token(TOKEN_POW, position_start=self.position))
                self.advance()
            elif self.current_character == "(":
                tokens.append(Token(TOKEN_LPAREN, position_start=self.position))
                self.advance()
            elif self.current_character == ")":
                tokens.append(Token(TOKEN_RPAREN, position_start=self.position))
                self.advance()
            elif self.current_character == "[":
                tokens.append(Token(TOKEN_LSQUARE, position_start=self.position))
                self.advance()
            elif self.current_character == "]":
                tokens.append(Token(TOKEN_RSQUARE, position_start=self.position))
                self.advance()
            elif self.current_character == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_character == "=":
                tokens.append(self.make_equals())
            elif self.current_character == "<":
                tokens.append(self.make_less_than())
            elif self.current_character == ">":
                tokens.append(self.make_greater_than())
            elif self.current_character == ",":
                tokens.append(Token(TOKEN_COMMA, position_start=self.position))
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

        while self.current_character and self.current_character in NUMERIC + ".":
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

    def make_identifier(self) -> "Token":
        identifier_string = ""
        position_start = self.position.copy()

        while self.current_character and self.current_character in ALPHANUMERIC:
            identifier_string += self.current_character
            self.advance()

        token_type = (
            TOKEN_KEYWORD if identifier_string in KEYWORDS else TOKEN_IDENTIFIER
        )

        return Token(token_type, identifier_string, position_start, self.position)

    def make_string(self) -> "Token":
        string = ""
        position_start = self.position.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            "n": "\n",
            "t": "\t",
        }

        while self.current_character and (
            self.current_character != '"' or escape_character
        ):
            if escape_character:
                string += escape_characters.get(
                    self.current_character, self.current_character
                )
            else:
                if self.current_character == "\\":
                    escape_character = True
                else:
                    string += self.current_character
            self.advance()
            escape_character = False

        self.advance()
        return Token(TOKEN_STRING, string, position_start, self.position)

    def make_not_equals(self) -> tuple["Token", BaseError]:
        position_start = self.position.copy()
        self.advance()

        if self.current_character == "=":
            self.advance()
            return (
                Token(
                    TOKEN_NEQ, position_start=position_start, position_end=self.position
                ),
                None,
            )

        self.advance()
        return None, ExpectedCharacterError(
            position_start, self.position, "'=' (after '!')"
        )

    def make_equals(self) -> "Token":
        token_type = TOKEN_EQ
        position_start = self.position.copy()
        self.advance()

        if self.current_character == "=":
            self.advance()
            token_type = TOKEN_EEQ
        elif self.current_character == ">":
            self.advance()
            token_type = TOKEN_ARROW

        return Token(
            token_type, position_start=position_start, position_end=self.position
        )

    def make_greater_than(self) -> "Token":
        token_type = TOKEN_GT
        position_start = self.position.copy()
        self.advance()

        if self.current_character == "=":
            self.advance()
            token_type = TOKEN_GTE

        return Token(
            token_type, position_start=position_start, position_end=self.position
        )

    def make_less_than(self) -> "Token":
        token_type = TOKEN_LT
        position_start = self.position.copy()
        self.advance()

        if self.current_character == "=":
            self.advance()
            token_type = TOKEN_LTE

        return Token(
            token_type, position_start=position_start, position_end=self.position
        )
