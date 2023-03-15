import textwrap

from includes.ottrToSmwPython.OTTRClassesForSMW import PrefixID, Template, Instance, SMWContext
from typing import List
import re
import json
import os
from includes.ottrToSmwPython.Settings import ottr_template_namespaces
from functools import reduce

NON_BREAKING_SPACE = "&nbsp;"


def debug_print(string):
    print("<pre>" + str(string) + "</pre>")


def mediawiki_wrap_in_code(string):
    return f"<code>{string}<\code>"


def mediawiki_literal(s):
    return "<pre>" + str(s) + "</pre>"


def get_iris_from_wikicode(arglist_wikicode):
    "Get IRIS(?) from wikicode ..."

    find_first_pattern = r'\|.*?;'
    find_others_pattern = r',.*?;'

    # find first ocurrence between | and ;.
    first = re.search(find_first_pattern, arglist_wikicode).group(0)[1:-1]
    others = [arg[1:-1] for arg in re.findall(find_others_pattern, arglist_wikicode)]

    ret = f"({first}"
    for arg in others:
        ret += f", {arg}"

    return ret + ')'

def mediawiki_print_if_exists(pagename,string):
    return "{{#ifeq: {{Exists|%s}} | 1 | %s |}}" % (pagename,string)

def mediawiki_sub_arg(arg):
    """
    Get string to substitute arg i in mediawiki.

    """

    return "{{{" + arg + "}}}"


def mediawiki_wrap_if_calldepht(s, calldepth):
    return "{{#ifexpr:{{{call_depth|0}}}=" + str(calldepth) + "|" + s + "}}"


def wrap_in_quotes(string):
    if string[0] != '"':
        string = f'"{string}'
    if string[-1] != '"':
        string = f'{string}"'

    return string


def mediawiki_build_template_with_args(template):
    """
    Get ottr template string with instance args. String will be read in mediawiki as

    dpm:Publication_single[

        arg1=foo
        arg2=bar

    ]

    """

    # "2.0" {0: ['Dpm:ExampleCompound', ['dpm:Fe', 'dpm:O'], '(dpm:Fe, dpm:O)', ['"2.0"^^xsd:string', '"2.0"^^xsd:string'], '("2.0"^^xsd:float,"2.0"^^xsd:float)']}

    values = get_arg_values()

    if not values:
        return None
    # [(argname,arg)]
    # arg = {{{i}}}, substituted by mediawiki
    par_arg_list = []

    for i, (par, value) in enumerate(zip(template.signature.parameters, values['0']), 1):
        # print('par',par.name)
        if isinstance(value, list):
            value = tuple(value)
        par_arg_list.append((par.name, value))

    # print('list_after',par_arg_list)

    s = f"{template.signature.template_name} (\n"

    s += f"<table>"
    parlens = [len(par) for (par, _) in par_arg_list]
    longest_par = max(parlens)

    for par, arg in par_arg_list:
        s += "<tr><td></td><td>"
        s += f"{par}"
        s += "</td><td>=</td>"

        s += "<td>"
        s += f"{arg},\n"
        s += "</td></tr>"

    s += "</table>"
    s += ")\n"
    # s += "</code>"

    s = mediawiki_replace_newline_br(s)

    # s = mediawiki_wrap_in_code(s)
    return s


def mediawiki_wrap_in_color_box(s, color='yellow'):
    return f"<span style=\"background-color:{color}\">{s}</span>"


def mediawiki_replace_newline_br(s):
    return s.replace("\n", "<br>")


def mediawiki_generate_template_in_correct_namespace_query():
    list_of_options = ["{{#ifeq:{{#pos:{{FULLPAGENAME}}|%s:}}|0|1|0}}" % x.capitalize() for x in
                       ottr_template_namespaces]

    options = reduce(lambda x, y: x + " or " + y, list_of_options, "0")

    return options


def mediawiki_generate_template_correct_name(name, warning):
    # gets a one if one namespace:name is equal to FULLPAGENAME and empty string otherwise
    possibilities = ''.join(
        ["{{#ifeq:%s:%s|{{FULLPAGENAME}}|1|}}" % (namespace.capitalize(), name) for namespace in ottr_template_namespaces]
        # add option of pagename == name
    +   ["{{#ifeq:%s|{{FULLPAGENAME}}|1|}}" % name]


    )

    # Prints warning if one of the paganemaes matches
    if_ex = "{{#if:%s||%s}}" % (possibilities,warning)
    return if_ex


