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
