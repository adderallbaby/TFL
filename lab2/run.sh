#!/bin/bash

while getopts mah OPTION; do
  case $OPTION in
    m)
      echo "you have selected manual" 
      python3 manual.py
      ;;
    a)
      echo "auto-testing not fully done yet"
      for i in {1..100}
        do 
          python3 generator.py
        done

      ;;
    h | ?)
      echo "script usage: sh run.sh [-m] [-a]\n -m for manual\n -a for auto-testing"  >&2
      exit 1
      ;;
  esac
done
if [ $OPTIND -eq 1 ]; then echo "No options were passed\nscript usage: sh run.sh [-m] [-a]\n -m for manual\n -a for auto-testing"; fi
