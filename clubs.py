#!/usr/bin/env python3
"""Clubs.py

Ask questions about Cal Poly clubs.

[//]: # (markdown comment # noqa)

Usage:
    clubs.py [IN_TXT_FILE]
             [ --sentence-separator=" " ]
             [ --club-separator="\\n\\n\\n" ]
             [ --fuzz-threshold=25 | --fuzz=25 ]
             [ --context-limit=25 | --limit=25 ]
             [ --verbose | -v ]
             [ --debug | -d ]
    clubs.py (--example | -e) [IN_TXT_FILE]
             [ --sentence-separator=" " ]
             [ --club-separator="\\n\\n\\n" ]
             [ --fuzz-threshold=25 | --fuzz=25 ]
             [ --context-limit=25 | --limit=25 ]
             [ --verbose | -v ]
             [ --debug | -d ]
    clubs.py (--make-doc | -m) [IN_CSV_FILE] [OUT_TXT_FILE]
             [ --sentence-separator=" " ]
             [ --club-separator="\\n\\n\\n" ]
             [ --fuzz-threshold=25 | --fuzz=25 ]
             [ --context-limit=25 | --limit=25 ]
             [ --verbose | -v ]
             [ --debug | -d ]
    clubs.py (-h | --help)
             [ --verbose | -v ]
             [ --debug | -d ]

Options:
    -h --help                       Show this screen.
    --example -e                    read IN_TXT_FILE and ask a default question.
    --make-doc -m                   read IN_CSV_FILE and do stuff and write out txt.
    [IN_TXT_FILE]                   defaults to "clubs.txt"
    [IN_CSV_FILE]                   defaults to "clubs.csv"
    [OUT_TXT_FILE]                  defaults to "clubs.txt"
    --fuzz-threshold=25 --fuzz=25   defaults to 25.
    --context-limit=25 --limit=25   defaults to 25.
    --verbose -v                    printouts while running.
    --debug -d                      printouts while running, extra debugging.
    --sentence-separator=" "        defaults to " ". Separates same club sentences.
    --club-separator="\\n\\n\\n"       defaults to "\\n\\n\\n". Separates different club sentences.

Example:
    $ python clubs.py --make-doc my_clubs_data.csv my_clubs_doc.txt

    $ python clubs.py --example my_clubs_doc.txt --verbose
    question: "What is blah?"
    ...
    context: "..."
    ...
    answer: "Blah is foobar"
    extradata: {...}

    $ python clubs.py my_clubs_doc.txt
    question: "user_input ¯\\_(ツ)_/¯"
    ...
    answer: "¯\\_(ツ)_/¯"

Resources:
    * docopt is cool
        * http://docopt.org
"""
import pandas as pd
import spacy
from docopt import docopt

from ntfp.ntfp import filter_string_by_relevance, transformer
from ntfp.ntfp_types import Context, Question
from utils.terminal_colors import green_bold, print_colored_doc, yellow_bold