def save_arg_values(instances):
    values = dict()

    for i, instance in enumerate(instances):
        values[i] = []
        constants = [x.term.inner_constant_ref for x in instance.argument_list]

        # process literals
        for constant in constants:

            # list of literals
            # Extra processing of lists is not needed for now!

            #            if constant.constant_list:
            #                conlist = []
            #                for constant_ in constant.constant_list:
            #                    #print(constant_.__dict__)
            #                    if constant_.literal:#
            #
            #                        conlist.append(constant_.literal.value + '^^' + constant_.literal.literal_type)
            #                    else:
            #                        conlist.append(constant_.source_str)
            #                values[i].append(conlist)

            # single literals
            if constant.literal:
                values[i].append(f"{wrap_in_quotes(constant.literal.value)}^^{constant.literal.literal_type}")
            else:
                values[i].append(constant.source_str)

    with open('values.txt', 'w') as f:
        json.dump(values, f, ensure_ascii=False)


def get_arg_values():
    try:
        with open('values.txt', 'r') as f:
            values = json.load(f)
        os.remove('values.txt')
    except FileNotFoundError as e:
        return None

    return values


def mediawiki_colorbox(title, content):
    """
    Template:Colored_box must be present in mediawiki!


    """

    return f"{{{{Colored box|title={title}|content={content}}}}}"


