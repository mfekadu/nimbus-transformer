import re

from colorama import init
from colors import strip_color
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()


def green_bold(s: str) -> str:
    return colored(s, "green", "on_grey", attrs=["bold"])


def yellow_bold(s: str) -> str:
    return colored(s, "yellow", "on_grey", attrs=["bold"])


def white_bold(s: str) -> str:
    return colored(s, "white", "on_grey", attrs=["bold"])


def red_bold(s: str) -> str:
    return colored(s, "red", "on_grey", attrs=["bold"])


def grey_out(s: str) -> str:
    return colored(s, "grey", "on_grey")


def print_colored_doc(doc):
    colored_doc = doc
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

    def repl(color_fun, strip=True):
        def _repl(m):
            s = m.group(1)
            s = strip_color(s) if strip else s
            return f"{color_fun(s)}"

        return _repl

    for s in to_color_yellow_bold:
        colored_doc = colored_doc.replace(s, yellow_bold(s))
    for s in to_color_green_bold:
        colored_doc = colored_doc.replace(s, green_bold(s))
    for s in to_color_white_bold:
        colored_doc = colored_doc.replace(s, white_bold(s))
    for s in to_color_grey_out:
        colored_doc = colored_doc.replace(s, grey_out(s))
    for s in to_color_red_bold_patterns:
        colored_doc = re.sub(s, repl(red_bold), colored_doc)
    for s in to_color_white_bold_patterns:
        colored_doc = re.sub(s, repl(white_bold), colored_doc)
    print(colored_doc)
