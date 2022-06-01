/* 
RDF turtle antlr grammar, reduced to rules for prefixes and terms
for use by stOTTR grammar. 
*/

grammar Turtle;

// [1] 
// turtleDoc : statement*;

// [2] 
// statement : directive | triples '.';

// [3] 
directive : prefixID | base | sparqlPrefix | sparqlBase;

// [4] 
prefixID : '@prefix' PNAME_NS IRIREF '.';

// [5] 
base : '@base' IRIREF '.';

// [5s] 
sparqlBase : 'BASE' IRIREF;

// [6s] 
sparqlPrefix : 'PREFIX' PNAME_NS IRIREF;

// [6] 
// triples : subject predicateObjectList | blankNodePropertyList predicateObjectList?;

// [7] 
// predicateObjectList : verb objectList (';' (verb objectList)?)*;

// [8] 
// objectList : object (',' object)*;

// [9] 
// verb : predicate | 'a';

// [10] 
// subject : iri | blankNode | collection;

// [11] 
// predicate : iri;

// [12] 
// object : iri | blankNode | collection | blankNodePropertyList | literal;

// [13] 
literal : rdfLiteral | numericLiteral | BooleanLiteral;

// [14] 
// blankNodePropertyList : '[' predicateObjectList ']';

// [15] 
// collection : '(' object* ')';

// [16] 
numericLiteral : INTEGER | DECIMAL | DOUBLE;

// [128s] 
rdfLiteral : String (LANGTAG | '^^' iri)?;

// [133s] 
BooleanLiteral : 'true' | 'false';

// [17] 
String : STRING_LITERAL_QUOTE | STRING_LITERAL_SINGLE_QUOTE | STRING_LITERAL_LONG_SINGLE_QUOTE | STRING_LITERAL_LONG_QUOTE;

// [135s] 
iri : IRIREF | prefixedName;

// [136s] 
prefixedName : PNAME_LN | PNAME_NS;

// [137s] 
blankNode : BLANK_NODE_LABEL | anon ;

// Productions for terminals
// [18] 
IRIREF : '<' ((~[\u0000-\u0020<>"{}|^`\\]) | UCHAR)* '>' /* #x00=NULL #01-#x1F=control codes #x20=space */ ;

// [139s] 
PNAME_NS : PN_PREFIX? ':';

// [140s] 
PNAME_LN : PNAME_NS PN_LOCAL;

// [141s] 
BLANK_NODE_LABEL : '_:' (PN_CHARS_U | [0-9]) ((PN_CHARS | '.')* PN_CHARS)?;

// [144s] 
LANGTAG : '@' [a-zA-Z]+ ('-' [a-zA-Z0-9]+)*;

// [19] 
INTEGER : [+-]? [0-9]+;

// [20] 
DECIMAL : [+-]? [0-9]* '.' [0-9]+;

// [21] 
DOUBLE : [+-]? ([0-9]+ '.' [0-9]* EXPONENT | '.' [0-9]+ EXPONENT | [0-9]+ EXPONENT);

// [154s] 
EXPONENT : [eE] [+-]? [0-9]+;

// [22] 
STRING_LITERAL_QUOTE : '"' ((~[\u0022\u005C\u000A\u000D]) | ECHAR | UCHAR)* '"' /* #x22=" #x5C=\ #xA=new line #xD=carriage return */ ;

// [23] 
STRING_LITERAL_SINGLE_QUOTE : '\'' ((~[\u0027\u005C\u000A\u000D]) | ECHAR | UCHAR)* '\'' /* #x27=' #x5C=\ #xA=new line #xD=carriage return */ ;

// [24] 
STRING_LITERAL_LONG_SINGLE_QUOTE : '\'\'\'' (('\'' | '\'\'')? ((~['\\]) | ECHAR | UCHAR))* '\'\'\'';

// [25] 
STRING_LITERAL_LONG_QUOTE : '"""' (('"' | '""')? ((~["\\]) | ECHAR | UCHAR))* '"""';

// [26] 
UCHAR : '\\u' HEX HEX HEX HEX | '\\U' HEX HEX HEX HEX HEX HEX HEX HEX;

// [159s] 
ECHAR : '\\' [tbnrf"'\\];

// [161s] 
WS :  [\u0020\u0009\u000D\u000A] -> skip /* #x20=space #x9=character tabulation #xD=carriage return #xA=new line */;

// [162s] 
anon : '[' WS* ']';

// [163s] 
PN_CHARS_BASE : 'A' .. 'Z' | 'a' .. 'z' | '\u00C0' .. '\u00D6' | '\u00D8' .. '\u00F6' | '\u00F8' .. '\u02FF' | '\u0370' .. '\u037D' | '\u037F' .. '\u1FFF' | '\u200C' .. '\u200D' | '\u2070' .. '\u218F' | '\u2C00' .. '\u2FEF' | '\u3001' .. '\uD7FF' | '\uF900' .. '\uFDCF' | '\uFDF0' .. '\uFFFD' /*| '\u10000' .. '\uEFFFF'*/ ;

// [164s] 
PN_CHARS_U : PN_CHARS_BASE | '_';

// [166s] 
PN_CHARS : PN_CHARS_U | '-' | [0-9] | [\u00B7] | [\u0300-\u036F] | [\u203F-\u2040];

// [167s] 
PN_PREFIX : PN_CHARS_BASE ((PN_CHARS | '.')* PN_CHARS)?;

// [168s] 
PN_LOCAL : (PN_CHARS_U | ':' | [0-9] | PLX) ((PN_CHARS | '.' | ':' | PLX)* (PN_CHARS | ':' | PLX))?;

// [169s] 
PLX : PERCENT | PN_LOCAL_ESC;

// [170s] 
PERCENT : '%' HEX HEX;

// [171s] 
HEX : [0-9] | [A-F] | [a-f];

// [172s] 
PN_LOCAL_ESC : '\\' ('_' | '~' | '.' | '-' | '!' | '$' | '&' | '\'' | '(' | ')' | '*' | '+' | ',' | ';' | '=' | '/' | '?' | '#' | '@' | '%');
