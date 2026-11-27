grammar Pseudocode;

// Parser Rules
program         : (statement | NL)* EOF;

// Statements can end with newlines or optional semicolons
statement       : metadata* (
                    assignment
                  | functionDecl
                  | functionCallStmt
                  | forEachLoop
                  | forLoop
                  | doWhileLoop
                  | ifStatement
                  | whileLoop
                  | returnStatement
                  | breakStatement
                  | continueStatement
                  ) (SEMI | NL)*;

// Supports standard '=' as well as '+=' and '-='
assignment      : metadata* assignable (EQ | PLUS_EQ | MINUS_EQ) (expression | arrayInitialization) ;

// Supports variable assignment and array index assignment (e.g., arr[j+1] = key)
assignable      : ID | ID LBRACK expression RBRACK ;

arrayInitialization
    : ARR LBRACK NL* from=expression TO NL* to=expression NL* RBRACK               # RangeArray
    | ARR LPAREN NL* size=expression (COMMA NL* defaultVal=expression)? NL* RPAREN # SizeArray
    | ARR LBRACK NL* expressionList? NL* RBRACK                                     # ValueArray
    ;

// Metadata integration for variables, functions, and loops
metadata        : AT ID LT metadataParams? GT;
metadataParams  : metadataParam (COMMA metadataParam)*;
metadataParam   : ID | INT | FLOAT | STRING;

// Shared block rule — used by all compound statements
block           : statement* ;

// Blocks require mandatory end identifiers
functionDecl    : FUN ID LPAREN paramList? RPAREN COLON NL+ block END FUN;
paramList       : param (COMMA param)*;
param           : metadata* ID;

// Optional parentheses for 'for-each' loops
forEachLoop     : FOR metadata* LPAREN? ID IN ID RPAREN? COLON NL+ block END FOR;

// Traditional for-loop (supports both commas and semicolons as separators)
forLoop         : FOR metadata* LPAREN assignment (COMMA | SEMI) expression (COMMA | SEMI) assignment RPAREN COLON NL+ block END FOR;

whileLoop       : WHILE LPAREN? expression RPAREN? COLON NL+ block END WHILE;

// Do-while loop to support the Hoare Partition script
doWhileLoop     : DO COLON? NL+ block WHILE LPAREN expression RPAREN;

ifStatement     : IF LPAREN? expression RPAREN? COLON NL+ block
                  (ELSEIF LPAREN? expression RPAREN? COLON NL+ block)*
                  (ELSE COLON NL+ block)?
                  END IF;

functionCallStmt: ID LPAREN expressionList? RPAREN;

returnStatement : metadata* RETURN expression;
breakStatement  : BREAK;
continueStatement : CONTINUE;

expressionList  : expression (COMMA NL* expression)*;

// Order of operations for expressions
expression               : logicalOrExpression ;

logicalOrExpression      : left=logicalAndExpression (op+=OR right+=logicalAndExpression)* ;

logicalAndExpression     : left=comparisonExpression (op+=AND right+=comparisonExpression)* ;

comparisonExpression
    : left=additiveExpression (op+=(EQEQ | NOTEQ | LESS_EQ | GREATER_EQ | LT | GT) right+=additiveExpression)* # CompareExpr
    ;

additiveExpression
    : left=multiplicativeExpression (op+=(PLUS | MINUS) right+=multiplicativeExpression)* # AddExpr
    ;

multiplicativeExpression
    : left=powerExpression (op+=(STAR | SLASH | MOD) right+=powerExpression)* # MulExpr
    ;

powerExpression          : left=unaryExpression (op+=POWER right+=unaryExpression)* ;

unaryExpression
    : MINUS unaryExpression  # UnaryMinusExpr
    | primaryExpression      # PrimaryExpr
    ;

primaryExpression
    : LPAREN expression RPAREN             # ParenExpression
    | ID LPAREN expressionList? RPAREN     # FunctionCallExpression
    | ID LBRACK expression RBRACK          # ArrayAccessExpression
    | atom                                 # AtomExpression
    ;

atom : ID | INT | FLOAT | STRING | TRUE | FALSE | NULL_VAL;

// Lexer Rules

// Reserved standard types
TYPE_INT    : 'Integer' | 'integer';
TYPE_FLOAT  : 'float'   | 'Float';
TYPE_STRING : 'string'  | 'String';
TYPE_BOOL   : 'boolean' | 'Boolean';
TYPE_DOUBLE : 'double'  | 'Double';

// Reserved Keywords
ARR     : 'arr';
TO      : 'to';
FUN     : 'fun';
FOR     : 'for';
IN      : 'in';
IF      : 'if';
ELSE    : 'else';
ELSEIF  : 'else if' | 'elseif';
RETURN  : 'return';
END     : 'end';
WHILE   : 'while';
DO      : 'do';
BREAK   : 'break';
AND     : 'and';
OR      : 'or';
CONTINUE : 'continue';

// Literals
TRUE    : 'True'  | 'true';
FALSE   : 'False' | 'false';
NULL_VAL: 'Null'  | 'null';

// Symbols & Punctuation
LBRACK  : '[';
RBRACK  : ']';
LPAREN  : '(';
RPAREN  : ')';
COLON   : ':';
COMMA   : ',';
SEMI    : ';';
AT      : '@';

// Operators
PLUS_EQ : '+=';
MINUS_EQ: '-=';
EQ      : '=';
EQEQ    : '==';
NOTEQ   : '!=';
PLUS    : '+';
MINUS   : '-';
POWER   : '**';
STAR    : '*';
SLASH   : '/';
LESS_EQ : '<=';
GREATER_EQ : '>=';
LT      : '<';
GT      : '>';
MOD     : '%';
MOD_EQ  : '%=';

// Primitives
ID      : [a-zA-Z_][a-zA-Z_0-9]*;
FLOAT   : [0-9]+ '.' [0-9]+;
INT     : [0-9]+;
STRING  : '"' (~["\r\n])* '"';

// Whitespace & Comments
NL      : '\r'? '\n' ; 
WS      : [ \t]+ -> skip;
COMMENT : ('#' | '//') ~[\r\n]* -> skip;
