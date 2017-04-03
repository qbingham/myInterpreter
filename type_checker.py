# Author: Quinlan Bingham
# Filename: type_checker.py
# Assignment: Assignment 5
# Description: This file sets and checks type throughout a file
# upon variable initialization and variable reference

import mypl_symbol_table
import mytoken
import error
import mypl_ast as ast


class TypeChecker(ast.Visitor):

    def __init__(self):
        self.sym_table = mypl_symbol_table.SymbolTable()
        self.current_type = None

    # visitor functions
    def visit_stmt_list(self, stmt_list):
        self.sym_table.push_environment()
        for stmt in stmt_list.stmts:
            stmt.accept(self)
        self.sym_table.pop_environment()

    def visit_simple_bool_expr(self, simple_bool_expr):
        simple_bool_expr.expr.accept(self)
        if self.current_type != mytoken.BOOL:
            err_msg = "expecting BOOL, found " + self.current_type
            line, column = self.__first_token(simple_bool_expr.expr)
            raise error.Error(err_msg, line, column)

    def visit_complex_bool_expr(self, complex_bool_expr):
        complex_bool_expr.second_expr.accept(self)
        right_hand_type = self.current_type
        complex_bool_expr.first_expr.accept(self)
        if not(right_hand_type == self.current_type):
            err_msg = "expecting " + self.current_type + ", found " + right_hand_type
            line, column = self.__first_token(complex_bool_expr.second_expr)
            raise error.Error(err_msg, line, column)
        if complex_bool_expr.has_bool_connector:
            complex_bool_expr.rest.accept(self)

    def visit_if_stmt(self, if_stmt):
        if_stmt.if_part.bool_expr.accept(self)
        if_stmt.if_part.stmt_list.accept(self)
        for elseif in if_stmt.elseifs:
            elseif.bool_expr.accept(self)
            elseif.stmt_list.accept(self)
        if if_stmt.has_else:
            if_stmt.else_stmts.accept(self)

    def visit_while_stmt(self, while_stmt):
        while_stmt.bool_expr.accept(self)
        while_stmt.stmt_list.accept(self)

    def visit_print_stmt(self, print_stmt):
        print_stmt.expr.accept(self)

    def visit_assign_stmt(self, assign_stmt):
        lhs = assign_stmt.lhs
        var_name = lhs.lexeme
        assign_stmt.rhs.accept(self)
        if not(self.sym_table.variable_exists(var_name)):
            self.sym_table.add_variable(var_name)
        self.sym_table.set_variable_type(var_name, self.current_type)

    def visit_simple_expr(self, simple_expr):
        term = simple_expr.term
        if term.tokentype == mytoken.ID:
            var_name = term.lexeme
            if self.sym_table.variable_exists(var_name):
                var_type = self.sym_table.get_variable_type(var_name)
                self.current_type = var_type
            else:
                err_msg = term.lexeme + " is undefined"
                raise error.Error(err_msg, term.line, term.column)
        else:
            self.current_type = term.tokentype

    def visit_index_expr(self, index_expr):
        pass

    def visit_list_expr(self, list_expr):
        pass

    def visit_read_expr(self, read_expr):
        if read_expr.is_int():
            self.current_type = mytoken.INT
        else:
            self.current_type = mytoken.STRING

    def visit_complex_expr(self, complex_expr):
        complex_expr.rest.accept(self)
        right_hand_type = self.current_type
        complex_expr.first_operand.accept(self)
        if not(right_hand_type == self.current_type):
            err_msg = "expecting " + self.current_type + ", found " + right_hand_type
            line, column = self.__first_token(complex_expr.rest)
            raise error.Error(err_msg, line, column)

    def __first_token(self, expr):
        line = expr.term.line
        column = expr.term.column
        return line, column