def make_sents(club):
    templates = (
        "The type of [club_name] is [types].",
        "Here is the description of [club_name]: [desc].",
        (  # multi-line string: https://stackoverflow.com/a/10660443/5411712
            "You can contact [club_name] by emailing"
            " [contact_person] at [contact_email]"
            " or [contact_email_2]."
        ),
        "You can call [club_name] by the phone number [contact_phone].",
        "The phone number for [club_name] is [contact_phone].",
        "[club_name] has the mail box [box].",
        "The mail box of [club_name] is [box].",
        "[club_name] has Professor [advisor] as their advisor.",
        "Professor [advisor] advises [club_name].",
        "Professor [advisor] is the advisor for [club_name].",
        "[club_name] affiliates with [affiliation].",
        "[club_name] has the affiliation [affiliation].",
    )

    club_data = {
        "club_name": club["club_name"],
        "types": club["types"],
        "desc": club["desc"],
        "contact_email": club["contact_email"],
        "contact_email_2": club["contact_email_2"],
        "contact_person": club["contact_person"],
        "contact_phone": club["contact_phone"],
        "box": club["box"],
        "advisor": club["advisor"],
        "affiliation": club["affiliation"],
    }
    final_sents = []
    for sent in templates:
        for key in club_data:
            data = club_data[key]
            sent = sent.replace(f"[{key}]", f"{data}")
        final_sents.append(sent)
    return final_sents


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Clubs 1.0", help=False)
    VERBOSE = arguments["--verbose"]
    DEBUG = arguments["--debug"]
    print(arguments) if DEBUG else None
    if arguments["--help"]:
        to_color_green_bold = (
            "clubs.py",
            "(--example | -e)",
            "(--make-doc | -m)",
            "(-h | --help)",
        )
        to_color_yellow_bold = (
            "[IN_TXT_FILE]",
            "[IN_CSV_FILE]",
            "[OUT_TXT_FILE]",
        )
        to_color_white_bold = (
            "Ask questions about Cal Poly clubs.",
            "Usage:",
            "Options:",
            "Resources:",
            "Example:",
        )
        to_color_white_bold_patterns = (r"(\$.*)",)
        to_color_red_bold_patterns = (r"(defaults to.*)",)
        to_color_grey_out = ("[//]: # (markdown comment # noqa)",)
        print_colored_doc(
            doc=__doc__,
            to_color_green_bold=to_color_green_bold,
            to_color_yellow_bold=to_color_yellow_bold,
            to_color_white_bold=to_color_white_bold,
            to_color_white_bold_patterns=to_color_white_bold_patterns,
            to_color_red_bold_patterns=to_color_red_bold_patterns,
            to_color_grey_out=to_color_grey_out,
        )
        exit()
    IN_CSV_FILE = arguments["IN_CSV_FILE"] or "clubs.csv"
    IN_TXT_FILE = arguments["IN_TXT_FILE"] or "clubs.txt"
    OUT_TXT_FILE = arguments["OUT_TXT_FILE"] or "clubs.txt"
    FUZZ = arguments["--fuzz-threshold"] or arguments["--fuzz"] or 25
    FUZZ = int(FUZZ)
    LIMIT = arguments["--context-limit"] or arguments["--limit"] or 25
    LIMIT = int(LIMIT)
    SENTENCE_SEPARATOR = arguments["--sentence-separator"] or " "
    CLUB_SEPARATOR = arguments["--club-separator"] or "\n\n\n"
    if arguments["--make-doc"]:
        print(f"reading from {IN_CSV_FILE}...") if DEBUG else None
        df = pd.read_csv(IN_CSV_FILE, escapechar="\\", engine="python")
        doc = ""
        print(f"making sentences...", end="") if DEBUG else None
        for _, club in df.iterrows():
            sents = make_sents(club)
            new_string = SENTENCE_SEPARATOR.join(sents)
            doc += new_string + CLUB_SEPARATOR
            print(f".", end="") if DEBUG else None
        print(f".", end="\n") if DEBUG else None
        print(f"writing to {OUT_TXT_FILE}.") if DEBUG else None
        with open(OUT_TXT_FILE, "w") as f:
            f.write(doc)
    elif arguments["--example"]:
        doc = ""
        print(f"reading from {IN_TXT_FILE}...") if DEBUG else None
        with open(IN_TXT_FILE, "r") as f:
            doc = f.read()
        club = "Computer Science and Artificial Intelligence"
        print(f"club: {club}...") if DEBUG else None
        question = f"who is the advisor for {club} club?"
        print(green_bold("question:"), question)
        spacy_nlp = spacy.load("en_core_web_sm")
        context = filter_string_by_relevance(
            to=question,
            string=doc,
            FUZZ=FUZZ,
            limit=LIMIT,
            sep=CLUB_SEPARATOR,
            nlp=spacy_nlp,
        )
        print(yellow_bold("context:"), context) if VERBOSE else None
        answer, extradata = transformer(Question(question), Context(context))
        print(green_bold("answer:"), answer)
        print(yellow_bold("extradata:"), extradata) if VERBOSE else None
    else:
        doc = ""
        print(f"reading from {IN_TXT_FILE}...") if DEBUG else None
        with open(IN_TXT_FILE, "r") as f:
            doc = f.read()
        question = input(green_bold("question: "))
        spacy_nlp = spacy.load("en_core_web_sm")
        context = filter_string_by_relevance(
            to=question,
            string=doc,
            FUZZ=FUZZ,
            limit=LIMIT,
            sep=CLUB_SEPARATOR,
            nlp=spacy_nlp,
        )
        print(yellow_bold("context:"), context) if VERBOSE else None
        answer, extradata = transformer(Question(question), Context(context))
        print(green_bold("answer:"), answer)
        print(yellow_bold("extradata:"), extradata) if VERBOSE else None
