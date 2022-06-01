import textwrap

from includes.ottrToSmwPython.OTTRParser import OTTRParser
from includes.ottrToSmwPython.Utils import get_text, DELIMITERS, get_min_max_size, get_prefix_special_page_name, VarNames, get_input_type_of_ottr_type
from includes.ottrToSmwPython.stOTTR.stOTTRParser import stOTTRParser
from typing import List


class SMWContext:
	"""	Transfer object for the argument representation of a template and the call occurrence counter.

	It also provides methods for generating code for the debug display part.
	"""
	IF_DEBUG = "{{#ifexpr: {{ottr:DebugOnOFF}}|%s}}"

	def __init__(self):
		self.variable_positions = None
		self.variable_strings = None
		self.default_repr_type = None
		self.call_occurrence_position = 0

	def produce_debug_str_start(self):
		""" For every information define (init) a variable for storing the debug info while executing the wiki code.

		:return: string of the init part of the debug display part.
		"""
		number_triples_init = "{{#vardefine:%s|0}}" % VarNames.TripleCount
		used_iris_init = "{{#vardefine:%s|}}" % VarNames.UsedIris
		max_depth_init = "{{#vardefine:%s|0}}" % VarNames.MaxDepth
		used_templates_init = "{{#vardefine:%s|}}" % VarNames.UsedTemplates

		return self.IF_DEBUG % (number_triples_init + used_iris_init + max_depth_init + used_templates_init)

	def produce_debug_str_end(self):
		""" Collect the information from the init variables.

		:return: string of the extraction and display part of the debug display string.
		"""
		number_triples = "{{#var:%s}}" % VarNames.TripleCount
		used_iris = "{{#arraydefine:ottr_used_iris_set|{{#var: %s}}|,}}{{#arrayunique:ottr_used_iris_set}}{{#arraysize:ottr_used_iris_set}}" \
					"{{#arrayreset:ottr_used_iris_set}}" % VarNames.UsedIris
		max_depth = "{{#var:%s}}" % VarNames.MaxDepth
		used_templates = ("{{#arraydefine:ottr_used_templates_set|{{#var:%s}}|,}}"
						"{{#arrayunique:ottr_used_templates_set}}"
						"{{#loop: ottr_used_templates_idx|0|{{#arraysize:ottr_used_templates_set}}|"
						"{{#ifexpr: {{#var:ottr_used_templates_idx}}|-|:-}} {{#arrayindex:ottr_used_templates_set|{{#var:ottr_used_templates_idx}}}}:  "
						"<b>{{#count:{{#var:%s}}|{{#arrayindex:ottr_used_templates_set|{{#var:ottr_used_templates_idx}}}},}}</b><br/>}}"
						"{{#arrayreset:ottr_used_templates_set}}" % (VarNames.UsedTemplates, VarNames.UsedTemplates))
		return self.IF_DEBUG % ("<b>Debug Info:</b>\n"
								"* <i>Number Init Triples:</i> <b>%s</b>\n"
								"* <i>Number Used IRIs:</i> <b>%s</b>\n"
								"* <i>Max Depth:</i> <b>%s</b>\n"
								"* <i>Used Templates:</i>\n%s\n<nowiki/>\n" % (number_triples, used_iris, max_depth, used_templates))

	def update_used_iri_triple(self):
		return ''.join([self.update_used_iri_single(i) for i in range(1, 4)])

	@staticmethod
	def increase_triple_count():
		return "{{#vardefine: %s|{{#expr:{{#var:%s}} + 1}}}}" % (VarNames.TripleCount, VarNames.TripleCount)

	@staticmethod
	def update_max_depth():
		return "{{#ifexpr: {{{call_depth}}} > {{#var:%s}}|{{#vardefine:%s|{{{call_depth}}}}}|}}" % (VarNames.MaxDepth, VarNames.MaxDepth)

	@staticmethod
	def update_used_templates(template_name):
		return "{{#vardefine:%s|{{#var:%s}}%s%s}}" % (VarNames.UsedTemplates, VarNames.UsedTemplates, template_name, ",")

	@staticmethod
	def produce_triple_display():
		return "{{#ifexpr: {{ottr:DisplayTriplesOnOff}}|{{ottr:AskForTriples}}}}"

	@staticmethod
	def update_used_iri_single(reference):
		return "{{#if: {{#pos:{{{ottr_arg_type_%i|}}}|ottr:IRI§}}|{{#vardefine: %s|{{#var:%s}}{{{%i|}}},}}}}" % (reference, VarNames.UsedIris, VarNames.UsedIris, reference)


class PrefixID:

	def __init__(self, ctx: stOTTRParser.PrefixIDContext):
		self.namespace = ctx.PNAME_NS().symbol.text[:-1]
		self.iri = ctx.IRIREF().symbol.text

	def has_namespace(self):
		return len(self.namespace) > 0

	def get_smw_repr(self):
		"""Produce the SMW Code for this prefix, such that, in case of rdf extraction of all generated ottr-triples, the information is in the database.

		Generate code for: Produce prefix sub-objects on the special prefix page if the code is present on such side.
		And check otherwise if such prefix is already on that page.

		:return: String with SMW Code
		"""
		return "{{#ifeq:{{FULLPAGENAME}}|%s|{{ottr:Prefix|%s|%s}}|{{ottr:PrefixCheck|%s|%s}}}}" % (
			get_prefix_special_page_name(),
			self.iri,
			self.namespace,
			self.iri,
			self.namespace,
		)


