# myInterpreter
"MyPL" programming language interpreter written for my CPSC 326 course, "Organization of a Programming Language"
Making this program was a 6 week process that I started in late January and finished in early March.

Part 1: Lexer
The goal of this part is to write a lexical analyzer (lexer) for MyPL.

Here is the list of tokens MyPL language:
PRINT
RPAREN
STRING
PLUS
IF
NOT
GREATER_THAN_EQUAL
DO
PRINTLN
SEMICOLON
INT
MINUS
THEN
AND
LESS_THAN_EQUAL 
EOS
READINT
ID
BOOL
DIVIDE
ELSEIF
OR
GREATER_THAN_EQUAL
READSTR 
LBRACKET 
COMMA 
MULTIPLY 
ELSE 
EQUAL
NOT_EQUAL
LPAREN
RBRACKET
ASSIGN
MODULUS
END
LESS_THAN_WHILE

The first assignment expects the test program to take a source file written in MyPL and output the set of tokens in the file.
For example, given this simple program (stored in p1.txt):
   println("Hello World!");
Running the test program prints the following.
   $ ./lexerTest.py p1.txt
   PRINTLN ’println’ 1:1
   LPAREN ’(’ 1:8
   STRING ’Hello World!’ 1:9
   RPAREN ’)’ 1:23
   SEMICOLON ’;’ 1:24
As an example the error handling in efect, the following source file
   "hello
   world!"
shall output
   Error: reached newline while reading string at line 1 column 7.

Part 2: Parser
The goal of this part was to implement a basic recursive descent parser for MyPL.
Here is the grammar for MyPL:
   <stmts> ::= <stmt> <stmts> | empty
     <stmt> ::= <output> | <assign> | <cond> | <loop>
     
   <output> ::= PRINT LPAREN <expr> RPAREN SEMICOLON
              | PRINTLN LPAREN <expr> RPAREN SEMICOLON
    <input> ::= READINT LPAREN STRING RPAREN
              | READSTR LPAREN STRING RPAREN
   <assign> ::= ID <listindex> ASSIGN <expr> SEMICOLON
<listindex> ::= LBRACKET <expr> RBRACKET | empty

     <expr> ::= <value> <exprt>
    <exprt> ::= <math_rel> <expr> | empty
    <value> ::= ID <listindex> | STRING | INT | BOOL | <input>
              | LBRACKET <exprlist> RBRACKET
 <exprlist> ::= <expr> <exprtail> | empty
 <exprtail> ::= COMMA <expr> <exprtail> | empty
 
 <math_rel> ::= PLUS | MINUS | DIVIDE | MULTIPLY | MODULUS
 
     <cond> ::= IF <bexpr> THEN <stmts> <condt> END
    <condt> ::= ELSEIF <bexpr> THEN <stmts> <condt> | ELSE <stmts> | empty
    <bexpr> ::= <expr> <bexprt> | NOT <expr> <bexprt>
   <bexprt> ::= <bool_rel> <expr> <bconnct> | empty
  <bconnct> ::= AND <bexpr> | OR <bexpr> | empty
 <bool_rel> ::= EQUAL | LESS_THAN | GREATER_THAN | LESS_THAN_EQUAL
              | GREATER_THAN_EQUAL | NOT_EQUAL
              
     <loop> ::= WHILE <bexpr> DO <stmts> END
    
The test program should take a source file written in MyPL and output any parser (or lexer) errors. If there are no errors, nothing should be output.
    $ python parserTest.py test.txt

Part 3: Abstract Syntax Tree
The goal of this portion is to extend the recursive descent parser to return an Abstract Syntax Tree.

As a simple example of what the program shall do when given the MyPL program test.txt: 
    println("Hello World!");
your program should output the following.
    $ python astTest.py test.txt
    StmtList:
      PrintStmt: PRINTLN
        SimpleExpr: STRING (Hello World!)
        
Part 4: Type Checker
The goal of this portion is to implement a type checker for MyPL.

As a simple example of what your program should do, given the MyPL program test.txt:
   x = "foo";
   y = 5 + 4;
   z = y + x;
your program should output the following error.
   $ python typeCheckerTest.py test.txt
   error: expecting INT found STRING at line 3 column 9
   
Part 5: Interpreter
The goal for this final portion is to implement the interpreter for MyPL.

As a simple example of what your program should do, given the MyPL program test.txt:
   x = 3 + 4;
   msg = "The value is: "
   print(msg);
   println(x);
your program should output the following.
   $ python interpreterTest.py test.txt
   The value is: 7
