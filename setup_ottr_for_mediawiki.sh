#!/bin/bash -
#===============================================================================
#
#          FILE: setup_ottr_for_mediawiki.sh
#
#         USAGE: ./setup_ottr_for_mediawiki.sh
#
#   DESCRIPTION: Setup OttrParserExtension for semantic media wiki. 
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Oliver Tautz
#  ORGANIZATION: University of bielefeld
#       CREATED: 06/14/2022 04:05:33 PM
#      REVISION: 0.1
#===============================================================================

set -o nounset                                  # Treat unset variables as an error

Help()
{
   # Display Help
   echo "Install OttrParserExtension for semantic media wiki."
   echo "More help here: https://github.com/Oliver-Tautz/OttrParserExtension."
   echo
   echo "Syntax: setup_ottr_for_mediawiki.sh [-hc] [-p path] [-e path]"
   echo "options:"
   echo "h     Print this Help."
   echo "p     use explicit python/conda binary instead of the one on PATH"
   echo "c     use conda instead of pip. Not implemented ..."
   echo "a     dont prompt and use standard behavioer ... useful if running in automated skript."
}


pythonpath="python"
envpath="ottr_env"
setuppath="."
use_conda=false
autoinst=false
shellname=bash

#Help
while getopts ":hacp:e:s:" option; do
   case $option in
      h) # display Help
          Help
          exit;;
      a) 
          autoinst=true;;
      p)
          pythonpath=$OPTARG;;
      i)
          setuppath=$OPTARG;;
      c)
          use_conda=true;;
      s)
          shellname=$OPTARG;;
      \?)
        echo "Error: Invalid option"
        Help
        exit;;
   esac
done
if [ "$autoinst" = false ]; then 
   while true; do

      read -p  "Setup and install ottrparser into new environment at $envpath ? [Y/N]" yn
      case $yn in
      [Yy]* ) 
              if [ "$use_conda" = true ] ; then
                 $pythonpath create -p $envpath
                 $pythonpath activate $envpath
                 $pythonpath install pip
                 pip install .
              else 
                 $pythonpath -m venv $envpath
                 $envpath/bin/python -m pip install wheel; 
                 $envpath/bin/python -m pip install $setuppath; 
              fi
              break;; 
      [Nn]* ) exit;;
      * ) echo "Please anser yes or no";;
      esac
   done
else
   $pythonpath -m venv $envpath
   $envpath/bin/python -m pip install wheel; 
   $envpath/bin/python -m pip install $setuppath; 
fi