class Type:
	"""	Class, that contains the information about a type restriction in the signature of a template definition.

	For simple comparison the parser only uses a ottr:IRI for all not used Literal Types (See the type string repr for iris in constants).
	NELists are Lists and LUB is ignored. More complex comparisons are only warnings.
	"""
	class KindOfTypes:
		LUB = "LUB"
		LIST = "List"
		NELIST = "NEList"
		BASIC = "BASIC"

	def __init__(self, ctx: stOTTRParser.OtypeContext):
		self.inner = None
		self.type_value = None
		self.type_ = None
		self.need_type_value = False

		if ctx.basicType():
			self.need_type_value = True
			self.type_ = self.KindOfTypes.BASIC
		elif ctx.lubType():
			self.type_ = self.KindOfTypes.LUB
		elif ctx.listType():
			self.type_ = self.KindOfTypes.LIST
		elif ctx.neListType():
			self.type_ = self.KindOfTypes.NELIST

		self.LITERAL_TYPES = {"rdfs:resource", "xsd:boolean", "xsd:float", "xsd:integer", "xsd:string"}
		self.SIMPLE_TYPES = self.LITERAL_TYPES | {"ottr:IRI"}

	def add_inner(self, inner):
		if self.inner:
			self.inner.add_inner(inner)
		else:
			self.inner = inner

	def insert_type_value(self, type_value):
		if self.need_type_value:
			self.type_value = type_value
			self.need_type_value = False
		else:
			self.inner.insert_type_value(type_value)

	def get_type_repr(self, original=False):
		""" Representation for type checking.

		NEList has the same repr as Lists, LUB shows only the inner. A type that is not known as a Literal Type is replaces as an abstracted ottr:IRI-

		:param original: for checking with the exactly specified type (not only ottr:IRI)
		:return: the reduced type representation.
		"""
		if self.type_ == self.KindOfTypes.BASIC:
			# the type representation is abstracted to the known simple types. Unknown URIs are pooled in ottr:IRI
			if self.type_value in self.LITERAL_TYPES or original:
				return self.type_value
			return "ottr:IRI"
		# the representation of the LUB type kind is equivalent to the representation of the inner type. And is checked only in the template repr.
		if self.type_ == self.KindOfTypes.LUB:
			return self.inner.get_type_repr()
		# the representation of the check for Not Empty Lists and normal Lists are the same. Also checked in the template repr.
		return f"List<{self.inner.get_type_repr()}>"

	def get_nested_type_value(self):
		tmp_type_ref = self
		while tmp_type_ref.inner:
			tmp_type_ref = tmp_type_ref.inner
		return tmp_type_ref.type_value

	def is_lub_type(self):
		return self.type_ == self.KindOfTypes.LUB

	def is_list_type(self):
		return self.type_ in [self.KindOfTypes.LIST, self.KindOfTypes.NELIST]

	def is_any_uri_type(self):
		return self.type_ == self.KindOfTypes.BASIC and self.type_value not in self.LITERAL_TYPES

	def is_simple_type_request(self):
		return self.get_nested_type_value() in self.SIMPLE_TYPES

	def get_smw_repr(self, smw_context: SMWContext = None):
		""" For displaying in forms the correct representation.

		:param smw_context: not important, only for consistency with other get_smw_repr methods.
		:return: string: same to the input of  the type restriction.
		"""
		if self.type_ == self.KindOfTypes.BASIC:
			return f"{self.type_value}"
		else:
			return f"{self.type_}&lt;{self.inner.get_smw_repr(smw_context)}&gt;"


