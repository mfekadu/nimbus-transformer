#!/usr/bin/env python3
"""Clubs.py

Ask questions about Cal Poly clubs.

[//]: # (markdown comment # noqa)

Usage:
    clubs.py [ --fuzz-threshold=50 | --fuzz=50 ]
             [ --context-limit=100 | --limit=100 ]
             [ --verbose | -v ]
    clubs.py (demo|d) [IN_TXT_FILE]
             [ --fuzz-threshold=50 | --fuzz=50 ]
             [ --context-limit=100 | --limit=100 ]
             [ --verbose | -v ]
    clubs.py (make-doc|md|doc|m) [IN_CSV_FILE] [OUT_TXT_FILE]
             [ --fuzz-threshold=50 | --fuzz=50 ]
             [ --context-limit=100 | --limit=100 ]
             [ --verbose | -v ]
    clubs.py (-h | --help)

Options:
    -h --help                     Show this screen.
    demo d                        read IN_TXT_FILE and ask a default question.
    make-doc md doc m             read IN_CSV_FILE and do stuff and write out txt
    IN_TXT_FILE                   defaults to "clubs.txt"
    IN_CSV_FILE                   defaults to "clubs.csv"
    OUT_TXT_FILE                  defaults to "clubs.txt"
    --fuzz-threshold=50 --fuzz    defaults to 50.
    --context-limit=50 --limit    defaults to 100.
    --verbose -v                  printouts while running.

"""
import pandas as pd
from docopt import docopt
from ntfp.ntfp import filter_string_by_relevance, transformer
from ntfp.ntfp_types import Question, Context
from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()


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


def green_bold(s: str) -> str:
    return colored(s, "green", attrs=["bold"])


def yellow_bold(s: str) -> str:
    return colored(s, "yellow", attrs=["bold"])


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Clubs 1.0")
    IN_CSV_FILE = arguments["IN_CSV_FILE"] or "clubs.csv"
    IN_TXT_FILE = arguments["IN_TXT_FILE"] or "clubs.txt"
    OUT_TXT_FILE = arguments["OUT_TXT_FILE"] or "clubs.txt"
    FUZZ = arguments["--fuzz-threshold"] or arguments["--fuzz"] or 50
    FUZZ = int(FUZZ)
    LIMIT = arguments["--context-limit"] or arguments["--limit"] or 100
    LIMIT = int(LIMIT)
    VERBOSE = arguments["--verbose"]
    print(arguments) if VERBOSE else None
    if arguments["make-doc"] or arguments["md"] or arguments["m"]:
        df = pd.read_csv(IN_CSV_FILE, escapechar="\\", engine="python")
        doc = ""
        for _, club in df.iterrows():
            sents = make_sents(club)
            new_string = "\n".join(sents)
            doc += new_string
        with open("clubs.txt", "w") as f:
            f.write(doc)
    elif arguments["demo"] or arguments["d"]:
        doc = ""
        with open(IN_TXT_FILE, "r") as f:
            doc = f.read()
        club = "Computer Science and Artificial Intelligence"
        question = f"who is the advisor for {club} club?"
        print(green_bold("question:"), question)
        context = filter_string_by_relevance(
            to=question, string=doc, FUZZ=FUZZ, limit=100
        )
        print(yellow_bold("context:"), context) if VERBOSE else None
        answer, extradata = transformer(Question(question), Context(context))
        print(green_bold("answer:"), answer)
        print(yellow_bold("extradata:"), extradata) if VERBOSE else None
    else:
        doc = ""
        with open(IN_TXT_FILE, "r") as f:
            doc = f.read()
        question = input(green_bold("question: "))
        context = filter_string_by_relevance(
            to=question, string=doc, FUZZ=FUZZ, limit=100
        )
        print(yellow_bold("context:"), context) if VERBOSE else None
        answer, extradata = transformer(Question(question), Context(context))
        print(green_bold("answer:"), answer)
        print(yellow_bold("extradata:"), extradata) if VERBOSE else None
