# Dev Instructions

This Document is supposed to explain some of the inner workings of the
ottrparserextension. 

For an Overview of the features see
https://www.mediawiki.org/wiki/Extension:OttrParser#In_a_Nutshell


## General Design

The OttrParserExtension uses many different technologies in conjunction. It is
an add-on of *semantic media wiki*. Mediawiki calls the extension via a parser
hook called *ParserFirstCallInit*. Hooks are php functions that are executed
when certain conditions in the wiki are met. In this case the hook is executed
when a page is parsed by the wiki. 

The php hook function then calls a *python script* from a local *python
environment* . The python script utilizes a parser called *antlr4* that parses
text on the wikipage that is contained in <ottr></ottr> tags. After parsing the
OTTR text, the python script generates wikicode to be displayed in the wiki. 

The python script comminicates with the wikis php function through a local file.
Everything the python process writes to stdout will be piped to the local file
to be read by php. So everything printed in the python script will be displayed
in the wiki.

In the wiki multiple templates and extensions parse the generated wikicode into
displayable html code.


## Installation

Detailed instructions at
https://www.mediawiki.org/wiki/Extension:OttrParser#Manual_Installation

To install the wiki

1. The git needs to be cloned to the extensions folder
2. *setup_ottr_for_mediawiki.sh* needs to be run.
3. a line needs to be added to the LocalSettings.php
4. Import the ottr pages from OTTR-Relevant-Pages.xml

The setupscript will create a new local python environment and install the
extension as a local package. The pages in OTTR-Relevant-Pages.xml contain
templates used by the extension. If this step is ommited wierd, hard to trace
errors will be displayed in the wiki.


## Docker Installation

Detailed instructions at
https://www.mediawiki.org/wiki/Extension:OttrParser#Docker_Installation

The Docker container was created as an easy solution for installing all
dependencies and create a usable wiki with a working OttrParserExtension.

To install it

1. clone the git
2. use docker compose to setup both the wiki and database
3. manually navigate the mediawiki setup at localhost:8080
4. run the after_setup_script.sh

Docker Compose is used to create a usable mariadb instance in addition to the
wiki itself. The after_setup_script does multiple things:
 * it adds some lines to the downloaded LocalSettings.php. This is done with a
   copy in /tmp
* it copies the modified LocalSettings.php into the docker container
* it runs the mediawiki script maintainence/update.php inside the docker
  container. This is needed for Semantic media wiki to work
* it imports templates from OTTR-Relevant-Pages.xml
* it starts the OTTR-API

## OTTR-API

The OTTR-API is documented at
https://www.mediawiki.org/wiki/Help:Extension:OttrParser/API

It can be used to bulk import and export ottr templates and instances. If
manually installing the api must be manually started.


## AutoCreatePage addon

Because the present AutoCreatePage extension does not work with modern mediawiki
versions, I developed it further. It uses a mediawiki api call to create pages.
Because of this the extension does not work with sqlite anymore. With sqlite the
extension will produce some kind of lock in the sqlite database. I did not find
any problems with mariadb.

The new addon writes to a definable logfile for debugging purposes.

## Tips and Tricks

* Mediawiki does not report many errors. Most error messages are also disabled
  because lots of depreciation warnings etc. can clutter the view. To enable
errors follow the steps at https://www.mediawiki.org/wiki/Manual:How_to_debug
* To develop the docker image I found two possible solutions: 1. enter the
  docker container with `docker exec -it OTTRWIKI bash`. This way you can use
command line tools like nano,vim for quick edits. 2. mount the container with a
[docker volume](https://docs.docker.com/storage/volumes/). This way it is
possible to use pycharm or similar, but the standard volume location is owned by
root. It is advisible to move it to a location accesible by an normal user (e.g.
some folder in home).
* To debug in the wiki, print strings in \<pre\>\</pre\> tags. Text inside the
  tags will not be parsed by mediawiki but printed as is
* adding whitespaces to lines in mediawiki code will produce grey boxes that
  look as if the text was in \<pre\> tags. This can be confusing
* ...


## Sensible design changes

* Using a local python environment and installing it via shellscript is not
  great. Move to some other deployment standard, e.g. use a global python env
and install the python package via pip?
* The Docker installation could possibly be automated further. Everything in the
  shellscript could probably be done in the dockerfile, but the manual
installation requires user input. This could probably be avoided with the
https://www.mediawiki.org/wiki/Manual:Install.php script. I propose to run the
script in the Dockerfile and pass the user credentials onto users in the
documentation. This would simplify the docker installation
* There are lots of raw mediawiki code strings in the python code. Some of it is
  very hard to maintain. Refractoring the code such that it uses python syntax
as a wrapper would be much preferred. This could be done with a new class
implementation or just some functions. It is a lot of work though. So I would only
do it if the extension is to be extended with many new features.

## Remaining Bugs

* When creating templates and instances, URIs referred only in the template but
  not the instancing itself will not be created as a page. As the URIs are not
present in the python code when instancing they need to be created when the user
creates a template or if the template is displayed. This should easily be doable
using the AutoCreatePage extension. 
