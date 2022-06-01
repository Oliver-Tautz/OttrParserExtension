<?php

class OttrParserExtension {
	// Register any render callbacks with the parser
	public static function onParserFirstCallInit( Parser $parser ) {
		$parser->setHook( 'ottr', [ self::class, 'renderOttrTag' ] );
		$parser->setFunctionHook( 'ottrFunction', [ self::class, 'renderOttrFunction' ], SFH_OBJECT_ARGS );
	}

	// Render <ottr>...</ottr>
	public static function renderOttrTag( $input, array $args, Parser $parser, PPFrame $frame ) {
		$filename = './'. uniqid() . '.txt';
		file_put_contents($filename, $input, LOCK_EX);
		$command = 'ottrToSMW ' . $filename . " 2>&1";
		$code = shell_exec($command);
		$deleted = unlink($filename);
		if (array_key_exists('form', $args)){
			return $code;
		} else {
			$display_ottr = '';
			$display_wikicode = '';
			$display_ottr = '<noinclude>{{#ifexpr: {{ottr:DisplayOttr}}|' . "'''OTTR-Definition:'''<br/><pre>" . htmlspecialchars($input) . '</pre>}}</noinclude>';
			$display_wikicode = '<noinclude>{{#ifexpr: {{ottr:DisplayCode}}|' . "'''Wikicode:'''<br/>" . '<pre>'. htmlspecialchars($code) . '</pre>' . '}}</noinclude>';
			$output = $parser->recursiveTagParse($display_ottr . $code . $display_wikicode, $frame);
			return '<div  class="wonderful">' .  $output . '</div>';
		}
	}

    // Render {{#ottrFunction: ...}}
	public static function renderOttrFunction(Parser $parser, $frame, $args) {
		$input = $args[0];
		foreach($args as $key => $value) {
			if ($key != 0) $input = $input . ' |' . $frame->expand($value);
		}
		$filename = './' . uniqid() . '.txt';
		file_put_contents($filename, $input, LOCK_EX);
		$command = 'ottrToSMW ' . $filename . " 2>&1";
		$code = shell_exec($command);
		$deleted = unlink($filename);
		$display_ottr = '';
		$display_wikicode = '';
		$display_ottr = '<noinclude><!--{{safesubst:#ottrFunction:'.str_replace(array("\r","\n"), '', $input).'}}-->{{#ifexpr: {{ottr:DisplayOttr}}|' . "'''OTTR-Definition:'''<br/><pre>" . htmlspecialchars($input) . '</pre>}}</noinclude>';
		$display_wikicode = '<noinclude>{{#ifexpr: {{ottr:DisplayCode}}|' . "'''Wikicode:'''<br/>" . '<pre>'. htmlspecialchars($code) . '</pre>' . '}}</noinclude>';
		$output = $display_ottr . $code . $display_wikicode;
		return $output;
	}
}