class Constant:
	""" Class for containing the information of the constant parts of an ottr-call.

	Can generate strings, that define arrays for a list constant.
	Can be an iri, blank_node, none, a literal or a list of constant.
	ottr:none is also handled as none.
	"""

	def __init__(self, ctx: OTTRParser.ConstantContext):
		self.constant_list = None
		self.iri = None
		self.blank_node = None
		self.none = None
		self.literal: Literal or None = None
		self.need_attribute = None  # for getting the value inside the parser tree

		if ctx.constantList():
			self.constant_list = []
		elif ctx.iri():
			self.need_attribute = "iri"
		elif ctx.blankNode():
			self.need_attribute = "blankNode"
		elif ctx.literal():
			self.need_attribute = "literal"
		elif ctx.none():
			self.none = True

		self.constant_list_smw_key = None
		self.constant_list_type = None

		self.source_str = " ".join(ctx.start.source[1].strdata[ctx.start.start:ctx.stop.stop + 1].split())

	def need_iri(self):
		return self.need_attribute == "iri"

	def need_blank_node(self):
		return self.need_attribute == "blankNode"

	def need_literal(self):
		return self.need_attribute == "literal"

	def is_constant_list(self):
		return self.constant_list is not None

	def insert_iri(self, iri):
		if iri.lower() == "ottr:none":
			self.iri = None
			self.none = True
		else:
			self.iri = iri
		self.need_attribute = None

	def set_blank_node(self, blank_node):
		self.blank_node = blank_node
		self.need_attribute = None

	def set_literal(self, literal):
		self.literal = literal
		self.need_attribute = None

	def define_list(self, list_pos, smw_context: SMWContext = None, is_instance=False):
		if self.is_constant_list():
			if is_instance:
				call_occur = "{{FULLPAGENAME}}"
			else:
				call_occur = "{{{call_occurrence}}}"
			# complex representation of lists in arrays: Lists in general are referred via there array keys.
			# elements in arrays contain first the value and than the type of the value (separated by a delimiter, e.g. ;)
			define_string = "".join([constant.define_list(f"{list_pos}_{pos}", smw_context, is_instance) for pos, constant in enumerate(self.constant_list)])
			list_key = "%s_%i_listkey_%s" % (call_occur, smw_context.call_occurrence_position, list_pos)  # Template call that generates valid list key
			self.constant_list_smw_key = list_key
			# the type of a list depends on the intersection of all the types in the type string and an adjustment with List<...>
			self.constant_list_type = "{{ottr:ListType|%s}}" % self.get_list_repr_string(DELIMITERS.ARRAY_ELEM_SPLIT, smw_context, False)
			array_define_template_call = "{{#arraydefine:%s|%s|%s}}" % (
				list_key,
				self.get_list_repr_string(DELIMITERS.ARRAY_ELEM_SPLIT, smw_context),
				DELIMITERS.ARRAY_ELEM_SPLIT
			)
			return define_string + array_define_template_call  # + "\n"
		return ""

	def get_list_repr_string(self, delimiter, smw_context: SMWContext = None, with_value=True):
		return delimiter.join([((constant.get_smw_repr(smw_context) + DELIMITERS.VALUE_TYPE_SPLIT) if with_value else "")
							+ constant.get_smw_repr_type(smw_context) for constant in self.constant_list])

	def get_smw_repr(self, smw_context: SMWContext = None, for_form = False):
		if self.iri:
			return self.iri
		elif self.blank_node:
			return "ottr:blank:{{{call_occurrence}}}_BN-%s" % self.blank_node
		elif self.literal:
			return self.literal.get_smw_repr()
		elif self.none:
			return ""
		else:
			if for_form:
				return self.source_str
			return self.constant_list_smw_key

	def get_smw_repr_type(self, smw_context: SMWContext = None):
		if self.iri:
			return "ottr:IRI§rdfs:resource§"
		elif self.blank_node:
			return "ottr:blank§ottr:IRI§rdfs:resource§"
		elif self.literal:
			return self.literal.get_smw_repr_type(smw_context)
		elif self.none:
			return "ottr:none§"
		else:
			return self.constant_list_type


class Parameter:
	""" Class containing information about a parameter of a template.

	Parameter modes are optional (?) and non_blank (!). It has a name and maybe a type restriction and maybe a default value,
	The arguments in ottr are not named accessible only positional, so the class has a attribute of the position in the template signature (1-based)
	"""

	def __init__(self, ctx: stOTTRParser.ParameterContext, otype: Type, pos: int, default: Constant):
		self.parameter_modes = [get_text(mode) for mode in ctx.ParameterMode()]
		self.name = get_text(ctx.Variable())
		self.otype = None
		self.default = None

		self.pos = pos

		if ctx.otype():
			self.otype = otype
		if ctx.defaultValue():
			self.default = default

	def is_optional(self):
		return '?' in self.parameter_modes

	def is_non_blank(self):
		return '!' in self.parameter_modes

	def get_variable_repr(self, smw_context: SMWContext = None):
		if self.default:
			return "{{#if: {{{%s|}}}|{{{%s}}}|%s}}" % (self.pos, self.pos, self.default.get_smw_repr(smw_context))
		else:
			return "{{{%s|}}}" % self.pos

	def get_default_repr_type(self, smw_context: SMWContext = None):
		if self.default:
			return self.default.get_smw_repr_type(smw_context)
		else:
			return "ottr:none"


class Argument:
	""" Class, containing the term of the argument and if it is written with a list_expand sign (++). """

	def __init__(self, ctx: stOTTRParser.ArgumentContext, term):
		self.list_expand = False
		if ctx.ListExpand():
			self.list_expand = True
		self.term = term

	def has_list_expand(self):
		return self.list_expand

	def get_smw_repr(self, smw_context: SMWContext = None, pattern=None, idx_ref=(None, None)):
		# pattern and idx_ref is for list representations
		if self.list_expand and pattern:
			return "{{#explode:%s|%s|0}}" % (pattern, DELIMITERS.VALUE_TYPE_SPLIT)
		if self.list_expand and idx_ref[0]:
			return self.get_smw_repr(smw_context, pattern="{{#arrayindex: %s|{{#var: %s}} }}" % (idx_ref[1], idx_ref[0]))
		return self.term.get_smw_repr(smw_context)

	def get_smw_repr_type(self, smw_context: SMWContext = None, pattern=None, idx_ref=(None, None)):
		# pattern and idx_ref is for list representations
		if self.list_expand and pattern:
			return "{{#explode:%s|%s|1}}" % (pattern, DELIMITERS.VALUE_TYPE_SPLIT)
		if self.list_expand and idx_ref[0]:
			return self.get_smw_repr_type(smw_context, pattern="{{#arrayindex: %s|{{#var: %s}} }}" % (idx_ref[1], idx_ref[0]))
		return self.term.get_smw_repr_type(smw_context)


