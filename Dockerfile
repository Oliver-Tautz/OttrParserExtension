from mediawiki:1.39.3
# install needed apt packages
RUN apt-get clean && apt-get update && apt-get install -y wget unzip zip sqlite3 python3-venv python3-pip curl


# install debian php8.1-curl. Ver complicated for some reason.

## Remove php lock
RUN mv /etc/apt/preferences.d/no-debian-php .

## Install prequisites
RUN apt-get install -y  lsb-release ca-certificates apt-transport-https software-properties-common gnupg2

## add repository
RUN echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/sury-php.list

## add key
RUN curl -fsSL  https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/sury-keyring.gpg
RUN apt-get update

RUN apt-get install -y php8.1-curl

#RUN mv ./no-debian-php /etc/apt/preferences.d


# switch to mediawiki workdir
WORKDIR /var/www/html

# download composer, php7.4.32 is supplied by mediawiki
RUN wget -q https://raw.githubusercontent.com/composer/getcomposer.org/76a7060ccb93902cd7576b67264ad91c8a2700e2/web/installer -O - -q | php -- --quiet

# Downgrade composer to supported version
#RUN php composer.phar self-update --1
 
# add semantic media wiki to composer.local.json 
RUN echo '{ "require": { "mediawiki/semantic-media-wiki": "~4.1.1" , "psr/http-message": "1.0.1"}}' > composer.local.json


# install smw
RUN php composer.phar update  --no-dev 
RUN php composer.phar install
# Download and install dependencies (mw extensions)
    # use github clones as mediawiki extensions download links are unreliable ...
    # use fixed versions where possible

#RUN mkdir extensions
WORKDIR /var/www/html/extensions

    # Install Arrays

RUN git clone https://github.com/wikimedia/mediawiki-extensions-Arrays.git  --branch REL1_39  Arrays

    # Install AutoCreatePage

RUN git clone https://github.com/Oliver-Tautz/AutoCreatePage.git AutoCreatePage
    
# Install Input Box
    # this seems to be installed 
#RUN git clone https://github.com/wikimedia/mediawiki-extensions-InputBox.git --branch REL1_39  InputBox

    # Install Loops
RUN git clone https://github.com/wikimedia/mediawiki-extensions-Loops.git --branch REL1_39  Loops

    # Install Pageforms
RUN git clone https://gerrit.wikimedia.org/r/mediawiki/extensions/PageForms.git --branch REL1_39 PageForms

    # Install ParserFunctions
    # this is already installed
#RUN git clone  https://github.com/wikimedia/mediawiki-extensions-ParserFunctions.git --branch REL1_39  ParserFunctions


RUN git clone https://github.com/wikimedia/mediawiki-extensions-Variables.git --branch REL1_39 Variables

RUN git clone https://gerrit.wikimedia.org/r/mediawiki/extensions/RegexFunctions.git --branch REL1_39 RegexFunctions

# install ottrparser

RUN git clone https://github.com/Oliver-Tautz/OttrParserExtension.git --branch docker_release
WORKDIR /var/www/html/extensions/OttrParserExtension
RUN python3 -m pip install wheel
RUN ./setup_ottr_for_mediawiki.sh -a -p python3

WORKDIR /var/www/html

# CMD ./extensions/OttrParserExtension/ottr_env/bin/python extensions/OttrParserExtension/includes/ottrToSmwPython/ottrServer.py --config /var/www/html/extensions/OttrParserExtension/includes/ottrToSmwPython/ottrServerExampleConfig.cfg --base-url http://localhost/ 
# This is done in after_setup_script for now ...

# Now start the manual setup ... 
