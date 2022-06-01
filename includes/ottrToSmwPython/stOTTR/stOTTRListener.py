# Generated from stOTTR.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .stOTTRParser import stOTTRParser
else:
    from stOTTRParser import stOTTRParser

# This class defines a complete listener for a parse tree produced by stOTTRParser.
class stOTTRListener(ParseTreeListener):

    # Enter a parse tree produced by stOTTRParser#stOTTRDoc.
    def enterStOTTRDoc(self, ctx:stOTTRParser.StOTTRDocContext):
        pass

    # Exit a parse tree produced by stOTTRParser#stOTTRDoc.
    def exitStOTTRDoc(self, ctx:stOTTRParser.StOTTRDocContext):
        pass


    # Enter a parse tree produced by stOTTRParser#statement.
    def enterStatement(self, ctx:stOTTRParser.StatementContext):
        pass

    # Exit a parse tree produced by stOTTRParser#statement.
    def exitStatement(self, ctx:stOTTRParser.StatementContext):
        pass


    # Enter a parse tree produced by stOTTRParser#signature.
    def enterSignature(self, ctx:stOTTRParser.SignatureContext):
        pass

    # Exit a parse tree produced by stOTTRParser#signature.
    def exitSignature(self, ctx:stOTTRParser.SignatureContext):
        pass


    # Enter a parse tree produced by stOTTRParser#templateName.
    def enterTemplateName(self, ctx:stOTTRParser.TemplateNameContext):
        pass

    # Exit a parse tree produced by stOTTRParser#templateName.
    def exitTemplateName(self, ctx:stOTTRParser.TemplateNameContext):
        pass


    # Enter a parse tree produced by stOTTRParser#parameterList.
    def enterParameterList(self, ctx:stOTTRParser.ParameterListContext):
        pass

    # Exit a parse tree produced by stOTTRParser#parameterList.
    def exitParameterList(self, ctx:stOTTRParser.ParameterListContext):
        pass


    # Enter a parse tree produced by stOTTRParser#parameter.
    def enterParameter(self, ctx:stOTTRParser.ParameterContext):
        pass

    # Exit a parse tree produced by stOTTRParser#parameter.
    def exitParameter(self, ctx:stOTTRParser.ParameterContext):
        pass


    # Enter a parse tree produced by stOTTRParser#defaultValue.
    def enterDefaultValue(self, ctx:stOTTRParser.DefaultValueContext):
        pass

    # Exit a parse tree produced by stOTTRParser#defaultValue.
    def exitDefaultValue(self, ctx:stOTTRParser.DefaultValueContext):
        pass


    # Enter a parse tree produced by stOTTRParser#annotationList.
    def enterAnnotationList(self, ctx:stOTTRParser.AnnotationListContext):
        pass

    # Exit a parse tree produced by stOTTRParser#annotationList.
    def exitAnnotationList(self, ctx:stOTTRParser.AnnotationListContext):
        pass


    # Enter a parse tree produced by stOTTRParser#annotation.
    def enterAnnotation(self, ctx:stOTTRParser.AnnotationContext):
        pass

    # Exit a parse tree produced by stOTTRParser#annotation.
    def exitAnnotation(self, ctx:stOTTRParser.AnnotationContext):
        pass


    # Enter a parse tree produced by stOTTRParser#baseTemplate.
    def enterBaseTemplate(self, ctx:stOTTRParser.BaseTemplateContext):
        pass

    # Exit a parse tree produced by stOTTRParser#baseTemplate.
    def exitBaseTemplate(self, ctx:stOTTRParser.BaseTemplateContext):
        pass


    # Enter a parse tree produced by stOTTRParser#template.
    def enterTemplate(self, ctx:stOTTRParser.TemplateContext):
        pass

    # Exit a parse tree produced by stOTTRParser#template.
    def exitTemplate(self, ctx:stOTTRParser.TemplateContext):
        pass


    # Enter a parse tree produced by stOTTRParser#patternList.
    def enterPatternList(self, ctx:stOTTRParser.PatternListContext):
        pass

    # Exit a parse tree produced by stOTTRParser#patternList.
    def exitPatternList(self, ctx:stOTTRParser.PatternListContext):
        pass


    # Enter a parse tree produced by stOTTRParser#instance.
    def enterInstance(self, ctx:stOTTRParser.InstanceContext):
        pass

    # Exit a parse tree produced by stOTTRParser#instance.
    def exitInstance(self, ctx:stOTTRParser.InstanceContext):
        pass


    # Enter a parse tree produced by stOTTRParser#argumentList.
    def enterArgumentList(self, ctx:stOTTRParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by stOTTRParser#argumentList.
    def exitArgumentList(self, ctx:stOTTRParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by stOTTRParser#argument.
    def enterArgument(self, ctx:stOTTRParser.ArgumentContext):
        pass

    # Exit a parse tree produced by stOTTRParser#argument.
    def exitArgument(self, ctx:stOTTRParser.ArgumentContext):
        pass


    # Enter a parse tree produced by stOTTRParser#otype.
    def enterOtype(self, ctx:stOTTRParser.OtypeContext):
        pass

    # Exit a parse tree produced by stOTTRParser#otype.
    def exitOtype(self, ctx:stOTTRParser.OtypeContext):
        pass


    # Enter a parse tree produced by stOTTRParser#listType.
    def enterListType(self, ctx:stOTTRParser.ListTypeContext):
        pass

    # Exit a parse tree produced by stOTTRParser#listType.
    def exitListType(self, ctx:stOTTRParser.ListTypeContext):
        pass


    # Enter a parse tree produced by stOTTRParser#neListType.
    def enterNeListType(self, ctx:stOTTRParser.NeListTypeContext):
        pass

    # Exit a parse tree produced by stOTTRParser#neListType.
    def exitNeListType(self, ctx:stOTTRParser.NeListTypeContext):
        pass


    # Enter a parse tree produced by stOTTRParser#lubType.
    def enterLubType(self, ctx:stOTTRParser.LubTypeContext):
        pass

    # Exit a parse tree produced by stOTTRParser#lubType.
    def exitLubType(self, ctx:stOTTRParser.LubTypeContext):
        pass


    # Enter a parse tree produced by stOTTRParser#basicType.
    def enterBasicType(self, ctx:stOTTRParser.BasicTypeContext):
        pass

    # Exit a parse tree produced by stOTTRParser#basicType.
    def exitBasicType(self, ctx:stOTTRParser.BasicTypeContext):
        pass


    # Enter a parse tree produced by stOTTRParser#term.
    def enterTerm(self, ctx:stOTTRParser.TermContext):
        pass

    # Exit a parse tree produced by stOTTRParser#term.
    def exitTerm(self, ctx:stOTTRParser.TermContext):
        pass


    # Enter a parse tree produced by stOTTRParser#constant.
    def enterConstant(self, ctx:stOTTRParser.ConstantContext):
        pass

    # Exit a parse tree produced by stOTTRParser#constant.
    def exitConstant(self, ctx:stOTTRParser.ConstantContext):
        pass


    # Enter a parse tree produced by stOTTRParser#none.
    def enterNone(self, ctx:stOTTRParser.NoneContext):
        pass

    # Exit a parse tree produced by stOTTRParser#none.
    def exitNone(self, ctx:stOTTRParser.NoneContext):
        pass


    # Enter a parse tree produced by stOTTRParser#termList.
    def enterTermList(self, ctx:stOTTRParser.TermListContext):
        pass

    # Exit a parse tree produced by stOTTRParser#termList.
    def exitTermList(self, ctx:stOTTRParser.TermListContext):
        pass


    # Enter a parse tree produced by stOTTRParser#constantList.
    def enterConstantList(self, ctx:stOTTRParser.ConstantListContext):
        pass

    # Exit a parse tree produced by stOTTRParser#constantList.
    def exitConstantList(self, ctx:stOTTRParser.ConstantListContext):
        pass


    # Enter a parse tree produced by stOTTRParser#directive.
    def enterDirective(self, ctx:stOTTRParser.DirectiveContext):
        pass

    # Exit a parse tree produced by stOTTRParser#directive.
    def exitDirective(self, ctx:stOTTRParser.DirectiveContext):
        pass


    # Enter a parse tree produced by stOTTRParser#prefixID.
    def enterPrefixID(self, ctx:stOTTRParser.PrefixIDContext):
        pass

    # Exit a parse tree produced by stOTTRParser#prefixID.
    def exitPrefixID(self, ctx:stOTTRParser.PrefixIDContext):
        pass


    # Enter a parse tree produced by stOTTRParser#base.
    def enterBase(self, ctx:stOTTRParser.BaseContext):
        pass

    # Exit a parse tree produced by stOTTRParser#base.
    def exitBase(self, ctx:stOTTRParser.BaseContext):
        pass


    # Enter a parse tree produced by stOTTRParser#sparqlBase.
    def enterSparqlBase(self, ctx:stOTTRParser.SparqlBaseContext):
        pass

    # Exit a parse tree produced by stOTTRParser#sparqlBase.
    def exitSparqlBase(self, ctx:stOTTRParser.SparqlBaseContext):
        pass


    # Enter a parse tree produced by stOTTRParser#sparqlPrefix.
    def enterSparqlPrefix(self, ctx:stOTTRParser.SparqlPrefixContext):
        pass

    # Exit a parse tree produced by stOTTRParser#sparqlPrefix.
    def exitSparqlPrefix(self, ctx:stOTTRParser.SparqlPrefixContext):
        pass


    # Enter a parse tree produced by stOTTRParser#literal.
    def enterLiteral(self, ctx:stOTTRParser.LiteralContext):
        pass

    # Exit a parse tree produced by stOTTRParser#literal.
    def exitLiteral(self, ctx:stOTTRParser.LiteralContext):
        pass


    # Enter a parse tree produced by stOTTRParser#numericLiteral.
    def enterNumericLiteral(self, ctx:stOTTRParser.NumericLiteralContext):
        pass

    # Exit a parse tree produced by stOTTRParser#numericLiteral.
    def exitNumericLiteral(self, ctx:stOTTRParser.NumericLiteralContext):
        pass


    # Enter a parse tree produced by stOTTRParser#rdfLiteral.
    def enterRdfLiteral(self, ctx:stOTTRParser.RdfLiteralContext):
        pass

    # Exit a parse tree produced by stOTTRParser#rdfLiteral.
    def exitRdfLiteral(self, ctx:stOTTRParser.RdfLiteralContext):
        pass


    # Enter a parse tree produced by stOTTRParser#iri.
    def enterIri(self, ctx:stOTTRParser.IriContext):
        pass

    # Exit a parse tree produced by stOTTRParser#iri.
    def exitIri(self, ctx:stOTTRParser.IriContext):
        pass


    # Enter a parse tree produced by stOTTRParser#prefixedName.
    def enterPrefixedName(self, ctx:stOTTRParser.PrefixedNameContext):
        pass

    # Exit a parse tree produced by stOTTRParser#prefixedName.
    def exitPrefixedName(self, ctx:stOTTRParser.PrefixedNameContext):
        pass


    # Enter a parse tree produced by stOTTRParser#blankNode.
    def enterBlankNode(self, ctx:stOTTRParser.BlankNodeContext):
        pass

    # Exit a parse tree produced by stOTTRParser#blankNode.
    def exitBlankNode(self, ctx:stOTTRParser.BlankNodeContext):
        pass


    # Enter a parse tree produced by stOTTRParser#anon.
    def enterAnon(self, ctx:stOTTRParser.AnonContext):
        pass

    # Exit a parse tree produced by stOTTRParser#anon.
    def exitAnon(self, ctx:stOTTRParser.AnonContext):
        pass


