#!/bin/bash -ex

if ! command -v cookiecutter &> /dev/null
then
    echo "Unable to find cookiecutter. Please install via \n 'python3 -m pip install --user cookiecutter' ."
    exit
fi

cookiecutter ./ -o apps/
