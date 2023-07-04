TOKEN_INT           = "INT"
TOKEN_FLOAT         = "FLOAT"

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

TOKEN_EOF           = "EOF"

NUMERIC             = "0123456789"
ALPHABETIC          = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHANUMERIC        = ALPHABETIC + NUMERIC + "_"

KEYWORDS            = [
    "auto",
    "and",
    "or",
    "not",
    "if",
    "then",
    "elif",
    "else",
    "for",
    "to",
    "increment",
    "decrement",
    "while",
]
