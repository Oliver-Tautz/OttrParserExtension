<?php
class SpecialOttrApiEdits extends \SpecialPage {
	function __construct() {
		parent::__construct( 'OttrApiEdits' );
	}

    function getGroupName() {
        return 'ottr';
    }

	function execute( $par ) {
		$request = $this->getRequest();
		$output = $this->getOutput();
		$this->setHeaders();

		# Get request data from, e.g.
		$param = $request->getText( 'param' );

		# Do stuff
		# ...
        $wikitext = '{{Template:Ottr:ApiEdits}}';
		$output->addWikiTextAsInterface( $wikitext );
	}
}
