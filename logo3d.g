grammar logo3d;

ID : [a-zA-Z_]+[a-zA-Z_0-9]* ;
INT : [0-9]+ ;
DEC : [0-9]+'.'[0-9]+ ;

MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;

expr :  SUB expr #negativeExpression
    |   expr MUL expr #multiply
    |   expr DIV expr #divide
    |   expr ADD expr #add
    |   expr SUB expr #subtract
    |   INT #atomInteger
    |   DEC #atomDecimal
    |   ID #atomIdentifier
    ;

GT : '>' ;
ST : '<' ;
GET : '>=' ;
SET : '<=' ;
EQ : '==' ;
NOTEQ : '!=' ;

boolExpr :  expr GT expr #greaterThan
    |       expr ST expr #smallerThan
    |       expr GET expr #greaterTHanOrEqual
    |       expr SET expr #smallerThanOrEqual
    |       expr EQ expr #equal
    |       expr NOTEQ expr #notEqual
    ;

ASSIG : ':=';
READ : '>>';
WRITE : '<<';

stat :  ID ASSIG expr #assign
    |   READ ID #read
    |   WRITE expr #write
    |   'WHILE' boolExpr 'DO' stat* 'END' #whileLoop
    |   'FOR' ID 'FROM' expr 'TO' expr 'DO' stat* 'END' #forLoop
    |   'IF' boolExpr 'THEN' stat* ('ELSE' stat*)? 'END' #ifThenElse
    |   ID'('(expr(','expr)*)?')' #callProcedure
    ;

procedure : 'PROC' ID'('(ID(','ID)*)?')' 'IS' stat* 'END' ;

WHITESPACE : [ \t]+ -> skip ;
NEWLINE : ('\r' '\n'? | '\n' ) -> skip ;
BLOCKCOMMENT : '/*' .*? '*/' -> skip ;
LINECOMMENT : '//' ~[\r\n]* -> skip ;

root : procedure+ ;
