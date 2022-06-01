# OTTR Parser Extension

An extension for the ([Semantic](https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki)) [Media Wiki](https://www.mediawiki.org/wiki/MediaWiki). It parses text in the [OTTR template language](https://ottr.xyz/) and produces code in Media Wiki Syntax. Triples are represented as subobjects.

More information about the extension **and how to install**: https://www.mediawiki.org/wiki/Extension:OttrParser.

The help page for wiki usage: https://www.mediawiki.org/wiki/Help:Extension:OttrParser.

## Installation
See Media Wiki page of the extension: [Install Instructions](https://www.mediawiki.org/wiki/Extension:OttrParser#Installation).

## Pages as XML
The [OTTR-Relevant-Pages.xml](OTTR-Relevant-Pages.xml) contains the data for the relevant pages and templates, that are part of the extension. Import them via the Special Page Import. (Special:Import)

## Code
The extension uses the [includes/Hooks.php](includes/Hooks.php). It calls the python script [printOttrInSmw.py](includes/OttrToSmwPython/printOttrInSmw.py). 
The script parses the text in the passed file and the Listener ([OTTRToSMWConverter.py](includes/OttrToSmwPython/OTTRToSMWConverter.py)) builds class objects (from the [OTTRClassesForSMW.py](includes/OttrToSmwPython/OTTRClassesForSMW.py)) related to the parsed text. 
The [SMWGenerator.py](includes/OttrToSmwPython/SMWGenerator.py) starts the generation of the final (Semantic) MediaWiki code based on the class objects and prints the result to the terminal. 
The Hook File reads the terminal output and returns the output to the media wiki page (with some additional information, e.g. the input text and wiki code in pre html-tags).

## Settings.py
In the [Settings.py](Settings.py) you can add your namespaces, that are used in the automated forms, for requested arguments with the type restriction ottr:IRI.

## Ideas
* currently, it does not add new namespace ids to the wiki