class Instance:
	""" Class, containing the information about the instances in an ottr-call. Differs between instances inside a template and outside.

	Template calls inside the media wiki code of instances have here additional arguments: call_occurrence, call_depth and
	for every normal argument a type argument with the type string for the corresponding argument.
	"""
	LIST_EXPAND_ERROR = "{{ottr:ErrorMsg|List expander needs argument with list expand and vis versa|code=6}}"
	VARIABLE_USAGE_ERROR = "{{ottr:ErrorMsg|No variables allowed in instances outside a template|code=5}}"

	def __init__(self, ctx: stOTTRParser.InstanceContext, argument_list: List[Argument], template_name: str, pos: int, is_instance: bool):
		self.list_expander = None
		self.template_name = template_name
		self.argument_list = argument_list

		self.pos = pos
		self.is_instance = is_instance
		if ctx.ListExpander():
			self.list_expander = get_text(ctx.ListExpander())
		self.additional_args = ""

	def get_smw_repr(self, smw_context: SMWContext = None):
		if self.correct_variable_usage():
			if self.correct_list_expand_usage():
				smw = self.define_arrays(smw_context)
				if self.list_expander is None:
					smw += "{{%s%s}}" % (self.template_name, self.argument_list_smw_repr(smw_context))
				else:
					smw += self.list_expand_smw_repr(smw_context)
					smw_context.call_occurrence_position += 1
				# idea: here undefine arrays ?
				return smw
			else:
				return self.LIST_EXPAND_ERROR
		else:
			return self.VARIABLE_USAGE_ERROR

	def argument_list_smw_repr(self, smw_context: SMWContext = None, idx_ref_keys=None):
		idx_keys = ""
		if idx_ref_keys:
			for i_k in sorted(list(set([k[0] for k in idx_ref_keys if k[0]]))):
				idx_keys += "_lexp_{{#var:%s}}" % i_k
		# additional arguments in template calls are: call_occurrence, call_depth and for each normal argument ottr_arg_type_%i containing the type string
		if self.is_instance:
			call_occurrence = "|call_occurrence={{FULLPAGENAME}}_%s%s|call_depth=1%s" % (smw_context.call_occurrence_position, idx_keys, self.additional_args)
		else:
			call_occurrence = "|call_occurrence={{{call_occurrence}}}_%s%s|call_depth={{#expr:{{{call_depth}}}+1}}%s" % (smw_context.call_occurrence_position, idx_keys, self.additional_args)

		if self.argument_list:
			if not idx_ref_keys:
				idx_ref_keys = [(None, None)] * len(self.argument_list)
			return ("|" + "|".join([arg.get_smw_repr(smw_context, idx_ref=idx_ref_keys[idx]) for idx, arg in enumerate(self.argument_list)])
					+ "|" + "|".join([f"ottr_arg_type_{idx + 1}={arg.get_smw_repr_type(smw_context, idx_ref=idx_ref_keys[idx])}" for idx, arg in enumerate(self.argument_list)])
					+ call_occurrence)
		return call_occurrence

	def list_expand_smw_repr(self, smw_context: SMWContext = None):
		array_keys = self.get_array_keys(smw_context)
		if self.number_of_list_expand() == 1:
			# only one list does not to concatenate a list only simple expand
			return "{{#loop: {{{call_occurrence}}}_%i_idxkey_0| 0 | {{#arraysize:%s}}|{{%s%s}}}}" % (
				smw_context.call_occurrence_position,
				self.get_arg_with_list_expand(0).get_smw_repr(smw_context),
				self.template_name,
				self.argument_list_smw_repr(smw_context,
											idx_ref_keys=[("{{{call_occurrence}}}_%i_idxkey_0" % smw_context.call_occurrence_position, k)
														  if k else (None, None) for k in array_keys])
			)
		else:
			if self.list_expander == "cross":
				# nested loops for every list
				smw = "%s"
				idx_ref_keys = []
				for idx in range(len(self.argument_list)):
					if self.argument_list[idx].list_expand:
						idx_key = "{{{call_occurrence}}}_%i_idxkey_%i" % (smw_context.call_occurrence_position, idx)
						idx_ref_keys.append((idx_key, array_keys[idx]))
						smw %= ("{{#loop:%s | 0 | {{#arraysize:%s}}|%%s}}" % (idx_key, array_keys[idx]))
					else:
						idx_ref_keys.append((None, None))
				smw %= ("{{%s%s}}" % (self.template_name, self.argument_list_smw_repr(smw_context, idx_ref_keys=idx_ref_keys)))
				return smw
			else:  # zipMin, zipMax
				# find length of min/max list and
				end_variable = "{{#vardefine:{{{call_occurrence}}}_%i_endvar|%s}}" % (
					smw_context.call_occurrence_position,
					get_min_max_size([k for k in array_keys if k], ">=" if self.list_expander == "zipMax" else "<=")
				)
				# loop min/max and add none if one list is to small
				loop_part = "{{#loop: {{{call_occurrence}}}_%i_idxkey_0| 0 |{{#var:{{{call_occurrence}}}_%i_endvar}}|{{%s%s}}}}" % (
					smw_context.call_occurrence_position,
					smw_context.call_occurrence_position,
					self.template_name,
					self.argument_list_smw_repr(smw_context,
												idx_ref_keys=[("{{{call_occurrence}}}_%i_idxkey_0" % smw_context.call_occurrence_position, k)
															  if k else (None, None) for k in array_keys]
												)
				)
				return end_variable + loop_part

	def arg_list_has_expand(self):
		return self.number_of_list_expand() > 0

	def correct_variable_usage(self):
		return not self.is_instance or all(arg.term.variable is None for arg in self.argument_list)

	def correct_list_expand_usage(self):
		return (self.list_expander is None and not self.arg_list_has_expand()) or (self.list_expander is not None and self.arg_list_has_expand())

	def number_of_list_expand(self):
		return sum([arg.list_expand for arg in self.argument_list])

	def get_arg_with_list_expand(self, idx=0):
		number_found = 0
		for arg in self.argument_list:
			if arg.list_expand:
				if idx == number_found:
					return arg
				number_found += 1

	def get_array_keys(self, smw_context: SMWContext = None):
		return [(arg.term.get_smw_repr(smw_context) if arg.list_expand else None) for arg in self.argument_list]

	def define_arrays(self, smw_context: SMWContext = None):
		smw = ""
		for idx, arg in enumerate(self.argument_list):
			if arg.term.is_list():
				smw += arg.term.define_list(idx, smw_context, is_instance=self.is_instance)
		return smw

	def set_additional_arguments_for_call(self, argument_string):
		self.additional_args = argument_string


