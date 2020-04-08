python -m spacy download en_core_web_sm

if [[ $1 == "--for-similarity" ]] ||
    [[ $1 == "--similarity" ]] ||
    [[ $1 == "--sim" ]] ||
    [[ $1 == "-s" ]] ||
    [[ $1 == "--with-vectors" ]] ||
    [[ $1 == "--vectors" ]] ||
    [[ $1 == "-v" ]]; then
    python -m spacy download en_core_web_lg
else
    echo "if you need word2vec then "
    echo "python -m spacy download en_core_web_lg"
fi
