from mediawiki:1.34.2
# install needed apt packages
RUN apt-get clean && apt-get update && apt-get install -y wget unzip zip sqlite3 python3-venv python3-pip


# install debian php-sqlite. for some reason it was blocked by preferences. restore preferences after install
#RUN mv /etc/apt/preferences.d/no-debian-php .
#RUN apt-get install -y php7.4-sqlite3
#RUN mv ./no-debian-php /etc/apt/preferences.d


# switch to mediawiki workdir
WORKDIR /var/www/html

# download composer, php7.4.32 is supplied by mediawiki
RUN wget -q https://raw.githubusercontent.com/composer/getcomposer.org/76a7060ccb93902cd7576b67264ad91c8a2700e2/web/installer -O - -q | php -- --quiet

# Downgrade composer to supported version
RUN php composer.phar self-update --1
 
# add semantic media wiki to composer.local.json 
RUN echo '{ "require": { "mediawiki/semantic-media-wiki": "~4.0" }}' > composer.local.json


# install smw
RUN php composer.phar update  --no-dev 
RUN php composer.phar install
# Download and install dependencies (mw extensions)
    # use github clones as mediawiki extensions download links are unreliable ...
    # use fixed versions where possible

#RUN mkdir extensions
WORKDIR /var/www/html/extensions

    # Install Arrays

RUN git clone https://github.com/wikimedia/mediawiki-extensions-Arrays.git  --branch REL1_37  Arrays

    # Install AutoCreatePage

RUN git clone https://github.com/mkroetzsch/AutoCreatePage.git AutoCreatePage

    # Install Input Box
    # this seems to be installed 
#RUN git clone https://github.com/wikimedia/mediawiki-extensions-InputBox.git --branch REL1_37  InputBox

    # Install Loops
RUN git clone https://github.com/wikimedia/mediawiki-extensions-Loops.git --branch REL1_37  Loops

    # Install Pageforms
RUN git clone https://gerrit.wikimedia.org/r/mediawiki/extensions/PageForms.git PageForms

    # Install ParserFunctions
    # this is already installed
#RUN git clone  https://github.com/wikimedia/mediawiki-extensions-ParserFunctions.git --branch REL1_37  ParserFunctions


RUN git clone https://github.com/wikimedia/mediawiki-extensions-Variables.git --branch REL1_37 Variables
# install ottrparser

RUN git clone https://github.com/Oliver-Tautz/OttrParserExtension.git
WORKDIR /var/www/html/extensions/OttrParserExtension
RUN python3 -m pip install wheel
RUN ./setup_ottr_for_mediawiki.sh -a -p python3

WORKDIR /var/www/html

# Now start the manual setup ... 
