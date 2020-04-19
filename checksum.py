#!/usr/bin/env python3
"""checksum.py

Calculate a sha256 checksum of the concatenation of all .py files in this repository.

[//]: # (markdown comment # noqa)

Usage:
    checksum.py [ --ends-with=".py" ]
                [ --verbose | -v ]
                [ --debug | -d ]
                [ -n ]
    checksum.py (-h | --help)
                [ --verbose | -v ]
                [ --debug | -d ]
                [ -n ]

Options:
    -h --help            Show this screen.
    --debug -d           printouts while running, extra debugging.
    --ends-with=".py"    defaults to ".py". Allows program to run on other kinds of files.
    -n                   Do not print the trailing newline character for final output.

Example:
    $ python checksum.py
    A_64_CHARACTER_HEXADECIMAL_STRING_GENERATED_BY_SHA_256_ALGORITHM

    $ python checksum.py --version
    Checksum 1.0.0

    # TEST CASE 1 (verifying basic input/output and concatenation property)
    # note that sha256("") = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    # note that sha256("hi") = '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4'
    # note that sha256("hihi") = '27e6f695d734689575e2a063b77668a1fab9c7a83071134630f6a02ebf697592'
    $ rm *.TEST_FOO
    $ python checksum.py --ends-with=".TEST_FOO"
    e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
    $ echo -n "hi" > 1.TEST_FOO
    $ python checksum.py --ends-with=".TEST_FOO"
    8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4
    $ echo -n "hi" > 2.TEST_FOO
    $ python checksum.py --ends-with=".TEST_FOO"
    27e6f695d734689575e2a063b77668a1fab9c7a83071134630f6a02ebf697592
    $ rm *.TEST_FOO

    # TEST CASE 2 (comparing against another sha256 tool, expect same results)
    $ python checksum.py --verbose
    ...
    ...
    py_files: ['./A.py', './B.py', './C.py', './D/efg.py']
    ...
    ...
    len(catted_files): 48114
    ...
    A_64_CHARACTER_HEXADECIMAL_STRING_GENERATED_BY_SHA_256_ALGORITHM
    $ cat A.py B.py C.py D/efg.py | shasum -a 256 -U
    A_64_CHARACTER_HEXADECIMAL_STRING_GENERATED_BY_SHA_256_ALGORITHM


Resources:
    * docopt is cool
        * http://docopt.org

Changelog:
    All notable changes to this file `checksum.py` will be documented here.
    The format is _loosely_ based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

    ## [1.0.0] - 2020-04-18 (latest)
    ### Added/Changed/Fixed
    - what was `checksum.sh` is now `checksum.py`
    - much more readable and hopefully future-proof.
    - also would work on windows because python is portable.
    - also works correctly as shown by simple "hihi" test case in Example
"""

import hashlib
import os

from docopt import docopt

from utils.terminal_colors import print_colored_doc, print_debug, print_verbose


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

    THIS_FILENAME = "checksum.py"
    print_debug("THIS_FILENAME", THIS_FILENAME) if DEBUG else None

    # ASSUMPTION 1 - this program is running from root directory
    # assert this assumption before anything else.
    msg = f"{THIS_FILENAME} expects to run in same directory that it exists"
    msg += "\n    and should run in the ROOT directory."
    assert THIS_FILENAME in os.listdir(), msg

    # ASSUMPTION 2 - the files we care about can be nested at arbitrary depth
    # Recursively get all file pathsfrom current directory downward
    FILEPATHS = [
        os.path.join(dp, f)
        for dp, dn, fn in os.walk(os.path.expanduser("."))
        for f in fn
    ]
    print_debug("FILEPATHS", FILEPATHS) if DEBUG else None
    print_verbose("FILEPATHS[:5]", FILEPATHS[:5]) if VERBOSE else None
    print_verbose("len(FILEPATHS)", len(FILEPATHS)) if VERBOSE or DEBUG else None

    # ASSUMPTION 3 - only python files need be considered for checksum
    ENDS_WITH = arguments["--ends-with"] or ".py"
    py_files = [x for x in filter(lambda x: x.endswith(ENDS_WITH), FILEPATHS)]
    print_verbose("py_files", py_files) if VERBOSE or DEBUG else None
    print_verbose("len(py_files)", len(py_files)) if VERBOSE or DEBUG else None

    # ASSUMPTION 4 - ORDER MATTERS
    #   once all python filepaths are found from current directory,
    #   then they will be sorted in alphabetical order
    # e.g. py_files:   ['./checksum.py', './clubs.py', './main.py',
    #                   './ntfp/ntfp_types.py', './ntfp/__init__.py',
    #                   './ntfp/ntfp.py', './utils/__init__.py',
    #                   './utils/terminal_colors.py']
    # sorted_py_files: ['./checksum.py', './clubs.py', './main.py',
    #                   './ntfp/__init__.py', './ntfp/ntfp.py',
    #                   './ntfp/ntfp_types.py', './utils/__init__.py',
    #                   './utils/terminal_colors.py']
    sorted_py_files = sorted(py_files)

    # ASSUMPTION 5 - the following code equivalent to `cat file.py **.py ...py`
    catted_files = b""
    for filename in sorted_py_files:
        with open(filename, "rb") as f:
            catted_files += f.read()
    print_debug("catted_files", catted_files) if DEBUG else None
    print_verbose("catted_files[:99]", catted_files[:99]) if VERBOSE else None
    print_verbose("len(catted_files)", len(catted_files)) if VERBOSE or DEBUG else None

    # ASSUMPTION 6 - hashlib.sha256 equiv to `shasum -a 256 -U` on macOS
    sha = hashlib.sha256(catted_files).hexdigest()
    print_verbose("sha", sha) if VERBOSE or DEBUG else None

    if arguments["-n"]:
        print(sha, end="")
    else:
        print(sha)
