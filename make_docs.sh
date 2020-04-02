#!/bin/bash
pdoc --html nimbus_transformer --output-dir docs --force

mv docs/nimbus_transformer/* docs
rmdir docs/nimbus_transformer

if [[ $1 == "--open" ]] ||
    [[ $2 == "--open" ]] ||
    [[ $1 == "-open" ]] ||
    [[ $2 == "-open" ]] ||
    [[ $1 == "open" ]] ||
    [[ $2 == "open" ]] ||
    [[ $1 == "o" ]] ||
    [[ $2 == "o" ]]; then
    open docs/index.html
else
    echo "open docs/index.html"
fi

if [[ $1 == "--ntfp" ]] ||
    [[ $2 == "--ntfp" ]] ||
    [[ $1 == "-n" ]] ||
    [[ $2 == "-n" ]] ||
    [[ $1 == "n" ]] ||
    [[ $2 == "n" ]] ||
    [[ $1 == "fp" ]] ||
    [[ $2 == "fp" ]]; then
    pdoc --html ntfp.py --output-dir docs --force
    open docs/ntfp.html
else
    echo "pdoc --html ntfp.py --output-dir docs --force"
    echo "open docs/ntfp.html"
fi
