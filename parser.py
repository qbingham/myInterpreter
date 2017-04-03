# Author: Quinlan Bingham
# Filename: parser.py
# Assignment: Assignment 4
# Description: This file is a recursive parser class that helps build the
# abstract syntax tree

import error
import mytoken
import mypl_ast


class Parser(object):

    # constructor for parser
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None

    def parse(self):
        """succeeds if program is syntactically well-formed"""
        stmt_list_node = mypl_ast.StmtList()
        self.advance()
        self.stmts(stmt_list_node)
        self.eat(mytoken.EOS, 'expecting end-of-file')
        return stmt_list_node

    # helper functions

    def advance(self):
        self.current_token = self.lexer.next_token()

    def eat(self, tokentype, error_msg):
        if self.current_token.tokentype == tokentype:
            self.advance()
        else:
            self.error(error_msg)

    def error(self, error_msg):
        s = error_msg + ' found "' + self.current_token.lexeme + '"'
        l = self.current_token.line
        c = self.current_token.column
        raise error.Error(s, l, c)

    def stmts(self, stmt_list_node):

        # output statements
        if self.current_token.tokentype == mytoken.PRINT:
            self.advance()
            print_node = mypl_ast.PrintStmt()
            self.eat(mytoken.LPAREN, 'expected "("')
            print_node.expr = self.expr()
            self.eat(mytoken.RPAREN, 'expected ")"')
            self.eat(mytoken.SEMICOLON, 'expected ";"')
            stmt_list_node.stmts.append(print_node)
            self.stmts(stmt_list_node)
        elif self.current_token.tokentype == mytoken.PRINTLN:
            self.advance()
            print_node = mypl_ast.PrintStmt()
            print_node.is_println = True
            self.eat(mytoken.LPAREN, 'expected "("')
            print_node.expr = self.expr()
            self.eat(mytoken.RPAREN, 'expected ")"')
            self.eat(mytoken.SEMICOLON, 'expected ";"')
            stmt_list_node.stmts.append(print_node)
            self.stmts(stmt_list_node)

        # assignment statements
        elif self.current_token.tokentype == mytoken.ID:
            assign_node = mypl_ast.AssignStmt()
            assign_node.lhs = self.current_token
            index_expr_node = mypl_ast.IndexExpr()
            index_expr_node.identifier = self.current_token
            self.advance()
            index_expr_node2 = self.list_index(index_expr_node)
            if index_expr_node2.expr != None:
                assign_node.index_expr = index_expr_node2
            self.eat(mytoken.ASSIGN, 'expected "="')
            expr_node = self.expr()
            assign_node.rhs = expr_node
            self.eat(mytoken.SEMICOLON, 'expected ";"')
            stmt_list_node.stmts.append(assign_node)
            self.stmts(stmt_list_node)

        # conditional statements
        elif self.current_token.tokentype == mytoken.IF:
            if_stmt_node = mypl_ast.IfStmt()
            self.advance()
            basic_if_node = mypl_ast.BasicIf()
            basic_if_node.bool_expr = self.bexpr()
            self.eat(mytoken.THEN, 'expected "then"')
            cond_stmts = mypl_ast.StmtList()
            self.stmts(cond_stmts)
            basic_if_node.stmt_list = cond_stmts
            if_stmt_node.if_part = basic_if_node
            if_stmt_node2 = self.cond_t(if_stmt_node)
            if_stmt_node.elseifs = if_stmt_node2.elseifs
            if_stmt_node.has_else = if_stmt_node2.has_else
            if_stmt_node.else_stmts = if_stmt_node2.else_stmts
            self.eat(mytoken.END, 'expected "end"')
            stmt_list_node.stmts.append(if_stmt_node)
            self.stmts(stmt_list_node)

        # loop statements
        elif self.current_token.tokentype == mytoken.WHILE:
            while_stmt_node = mypl_ast.WhileStmt()
            self.advance()
            while_stmt_node.bool_expr = self.bexpr()
            self.eat(mytoken.DO, 'expected "do"')
            while_stmts = mypl_ast.StmtList()
            while_stmt_node.stmt_list = while_stmts
            self.stmts(while_stmts)
            self.eat(mytoken.END, 'expected "end"')
            stmt_list_node.stmts.append(while_stmt_node)
            self.stmts(stmt_list_node)

    # <list_index> non-terminal
    def list_index(self, index_expr_node):
        if self.current_token.tokentype == mytoken.LBRACKET:
            self.advance()
            index_expr_node.expr = self.expr()
            self.eat(mytoken.RBRACKET, 'expected "]"')
        return index_expr_node

    # <input> non-terminal
    def input(self):
        read_expr_node = mypl_ast.ReadExpr()
        if self.current_token.tokentype == mytoken.READINT:
            read_expr_node.is_read_int = True
            self.advance()
            self.eat(mytoken.LPAREN, 'expected "("')
            read_expr_node.msg = self.current_token
            self.eat(mytoken.STRING, 'expected string')
            self.eat(mytoken.RPAREN, 'expected ")"')
        elif self.current_token.tokentype == mytoken.READSTR:
            self.advance()
            self.eat(mytoken.LPAREN, 'expected "("')
            read_expr_node.msg = self.current_token
            self.eat(mytoken.STRING, 'expected string')
            self.eat(mytoken.RPAREN, 'expected ")"')
        return read_expr_node

    # <expr> non-terminal
    def expr(self):
        expr_node = mypl_ast.SimpleExpr()
        expr_node2 = self.value(expr_node)
        expr_node3 = self.expr_t(expr_node2)
        return expr_node3

    # <exprt> non-terminal
    def expr_t(self, expr_node):
        if self.current_token.tokentype == mytoken.PLUS:
            expr_node2 = mypl_ast.ComplexExpr()
            expr_node2.first_operand = expr_node
            expr_node2.math_rel = self.current_token
            self.advance()
            expr_node2.rest = self.expr()
            expr_node = mypl_ast.ComplexExpr()
            expr_node.first_operand = expr_node2.first_operand
            expr_node.math_rel = expr_node2.math_rel
            expr_node.rest = expr_node2.rest
        elif self.current_token.tokentype == mytoken.MINUS:
            expr_node2 = mypl_ast.ComplexExpr()
            expr_node2.first_operand = expr_node
            expr_node2.math_rel = self.current_token
            self.advance()
            expr_node2.rest = self.expr()
            expr_node = mypl_ast.ComplexExpr()
            expr_node.first_operand = expr_node2.first_operand
            expr_node.math_rel = expr_node2.math_rel
            expr_node.rest = expr_node2.rest
        elif self.current_token.tokentype == mytoken.MULTIPLY:
            expr_node2 = mypl_ast.ComplexExpr()
            expr_node2.first_operand = expr_node
            expr_node2.math_rel = self.current_token
            self.advance()
            expr_node2.rest = self.expr()
            expr_node = mypl_ast.ComplexExpr()
            expr_node.first_operand = expr_node2.first_operand
            expr_node.math_rel = expr_node2.math_rel
            expr_node.rest = expr_node2.rest
        elif self.current_token.tokentype == mytoken.DIVIDE:
            expr_node2 = mypl_ast.ComplexExpr()
            expr_node2.first_operand = expr_node
            expr_node2.math_rel = self.current_token
            self.advance()
            expr_node2.rest = self.expr()
            expr_node = mypl_ast.ComplexExpr()
            expr_node.first_operand = expr_node2.first_operand
            expr_node.math_rel = expr_node2.math_rel
            expr_node.rest = expr_node2.rest
        elif self.current_token.tokentype == mytoken.MODULUS:
            expr_node2 = mypl_ast.ComplexExpr()
            expr_node2.first_operand = expr_node
            expr_node2.math_rel = self.current_token
            self.advance()
            expr_node2.rest = self.expr()
            expr_node = mypl_ast.ComplexExpr()
            expr_node.first_operand = expr_node2.first_operand
            expr_node.math_rel = expr_node2.math_rel
            expr_node.rest = expr_node2.rest
        return expr_node

    # <value> non-terminal
    def value(self, expr_node):
        if self.current_token.tokentype == mytoken.ID:
            expr_node.term = self.current_token
            self.advance()
            index_expr_node = mypl_ast.IndexExpr()
            list_index_expr_node = self.list_index(index_expr_node)
            if list_index_expr_node.expr != None:
                list_index_expr_node.identifier = expr_node.term
                expr_node = list_index_expr_node
        elif self.current_token.tokentype == mytoken.STRING:
            expr_node.term = self.current_token
            self.advance()
        elif self.current_token.tokentype == mytoken.INT:
            expr_node.term = self.current_token
            self.advance()
        elif self.current_token.tokentype == mytoken.BOOL:
            expr_node.term = self.current_token
            self.advance()
        elif self.current_token.tokentype == mytoken.LBRACKET:
            self.advance()
            expr_node2 = mypl_ast.ListExpr()
            expr_node = self.expr_list(expr_node2)
            self.eat(mytoken.RBRACKET, 'expected "]"')
        else:
            expr_node = self.input()
        return expr_node

    # <expr_list> non-terminal
    def expr_list(self, expr_node):
        if self.current_token.lexeme != '':
            expr_node2 = self.expr()
            expr_node.expressions.append(expr_node2)
            self.expr_tail(expr_node)
        return expr_node

    # <expr_tail> non-terminal
    def expr_tail(self, expr_node):
        if self.current_token.tokentype == mytoken.COMMA:
            self.advance()
            expr_node2 = self.expr()
            expr_node.expressions.append(expr_node2)
            self.expr_tail(expr_node)
        return expr_node

    # <cond_t> non_terminal
    def cond_t(self, if_stmt_node):
        if self.current_token.tokentype == mytoken.ELSEIF:
            basic_if_node = mypl_ast.BasicIf()
            self.advance()
            basic_if_node.bool_expr = self.bexpr()
            self.eat(mytoken.THEN, 'expected then')
            elseif_stmts = mypl_ast.StmtList()
            self.stmts(elseif_stmts)
            basic_if_node.stmt_list = elseif_stmts
            if_stmt_node.elseifs.append(basic_if_node)
            self.cond_t(if_stmt_node)
        elif self.current_token.tokentype == mytoken.ELSE:
            if_stmt_node.has_else = True
            else_stmts = mypl_ast.StmtList()
            self.advance()
            self.stmts(else_stmts)
            if_stmt_node.else_stmts = else_stmts
        return if_stmt_node

    # <bexpr> non-terminal
    def bexpr(self):
        bool_expr_node = mypl_ast.SimpleBoolExpr()
        if self.current_token.tokentype == mytoken.NOT:
            bool_expr_node.negated = True
            self.advance()
            bool_expr_node.expr = self.expr()
            if (self.current_token.tokentype == mytoken.EQUAL or self.current_token.tokentype == mytoken.LESS_THAN or
                self.current_token.tokentype == mytoken.GREATER_THAN or
                self.current_token.tokentype == mytoken.LESS_THAN_EQUAL or
                self.current_token.tokentype == mytoken.GREATER_THAN_EQUAL or
                self.current_token.tokentype == mytoken.NOT_EQUAL):
                bool_expr_node2 = self.bexpr_t()
                bool_expr_node2.first_expr = bool_expr_node.expr
            else:
                bool_expr_node2 = self.bexpr_t()
                bool_expr_node2.expr = bool_expr_node.expr
        else:
            bool_expr_node.expr = self.expr()
            if (self.current_token.tokentype == mytoken.EQUAL or self.current_token.tokentype == mytoken.LESS_THAN or
                self.current_token.tokentype == mytoken.GREATER_THAN or
                self.current_token.tokentype == mytoken.LESS_THAN_EQUAL or
                self.current_token.tokentype == mytoken.GREATER_THAN_EQUAL or
                self.current_token.tokentype == mytoken.NOT_EQUAL):
                bool_expr_node2 = self.bexpr_t()
                bool_expr_node2.first_expr = bool_expr_node.expr
            else:
                bool_expr_node2 = self.bexpr_t()
                bool_expr_node2.expr = bool_expr_node.expr
        bool_expr_node2.negated = bool_expr_node.negated
        return bool_expr_node2

    # <bexpr_t> non-terminal
    def bexpr_t(self):
        bool_expr_node2 = mypl_ast.SimpleBoolExpr()
        if self.current_token.tokentype == mytoken.EQUAL:
            bool_expr_node2 = mypl_ast.ComplexBoolExpr()
            bool_expr_node2.bool_rel = self.current_token
            self.advance()
            bool_expr_node2.second_expr = self.expr()
            bool_expr_node3 = self.bconnct()
            bool_expr_node2.has_bool_connector = bool_expr_node3.has_bool_connector
            bool_expr_node2.bool_connector = bool_expr_node3.bool_connector
            bool_expr_node2.rest = bool_expr_node3.rest
        elif self.current_token.tokentype == mytoken.LESS_THAN:
            bool_expr_node2 = mypl_ast.ComplexBoolExpr()
            bool_expr_node2.bool_rel = self.current_token
            self.advance()
            bool_expr_node2.second_expr = self.expr()
            bool_expr_node3 = self.bconnct()
            bool_expr_node2.has_bool_connector = bool_expr_node3.has_bool_connector
            bool_expr_node2.bool_connector = bool_expr_node3.bool_connector
            bool_expr_node2.rest = bool_expr_node3.rest
        elif self.current_token.tokentype == mytoken.LESS_THAN_EQUAL:
            bool_expr_node2 = mypl_ast.ComplexBoolExpr()
            bool_expr_node2.bool_rel = self.current_token
            self.advance()
            bool_expr_node2.second_expr = self.expr()
            bool_expr_node3 = self.bconnct()
            bool_expr_node2.has_bool_connector = bool_expr_node3.has_bool_connector
            bool_expr_node2.bool_connector = bool_expr_node3.bool_connector
            bool_expr_node2.rest = bool_expr_node3.rest
        elif self.current_token.tokentype == mytoken.GREATER_THAN:
            bool_expr_node2 = mypl_ast.ComplexBoolExpr()
            bool_expr_node2.bool_rel = self.current_token
            self.advance()
            bool_expr_node2.second_expr = self.expr()
            bool_expr_node3 = self.bconnct()
            bool_expr_node2.has_bool_connector = bool_expr_node3.has_bool_connector
            bool_expr_node2.bool_connector = bool_expr_node3.bool_connector
            bool_expr_node2.rest = bool_expr_node3.rest
        elif self.current_token.tokentype == mytoken.GREATER_THAN_EQUAL:
            bool_expr_node2 = mypl_ast.ComplexBoolExpr()
            bool_expr_node2.bool_rel = self.current_token
            self.advance()
            bool_expr_node2.second_expr = self.expr()
            bool_expr_node3 = self.bconnct()
            bool_expr_node2.has_bool_connector = bool_expr_node3.has_bool_connector
            bool_expr_node2.bool_connector = bool_expr_node3.bool_connector
            bool_expr_node2.rest = bool_expr_node3.rest
        elif self.current_token.tokentype == mytoken.NOT_EQUAL:
            bool_expr_node2 = mypl_ast.ComplexBoolExpr()
            bool_expr_node2.bool_rel = self.current_token
            self.advance()
            bool_expr_node2.second_expr = self.expr()
            bool_expr_node3 = self.bconnct()
            bool_expr_node2.has_bool_connector = bool_expr_node3.has_bool_connector
            bool_expr_node2.bool_connector = bool_expr_node3.bool_connector
            bool_expr_node2.rest = bool_expr_node3.rest
        return bool_expr_node2

    # <bconnct> non-terminal
    def bconnct(self):
        bool_expr_node = mypl_ast.ComplexBoolExpr()
        if self.current_token.tokentype == mytoken.AND:
            bool_expr_node.has_bool_connector = True
            bool_expr_node.bool_connector = self.current_token
            self.advance()
            bool_expr_node.rest = self.bexpr()
        elif self.current_token.tokentype == mytoken.OR:
            bool_expr_node.has_bool_connector = True
            bool_expr_node.bool_connector = self.current_token
            self.advance()
            bool_expr_node.rest = self.bexpr()
        return bool_expr_node
