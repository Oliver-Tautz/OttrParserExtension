import sys
import os.path
#sys.path.append(
#    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))

import includes.ottrToSmwPython.Settings


def get_text(context):
    return context.symbol.text


class DELIMITERS:
    VALUE_TYPE_SPLIT = ";"
    ARRAY_ELEM_SPLIT = ","
    POSSIBLE_TYPES_SPLIT = "§"


def get_input_type_of_ottr_type(type):
    if type is not None:
        if type.type_ == "BASIC":
            if type.type_value == "ottr:IRI":
                return "combobox|values from namespace=" + ",".join(Settings.Default_Namespaces)
            if type.type_value in ["xsd:integer", "xsd:float"]:
                return "text"
            if type.type_value == "xsd:boolean":
                return "dropdown|values=true,false"
            if type.type_value == "xsd:string":
                return "textarea"
            return "combobox|values from category=" + type.type_value
    # if is lub: only first category without depth?
    return "text"


def get_min_max_size(array_keys, operator):
    # OR Implement new extension for min and max
    min_expr = "%s"
    for idx in range(len(array_keys) - 1):
        inner_expressions = []
        for idx_2 in list(range(len(array_keys))[idx+1:]) + list(range(len(array_keys))[:idx]):
            inner_expressions.append("({{#arraysize:%s}} %s {{#arraysize:%s}})" % (array_keys[idx], operator, array_keys[idx_2]))
        min_expr %= ("{{#ifexpr: %s|%s|%%s}}" % (" and ".join(inner_expressions), ("{{#arraysize:%s}}" % array_keys[idx])))
    min_expr %= ("{{#arraysize:%s}}" % array_keys[-1])
    return min_expr


def get_prefix_special_page_name():
    return "Ottr:OttrPrefixes"


class UtilTemplateExamples:
    # Attention! Old versions!
    # ListKey = "<includeonly>{{{1}}}_listkey_{{{2}}}</includeonly>"
    # delimiterCall = "<includeonly>%s</includeonly>" % DELIMITERS.ARRAY_ELEM_SPLIT
    ListType = "<includeonly>{{#if: {{{1|}}}|{{#arraydefine:mykey|{{{1}}}|,}}{{#arraydefine:incommonarray|{{#explode:{{#arrayindex:mykey|0}}|;|1}}|§}}{{#loop: idx|0|{{#arraysize:mykey}}|{{#arraydefine: i_array|{{#explode:{{#arrayindex:mykey|{{#var:idx}}}}|;|1}}|§}}{{#arrayintersect:incommonarray|incommonarray|i_array}}}}{{#loop: idx|0|{{#arraysize:incommonarray}}|NEList<{{#arrayindex:incommonarray|{{#var:idx}}}}>§}}{{#arrayreset:mykey|incommonarray|i_array}}|List<>&}}</includeonly>"  # INTERSECTION
    getTypeString = "<includeonly>{{#ask:[[Category:{{{1}}}]]|format=list|sep=§|link=none|outro=§}}</includeonly>"  # ASK QUERY
    # idx_key = "<includeonly>{{{1}}}_idxkey_{{{2}}}</includeonly>"
    # end_var = "<includeonly>{{{1}}}_endvar</includeonly>"
    Prefix = "<includeonly># Prefix: '''{{{2}}}''' :   {{{1}}} {{#subobject: |iri={{#replace:{{#replace:{{{1}}}|<|}}|>|}} |namespace={{{2}}}|subobject-category=OTTR-Prefix}}<br/></includeonly>"
    PrefixCheck = "<includeonly>{{#if:; {{#ask:; [[-Has subobject::Ottr:OttrPrefixes]][[namespace::{{{2}}}]] |?namespace}}|| <--Prefix '''{{{2}}}''' is not defined on page [[Ottr:OttrPrefixes]]!-->}}</includeonly>"
    DebugOnOff = "<includeonly>1</includeonly><noinclude> 1 for debug on, 0 for off</noinclude>"
    AllAnnotationsOnOff = "<includeonly>0</includeonly><noinclude> 1 for display all annotation independent of depth, 0 for off</noinclude>"
    DisplayTriplesOnOff = "<includeonly>0</includeonly><noinclude> 1 for display all Triples generated on a page, 0 for off</noinclude>"
    DisplayCode = "<includeonly>0</includeonly><noinclude> 1 for display generated smw code, 0 for off</noinclude>"
    DisplayOttr = "<includeonly>0</includeonly><noinclude> 1 for display ottr input, 0 for off</noinclude>"
    AskForTriples = "<includeonly>{{#ask: [[-Has subobject::{{FULLPAGENAME}}]] |?subject |?predicate |?object}}</inlcudeonly>"
    ErrorMsg = """<includeonly><table class="warning-message" cellspacing="0" cellpadding="0" border="0" style="box-sizing:border-box; border:1px #d33 solid; background: transparent; margin:0.5em 0;padding:0.5em;background-color: #fee7e6"><tr><td nowrap="nowrap" valign="top">'''{{{type|Error}}}:''' </td><td valign="top" style="padding-{{dir|{{pagelang}}|right|left}}:0.5em;">&emsp;{{{msg|{{{1|}}}}}}</td></tr></table><br/></includeonly><noinclude>Error Box. msg via "msg" argument or first argument</noinclude>"""

    # not as a Template:
    FormTemplate = """<no<includeonly></includeonly>include>
[[Category:OTTR Template Signature Form]]This is the '''$1''' form.
To create a page with this form, enter the page name below. 
If a page with that name already exists, you will be sent to a form to edit that page.{{#forminput:form=$1$3
</no<includeonly></includeonly>include>
<include<includeonly></includeonly>only>
<ot<includeonly></includeonly>tr>
$2
</ot<includeonly></includeonly>tr>
</include<includeonly></includeonly>only>"""


class VarNames:
    TripleCount = "ottr_triple_count"
    UsedIris = "ottr_used_iris"
    MaxDepth = "ottr_max_depth"
    UsedTemplates = "ottr_used_templates"
