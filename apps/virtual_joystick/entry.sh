#!/bin/bash -ex
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$DIR/../../bootstrap.sh $DIR $DIR/venv

$DIR/venv/bin/python $DIR/main.py --port 50060 # ${1} ${2} ${3} ${4}

exit 0
