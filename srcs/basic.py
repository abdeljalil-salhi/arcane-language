class Error:
    def __init__(self, position_start: 'Position', position_end: 'Position', name: str, details: str) -> None:
        self.position_start = position_start
        self.position_end = position_end
        self.name = name
        self.details = details
    
    def as_string(self) -> str:
        result = f'{self.name}: {self.details}\n'
        result += f'File {self.position_start.file_name}, line {self.position_start.line + 1}'
        return result

class IllegalCharacterError(Error):
    def __init__(self, position_start: 'Position', position_end: 'Position', details: str) -> None:
        super().__init__(position_start, position_end, "Illegal Character", details)

class Position:
    def __init__(self, index: int, line: int, column: int, file_name: str, file_text: str) -> None:
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name
        self.file_text = file_text
    
    def advance(self, current_character: str) -> 'Position':
        self.index += 1
        self.column += 1

        if current_character == '\n':
            self.line += 1
            self.column = 0
        
        return self

    def copy(self) -> 'Position':
        return Position(self.index, self.line, self.column, self.file_name, self.file_text)

TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_PLUS = 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_MUL = 'MUL'
TOKEN_DIV = 'DIV'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN = 'RPAREN'

class Token:
    def __init__(self, _type: str, value: str = None) -> None:
        self.type = _type
        self.value = value
    
    def __repr__(self) -> str:
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer:
    def __init__(self, file_name: str, text: str) -> None:
        self.file_name = file_name
        self.text = text
        self.position = Position(-1, 0, -1, self.file_name, self.text)
        self.current_character = None
        
        self.advance()
    
    def advance(self) -> None:
        self.position.advance(self.current_character)
        self.current_character = self.text[self.position.index] if self.position.index < len(self.text) else None

    def make_tokens(self) -> tuple[list['Token'], Error]:
        tokens = []
        
        while self.current_character:
            if self.current_character in ' \t':
                self.advance()
            elif self.current_character in '0123456789':
                tokens.append(self.make_number())
            elif self.current_character == '+':
                tokens.append(Token(TOKEN_PLUS))
                self.advance()
            elif self.current_character == '-':
                tokens.append(Token(TOKEN_MINUS))
                self.advance()
            elif self.current_character == '*':
                tokens.append(Token(TOKEN_MUL))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(TOKEN_DIV))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TOKEN_LPAREN))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TOKEN_RPAREN))
                self.advance()
            else:
                position_start = self.position.copy()
                char = self.current_character
                self.advance()
                return [], IllegalCharacterError(position_start, self.position, f"'{char}'")
        
        return tokens, None

    def make_number(self) -> 'Token':
        number_string = ''
        dot_count = 0

        while self.current_character and self.current_character in '0123456789.':
            if self.current_character == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                number_string += '.'
            else:
                number_string += self.current_character
            self.advance()
        
        if dot_count == 0:
            return Token(TOKEN_INT, int(number_string))
        return Token(TOKEN_FLOAT, float(number_string))
    
def run(file_name: str, text: str) -> tuple[list['Token'], Error]:
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
