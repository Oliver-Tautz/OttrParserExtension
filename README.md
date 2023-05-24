# OTTR Parser Extension

An extension for the ([Semantic](https://www.semantic-mediawiki.org/wiki/Semantic_MediaWiki)) [Media Wiki](https://www.mediawiki.org/wiki/MediaWiki). It parses text in the [OTTR template language](https://ottr.xyz/) and produces code in Media Wiki Syntax. Triples are represented as subobjects.

The extension also comes with an **API to export and import .stottr files to and from mediawiki**. Find the documentation here: https://www.mediawiki.org/wiki/Help:Extension:OttrParser:API .

## Installation: For mediawiki admins

Find installation and maintenance instructions at https://www.mediawiki.org/wiki/Extension:OttrParser

## For Users

Find usage instructions at https://www.mediawiki.org/wiki/Help:Extension:OttrParser.

## Development

In deployment, the extension uses the [includes/Hooks.php](includes/Hooks.php). It calls the python script [printOttrInSmw.py](includes/ottrToSmwPython/printOttrInSmw.py) from an installed python environment. You should use [setup_ottr_for_mediawiki.sh](setup_ottr_for_mediawiki.sh) for setting it up.
If you want to further develop this extension, it is advised to change the [includes/Hooks.php](includes/Hooks.php) such that it uses a direct python call without the installation, as it is easier to test changes this way. 

All relevant source code can be found in [includes/ottrToSmwPython](includes/ottrToSmwPython). The script parses the text in the passed file and the Listener ([OTTRToSMWConverter.py](includes/OttrToSmwPython/OTTRToSMWConverter.py)) builds class objects (from the [OTTRClassesForSMW.py](includes/OttrToSmwPython/OTTRClassesForSMW.py)) related to the parsed text. 

The [SMWGenerator.py](includes/OttrToSmwPython/SMWGenerator.py) starts the generation of the final (Semantic) MediaWiki code based on the class objects and prints the result to the terminal. 

The Hook File reads the terminal output and returns the output to the media wiki page (with some additional information, e.g. the input text and wiki code in pre html-tags).


The source files in [includes/ottrToSmwPython/stOTTR](includes/ottrToSmwPython/stOTTR) are generated by [antlr4](https://github.com/antlr/antlr4). If you want to change its behavior, e.g. use the latest [OTTR grammer](https://dev.spec.ottr.xyz/stOTTR/stOTTR.g4) you need to adapt [stOTTR.g4](includes/ottrToSmwPython/stOTTR/stOTTR.g4) and regenerate the files with antlr4. It is important to redirect the comments to another antlr channel, like so:

```
Comment
 : '#' ~('\r' | '\n')* -> channel(HIDDEN)
 ;

CommentBlock
 : '/***' .*? '***/' -> channel(HIDDEN)
 ;
```

In the [Settings.py](Settings.py) you can add your namespaces, that are used in the automated forms, for requested arguments with the type restriction `ottr:IRI`.



## Ideas
* currently, it does not add new namespace ids to the wiki



