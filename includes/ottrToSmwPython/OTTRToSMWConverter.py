from includes.ottrToSmwPython.OTTRParser import OTTRParser
from includes.ottrToSmwPython.OTTRClassesForSMW import PrefixID, Parameter, Constant, Type, Signature, Template, Instance, Argument, Term, Annotation, Literal
from includes.ottrToSmwPython.SMWGenerator import SMWGenerator
from includes.ottrToSmwPython.Utils import get_text
from includes.ottrToSmwPython.stOTTR.stOTTRListener import stOTTRListener
from includes.ottrToSmwPython.stOTTR.stOTTRParser import stOTTRParser


class OTTRToSMWConverter(stOTTRListener):

	def __init__(self):
		self.term = None
		self.args_list = None
		self.otype = None
		self.template_name = None
		self.annos = None
		self.params = None
		self.signature = None
		self.instance = None
		self.patternlist = None
		self.anonymous_blank_node_counter = None
		self.instance_statements = None
		self.definition_statements = None
		self.prefixIds = None
		self.constant = None
		self.literal = None
		self.blank_node_name = None
		self.iri = None
		self.type_value = None
		self.template_name_buffer = None

	# Enter a parse tree produced by stOTTRParser#stOTTRDoc.
	def enterStOTTRDoc(self, ctx: stOTTRParser.StOTTRDocContext):
		self.prefixIds = []
		self.definition_statements = []
		self.instance_statements = []
		self.anonymous_blank_node_counter = 0

	# Exit a parse tree produced by stOTTRParser#stOTTRDoc.
	def exitStOTTRDoc(self, ctx: stOTTRParser.StOTTRDocContext):

		smw_generator = SMWGenerator(prefixes=self.prefixIds, definitions=self.definition_statements, instances=self.instance_statements)
		smw_code = smw_generator.produce_smw()

		self.prefixIds = None
		self.definition_statements = None
		self.instance_statements = None
		self.anonymous_blank_node_counter = None

	# Enter a parse tree produced by stOTTRParser#statement.
	def enterStatement(self, ctx: stOTTRParser.StatementContext):
		self.patternlist = None
		if ctx.instance():
			self.instance = None

	# Exit a parse tree produced by stOTTRParser#statement.
	def exitStatement(self, ctx: stOTTRParser.StatementContext):

		if ctx.instance():
			self.instance_statements.append(self.instance)
			#print(self.instance)
		else:
			self.definition_statements.append(Template(self.signature, self.patternlist))
		self.signature = None
		self.patternlist = None
		pass

	# Enter a parse tree produced by stOTTRParser#signature.
	def enterSignature(self, ctx: stOTTRParser.SignatureContext):
		self.params = []
		self.annos = []
		pass

	# Exit a parse tree produced by stOTTRParser#signature.
	def exitSignature(self, ctx: stOTTRParser.SignatureContext):

		self.signature = Signature(ctx, self.template_name, self.params, self.annos)
		self.params = None
		self.annos = None
		self.template_name = None

	# Enter a parse tree produced by stOTTRParser#templateName.
	def enterTemplateName(self, ctx: stOTTRParser.TemplateNameContext):
		pass

	# Exit a parse tree produced by stOTTRParser#templateName.
	def exitTemplateName(self, ctx: stOTTRParser.TemplateNameContext):
		self.template_name = self.iri
		self.iri = None
		self.args = self.args_list

	# Enter a parse tree produced by stOTTRParser#parameterList.
	def enterParameterList(self, ctx: stOTTRParser.ParameterListContext):
		pass

	# Exit a parse tree produced by stOTTRParser#parameterList.
	def exitParameterList(self, ctx: stOTTRParser.ParameterListContext):
		pass

	# Enter a parse tree produced by stOTTRParser#parameter.
	def enterParameter(self, ctx: stOTTRParser.ParameterContext):
		self.otype = None
		self.constant = None
		pass

	# Exit a parse tree produced by stOTTRParser#parameter.
	def exitParameter(self, ctx: stOTTRParser.ParameterContext):
		self.params.append(Parameter(ctx, otype=self.otype, pos=len(self.params) + 1, default=self.constant))
		self.otype = None
		self.constant = None
		pass

	# Enter a parse tree produced by stOTTRParser#defaultValue.
	def enterDefaultValue(self, ctx: stOTTRParser.DefaultValueContext):
		pass

	# Exit a parse tree produced by stOTTRParser#defaultValue.
	def exitDefaultValue(self, ctx: stOTTRParser.DefaultValueContext):
		pass

	# Enter a parse tree produced by stOTTRParser#annotationList.
	def enterAnnotationList(self, ctx: stOTTRParser.AnnotationListContext):
		self.template_name_buffer = self.template_name
		pass

	# Exit a parse tree produced by stOTTRParser#annotationList.
	def exitAnnotationList(self, ctx: stOTTRParser.AnnotationListContext):
		self.template_name = self.template_name_buffer
		self.template_name_buffer = None
		pass

	# Enter a parse tree produced by stOTTRParser#annotation.
	def enterAnnotation(self, ctx: stOTTRParser.AnnotationContext):
		self.instance = None
		pass

	# Exit a parse tree produced by stOTTRParser#annotation.
	def exitAnnotation(self, ctx: stOTTRParser.AnnotationContext):
		self.annos.append(Annotation(ctx, self.instance))
		self.instance = None
		pass

	# Enter a parse tree produced by stOTTRParser#baseTemplate.
	def enterBaseTemplate(self, ctx: stOTTRParser.BaseTemplateContext):
		pass

	# Exit a parse tree produced by stOTTRParser#baseTemplate.
	def exitBaseTemplate(self, ctx: stOTTRParser.BaseTemplateContext):
		self.patternlist = "BASE"
		pass

	# Enter a parse tree produced by stOTTRParser#template.
	def enterTemplate(self, ctx: stOTTRParser.TemplateContext):
		pass

	# Exit a parse tree produced by stOTTRParser#template.
	def exitTemplate(self, ctx: stOTTRParser.TemplateContext):
		pass

	# Enter a parse tree produced by stOTTRParser#patternList.
	def enterPatternList(self, ctx: stOTTRParser.PatternListContext):
		self.patternlist = []
		pass

	# Exit a parse tree produced by stOTTRParser#patternList.
	def exitPatternList(self, ctx: stOTTRParser.PatternListContext):
		pass

	# Enter a parse tree produced by stOTTRParser#instance.
	def enterInstance(self, ctx: stOTTRParser.InstanceContext):
		self.args_list = []

	# Exit a parse tree produced by stOTTRParser#instance.
	def exitInstance(self, ctx: stOTTRParser.InstanceContext):
		if type(self.patternlist) == list:
			inst = Instance(ctx, self.args_list, self.template_name, pos=len(self.patternlist) + 1, is_instance=False)
			for arg in inst.argument_list:
				#print(arg.term.c)
				pass
			self.patternlist.append(inst)

		else:  # if type(ctx.parentCtx) == stOTTRParser.AnnotationContext:
			is_instance = type(ctx.parentCtx) != stOTTRParser.AnnotationContext

			self.instance = Instance(ctx, self.args_list, self.template_name, len(self.instance_statements) + 1, is_instance=is_instance)

		self.template_name = None
		self.args_list = None

	# Enter a parse tree produced by stOTTRParser#argumentList.
	def enterArgumentList(self, ctx: stOTTRParser.ArgumentListContext):
		pass

	# Exit a parse tree produced by stOTTRParser#argumentList.
	def exitArgumentList(self, ctx: stOTTRParser.ArgumentListContext):
		pass

	# Enter a parse tree produced by stOTTRParser#argument.
	def enterArgument(self, ctx: stOTTRParser.ArgumentContext):
		self.term = None

	# Exit a parse tree produced by stOTTRParser#argument.
	def exitArgument(self, ctx: stOTTRParser.ArgumentContext):
		#print(self.term.ctx.getText())
		self.args_list.append(Argument(ctx, self.term))
		#print(len(self.args_list))
		self.term = None

	# Enter a parse tree produced by stOTTRParser#otype.
	def enterOtype(self, ctx: stOTTRParser.OtypeContext):
		if self.otype:
			self.otype.add_inner(Type(ctx))
		else:
			self.otype = Type(ctx)

	# Exit a parse tree produced by stOTTRParser#otype.
	def exitOtype(self, ctx: stOTTRParser.OtypeContext):
		if self.type_value:
			self.otype.insert_type_value(self.type_value)
			self.type_value = None

	# Enter a parse tree produced by stOTTRParser#listType.
	def enterListType(self, ctx: stOTTRParser.ListTypeContext):
		pass

	# Exit a parse tree produced by stOTTRParser#listType.
	def exitListType(self, ctx: stOTTRParser.ListTypeContext):
		pass

	# Enter a parse tree produced by stOTTRParser#neListType.
	def enterNeListType(self, ctx: stOTTRParser.NeListTypeContext):
		pass

	# Exit a parse tree produced by stOTTRParser#neListType.
	def exitNeListType(self, ctx: stOTTRParser.NeListTypeContext):
		pass

	# Enter a parse tree produced by stOTTRParser#lubType.
	def enterLubType(self, ctx: stOTTRParser.LubTypeContext):
		pass

	# Exit a parse tree produced by stOTTRParser#lubType.
	def exitLubType(self, ctx: stOTTRParser.LubTypeContext):
		pass

	# Enter a parse tree produced by stOTTRParser#basicType.
	def enterBasicType(self, ctx: stOTTRParser.BasicTypeContext):
		if type(ctx.parentCtx) == stOTTRParser.LubTypeContext:
			self.otype.add_inner(Type(ctx.parentCtx))
		pass

	# Exit a parse tree produced by stOTTRParser#basicType.
	def exitBasicType(self, ctx: stOTTRParser.BasicTypeContext):
		self.type_value = ctx.prefixedName().start.text
		pass

	# Enter a parse tree produced by stOTTRParser#term.
	def enterTerm(self, ctx: OTTRParser.TermContext):
		ctx.term = Term(ctx)

	# Exit a parse tree produced by stOTTRParser#term.
	def exitTerm(self, ctx: OTTRParser.TermContext):
		ctx.term.set_inner_constant(ctx)
		if type(ctx.parentCtx) == stOTTRParser.ArgumentContext:
			#print('\n\n', type(ctx.parentCtx), ctx.getText(), '\n\n')
			self.term = ctx.term
		elif type(ctx.parentCtx) == stOTTRParser.TermListContext:
			ctx.parentCtx.term.term_list.append(ctx.term)

	# Enter a parse tree produced by stOTTRParser#constant.
	def enterConstant(self, ctx: OTTRParser.ConstantContext):
		ctx.inner_constant_ref = Constant(ctx)

	# Exit a parse tree produced by stOTTRParser#constant.
	def exitConstant(self, ctx: OTTRParser.ConstantContext):
		if ctx.inner_constant_ref and ctx.inner_constant_ref.need_iri():
			ctx.inner_constant_ref.insert_iri(self.iri)
			self.iri = None
		if ctx.inner_constant_ref and ctx.inner_constant_ref.need_blank_node():
			ctx.inner_constant_ref.set_blank_node(self.blank_node_name)
			self.blank_node_name = None
		if ctx.inner_constant_ref and ctx.inner_constant_ref.need_literal():
			ctx.inner_constant_ref.set_literal(self.literal)
			self.literal = None
		if type(ctx.parentCtx) == OTTRParser.TermContext:
			ctx.parentCtx.inner_constant = ctx.inner_constant_ref
		elif type(ctx.parentCtx) == stOTTRParser.DefaultValueContext:
			self.constant = ctx.inner_constant_ref
		elif type(ctx.parentCtx) == stOTTRParser.ConstantListContext:
			ctx.parentCtx.parentCtx.inner_constant_ref.constant_list.append(ctx.inner_constant_ref)

	# Enter a parse tree produced by stOTTRParser#none.
	def enterNone(self, ctx: stOTTRParser.NoneContext):
		pass

	# Exit a parse tree produced by stOTTRParser#none.
	def exitNone(self, ctx: stOTTRParser.NoneContext):
		pass

	# Enter a parse tree produced by stOTTRParser#termList.
	def enterTermList(self, ctx: stOTTRParser.TermListContext):
		pass

	# Exit a parse tree produced by stOTTRParser#termList.
	def exitTermList(self, ctx: stOTTRParser.TermListContext):
		pass

	# Enter a parse tree produced by stOTTRParser#constantList.
	def enterConstantList(self, ctx: stOTTRParser.ConstantListContext):
		pass

	# Exit a parse tree produced by stOTTRParser#constantList.
	def exitConstantList(self, ctx: stOTTRParser.ConstantListContext):
		pass

	# Enter a parse tree produced by stOTTRParser#directive.
	def enterDirective(self, ctx: stOTTRParser.DirectiveContext):
		pass

	# Exit a parse tree produced by stOTTRParser#directive.
	def exitDirective(self, ctx: stOTTRParser.DirectiveContext):
		pass

	# Enter a parse tree produced by stOTTRParser#prefixID.
	def enterPrefixID(self, ctx: stOTTRParser.PrefixIDContext):
		self.prefixIds.append(PrefixID(ctx))
		pass

	# Exit a parse tree produced by stOTTRParser#prefixID.
	def exitPrefixID(self, ctx: stOTTRParser.PrefixIDContext):
		pass

	# Enter a parse tree produced by stOTTRParser#base.
	def enterBase(self, ctx: stOTTRParser.BaseContext):
		pass

	# Exit a parse tree produced by stOTTRParser#base.
	def exitBase(self, ctx: stOTTRParser.BaseContext):
		pass

	# Enter a parse tree produced by stOTTRParser#sparqlBase.
	def enterSparqlBase(self, ctx: stOTTRParser.SparqlBaseContext):
		pass

	# Exit a parse tree produced by stOTTRParser#sparqlBase.
	def exitSparqlBase(self, ctx: stOTTRParser.SparqlBaseContext):
		pass

	# Enter a parse tree produced by stOTTRParser#sparqlPrefix.
	def enterSparqlPrefix(self, ctx: stOTTRParser.SparqlPrefixContext):
		pass

	# Exit a parse tree produced by stOTTRParser#sparqlPrefix.
	def exitSparqlPrefix(self, ctx: stOTTRParser.SparqlPrefixContext):
		pass

	# Enter a parse tree produced by stOTTRParser#literal.
	def enterLiteral(self, ctx: stOTTRParser.LiteralContext):
		pass

	# Exit a parse tree produced by stOTTRParser#literal.
	def exitLiteral(self, ctx: stOTTRParser.LiteralContext):
		if ctx.BooleanLiteral():
			self.literal = Literal(get_text(ctx.BooleanLiteral()), Literal.LiteralType.BOOL)
		pass

	# Enter a parse tree produced by stOTTRParser#numericLiteral.
	def enterNumericLiteral(self, ctx: stOTTRParser.NumericLiteralContext):
		if ctx.INTEGER():
			self.literal = Literal(get_text(ctx.INTEGER()), Literal.LiteralType.INTEGER)
		elif ctx.DECIMAL():
			self.literal = Literal(get_text(ctx.DECIMAL()), Literal.LiteralType.DECIMAL)
		else:
			self.literal = Literal(get_text(ctx.DOUBLE()), Literal.LiteralType.DECIMAL)

	# Exit a parse tree produced by stOTTRParser#numericLiteral.
	def exitNumericLiteral(self, ctx: stOTTRParser.NumericLiteralContext):
		pass

	# Enter a parse tree produced by stOTTRParser#rdfLiteral.
	def enterRdfLiteral(self, ctx: stOTTRParser.RdfLiteralContext):
		pass

	# Exit a parse tree produced by stOTTRParser#rdfLiteral.
	def exitRdfLiteral(self, ctx: stOTTRParser.RdfLiteralContext):
		if ctx.iri():
			self.literal = Literal(get_text(ctx.String()), Literal.LiteralType.RDFLIT, (Literal.LiteralType.IRI_, self.iri))
			self.iri = None
		elif ctx.LANGTAG():
			self.literal = Literal(get_text(ctx.String()), Literal.LiteralType.RDFLIT, (Literal.LiteralType.LANG_, get_text(ctx.LANGTAG())))
		else:
			self.literal = Literal(get_text(ctx.String()), Literal.LiteralType.RDFLIT)

	# Enter a parse tree produced by stOTTRParser#iri.
	def enterIri(self, ctx: stOTTRParser.IriContext):
		if ctx.prefixedName():
			self.iri = ctx.prefixedName().start.text
		else:
			self.iri = get_text(ctx.IRIREF())

	# Exit a parse tree produced by stOTTRParser#iri.
	def exitIri(self, ctx: stOTTRParser.IriContext):
		pass

	# Enter a parse tree produced by stOTTRParser#prefixedName.
	def enterPrefixedName(self, ctx: stOTTRParser.PrefixedNameContext):
		pass

	# Exit a parse tree produced by stOTTRParser#prefixedName.
	def exitPrefixedName(self, ctx: stOTTRParser.PrefixedNameContext):
		pass

	# Enter a parse tree produced by stOTTRParser#blankNode.
	def enterBlankNode(self, ctx: stOTTRParser.BlankNodeContext):
		if ctx.anon():
			self.anonymous_blank_node_counter += 1
			self.blank_node_name = str(self.anonymous_blank_node_counter)
		else:
			self.blank_node_name = get_text(ctx.BLANK_NODE_LABEL())[2:]

	# Exit a parse tree produced by stOTTRParser#blankNode.
	def exitBlankNode(self, ctx: stOTTRParser.BlankNodeContext):
		pass

	# Enter a parse tree produced by stOTTRParser#anon.
	def enterAnon(self, ctx: stOTTRParser.AnonContext):
		pass

	# Exit a parse tree produced by stOTTRParser#anon.
	def exitAnon(self, ctx: stOTTRParser.AnonContext):
		pass
