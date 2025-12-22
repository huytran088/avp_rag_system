grammar Pseudocode;

// This rule is updated to use NL as a statement separator
program         : NL* statement (NL+ statement)* NL* EOF;

statement       : assignment | functionDecl | forEachLoop | ifStatement | whileLoop | returnStatement | breakStatement;
assignment      : ID EQ (expression | arrayInitialization);

// REMOVED 'ARR' token requirement to match documentation (e.g. [1 to 10] instead of arr[1 to 10])
arrayInitialization:
    LBRACK from=expression TO to=expression RBRACK    # RangeArray
  | LPAREN size=INT RPAREN             # SizeArray
  | LBRACK INT (COMMA INT)* RBRACK     # ValueArray
  ;

// These block rules are updated to require newlines
functionDecl    : FUN ID LPAREN paramList? RPAREN COLON NL+ (statement (NL+ statement)*)? NL* END FUN;
paramList       : ID (COMMA ID)*;
forEachLoop     : FOR ID IN ID COLON NL+ (statement (NL+ statement)*)? NL* END FOR;
// Update to support 'else if' and 'else'
ifStatement     : IF expression COLON NL+ block 
                  (ELSE IF expression COLON NL+ block)* (ELSE COLON NL+ block)? 
                  END IF;
whileLoop       : WHILE expression COLON NL+ (statement (NL+ statement)*)? NL* END WHILE;

returnStatement : RETURN expression;
breakStatement  : BREAK;

// Helper rule for code block
block       : (statement (NL+ statement)*)? NL*;

expression
    : logicalOrExpression
    ;

logicalOrExpression
    : left=logicalAndExpression (OR right=logicalAndExpression)+ # OrExpr
    | logicalAndExpression # OrPass
    ;

logicalAndExpression
    : left=comparisonExpression (AND right=comparisonExpression)+ # AndExpr
    | comparisonExpression # AndPass
    ;

comparisonExpression
    : left=additiveExpression op=(EQEQ | LOW_THAN | GREATER_THAN | LESS_EQ | GREATER_EQ) right=additiveExpression # CompareExpr
    | additiveExpression # ComparisonPass
    ;

additiveExpression
    : left=multiplicativeExpression (op=(PLUS | MINUS) right=multiplicativeExpression)+ # AddExpr
    | multiplicativeExpression # AdditivePass
    ;

multiplicativeExpression
    : left=powerExpression (op=(STAR | SLASH) right=powerExpression)+ # MulExpr
    | powerExpression # MultiplicativePass
    ;

powerExpression
    : left=unaryExpression (POW right=unaryExpression)+ # PowExpr
    | unaryExpression # PowerPass
    ;

unaryExpression
    : MINUS unaryExpression # UnaryMinusExpr
    | primaryExpression # UnaryPass
    ;

primaryExpression
    : LPAREN expression RPAREN         # ParenExpression
    | ID LPAREN expressionList? RPAREN # FunctionCallExpression
    | ID LBRACK expression RBRACK    # ArrayAccessExpression
    | atom                           # AtomExpression
    ;

expressionList
    : expression (COMMA expression)*
    ;

atom
    : ID | INT | TRUE | FALSE;

// Keywords
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

// Identifiers & numbers
ID      : [a-zA-Z_][a-zA-Z_0-9]*;
INT     : [0-9]+;

// Commments
COMMENT : '//' ~[\r\n]* -> skip;

// Symbols
LBRACK  : '[';
RBRACK  : ']';
EQ      : '=';
EQEQ    : '==';
LPAREN  : '(';
RPAREN  : ')';
COLON   : ':';
COMMA   : ',';
PLUS    : '+';
MINUS   : '-';
STAR    : '*';
SLASH   : '/';
POW     : '**';
LOW_THAN : '<';
GREATER_THAN : '>';
LESS_EQ : '<=';
GREATER_EQ : '>=';

// --- LEXER CHANGES ARE HERE ---
// Newlines are now a dedicated token
NL      : '\r'? '\n' ; 
// Whitespace no longer includes newlines
WS      : [ \t]+ -> skip;