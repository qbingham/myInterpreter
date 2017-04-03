# Author: Quinlan Bingham
# Filename: interpreter.py
# Assignment: Assignment 6
# Description: This interpreter takes a text file written in MyPL
# and should return the appropriate output if syntactically correct

import mypl_symbol_table
import mytoken
import mypl_ast as ast
import sys

class Interpreter(ast.Visitor):

    def __init__(self):
        self.sym_table = mypl_symbol_table.SymbolTable()
        self.current_value = None

    def visit_stmt_list(self, stmt_list):
        self.sym_table.push_environment()
        for stmt in stmt_list.stmts:
            stmt.accept(self)
        self.sym_table.pop_environment()

    def visit_simple_bool_expr(self, simple_bool_expr):
        simple_bool_expr.expr.accept(self)

    def visit_complex_bool_expr(self, complex_bool_expr):
        complex_bool_expr.second_expr.accept(self)
        right_hand_val = self.current_value
        complex_bool_expr.first_expr.accept(self)
        left_hand_val = self.current_value

        if complex_bool_expr.bool_rel.tokentype == mytoken.EQUAL:
            if left_hand_val == right_hand_val:
                self.current_value = True
                left_expr = True
            else:
                self.current_value = False
                left_expr = False
        elif complex_bool_expr.bool_rel.tokentype == mytoken.LESS_THAN:
            if left_hand_val < right_hand_val:
                self.current_value = True
                left_expr = True
            else:
                self.current_value = False
                left_expr = False
        elif complex_bool_expr.bool_rel.tokentype == mytoken.LESS_THAN_EQUAL:
            if left_hand_val <= right_hand_val:
                self.current_value = True
                left_expr = True
            else:
                self.current_value = False
                left_expr = False
        elif complex_bool_expr.bool_rel.tokentype == mytoken.GREATER_THAN:
            if left_hand_val > right_hand_val:
                self.current_value = True
                left_expr = True
            else:
                self.current_value = False
                left_expr = False
        else:
            if left_hand_val >= right_hand_val:
                self.current_value = True
                left_expr = True
            else:
                self.current_value = False
                left_expr = False

        if complex_bool_expr.has_bool_connector:
            complex_bool_expr.rest.accept(self)
            if complex_bool_expr.bool_connector.tokentype == mytoken.AND:
                if left_expr and self.current_value:
                    self.current_value = True
                else:
                    self.current_value = False
            else:
                if left_expr or self.current_value:
                    self.current_value = True
                else:
                    self.current_value = False

    def visit_if_stmt(self, if_stmt):
        if_stmt.if_part.bool_expr.accept(self)

        if self.current_value:
            if_stmt.if_part.stmt_list.accept(self)
            for elseif in if_stmt.elseifs:
                elseif.bool_expr.accept(self)
                if self.current_value:
                    elseif.stmt_list.accept(self)
        else:
            for elseif in if_stmt.elseifs:
                elseif.bool_expr.accept(self)
                if self.current_value:
                    elseif.stmt_list.accept(self)
            if if_stmt.has_else:
                if not self.current_value:
                    if_stmt.else_stmts.accept(self)

    def visit_while_stmt(self, while_stmt):
        while_stmt.bool_expr.accept(self)
        if self.current_value:
            while_stmt.stmt_list.accept(self)
            while_stmt.accept(self)

    def visit_print_stmt(self, print_stmt):
        print_stmt.expr.accept(self)
        if type(self.current_value) == bool:
            if self.current_value == True:
                self.__write("true")
            else:
                self.__write("false")
        elif type(self.current_value) == int:
            val = str(self.current_value)
            self.__write(val)
        else:
            self.__write(self.current_value)

        if print_stmt.is_println:
            self.__write("\n")

    def visit_assign_stmt(self, assign_stmt):
        var_name = assign_stmt.lhs.lexeme
        assign_stmt.rhs.accept(self)
        if not(self.sym_table.variable_exists(var_name)):
            self.sym_table.add_variable(var_name)
        self.sym_table.set_variable_value(var_name, self.current_value)

    def visit_simple_expr(self, simple_expr):
        if simple_expr.term.tokentype == mytoken.ID:
            var_name = simple_expr.term.lexeme
            var_val = self.sym_table.get_variable_value(var_name)
            self.current_value = var_val
        elif simple_expr.term.tokentype == mytoken.INT:
            self.current_value = int(simple_expr.term.lexeme)
        elif simple_expr.term.tokentype == mytoken.BOOL:
            if simple_expr.term.lexeme == "true":
                self.current_value = True
            else:
                self.current_value = False
        else:
            self.current_value = simple_expr.term.lexeme

    def visit_index_expr(self, index_expr):
        pass

    def visit_list_expr(self, list_expr):
        pass

    def visit_read_expr(self, read_expr):
        val = raw_input(read_expr.msg.lexeme)
        if read_expr.is_read_int:
            try:
                self.current_value = int(val)
            except ValueError:
                self.current_value = 0
        else:
            self.current_value = val

    def visit_complex_expr(self, complex_expr):
        complex_expr.rest.accept(self)
        right_hand_val = self.current_value
        complex_expr.first_operand.accept(self)
        left_hand_val = self.current_value
        if complex_expr.math_rel.tokentype == mytoken.PLUS:
            self.current_value = left_hand_val + right_hand_val
        elif complex_expr.math_rel.tokentype == mytoken.MINUS:
            self.current_value = left_hand_val - right_hand_val
        elif complex_expr.math_rel.tokentype == mytoken.MULTIPLY:
            self.current_value = left_hand_val * right_hand_val
        elif complex_expr.math_rel.tokentype == mytoken.DIVIDE:
            self.current_value = left_hand_val / right_hand_val
        elif complex_expr.math_rel.tokentype == mytoken.MODULUS:
            self.current_value = left_hand_val % right_hand_val

    def __write(self, msg):
        sys.stdout.write(msg)