########### Added by OTTRParser after_setup_script ###########
#SMW include 
wfLoadExtension( 'SemanticMediaWiki' );
enableSemantics( 'localhost/mediawiki-1.37.1' );

# OTTR extension

wfLoadExtension( 'OttrParserExtension' );
# OTTR extension dependencies

wfLoadExtension( 'ParserFunctions' );
$wgPFEnableStringFunctions = true;
wfLoadExtension( 'Loops' );
wfLoadExtension( 'Arrays' );
wfLoadExtension( 'PageForms' );
wfLoadExtension( 'InputBox' );
wfLoadExtension( 'Variables' );
wfLoadExtension( 'RegexFunctions' );


require_once "$IP/extensions/AutoCreatePage/AutoCreatePage.php";
#wfLoadExtension( 'AutoCreatePage' );

# This surpresses some warnings ..
$wgDeprecationReleaseLimit = '1.x';
error_reporting(E_ALL ^ (E_NOTICE | E_WARNING | E_DEPRECATED));
ini_set( 'display_errors',1 );

# dpm namespace
define("NS_dpm", 3000);
$wgExtraNamespaces[3000] = "Dpm";
$smwgNamespacesWithSemanticLinks[3000] = true;

# AutoCreatePage variables
$egAutoCreatePageNamespaces = [
     NS_MAIN,
     NS_USER,
     NS_TEMPLATE,
     NS_dpm
];


$egAutoCreatePageLogfile="autocreatepage.log";
$egAutoCreatePageAPIEndpoint="http://localhost/api.php";

###############################################################
