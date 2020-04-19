#!/usr/bin/env python3
"""checksum.py

Calculate a sha256 checksum of the concatenation of all .py files in this repository.

[//]: # (markdown comment # noqa)

Usage:
    checksum.py [ --verbose | -v ]
                [ --debug | -d ]
    checksum.py (-h | --help)
                [ --verbose | -v ]
                [ --debug | -d ]

Options:
    -h --help                       Show this screen.
    --debug -d                      printouts while running, extra debugging.

Example:
    $ python checksum.py
    3f8e39f1256e4a59b9ff4a8a961ad4e132a00f34a3966eb62abe8984c76eda1b

    $ python checksum.py --version
    Checksum 1.0.0

Resources:
    * docopt is cool
        * http://docopt.org

Changelog:
    All notable changes to this file `checksum.py` will be documented here.
    The format is _loosely_ based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

    ## [1.0.0] - 2020-04-18 (latest)
    ### Added/Changed
    - what was `checksum.sh` is now `checksum.py`
    - much more readable and hopefully future-proof.
    - also would work on windows because python is portable.
"""

from utils.terminal_colors import print_colored_doc
from docopt import docopt


def print_help():
    to_color_green_bold = (
        "checksum.py",
        "(-h | --help)",
    )
    to_color_yellow_bold = tuple()
    to_color_white_bold = (
        "Calculate a sha256 checksum of the concatenation of all .py files in this repository.",  # noqa
        "Usage:",
        "Options:",
        "Example:",
        "Resources:",
        "Changelog:",
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


if __name__ == "__main__":
    # My basic docopt setup...
    arguments = docopt(__doc__, version="Checksum 1.0.0", help=False)
    VERBOSE = arguments["--verbose"] or arguments["-v"]
    DEBUG = arguments["--debug"]
    print(arguments) if DEBUG else None
    print("VERBOSE:", VERBOSE) if DEBUG else None
    print("DEBUG:", DEBUG) if DEBUG else None
    if arguments["--help"]:
        print_help()
        exit()

    # main code...
    print("hello world")