class Annotation:
	""" Currently only a storage of instances, connected to a template via annotation syntax. """

	def __init__(self, ctx: stOTTRParser.AnnotationContext, instance: Instance):
		self.instance = instance


class Signature:
	""" Class, containing signature information of a template. Produces 'checking wiki code' for correct template call.

	References to the parameters, annotations and template name. The SMW representation check the correct call of the template.
	Optional Check, Non Blank Check and Type Check.
	If the template has no hull and BASE ref, the signature is used to produce only the wiki code used in a form.
	"""

	def __init__(self, ctx: stOTTRParser.SignatureContext, template_name: str, parameters: List[Parameter], annotations: List[Annotation]):
		self.parameters = parameters
		self.annotations = annotations
		self.template_name = template_name
		self.source_str = " ".join(ctx.start.source[1].strdata[ctx.start.start:ctx.parameterList().stop.stop + 1].split())

	def get_smw_repr(self, smw_context: SMWContext = None):
		variable_strings = {}
		variable_positions = {}
		default_type_repr = {}
		debug_smw = smw_context.IF_DEBUG % (smw_context.update_used_templates(self.template_name) + smw_context.update_max_depth())
		default_lists = ""
		opt_check = []
		non_blank_check = []
		type_check = []
		for idx, para in enumerate(self.parameters):
			if para.default is not None and para.default.constant_list is not None:
				default_lists += para.default.define_list(idx, smw_context)

		for para in self.parameters:
			variable_positions[para.name] = para.pos
			variable_strings[para.name] = para.get_variable_repr(smw_context)
			default_type_repr[para.name] = para.get_default_repr_type(smw_context)
			# all not optional parameters has to be there, if the template should produce instances
			if "?" not in para.parameter_modes:
				opt_check.append('{{#if: %s||<strong class="error">b</strong>}}' % variable_strings[para.name])
			# a non blank parameter has to be not a blank node
			if "!" in para.parameter_modes:
				non_blank_check.append('{{#if: {{#pos:{{{ottr_arg_type_%i|}}}|ottr:blank§}}'
									'|{{#vardefine:ottr_arg_non_blankerror_msg|{{#var:ottr_arg_non_blankerror_msg}}Argument %i (%s) is a blank node, but declared as non blank<br/>}}'
									'<strong class="error">b</strong>|}}' % (para.pos, para.pos, para.name))
			if para.otype:
				para_type_repr = para.otype.get_type_repr()
				error_msg_call = ("{{ottr:ErrorMsg|Have not found a (simple) type match of the input "
								"'{{{%i|}}}' for argument %i in template '%s' "
								"(%s§ in '{{{ottr_arg_type_%i|}}}')|code=4}}" % (para.pos, para.pos, self.template_name, para_type_repr, para.pos))
				none_is_every_type = "{{#if: {{{%i|}}}|%s|}}"
				# throw an error if the match of simple types e.g. literal type and list nesting, does not match.
				check_for_string_type_hint = ('{{#if: {{#pos:{{{ottr_arg_type_%i}}}|xsd:string}}|'
											'{{#if: {{#pos:{{{ottr_arg_type_%i|}}}|%s§}}||<strong class="error">b</strong>}}'
											'|<strong class="error">b</strong>}}' % (para.pos, para.pos, para.otype.get_type_repr(original=True)))
				check_for_equal_simple_types = '{{#if: {{#pos:{{{ottr_arg_type_%i|}}}|%s§}}||%s}}' % (para.pos, para_type_repr, check_for_string_type_hint)

				error_check = "{{#iferror: %s|%s|%%s}}" % ((none_is_every_type % (para.pos, check_for_equal_simple_types)), error_msg_call)

				nested_check = ""
				if not para.otype.is_simple_type_request():
					nested_check = "%s"
					# produce only warnings if other type check (via ax:Type instances and ax:SubClassOf relations) and Not-Empty-List does not match.
					nested_warning = "{{#if: %s|{{ottr:ErrorMsg|%s|code=%i|type=Warning}}|}}"
					tmp_inner_ref = para.otype
					value_ref_name = "{{{%i|}}}" % para.pos
					loop_idx = 0
					while tmp_inner_ref.is_list_type():
						if tmp_inner_ref.type_ == tmp_inner_ref.KindOfTypes.NELIST:
							nested_check %= ("{{#ifexpr: {{#arraysize:%s}} = 0|%s|%%s}}" % (
								value_ref_name,
								nested_warning % (value_ref_name, "Checked for Not Empty List, but found empty list in template call '%s' and argument %i" % (self.template_name, para.pos), 7)
							))
						nested_check %= "{{#loop:type_list_test_%i|0|{{#arraysize:%s}}|%%s}}" % (loop_idx, value_ref_name)
						value_ref_name = "{{#explode:{{#arrayindex:%s|{{#var:type_list_test_%i}}}}|%s|0}}" % (value_ref_name, loop_idx, DELIMITERS.VALUE_TYPE_SPLIT)
						tmp_inner_ref = tmp_inner_ref.inner
						loop_idx += 1
					if tmp_inner_ref.is_lub_type():
						target_type = tmp_inner_ref.inner.type_value
						nested_check %= ("{{#ifeq: {{ottr:checkLUBType|%s|%s}}|NoMatch|%s|}}" % (
							value_ref_name,
							target_type,
							nested_warning % (value_ref_name, "Least upper bound type check was not successful for target type '%s' and input '%s'" % (target_type, value_ref_name), 8)
						))
					elif tmp_inner_ref.is_any_uri_type():
						target_type = tmp_inner_ref.type_value
						nested_check %= ("{{#ifeq: {{ottr:checkType|%s|%s}}|NoMatch|%s|}}" % (
							value_ref_name,
							target_type,
							nested_warning % (value_ref_name, "Type check was not successfull for target type '%s' and input '%s'" % (target_type, value_ref_name), 9)
						))
				type_check.append(error_check % ("{{#if:{{#pos:{{{ottr_arg_type_%i}}}|ottr:IRI}}|%s}}" % (para.pos, nested_check)))

		smw_context.variable_positions = variable_positions
		smw_context.variable_strings = variable_strings
		smw_context.default_repr_type = default_type_repr
		# idea: also add list check to type check if variable is used with list expand?
		if len(self.annotations) > 0:
			annotations = "{{#ifexpr: {{{call_depth|0}}} or {{ottr:AllAnnotationsOnOff}}|%s}}"
			for anno in self.annotations:
				# if an annotation template is in 'Layout:' namespace add additional arguments about the input arguments of the template
				additional_anno_args = self.get_additional_args_for_annos(anno)
				anno.instance.set_additional_arguments_for_call(additional_anno_args)
				annotations %= (anno.instance.get_smw_repr(smw_context) + "%s")
			annotations %= ""
			annotations += "%s"
		else:
			annotations = "%s"

		smw = "%s%s%%s" % (debug_smw, default_lists)
		smw %= (((("{{#iferror: %s||%%s}}" % ''.join(opt_check))
				% ("{{#iferror: %s|{{ottr:ErrorMsg|{{#var:ottr_arg_non_blankerror_msg}}|code=3}}|%%s}}" % ''.join(non_blank_check)))
				% (''.join(type_check) + "%s"))
				% annotations)

		return smw

	def get_additional_args_for_annos(self, anno:Annotation):
		args = "|ottr_is_anno=1"
		if "layout:" in anno.instance.template_name.lower():
			args += "|ottr_number_anno_args=%i" % len(self.parameters)
			for para in self.parameters:
				args += "|ottr_anno_arg_name_%i=%s" % (para.pos, para.name)
				args += "|ottr_anno_arg_value_%i=%s" % (para.pos, para.get_variable_repr())
				args += "|ottr_anno_arg_used_default_%i=%s" % (para.pos, "{{#if: {{{%s|}}}|0|1}}" % para.pos)
		return args

	def get_form_repr(self, position_in_multiple, needs_minimum):
		# multi instances part of a template in a form
		# the form of a template has hidden fields with default for template name and number of args of the template.
		return textwrap.dedent("""\
		{{{for template|ottr:SingleInstanceForMultiCreation%i|label=Add instances of the '%s'-Template|multiple|add button text=Add another instance|%sembed in field=ottr:MultiInstanceCreation[template_%i]}}}
		{{{field|template_name|hidden|default=%s|mandatory}}}
		{{{field|number_args|hidden|default=%i|mandatory}}}
		<table class="formtable">
		<tbody>%s</tbody></table>
		{{{end template}}} """) % (
			position_in_multiple,
			self.template_name,
			"minimum instances=1|" if needs_minimum else "",
			position_in_multiple,
			self.template_name,
			len(self.parameters),
			self.get_arg_form_repr()
		)

	def get_arg_form_repr(self):
		args_form = ""
		for para in self.parameters:
			# input type of the field depends on requested type of the parameter, mapping is defined in Utils.py
			field = "{{{field|arg_%i|input type=%s%s%s}}}" % (
				para.pos,
				get_input_type_of_ottr_type(para.otype),
				("|default=" + para.default.get_smw_repr(for_form=True)) if para.default else "",
				"|placeholder=%i. argument" % para.pos
			)
			# information around the field
			args_form += "<tr><th>%s:</th><td>%s</td><td>%s</td>%s%s</tr>" % (
				para.name[1:].capitalize(),
				"".join(para.parameter_modes) + ("-DFLT-" if para.default else ""),
				field,
				("<td><i>(of type %s)</i></td>" % para.otype.get_smw_repr()) if para.otype else "",
				"<td><i>-- elements in ( .. ) separated by ',' --</i></td>" if para.otype and para.otype.type_ in [Type.KindOfTypes.LIST, Type.KindOfTypes.NELIST] else ""
			)
		return args_form


