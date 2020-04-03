#!/usr/bin/env python3
"""it's like [Nimbus][1] but uses [a transformer language model][2]

Implemented in a [functional programming style][4]

[//]: # (markdown comment # noqa)

Resources:
    * [import typing][python3_typing]
    * [import functools][python3_functools]
    * [Functional Design Patterns - Scott Wlaschin][wlaschin_talk]
    * ["Types are not classes... they're sort of like Sets"][wlaschin_talk_types]
    * [Why Isn't Functional Programming the Norm? – Richard Feldman][richard_feldman_talk]
    * ["NewType declares one type to be a _subtype_ of another"][new_type]
        * _subtype_ means the same thing as _subclass_ in this context
    * [__pdoc__override]
    * [pyre-check error suppression][5]
    * [mypy type hints cheat sheet][6]
    * [Carl Meyer - Type-checked Python in the real world - PyCon 2018][carl_myer_pycon2018]

[1]: http://github.com/calpoly-csai/api
[2]: https://github.com/huggingface/transformers
[3]: http://github.com/mfekadu/nimbus-transformer

[4]: https://realpython.com/courses/functional-programming-python/

[5]: https://pyre-check.org/docs/error-suppression.html

[6]: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

[carl_myer_pycon2018]: https://youtu.be/pMgmKJyWKn8

[python3_typing]: https://docs.python.org/3/library/typing.html
[python3_functools]: https://docs.python.org/3/library/functools.html

[wlaschin_talk]: https://youtu.be/ucnWLfBA1dc
[wlaschin_talk_types]: https://youtu.be/ucnWLfBA1dc?t=685

[richard_feldman_talk]: https://youtu.be/QyJZzq0v7Z4

[new_type]: https://docs.python.org/3/library/typing.html#newtype

[__pdoc__override]: https://pdoc3.github.io/pdoc/doc/pdoc/#overriding-docstrings-with-__pdoc__
"""

from typing import (
    Callable,
    List,
    NewType,
    TypeVar,
    get_type_hints,
)  # TODO: typing.Literal typing.Final both in python3.8

from typing_extensions import Final, Literal

import googlesearch
from transformers import pipeline

__pdoc__ = {}

Question = NewType("Question", str)
Query = NewType("Query", str)
SanitizedQuery = NewType("SanitizedQuery", Query)
Context = NewType("Context", str)
Result = NewType("Result", str)
Results = NewType("Results", List[str])
Answer = NewType("Answer", str)
Transformer = Callable[[str, str], str]
IDK_TYPE = Literal["¯\\_(ツ)_/¯"]


# fmt: off
QuestionTypeVar = TypeVar("Question", Question, Question)
"""Question"""
__pdoc__["Question"] = """A Question type
Example:
    `Question`: "what is foaad khosmood's email?"

    `Query`: "what is foaad khosmood's email? site:calpoly.edu"

    `Context`: "The email is foaad@calpoly.edu."

    `Answer`: "foaad@calpoly.edu"
"""

ContextTypeVar = TypeVar("Context", Context, Context)
"""Context"""
__pdoc__["Context"] = """A Context type
Example:
    `Question`: "what is foaad khosmood's email?"

    `Query`: "what is foaad khosmood's email? site:calpoly.edu"

    `Context`: "The email is foaad@calpoly.edu."

    `Answer`: "foaad@calpoly.edu"
"""

AnswerTypeVar = TypeVar("Answer", Answer, Answer)
"""Answer"""
__pdoc__["Answer"] = """An Answer type
Example:
    `Question`: "what is foaad khosmood's email?"

    `Query`: "what is foaad khosmood's email? site:calpoly.edu"

    `Context`: "The email is foaad@calpoly.edu."

    `Answer`: "foaad@calpoly.edu"
"""


