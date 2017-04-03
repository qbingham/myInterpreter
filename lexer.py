# Quinlan Bingham
# lexer.py
# HW2
# This file is responsible for iterating over the input stream and
# identifying tokens for the Token class

from mytoken import *
from error import *


class Lexer(object):
    # the constructor places us at the beginning of the file
    def __init__(self, input_stream):
        self.line = 1
        self.column = 0
        self.input_stream = input_stream

    # the peek method returns the symbol at the current line and column
    # without jumping over to the next column afterwards
    def __peek(self):
        pos = self.input_stream.tell()
        symbol = self.input_stream.read(1)
        self.input_stream.seek(pos)
        return symbol

    # the read method returns the symbol at the current line and column
    # and moves over to the next column
    def __read(self):
        return self.input_stream.read(1)

    # the next_token method is the backbone of the lexical analyzer
    # it is responsible for recognizing every lexeme and providing its token
    def next_token(self):
        if self.__peek() == '':
            return Token(EOS, '', self.line, self.column)
        # stores each character in the input_stream in the symbol variable
        # and checks for a token match one at a time
        symbol = str(self.__read())
        self.column += 1


        # Syntactic tokens
        # if there's a match, this returns a new Token object
        if symbol == ';':
            return Token(SEMICOLON, ';', self.line, self.column)
        elif symbol == '[':
            return Token(LBRACKET, '[', self.line, self.column)
        elif symbol == ']':
            return Token(RBRACKET, ']', self.line, self.column)
        elif symbol == '(':
            return Token(LPAREN, '(', self.line, self.column)
        elif symbol == ')':
            return Token(RPAREN, ')', self.line, self.column)
        elif symbol == ',':
            return Token(COMMA, ',', self.line, self.column)

        # Operator tokens

        # Distinguishes between ">" and ">=" by checking if there is a "="
        # following the ">"
        elif symbol == '>':
            start_column = self.column
            if str(self.__read()) == '=':
                return Token(GREATER_THAN_EQUAL, '>=', self.line, start_column)
            else:
                return Token(GREATER_THAN, '>', self.line, start_column)

        # Distinguishes between "<" and "<=" by checking if there is a "="
        # following the "<"
        elif symbol == '<':
            start_column = self.column
            if str(self.__read()) == '=':
                return Token(LESS_THAN_EQUAL, '<=', self.line, start_column)
            else:
                return Token(LESS_THAN, '<', self.line, start_column)

        # Distinguishes between = and == in the same way
        elif symbol == '=':
            start_column = self.column
            if str(self.__read()) == '=':
                return Token(EQUAL, '==', self.line, start_column)
            else:
                return Token(ASSIGN, '=', self.line, start_column)

        elif symbol == '!':
            start_column = self.column
            if str(self.__read()) == '=':
                return Token(NOT_EQUAL, '!=', self.line, start_column)

        elif symbol == '+':
            return Token(PLUS, '+', self.line, self.column)
        elif symbol == '-':
            return Token(MINUS, '-', self.line, self.column)
        elif symbol == '*':
            return Token(MULTIPLY, '*', self.line, self.column)
        elif symbol == '/':
            return Token(DIVIDE, '/', self.line, self.column)
        elif symbol == '%':
            return Token(MODULUS, '%', self.line, self.column)


        # STRING Token: this was the hardest token to work with because it includes
        # raising an error, and I had to tinker with where to use read/peak worked best
        elif symbol == '"':
            start_column = self.column
            string_lexeme = str(self.__read())
            while str(self.__peek()) != '"':
                string_lexeme += str(self.__read())
                if str(self.__peek()) == '\n':
                    raise Error("Reached newline while reading string", self.line, self.column)
                self.column += 1
            pos = self.input_stream.tell()
            self.input_stream.seek(pos + 1)
            self.column += 2
            return Token(STRING, string_lexeme, self.line, start_column)

        # INT Token: if we encounter a stray integer, we check to see how long it is
        elif symbol.isdigit():
            string_int = symbol
            while str(self.__peek()).isdigit():
                string_int += str(self.__read())
            return Token(INT, string_int, self.line, self.column)

        # ID Token: similar to INT Token except special words (like while, if, and print)
        # are going to be caught by this elifm so we filter all of those out before returning
        # an ID token
        elif symbol.isalpha():
            string_id = symbol
            start_column = self.column
            while str(self.__peek()).isalpha() or str(self.__peek()).isdigit() or str(self.__peek()) == "_":
                string_id += str(self.__read())

            # Filter out special words
            if string_id == "while":
                return Token(WHILE, string_id, self.line, start_column)
            elif string_id == "do":
                return Token(DO, string_id, self.line, start_column)
            elif string_id == "end":
                return Token(END, string_id, self.line, start_column)
            elif string_id == "if":
                return Token(IF, string_id, self.line, start_column)
            elif string_id == "elseif":
                return Token(ELSEIF, string_id, self.line, start_column)
            elif string_id == "else":
                return Token(ELSE, string_id, self.line, start_column)
            elif string_id == "then":
                return Token(THEN, string_id, self.line, start_column)
            elif string_id == "print":
                return Token(PRINT, string_id, self.line, start_column)
            elif string_id == "println":
                return Token(PRINTLN, string_id, self.line, start_column)
            elif string_id == "readint":
                return Token(READINT, string_id, self.line, start_column)
            elif string_id == "readstr":
                return Token(READSTR, string_id, self.line, start_column)
            elif string_id == "true":
                return Token(BOOL, string_id, self.line, start_column)
            elif string_id == "false":
                return Token(BOOL, string_id, self.line, start_column)
            elif string_id == "and":
                return Token(AND, string_id, self.line, start_column)
            elif string_id == "or":
                return Token(OR, string_id, self.line, start_column)
            elif string_id == "not":
                return Token(NOT, string_id, self.line, start_column)

            # If it wasn't one of those special words, then it's an identifier
            else:
                return Token(ID, string_id, self.line, start_column)

        # if it's time for a newline or comment, this increments the
        # line count and resets the column to 0
        elif symbol == '#':
            while str(self.__read()) != '\n':
                self.column += 1
            pos = self.input_stream.tell()
            self.input_stream.seek(pos - 1)
            return self.next_token()

        elif symbol == '\n':
            self.line += 1
            self.column = 0
            return self.next_token()

        elif symbol.isspace():
            return self.next_token()
