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