class Template:
	""" Class, containing information of a template definition.

	If the pattern_list attribute is None, it is only a signature without hull.
	If the pattern_list is equal to 'BASE' it is a base template.
	Else pattern_list contains a list of Instances.

	The representation of a base template is always a subobject for an ottr-Triple.
	"""

	class KindOf:
		SIGNATURE = "SIG"
		BASE = "BAS"
		TEMPLATE = "TMP"

	def __init__(self, signature: Signature, pattern_list: List[Instance]):
		self.signature = signature
		self.pattern_list = pattern_list

	def get_smw_repr(self, smw_context: SMWContext = None):
		if type(self.pattern_list) == list:
			smw = self.signature.get_smw_repr(smw_context)
			for instance in self.pattern_list:
				if not instance.correct_list_expand_usage():
					return instance.LIST_EXPAND_ERROR
				smw %= (instance.get_smw_repr(smw_context) + "%s")
				smw_context.call_occurrence_position += 1
			return smw % ""
		elif self.pattern_list == "BASE":
			# base templates always produce sub object containing the triple
			smw = self.signature.get_smw_repr(smw_context)
			debug_smw_init_triples = (smw_context.IF_DEBUG % (smw_context.increase_triple_count()) + smw_context.update_used_iri_triple())
			smw_lists_triple = debug_smw_init_triples

			def get_loop_blank_node(loop, plus_one=False):
				return "ottr:blank:{{{call_occurrence}}}_BN-Arg%i-b%s" % (loop, ("{{#expr:%s+1}}" if plus_one else "%s") % ("{{#var:triple_list_{{{call_occurrence}}}_arg%i}}" % loop))

			for arg in [1,3]:
				fst_triple = ("{{#subobject:|subject=%s|predicate=rdf:first"
							"|object={{#explode:{{#arrayindex:{{{%i}}}|{{#var:triple_list_{{{call_occurrence}}}_arg%i}}}}|%s|0}}"
							"|subobject-category=OTTR-Triple }}" % (get_loop_blank_node(arg),arg, arg, DELIMITERS.VALUE_TYPE_SPLIT))
				rest_triple = ("{{#subobject:|subject=%s|predicate=rdf:rest"
							"|object={{#ifexpr:{{#expr:{{#var:triple_list_{{{call_occurrence}}}_arg%i}} + 1}} = {{#arraysize:{{{%i}}}}}|rdf:nil|%s}}"
							"|subobject-category=OTTR-Triple }}" % (get_loop_blank_node(arg), arg, arg, get_loop_blank_node(arg, True)))

				list_to_turtle = "{{#if: {{#pos:{{{ottr_arg_type_%i|}}}|List<}}|{{#vardefine:triple_var_{{{call_occurrence}}}_%i|%s}}{{#loop:triple_list_{{{call_occurrence}}}_arg%i|0|{{#arraysize:{{{%i}}}}}|%s%s}}|}}"
				list_to_turtle %= (
					arg,
					arg,
					"ottr:blank:{{{call_occurrence}}}_BN-Arg%i-b0" % arg,
					arg,
					arg,
					fst_triple,
					rest_triple
				)
				smw_lists_triple += list_to_turtle
			smw_lists_triple += "{{#subobject: |subject={{#if:{{#pos:{{{ottr_arg_type_1|}}}|List<}}|{{#var:triple_var_{{{call_occurrence}}}_1}}|{{{1}}}}} |predicate={{{2}}} |object={{#if:{{#pos:{{{ottr_arg_type_3|}}}|List<}}|{{#var:triple_var_{{{call_occurrence}}}_3}}|{{{3}}}}} |subobject-category=OTTR-Triple }}"
			return smw % smw_lists_triple
			# smw += "{{#subobject: |subject={{{1}}} |predicate={{{2}}} |object={{{3}}} |subobject-category=OTTR-Triple }}"
		return ""

	def get_form_repr(self, position_in_multiple, needs_minimum):
		return self.signature.get_form_repr(position_in_multiple, needs_minimum)

	def get_form_help_str(self):
		return textwrap.dedent("""\
		<b>Form Info:</b><br/>The OTTR-Extension comes with an automated form creation, which simplifies the generation of instances of a template via input fields:
		{{#ifexpr: {{exists|Form:%s}}|: [[Form:%s|Create instance with form]]
		|<inputbox>
		type=create
		preload=ottr:FormTemplate
		hidden=yes
		inline=true
		default=Form:%s
		buttonlabel=Create Form
		preloadparams[]=%s
		preloadparams[]=%s.
		preloadparams[]=}}
		</inputbox>}}""") % (self.signature.template_name, self.signature.template_name, self.signature.template_name, self.signature.template_name, self.signature.source_str)


