# Quinlan Bingham
# error.py
# HW2
# This file gives an error notification


class Error(Exception):
    # constructor creates an instance of an error
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column

    # formats the output string for the token
    def __str__(self):
        s = ""
        s += "Error: " + self.message
        s += " at line " + str(self.line)
        s += ", column " + str(self.column)
        return s
