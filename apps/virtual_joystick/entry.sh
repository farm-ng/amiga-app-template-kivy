#!/bin/bash -ex
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$DIR/../../bootstrap.sh $DIR $DIR/venv

$DIR/venv/bin/python $DIR/main.py \
    --camera-port 50051 \
    --canbus-port 50060

exit 0
