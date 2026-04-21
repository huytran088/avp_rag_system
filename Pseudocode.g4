grammar Pseudocode;

// NL is the statement separator
program         : NL* statement (NL+ statement)* NL* EOF;

statement       : assignment
                | functionDecl
                | functionCallStatement
                | forEachLoop
                | regularForLoop
                | ifStatement
                | whileLoop
                | returnStatement
                | breakStatement
                ;

assignment      : ID EQ (expression | arrayInitialization);

// 'arr' prefix is required for all array forms per language spec
arrayInitialization
    : ARR LBRACK from=expression TO to=expression RBRACK          # RangeArray
    | ARR LPAREN size=INT (COMMA fill=expression)? RPAREN         # SizeArray
    | ARR LBRACK expression (COMMA expression)* RBRACK            # ValueArray
    ;

functionDecl         : FUN ID LPAREN paramList? RPAREN COLON NL+ (statement (NL+ statement)*)? NL* END FUN;
functionCallStatement: ID LPAREN expressionList? RPAREN;
paramList            : ID (COMMA ID)*;

// for-each: no parens; regular for: parens wrap the three-part header
forEachLoop    : FOR ID IN ID COLON NL+ (statement (NL+ statement)*)? NL* END FOR;
regularForLoop : FOR LPAREN ID EQ expression COMMA expression COMMA forUpdate RPAREN COLON NL+ block END FOR;
forUpdate      : ID (PLUS_EQ | MINUS_EQ | STAR_EQ | SLASH_EQ) expression;

// Conditions are encased in parentheses; supports 'else if' and 'else'
ifStatement    : IF LPAREN expression RPAREN COLON NL+ block
                 (ELSE IF LPAREN expression RPAREN COLON NL+ block)* (ELSE COLON NL+ block)?
                 END IF;

whileLoop      : WHILE LPAREN expression RPAREN COLON NL+ (statement (NL+ statement)*)? NL* END WHILE;

returnStatement : RETURN expression;
breakStatement  : BREAK;

// Helper rule for code block
block       : (statement (NL+ statement)*)? NL*;

expression
    : logicalOrExpression
    ;

logicalOrExpression
    : left=logicalAndExpression (OR right=logicalAndExpression)+ # OrExpr
    | logicalAndExpression                                        # OrPass
    ;

logicalAndExpression
    : left=comparisonExpression (AND right=comparisonExpression)+ # AndExpr
    | comparisonExpression                                         # AndPass
    ;

comparisonExpression
    : left=additiveExpression op=(EQEQ | LOW_THAN | GREATER_THAN | LESS_EQ | GREATER_EQ) right=additiveExpression # CompareExpr
    | additiveExpression                                                                                             # ComparisonPass
    ;

additiveExpression
    : left=multiplicativeExpression (op=(PLUS | MINUS) right=multiplicativeExpression)+ # AddExpr
    | multiplicativeExpression                                                            # AdditivePass
    ;

multiplicativeExpression
    : left=powerExpression (op=(STAR | SLASH) right=powerExpression)+ # MulExpr
    | powerExpression                                                   # MultiplicativePass
    ;

powerExpression
    : left=unaryExpression (POW right=unaryExpression)+ # PowExpr
    | unaryExpression                                    # PowerPass
    ;

unaryExpression
    : MINUS unaryExpression # UnaryMinusExpr
    | primaryExpression     # UnaryPass
    ;

primaryExpression
    : LPAREN expression RPAREN         # ParenExpression
    | ID LPAREN expressionList? RPAREN # FunctionCallExpression
    | ID LBRACK expression RBRACK      # ArrayAccessExpression
    | atom                             # AtomExpression
    ;

expressionList
    : expression (COMMA expression)*
    ;

atom    : ID | INT | FLOAT | TRUE | FALSE | NULL | STRING;

// Keywords (must be defined before ID)
ARR     : 'arr';
TO      : 'to';
FUN     : 'fun';
FOR     : 'for';
IN      : 'in';
IF      : 'if';
ELSE    : 'else';
RETURN  : 'return';
END     : 'end';
WHILE   : 'while';
BREAK   : 'break';
TRUE    : 'True';
FALSE   : 'False';
AND     : 'and';
OR      : 'or';
NULL    : 'Null';

// Identifiers & literals
ID      : [a-zA-Z_][a-zA-Z_0-9]*;
FLOAT   : [0-9]+ '.' [0-9]+;
INT     : [0-9]+;
STRING  : '"' (~["\r\n])* '"';

// Comments
COMMENT : '//' ~[\r\n]* -> skip;

// Symbols — multi-char tokens before their single-char prefixes
EQEQ        : '==';
EQ          : '=';
LESS_EQ     : '<=';
LOW_THAN    : '<';
GREATER_EQ  : '>=';
GREATER_THAN: '>';
POW         : '**';
STAR_EQ     : '*=';
STAR        : '*';
PLUS_EQ     : '+=';
PLUS        : '+';
MINUS_EQ    : '-=';
MINUS       : '-';
SLASH_EQ    : '/=';
SLASH       : '/';
LBRACK      : '[';
RBRACK      : ']';
LPAREN      : '(';
RPAREN      : ')';
COLON       : ':';
COMMA       : ',';

// Newlines are significant; non-newline whitespace is skipped
NL      : '\r'? '\n';
WS      : [ \t]+ -> skip;
