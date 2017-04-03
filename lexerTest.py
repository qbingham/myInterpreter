# Quinlan Bingham
# hw2.py
# HW2
# This file has the main function that is responsible
# for piecing together all the components, but besides
# some error handling

import sys
import error
import lexer
import token


def main(filename):
    try:
        # open the file for lexical analysis
        file_stream = open(filename, 'r')
        the_lexer = lexer.Lexer(file_stream)
        t = the_lexer.next_token()
        # while not at end of file,
        while t != None and t.tokentype != token.EOS:
            # print the next token
            print t
            t = the_lexer.next_token()
    # in case the user chooses a bad file, let them know why it's not working
    except IOError as e:
        print "error: unable to open file '" + filename + "'"
        sys.exit(1)
    except error.Error as e:
        print e
        sys.exit(1)
        
    if __name__ == '__main__':
        if len(sys.argv) != 2:
            print 'usage:', sys.argv[0], 'source-code-file'
            sys.exit(1)
        else:
            main(sys.argv[1])

# prompt the user to choose test file
filename = input("What file would you like to use?: ")
main(filename)