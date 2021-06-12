import sys
from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import Visitor


program = sys.argv[1]
main = 'main'
parameters = []
if len(sys.argv) > 2:
    main = sys.argv[2]
    parameters = sys.argv[3:]
inputStream = FileStream(program)
lexer = logo3dLexer(inputStream)
tokenStream = CommonTokenStream(lexer)
parser = logo3dParser(tokenStream)
tree = parser.root()
visitor = Visitor(main, parameters)
visitor.visit(tree)
