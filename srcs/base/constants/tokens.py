TOKEN_INT           = "INT"
TOKEN_FLOAT         = "FLOAT"
TOKEN_STRING        = "STRING"

TOKEN_IDENTIFIER    = "IDENTIFIER"
TOKEN_KEYWORD       = "KEYWORD"

TOKEN_PLUS          = "PLUS"
TOKEN_MINUS         = "MINUS"
TOKEN_MUL           = "MUL"
TOKEN_DIV           = "DIV"
TOKEN_MOD           = "MOD"
TOKEN_POW           = "POW"
TOKEN_EQ            = "EQ"
TOKEN_EEQ           = "EEQ"
TOKEN_NEQ           = "NEQ"
TOKEN_LT            = "LT"
TOKEN_LTE           = "LTE"
TOKEN_GT            = "GT"
TOKEN_GTE           = "GTE"

TOKEN_LPAREN        = "LPAREN"
TOKEN_RPAREN        = "RPAREN"
TOKEN_LSQUARE       = "LSQUARE"
TOKEN_RSQUARE       = "RSQUARE"

TOKEN_COMMA			= "COMMA"
TOKEN_ARROW			= "ARROW"
TOKEN_NEWLINE       = "NEWLINE"

TOKEN_EOF           = "EOF"

NUMERIC             = "0123456789"
ALPHABETIC          = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHANUMERIC        = ALPHABETIC + NUMERIC + "_"

KEYWORD_VARIABLE	= "auto"
KEYWORD_AND			= "and"
KEYWORD_OR			= "or"
KEYWORD_THEN		= "then"
KEYWORD_FUNCTION    = "const"

KEYWORDS            = [
    KEYWORD_VARIABLE,
    KEYWORD_AND,
    KEYWORD_OR,
    "not",
    "if",
    KEYWORD_THEN,
    "elif",
    "else",
    "for",
    "to",
    "increment",
    "decrement",
    "while",
    KEYWORD_FUNCTION,
    "end",
    "return",
    "continue",
    "break"
]
