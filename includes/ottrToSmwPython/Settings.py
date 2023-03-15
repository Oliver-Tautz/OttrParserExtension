
#Acceptable namespaces for ottr_templates.
#Add yours to call ottr templates from these namespaces.

#The namespaces also need to be introduced in the LocalSettings.php in your wiki to work correctly.

#Namespaces are case-sensitive!
ottr_template_namespaces = ('Template','Dpm')

# Dictionary of typehints. You can define hints for arbitrary types here. they will be shown to the user on form pages.
FORM_TYPEHINT_MAPPING = {'xsd:date': "--date-format = (YYYY-MM-DD)"}

# typehint for lists. Shown on forms
FORM_LISTHINT = "--elements in ( .. ) separated by ','"

# Limit for pages queried at a time.
# Default limit is 50. Can be extended to 500 but needs additional rights in mediawiki.
API_QUERY_LIMIT = 50
