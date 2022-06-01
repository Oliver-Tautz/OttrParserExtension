import textwrap

from includes.ottrToSmwPython.OTTRClassesForSMW import PrefixID, Template, Instance, SMWContext
from typing import List
import re


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


def mediawiki_sub_arg(arg):
    """
    Get string to substitute arg i in mediawiki.

    """

    return "{{{"+arg+"}}}"


def mediawiki_wrap_if_calldepht(s,calldepth):
    return "{{#ifexpr:{{{call_depth|0}}}="+str(calldepth)+"|" + s + "}}"

def mediawiki_build_template_with_args(template):
    """
    Get ottr template string with instance args. String will be read in mediawiki as

    dpm:Publication_single[

        arg1=foo
        arg2=bar

    ]

    """
    s=""

    # [(argname,arg)]
    # arg = {{{i}}}, substituted by mediawiki
    par_arg_list = []

    for i, par in enumerate(template.signature.parameters, 1):
        par_arg_list.append((par.name,mediawiki_sub_arg(str(i))))


    s = f"{template.signature.template_name} [\n"

    parlens = [len(par) for (par,_) in par_arg_list]
    longest_par = max(parlens)

    for par, arg in par_arg_list:

        s+= NON_BREAKING_SPACE*8
        s+= f"{par}"
        s+= NON_BREAKING_SPACE*(longest_par-len(par)+2) +"=" + NON_BREAKING_SPACE*2
        s+= f"{arg}\n"

    s+= "]\n"
    #s += "</code>"


    s = mediawiki_replace_newline_br(s)

    #s = mediawiki_wrap_in_code(s)
    return s

def mediawiki_wrap_in_color_box(s,color='yellow'):

    return f"<span style=\"background-color:{color}\">{s}</span>"

def mediawiki_replace_newline_br(s):
    return s.replace("\n","<br>")


def mediawiki_colorbox(title,content):
    """
    Template:Colored_box must be present in mediawiki!


    """

    return f"{{{{Colored box|title={title}|content={content}}}}}"

class SMWGenerator:

    def __init__(self, prefixes: List[PrefixID], definitions: List[Template], instances: List[Instance]):
        self.prefixes = prefixes
        self.definitions = definitions
        self.instances = instances


    def produce_smw(self):
        """Produce the valid SMW Code for the init arguments for a page in a wiki.

        This means produce all prefix code. Instances only if there are no template definitions.
        If there are template definitions produce only the first one. Add errors for instances outside a template and
        for input with more than one template definition.
        A call with only signature template definitions is handled as a form input and so produce only form relevant code.

        :return: Triple of strings containing the smw for the prefixes, instances and template_definitions
        """

        prefixes = self.produce_prefixes()
        instances = ""
        template_definitions = ""
        warnings = ""

        ### instance code here
        if len(self.instances) > 0 and len(self.definitions) == 0:
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
            template_definitions = self.produce_templates(produce_forms)
            # is this correct?

            #print(template_definitions)

        return prefixes, instances, template_definitions

    def produce_prefixes(self):
        return "".join([prefix.get_smw_repr() for prefix in self.prefixes])

    def produce_instances(self):
        smw_context = SMWContext()

        instance_string = ""
        for inst_pos, instance in enumerate(self.instances):
            smw_context.call_occurrence_position = inst_pos
            instance_string += instance.get_smw_repr(smw_context)


        return smw_context.produce_debug_str_start()  + mediawiki_colorbox('instance assignements',instance_string)+ smw_context.produce_debug_str_end() + smw_context.produce_triple_display() + "\n[[Category:OTTR_Instance]]"

    def produce_templates(self, produce_form):
        form_string = ""
        if produce_form:
            # all forms are multi instances with multi templates (brought about by more than one template signature in the input)
            form_string = textwrap.dedent("""\
			<div id="wikiPreview" style="display: none; padding-bottom: 25px; margin-bottom: 25px; border-bottom: 1px solid #AAAAAA;"></div>
			Add/Change here OTTR instances for the generated/edited page.<br/>
			<i>"?": optional argument, &emsp;"!": not a blank node ([] or _:example), &emsp; "DFLT": default value available</i> <br/>
			Add '''none''' or '''ottr:none''' for optional arguments or for arguments that should be replaced by the default value.
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
                #print('\n')
                #print(template.signature.template_name)


                s = mediawiki_build_template_with_args(template)
                #s= mediawiki_wrap_in_color_box(s)
                # use noinclude?!
                print(mediawiki_wrap_if_calldepht(s,1))

###
                # a check if the template is in the template namespace
                # and a check if the template name is the same as the page name (without the 'Template:'-Prefix) and throws an error otherwise
                return (("<noinclude>"
                         "{{#ifeq:{{#pos:{{FULLPAGENAME}}|Template:}}|0|"
                         "{{#ifeq:{{#sub:{{FULLPAGENAME}}|9}}|%s||"
                         "{{ottr:ErrorMsg|Template name and Page name should be the same: %s (Template name), <b>{{#sub:{{FULLPAGENAME}}|9}}</b> (Pagename)|code=-1|type=Warning}}}}"
                         "|{{ottr:ErrorMsg|Page does <b>NOT</b> lie in the <b>Template</b> namespace ({{FULLPAGENAME}})|code=-2|type=Warning}}}}"
                         " </noinclude>" % (upper_template_name, upper_template_name))
                        + (
                                "<noinclude>{{#ifexpr: {{ottr:DisplayFormHelp}}|%s|}}</noinclude>" % template.get_form_help_str())
                        + "<includeonly>"
                        + template.get_smw_repr(smw_context)
                        + "</includeonly><noinclude>[[Category:OTTR_Template]]</noinclude>")
        return form_string % ""