QueryTypeVar = TypeVar("Query", Query, Query)
"""Query"""
__pdoc__["Query"] = """A Query type

Has _subtype_ `SanitizedQuery`

Example:
    `Question`: "what is foaad khosmood's email?"

    `Query`: "what is foaad khosmood's email? site:calpoly.edu"

    `Context`: "The email is foaad@calpoly.edu."

    `Answer`: "foaad@calpoly.edu"
"""

SanitizedQueryTypeVar = TypeVar(
    "SanitizedQuery",
    SanitizedQuery,
    SanitizedQuery
)
"""SanitizedQuery"""
__pdoc__["SanitizedQuery"] = """A SanitizedQuery type

Has _supertype_ `Query`.

Example:
    ```
    "what+is+foaad+khosmood%27s+email%3F+site%3Acalpoly.edu"
    ```
"""

ResultTypeVar = TypeVar("Result", Result, Result)
"""Result"""
__pdoc__["Result"] = """A Result type
Example:
    ```
    "<html><body><div>...</div></body></html>"
    ```
"""

ResultsTypeVar = TypeVar(
    "Results",
    List[Result],
    List[Result]
)
"""Results"""
__pdoc__["Results"] = """A Results type
Example:
    ```
    [
        "<html><body><div>...</div></body></html>",
        "<html><body><div>...</div></body></html>"
    ]
    ```
"""

IDK_TYPE_TypeVar = TypeVar(
    "IDK_TYPE",
    IDK_TYPE,
    IDK_TYPE
)
"""IDK_TYPE"""

IDK: IDK_TYPE = "¯\\_(ツ)_/¯"
"""IDK: `IDK_TYPE`"""

TransformerTypeVar = TypeVar(
    "Transformer",
    Transformer,
    Transformer
)
"""Transformer"""
__pdoc__["Transformer"] = """
Example:
>>> question = "what is the meaning of life?"
>>> context = "The meaning of life is 42."
>>> t: Transformer = lambda q, c: "42"
>>> t(question, context)
'42'
"""
# fmt: on


def create_query(question: Question) -> Query:
    """
    Describes how to create a new `Query` string object
        from a given `nimbus_transformer.question.Question`.

    Args:
        question: A `nimbus_transformer.question.Question` string.

    Returns:
        A `Query` object.
    """
    # make a Google query with appropriate scope of domain name
    query: Query = Query(f"{question} site:calpoly.edu")
    return query


def url_param_sanitize(q: Query) -> SanitizedQuery:
    """url_param_sanitize"""
    return SanitizedQuery(googlesearch.quote_plus(q))  # pyre-ignore[16]


def transformer(q: Question, c: Context) -> Answer:
    """transformer

    Is a `Transformer`.
    """
    # this line below needs an internet connection!
    nlp = pipeline("question-answering")
    input_data = {"question": q, "context": c}
    answer = nlp(input_data)
    return answer.get("answer", IDK)


if __name__ == "__main__":
    print()
    print("IDK: ", IDK, "\n")
    print("type(IDK): ", type(IDK), "\n")
    print("IDK_TYPE: ", IDK_TYPE, "\n")
    print("type(IDK_TYPE): ", type(IDK_TYPE), "\n")
    print("IDK_TYPE_TypeVar: ", IDK_TYPE_TypeVar, "\n")
    print("type(IDK_TYPE_TypeVar): ", type(IDK_TYPE_TypeVar), "\n")
    # print('IDK_TYPE("hello"): ', IDK_TYPE("hello"), "\n")
    # print('type(IDK_TYPE("hello")): ', type(IDK_TYPE("hello")), "\n")
    print("transformer: ", transformer, "\n")
    print("type(transformer): ", type(transformer), "\n")
    print("Transformer: ", Transformer, "\n")
    print("type(Transformer): ", type(Transformer), "\n")
    print("get_type_hints(transformer): ", get_type_hints(transformer), "\n")
    print("create_query(Question('what?')): ", create_query(Question("what?")))
    # print(": ", transformer("ok", "cool"))
