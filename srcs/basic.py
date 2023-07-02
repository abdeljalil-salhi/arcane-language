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

class NumberNode:
    def __init__(self, token: 'Token') -> None:
        self.token = token
    
    def __repr__(self) -> str:
        return f'{self.token}'

class BinaryOperationNode:
    def __init__(self, left_node: 'NumberNode', operator_token: 'Token', right_node: 'NumberNode') -> None:
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
    
    def __repr__(self) -> str:
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'

class Parser:
    def __init__(self, tokens: list['Token']) -> None:
        self.tokens = tokens
        self.token_index = -1
        
        self.advance()
    
    def advance(self) -> None:
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self) -> 'BinaryOperationNode':
        return self.expr()
    
    def factor(self) -> 'NumberNode':
        token = self.current_token
        if token.type in (TOKEN_INT, TOKEN_FLOAT):
            self.advance()
            return NumberNode(token)
    
    def term(self) -> 'BinaryOperationNode':
        return self.binary_operation(self.factor, (TOKEN_MUL, TOKEN_DIV))
    
    def expr(self) -> 'BinaryOperationNode':
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS))
    
    def binary_operation(self, function, operation_tokens: list['Token']) -> 'BinaryOperationNode':
        left_node = function()
        while self.current_token.type in operation_tokens:
            operator_token = self.current_token
            self.advance()
            right_node = function()
            left_node = BinaryOperationNode(left_node, operator_token, right_node)
        return left_node
        

def run(file_name: str, text: str) -> tuple[list['Token'], Error]:
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return [], error
    
    parser = Parser(tokens)
    ast = parser.parse()

    return ast, None
