//From https://dev.spec.ottr.xyz/stOTTR/stOTTR.g4
// Changes:
// - adding python target
// - rename type nonterminal to otype to avoid conflict with python
// - add constantList-rule and constantList to constant as an alternative.

grammar stOTTR;
options {language=Python3;} // Only change in document..

import Turtle;


stOTTRDoc
 : ( directive // Turtle prefixes and base
   | statement )* EOF
 ;

statement
 : ( signature
     | template
     | baseTemplate
     | instance
   )
 '.'
 ;


/*** Comments ***/

Comment
 : '#' ~('\r' | '\n')* -> skip
 ;

CommentBlock
 : '/***' .*? '***/' -> skip
 ;


/*** Signature ***/

signature
 : templateName parameterList annotationList?
 ;

templateName
 : iri
 ;

parameterList
 : '[' (parameter (',' parameter)*)? ']'
 ;

parameter
 : ParameterMode* otype? Variable defaultValue?
 ;

ParameterMode
 : '?'  /* optional */
 | '!'  /* non blank */
 ;

defaultValue
 : '=' constant
 ;

annotationList
 : annotation (',' annotation)*
 ;

annotation
 : '@@' instance
 ;


/*** Templates ***/

baseTemplate
 : signature '::' 'BASE'
 ;

template
 : signature '::' patternList
 ;

patternList
 : '{' (instance (',' instance)*)? '}'
 ;


/*** Instance ***/

instance
 : (ListExpander '|')? templateName argumentList
 ;

ListExpander
 : 'cross'
 | 'zipMin'
 | 'zipMax'
 ;

argumentList
 : '(' (argument (',' argument)*)? ')'
 ;

argument
 : ListExpand? term
 ;

ListExpand
 : '++'
 ;


/*** Types ***/

otype
 : basicType
 | lubType
 | listType
 | neListType
 ;

listType
 : 'List<' otype '>'
 ;

neListType
 : 'NEList<' otype '>'
 ;

lubType
 : 'LUB<' basicType '>'
 ;

basicType
 : prefixedName
 ;


/*** Terms ***/

term
 : Variable
 | constant
 | termList
 ;

Variable
 : '?' BNodeLabel
 ;

/* Turtle blank node labels without trailing '_:' */
fragment BNodeLabel
 : (PN_CHARS_U) ((PN_CHARS | '.')* PN_CHARS)?
 ;


constant
 : iri
 | blankNode
 | literal
 | none
 | constantList
 ;

none
 : 'none'
 ;

termList
 : '(' (term (',' term)*)? ')'
 ;

constantList
 : '(' (constant (',' constant)*)? ')'
 ;