class SMWGenerator:

    def __init__(self, prefixes: List[PrefixID], definitions: List[Template], instances: List[Instance], comments):
        self.prefixes = prefixes
        self.definitions = definitions
        self.instances = instances
        self.comments = comments

    def produce_smw(self):
        """Produce the valid SMW Code for the init arguments for a page in a wiki.

        This means produce all prefix code. Instances only if there are no template definitions.
        If there are template definitions produce only the first one. Add errors for instances outside a template and
        for input with more than one template definition.
        A call with only signature template definitions is handled as a form input and so produce only form relevant code.

        :return: Triple of strings containing the smw for the prefixes, instances and template_definitions
        """

        prefixes = self.produce_prefixes()
        if prefixes:
            print(prefixes)
            pass
        instances = ""
        template_definitions = ""
        warnings = ""

        ### instance code here
        if len(self.instances) > 0 and len(self.definitions) == 0:
            # print(self.instances[0].argument_list[0].term.is_list())
            save_arg_values(self.instances)
            instances = self.produce_instances()
            # print("<pre>"+instances+"</pre>")
            print(instances)



        ### Template code here!
        elif len(self.definitions) > 0:
            templates_with_content = [d for d in self.definitions if d.pattern_list is not None]
            if len(self.instances) > 0:
                warnings = "{{ottr:ErrorMsg|No instances in a template allowed. Converting only the template|code=1|type=Warning}}"
            if len(templates_with_content) > 1:
                warnings = "{{ottr:ErrorMsg|Only ONE template definition per page and call. Converting only first template|code=2|type=Warning}}"
            if len(templates_with_content) > 0:
                self.definitions = templates_with_content[:1]
                produce_forms = False
            else:
                produce_forms = True
            if warnings:
                print(warnings)
                pass
            template_definitions = self.produce_templates(produce_forms)
            template_definitions = template_definitions

            print(template_definitions)

        return prefixes, instances, template_definitions

    def produce_prefixes(self):
        return "".join([prefix.get_smw_repr() for prefix in self.prefixes])

    def produce_instances(self):
        smw_context = SMWContext()

        instance_string = ""
        for inst_pos, instance in enumerate(self.instances):
            smw_context.call_occurrence_position = inst_pos
            instance_string += instance.get_smw_repr(smw_context)

        return smw_context.produce_debug_str_start() + instance_string + smw_context.produce_debug_str_end() + smw_context.produce_triple_display() + "\n[[Category:OTTR_Instance]]"

    def produce_templates(self, produce_form):
        form_string = ""

        def wrap_comments():
            if self.comments:
                comms = [f"{x.strip()}" for x in self.comments]
                comms = "\n".join(comms)
                return f"\n<pre>{comms}</pre>"
            else:
                return ""

        if produce_form:
            # all forms are multi instances with multi templates (brought about by more than one template signature in the input)
            form_string = textwrap.dedent("""\
			<div id="wikiPreview" style="display: none; padding-bottom: 25px; margin-bottom: 25px; border-bottom: 1px solid #AAAAAA;"></div>
			Add/Change here OTTR instances for the generated/edited page.<br/>
			<i>"?": optional argument, &emsp;"!": not a blank node ([] or _:example), &emsp; "DFLT": default value available</i> <br/>
			Add '''none''' or '''ottr:none''' for optional arguments or for arguments that should be replaced by the default value. <br/>
			%s
			{{{for template|ottr:MultiInstanceCreation}}}
			%s
			{{{field|default_form|hidden|default=%s}}}
			{{{end template}}}
			%%s
			<br/>
			<b>Free text:</b>

			{{{standard input|free text|rows=10}}}

			{{{standard input|summary}}}

			{{{standard input|minor edit}}} {{{standard input|watch}}}

			{{{standard input|save}}} {{{standard input|preview}}} {{{standard input|changes}}} {{{standard input|cancel}}}
			""") % (
                wrap_comments(),
                "".join([("{{{field|template_%i|holds template}}}" % i) for i in range(1, len(self.definitions) + 1)]),
                self.definitions[0].signature.template_name)

        for i, template in enumerate(self.definitions, start=1):

            if template.pattern_list is None:
                form_string = form_string % (template.get_form_repr(i, len(self.definitions) == 1) + "%s")

            else:

                ### Template Code is run here ...
                smw_context = SMWContext()
                smw_context.call_occurrence_position = 0
                upper_template_name = (template.signature.template_name[:1].upper() + template.signature.template_name[
                                                                                      1:]).replace("_", " ")

                ###
                print(f"{{{{#set: instance_template_name={template.signature.template_name} }}}}")
                # print template with args in colorbox here.
                s = mediawiki_build_template_with_args(template)

                if s:
                    s = mediawiki_wrap_if_calldepht(s, 1)
                    # Print instance assignements
                    print(mediawiki_colorbox('instance assignements', s))

                    # Print template link.
                    template_name= template.signature.template_name

                    possible_template_sitenames = [template_name] + [prefix + ':' + template_name for prefix in ottr_template_namespaces]
                    possible_template_links = [f"[[{sitename}]]" for sitename in possible_template_sitenames]
                    possible_template_links_exist_wrapped = []

                    print("\'\'\'Template Link:\'\'\'" )
                    for name,link in zip(possible_template_sitenames,possible_template_links):
                        print( mediawiki_print_if_exists(name,mediawiki_wrap_if_calldepht(link, 1)))

                ###

                wrong_namespace_warning_text = "{{ottr:ErrorMsg|Page ({{FULLPAGENAME}}) does <b>NOT</b> lie in one of <b>%s</b> namespaces. You can add custom namespaces to Settings.py! )|code=-2|type=Warning}}" % (
                    ottr_template_namespaces,)

                # a check if the template is in the template valuespace
                # and a check if the template name is the same as the page name (without the 'Template:'-/-->Prefix) and throws an error otherwise

                wrong_name_warning = "{{ottr:ErrorMsg|Template name and Page name should be the same:<b> %s </b>(Template name) , <b>{{FULLPAGENAME}}</b> (Pagename)|code=-1|type=Warning}}" % upper_template_name

                wrong_name_warning_string = mediawiki_generate_template_correct_name(upper_template_name,wrong_name_warning)  + " </noinclude>"

                return (("<noinclude>"

                         "{{#ifexpr: %s ||%s}}" % (
                         mediawiki_generate_template_in_correct_namespace_query(), wrong_namespace_warning_text)

                         + wrong_name_warning_string)
                        + (
                                "<noinclude>{{#ifexpr: {{ottr:DisplayFormHelp}}|%s|}}</noinclude>" % template.get_form_help_str(
                            self.comments))
                        + mediawiki_wrap_if_calldepht(wrap_comments(), 0)
                        + "<includeonly>"
                        + template.get_smw_repr(smw_context) + "</includeonly><noinclude>"
                        + f"\nExisting Instances: {{{{#ask:\
             [[Category:OTTR Instance]]\
             [[Instance template name ::{template.signature.template_name}]]\
             |limit=10   }}}}"
                        + "[[Category:OTTR_Template]]</noinclude>")
        return form_string % ""