class Term:
	""" Class, contains information about a term part of an argument.

	Can be a variable (argument reference) of a template, a constant or a list of terms.
	Also defines lists in arrays if they are constants in an argument.
	"""

	def __init__(self, ctx: OTTRParser.TermContext):
		self.term_list = None
		self.inner_constant_ref = None
		self.variable = None
		if ctx.Variable():
			self.variable = get_text(ctx.Variable())
		elif ctx.constant():
			self.inner_constant_ref = ctx.inner_constant
		elif ctx.termList():
			self.term_list = []

		self.term_list_smw_key = None
		self.term_list_type = None
		self.ctx = ctx
	def set_inner_constant(self, ctx):
		self.inner_constant_ref = ctx.inner_constant

	def is_list(self):
		return self.term_list is not None or (self.inner_constant_ref and self.inner_constant_ref.is_constant_list())

	def define_list(self, list_pos, smw_context: SMWContext = None, is_instance=False):
		# similar to the list definition ib the constant class
		if self.is_list():
			if self.term_list is not None:
				if is_instance:
					call_occur = "{{FULLPAGENAME}}"
				else:
					call_occur = "{{{call_occurrence}}}"
				define_string = "".join([term.define_list(f"{list_pos}_{pos}", smw_context, is_instance) for pos, term in enumerate(self.term_list)])
				list_key = "%s_%i_listkey_%s" % (call_occur, smw_context.call_occurrence_position, list_pos)
				self.term_list_smw_key = list_key
				self.term_list_type = "{{ottr:ListType|%s}}" % self.get_list_repr_string(DELIMITERS.ARRAY_ELEM_SPLIT, smw_context, False)
				array_define_template_call = "{{#arraydefine:%s|%s|%s}}" % (
					list_key,
					self.get_list_repr_string(DELIMITERS.ARRAY_ELEM_SPLIT, smw_context),
					DELIMITERS.ARRAY_ELEM_SPLIT
				)
				return define_string + array_define_template_call
			else:
				#return None
				return self.inner_constant_ref.define_list(list_pos, smw_context, is_instance)
		return ""

	def get_smw_repr(self, smw_context: SMWContext = None):
		if self.inner_constant_ref:
			return self.inner_constant_ref.get_smw_repr(smw_context)
		elif self.variable:
			return smw_context.variable_strings[self.variable]
		else:
			return self.term_list_smw_key

	def get_smw_repr_type(self, smw_context: SMWContext = None):
		if self.inner_constant_ref:
			return self.inner_constant_ref.get_smw_repr_type(smw_context)
		elif self.variable:
			return "{{#if: {{{%i|}}}|{{{ottr_arg_type_%i}}}|%s}}" % (
				smw_context.variable_positions[self.variable],
				smw_context.variable_positions[self.variable],
				smw_context.default_repr_type[self.variable]
			)
		else:
			return self.term_list_type

	def get_list_repr_string(self, delimiter, smw_context: SMWContext = None, with_value=True):
		return delimiter.join([((term.get_smw_repr(smw_context) + DELIMITERS.VALUE_TYPE_SPLIT) if with_value else "")
							+ term.get_smw_repr_type(smw_context) for term in self.term_list])


