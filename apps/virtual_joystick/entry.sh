#!/bin/bash -ex
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$DIR/../../helpers/bootstrap.sh $DIR $DIR/venv

$DIR/venv/bin/python $DIR/main.py \
    --address 10.95.76.10 \
    --camera-port 50051 \
    --canbus-port 50060

exit 0
