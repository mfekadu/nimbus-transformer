#!/bin/bash
pdoc --html ntfp --output-dir docs --force

mv docs/ntfp/* docs
rmdir docs/ntfp

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

if [[ $1 == "--oop" ]] ||
    [[ $2 == "--oop" ]] ||
    [[ $1 == "-oo" ]] ||
    [[ $2 == "-oo" ]] ||
    [[ $1 == "oop" ]] ||
    [[ $2 == "oop" ]] ||
    [[ $1 == "object-oriented" ]] ||
    [[ $2 == "object-oriented" ]]; then
    pdoc --html nimbus_transformer --output-dir docs --force
    open docs/nimbus_transformer/index.html
else
    echo "pdoc --html nimbus_transformer --output-dir docs --force"
    echo "open docs/index.html"
fi