class Literal:
	""" Class, containing a literal and the parsed ottr-type.

	The type of a literal is a list of different types. Strings can have a type hint (annotation) or a lang tag.
	"""

	class LiteralType:
		INTEGER = "xsd:integer"
		DECIMAL = "xsd:float"
		BOOL = "xsd:boolean"
		RDFLIT = "xsd:string"
		LANG_ = "lng"
		IRI_ = "iri"

	def __init__(self, value: str, literal_type, optional_hint=None):
		self.value = value
		self.literal_type = literal_type
		self.optional_hint = optional_hint

		self.type_to_type_string = {
			self.LiteralType.RDFLIT: "xsd:string§rdfs:resource§",
			self.LiteralType.BOOL: "xsd:boolean§rdfs:resource§",
			self.LiteralType.INTEGER: "xsd:integer§xsd:float§rdfs:resource§",
			self.LiteralType.DECIMAL: "xsd:float§rdfs:resource§",
		}

	def get_smw_repr(self):
		opt = ""
		if self.optional_hint:
			if self.optional_hint[0] == self.LiteralType.IRI_:
				opt = f"^^{self.optional_hint[1]}"
			else:
				opt = f"{self.optional_hint[1]}" # @ is included in the text, somehow
		if self.literal_type == self.LiteralType.RDFLIT:
			return str(self.value) + opt
		return '"' + str(self.value) + '"^^' + self.literal_type

	def get_smw_repr_type(self, smw_context: SMWContext = None):
		additional_type = ""
		if self.optional_hint and self.optional_hint[0] == self.LiteralType.IRI_:
			additional_type = self.optional_hint[1] + "§"
			if self.optional_hint[1] in self.type_to_type_string:
				return self.type_to_type_string[self.optional_hint[1]]

		return self.type_to_type_string[self.literal_type] + additional_type
