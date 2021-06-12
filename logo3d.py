import sys
from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import Visitor

inputStream = FileStream(sys.argv[1])
lexer = logo3dLexer(inputStream)
tokenStream = CommonTokenStream(lexer)
parser = logo3dParser(tokenStream)
tree = parser.root()
visitor = Visitor()
visitor.visit(tree)
