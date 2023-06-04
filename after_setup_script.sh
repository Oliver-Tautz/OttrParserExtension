#!/bin/bash -
#===============================================================================
#
#          FILE: setup.sh
#
#         USAGE: ./setup.sh
#
#   DESCRIPTION: A simple script calling some docker and mediawiki funtions to 
#                finisch up after manual setup. 
#
#       OPTIONS: -s, -c 
#  REQUIREMENTS: getopt
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Oliver Tautz, 
#  ORGANIZATION: Bielefeld University
#       CREATED: 10/19/2022 03:41:31 PM
#      REVISION: 0.1.1
#===============================================================================


set -o nounset                                  # Treat unset variables as an error



#### PARSE ARGS ####


MEDIAWIKI_CONTAINER_NAME='OTTRWIKI'
LOCALSETTINGS_PATH='LocalSettings.php'
MEDIAWIKI_VOLUME_NAME='WIKIVOLUME'
LOCALSETTINGS_PATH_TMP='/tmp/LocalSettings.php_tmp' 

usage()
{
  echo  "Usage setup [-s LOCALSETTINGS_PATH] [-c MEDIAWIKI_CONTAINER_NAME] "
  exit 2
}

while getopts "s:c:v:" o; do
    case "${o}" in
        s)
            LOCALSETTINGS_PATH=${OPTARG}
            ;;
        c)
            MEDIAWIKI_CONTAINER_NAME=${OPTARG}
            ;;

        *)
            usage
            ;;
    esac
done




# getopt version here, depreciated
#PARSED_ARGUMENTS=$(getopt -a setup -o '' --long localsettings-path:,mediawiki-container:,mediawiki-volume: -- "$@")
#VALID_ARGUMENTS=$?
#if [ "$VALID_ARGUMENTS" != "0" ]; then
#  usage
#fi
#
#eval set -- "$PARSED_ARGUMENTS"
#while :
#do
#  case "$1" in
#    --localsettings-path)  LOCALSETTINGS_PATH="$2" ; shift 2 ;;
#    --mediawiki-container) MEDIAWIKI_CONTAINER_NAME="$2"   ; shift 2 ;;
#    --mediawiki-volume)    MEDIAWIKI_VOLUME_NAME="$2"   ; shift 2 ;;
#    # -- means the end of the arguments; drop this, and break out of the while loop
#    --) shift; break ;;
#    # If invalid options were passed, then getopt should have reported an error,
#    # which we checked as VALID_ARGUMENTS when getopt was called...
#    *) echo "Unexpected option: $1 - this should not happen."
#       usage ;;
#  esac
#done

### Check Input ####


## Check if Docker deamon is accessable

if ! docker info > /dev/null 2>&1; then
  echo "This script uses docker. Is the deamon running and do you have the rights to use it?"
  echo "To start the deamon use 'systemctl start docker'. "
  echo "Maybe try to start this script with sudo."
  exit 1
fi

## Check if Volume exists


# This check is not needed anymore.
# get path of volume mount
#volume_path=$(docker inspect $MEDIAWIKI_VOLUME_NAME 2>&1 | jq '.[0].Mountpoint')
#
#
#if [ "$volume_path" = "null" ]; then
#    echo "The docker volume does not exist! Use the --mediawiki-volume option. You can find your volume with 'docker volume ls'."
#    exit
#fi


## Check if Container exists

check_container=$(docker container inspect $MEDIAWIKI_CONTAINER_NAME | jq '.')


if [ "$check_container" = "[]" ]; then
    echo "The docker container does not exist! Use the -c option. You can find your container with 'docker container ls'."
    exit 1
fi




## Check if LocalSettings path exists


if [[ ! -f "$LOCALSETTINGS_PATH" ]] ; then
    echo "$LOCALSETTINGS_PATH not found. Abort."
    exit 1
    
fi


####Do things :)####

# add some lines to Localsettings (activate extensions)
echo 'copy LocalSettings.php to /tmp.'
cp $LOCALSETTINGS_PATH $LOCALSETTINGS_PATH_TMP
cat add_to_localsettings.php >> $LOCALSETTINGS_PATH_TMP


# copy LocalSettings.php to volume
echo 'copy modified LocalSettings.php to docker Container.'
docker cp $LOCALSETTINGS_PATH_TMP "$MEDIAWIKI_CONTAINER_NAME:/var/www/html/LocalSettings.php"


# update database for smw to function ...
echo 'running update.php ...'
docker exec $MEDIAWIKI_CONTAINER_NAME php maintenance/update.php
echo 'done running update.php ...'


# import ottr xml pages
echo 'importing ottr pages from xml...'
docker exec $MEDIAWIKI_CONTAINER_NAME php maintenance/importDump.php extensions/OttrParserExtension/OTTR-Relevant-Pages.xml
echo 'done importing ottr pages from xml'

docker exec $MEDIAWIKI_CONTAINER_NAME nohup ./extensions/OttrParserExtension/ottr_env/bin/python extensions/OttrParserExtension/includes/ottrToSmwPython/ottrServer.py --config /var/www/html/extensions/OttrParserExtension/includes/ottrToSmwPython/ottrServerExampleConfig.cfg --base-url http://localhost/ &


