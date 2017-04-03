# Quinlan Bingham
# mytoken.py
# HW2
# This file creates the Tokens and formats the output for the tokens


PRINT = 'PRINT'
PRINTLN = 'PRINTLN'
READINT = 'READINT'
READSTR = 'READSTR'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
SEMICOLON = 'SEMICOLON'
ID = 'ID'
STRING = 'STRING'
THEN = 'THEN'
ELSEIF = 'ELSEIF'
IF = 'IF'
ELSE = 'ELSE'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
EQUAL = 'EQUAL'
NOT_EQUAL = 'NOT_EQUAL'
GREATER_THAN = 'GREATER_THAN'
LESS_THAN = 'LESS_THAN'
GREATER_THAN_EQUAL = 'GREATER_THAN_EQUAL'
LESS_THAN_EQUAL = 'LESS_THAN_EQUAL'
WHILE = 'WHILE'
DO = 'DO'
END = 'END'
INT = 'INT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MODULUS = 'MODLUS'
MULTIPLY = 'MULTIPLY'
DIVIDE= 'DIVIDE'
EOS = 'EOS'
BOOL = 'BOOL'
RBRACKET = 'RBRACKET'
LBRACKET = 'LBRACKET'
COMMA = 'COMMA'
ASSIGN = 'ASSIGN'



class Token(object):
    # constructor creates an instance of a Token
    def __init__(self, tokentype, lexeme, line, column):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.line = line
        self.column = column

    # formats the output string for the token
    def __str__(self):
        tokenStr = str(self.tokentype)
        tokenStr += " '" + self.lexeme
        tokenStr += "' " + str(self.line)
        tokenStr += ":" + str(self.column)

        return tokenStr