grammar Pseudocode;

// NL is the statement separator
program         : NL* statement (NL+ statement)* NL* EOF;

statement
    : annotation? assignment SEMICOLON?
    | functionDecl
    | annotation? functionCallStatement SEMICOLON?
    | forEachLoop
    | regularForLoop
    | annotation? ifStatement
    | annotation? whileLoop
    | annotation? returnStatement SEMICOLON?
    | annotation? breakStatement SEMICOLON?
    | annotation? compoundAssignment SEMICOLON?
    ;

// lvalue covers both simple variable and array-element assignment targets
lvalue          : ID LBRACK expression RBRACK   # ArrayLvalue
                | ID                             # SimpleLvalue
                ;

assignment      : lvalue EQ (expression | arrayInitialization);

// 'arr' prefix is required for all array forms per language spec
arrayInitialization
    : ARR LBRACK start=expression TO stop=expression RBRACK        # RangeArray
    | ARR LPAREN size=expression (COMMA fill=expression)? RPAREN   # SizeArray
    | ARR LBRACK expression (COMMA expression)* RBRACK            # ValueArray
    ;

// Compound assignment as a standalone statement (e.g. i += 1, count[j] += 1)
compoundAssignment
    : lvalue (PLUS_EQ | MINUS_EQ | STAR_EQ | SLASH_EQ) expression;

functionDecl         : FUN ID LPAREN paramList? RPAREN COLON NL+ (statement (NL+ statement)*)? NL* END FUN;
functionCallStatement: ID LPAREN expressionList? RPAREN;
paramList            : annotatedParam (COMMA annotatedParam)*;
annotatedParam       : annotation? ID;

// Annotation syntax: @name<arg, ...>
// Used as parameter decorators (@init<table>) and statement prefixes (@mark<...>, @log<...>)
annotation          : AT ID LOW_THAN annotationArgList GREATER_THAN;
annotationArgList   : annotationArg (COMMA annotationArg)*;
annotationArg       : ID | STRING | INT;

// for-each: annotation (if any) appears between 'for' and the iterator variable
// regular for: annotation (if any) appears between 'for' and the '('
// Separators in regular-for header accept both ',' and ';'
forEachLoop    : FOR annotation? ID IN ID COLON NL+ (statement (NL+ statement)*)? NL* END FOR;
regularForLoop : FOR annotation? LPAREN ID EQ expression (COMMA | SEMICOLON) expression (COMMA | SEMICOLON) forUpdate RPAREN COLON NL+ block END FOR;
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
TRUE    : 'True' | 'true';
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
SEMICOLON   : ';';
AT          : '@';

// Newlines are significant; non-newline whitespace is skipped
NL      : '\r'? '\n';
WS      : [ \t]+ -> skip;
