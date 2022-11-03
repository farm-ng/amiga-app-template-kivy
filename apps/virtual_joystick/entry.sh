#!/bin/bash -ex
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$DIR/../../helpers/bootstrap.sh $DIR $DIR/venv

# This will pass the minimum required two args.
$DIR/venv/bin/python $DIR/main.py ${1} ${2} ${3} ${4}

exit 0