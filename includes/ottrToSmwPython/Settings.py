
Default_Namespaces = ['Main','Template']

# acceptable namespaces for ottr_templates
# add yours to call ottr templates from these namespaces
# This is case sensitive!

ottr_template_namespaces = ('Template','Dpm')

# typehint for ottr types ... will be printed next to the type in forms
form_typehint_mapping = {'xsd:date': "--date-format = (YYYY-MM-DD)"}

# typehint for lists. printed in forms
form_listhint = "--elements in ( .. ) separated by ','"

# default limit is 50. Can be extended to 500
API_QUERY_LIMIT = 50
