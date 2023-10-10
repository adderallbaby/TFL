#!/bin/bash

while getopts mah OPTION; do
  case $OPTION in
    m)
      echo "manual" 
      python3 manual.py
      ;;
    a)
      echo "testov net"


      ;;
    h | ?)
      echo "usage: sh run.sh [-m] [-a]\n -m manual\n -a auto"  >&2
      exit 1
      ;;
  esac
done
if [ $OPTIND -eq 1 ]; then echo "No options were passed\nscript usage: sh run.sh [-m] [-a]\n -m manual\n -a auto"; fi

