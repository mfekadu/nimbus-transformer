#!/usr/bin/env python3
# flake8: noqa
from typing import Callable, Iterator, List, NewType, Type
from typing_extensions import Literal

__pdoc__ = {}

Question = NewType("Question", str)
"""Question"""
__pdoc__[
    "Question"
] = """A Question type
Example:
    [`Question`](#ntfp.ntfp_types.Question): "what is foaad khosmood's email?"

    [`Query`](#ntfp.ntfp_types.Query): "what is foaad khosmood's email? site:calpoly.edu"

    [`Context`](#ntfp.ntfp_types.Context): "The email is foaad@calpoly.edu."

    [`Answer`](#ntfp.ntfp_types.Answer): "foaad@calpoly.edu"
"""

Query = NewType("Query", str)
"""Query"""
__pdoc__[
    "Query"
] = """A Query type

Has _subtype_ [`SanitizedQuery`](#ntfp.ntfp_types.SanitizedQuery)

Example:
    [`Question`](#ntfp.ntfp_types.Question): "what is foaad khosmood's email?"

    [`Query`](#ntfp.ntfp_types.Query): "what is foaad khosmood's email? site:calpoly.edu"

    [`Context`](#ntfp.ntfp_types.Context): "The email is foaad@calpoly.edu."

    [`Answer`](#ntfp.ntfp_types.Answer): "foaad@calpoly.edu"
"""

SanitizedQuery = NewType("SanitizedQuery", Query)
"""SanitizedQuery"""
__pdoc__[
    "SanitizedQuery"
] = """A SanitizedQuery type

Has _supertype_ [`Query`](#ntfp.ntfp_types.Query).

Example:
    ```
    "what+is+foaad+khosmood%27s+email%3F+site%3Acalpoly.edu"
    ```
"""

WebPage = NewType("WebPage", str)
"""WebPage"""
__pdoc__[
    "WebPage"
] = """A WebPage type

Has _subtype_ [`GoogleResultPage`](#ntfp.ntfp_types.GoogleResultPage).

Has _subtype_ [`GoogleResultURLPage`](#ntfp.ntfp_types.GoogleResultURLPage).

Example:
    ```
    "<html><body><div>...Website.com...</div></body></html>"
    ```
"""
WebPages = List[WebPage]
WebPageIterataor = Iterator[WebPage]

URL = NewType("URL", str)
"""URL"""
__pdoc__[
    "URL"
] = """A URL type

Has _subtype_ [`GoogleResultURL`](#ntfp.ntfp_types.GoogleResultURL).

Example:
    ```
    "https://www.website.com/..."
    ```
"""
URLs = List[URL]
URLIterataor = Iterator[URL]

GoogleResultPage = NewType("GoogleResultPage", WebPage)
"""GoogleResultPage"""
__pdoc__[
    "GoogleResultPage"
] = """A GoogleResultPage type

Has _supertype_ [`WebPage`](#ntfp.ntfp_types.WebPage).

Example:
    ```
    "<html><body><div>...Google.com...</div></body></html>"
    ```
"""
GoogleResultPages = List[GoogleResultPage]
GoogleResultPageIterataor = Iterator[GoogleResultPage]

GoogleResultURL = NewType("GoogleResultURL", URL)
"""GoogleResultURL"""
__pdoc__[
    "GoogleResultURL"
] = """A GoogleResultURL type

Has _supertype_ [`URL`](#ntfp.ntfp_types.URL).

A URL found in a GoogleResultPage like:

```
"http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu"
```

Example:
    >>> query: Query = Query("what is foaad site:calpoly.edu")
    >>> get_google_result_urls(query)
    ... [
    ...     'https://cpe.calpoly.edu/faculty/foaad/',
    ...     'http://users.csc.calpoly.edu/~dekhtyar/466-Spring2012/',
    ...     'https://lib.calpoly.edu/events/my-tech-journey/',
    ...     'https://cpe.calpoly.edu/faculty/',
    ...     '...'
    ... ]
"""
GoogleResultURLs = List[GoogleResultURL]
GoogleResultURLIterator = Iterator[GoogleResultURL]

GoogleResultURLPage = NewType("GoogleResultURLPage", WebPage)
"""GoogleResultURLPage"""
__pdoc__[
    "GoogleResultURLPage"
] = """A GoogleResultURLPage type

Has _supertype_ [`WebPage`](#ntfp.ntfp_types.WebPage).

Example:
    ```
    "<html><body><div>...ResultURL.com...</div></body></html>"
    ```
"""
GoogleResultURLPages = List[GoogleResultURLPage]
GoogleResultURLPageIterator = Iterator[GoogleResultURLPage]

Context = NewType("Context", str)
"""Context"""
__pdoc__[
    "Context"
] = """A Context type
Example:
    [`Question`](#ntfp.ntfp_types.Question): "what is foaad khosmood's email?"

    [`Query`](#ntfp.ntfp_types.Query): "what is foaad khosmood's email? site:calpoly.edu"

    [`Context`](#ntfp.ntfp_types.Context): "The email is foaad@calpoly.edu."

    [`Answer`](#ntfp.ntfp_types.Answer): "foaad@calpoly.edu"
"""

Answer = NewType("Answer", str)
"""Answer"""
__pdoc__[
    "Answer"
] = """An Answer type
Example:
    [`Question`](#ntfp.ntfp_types.Question): "what is foaad khosmood's email?"

    [`Query`](#ntfp.ntfp_types.Query): "what is foaad khosmood's email? site:calpoly.edu"

    [`Context`](#ntfp.ntfp_types.Context): "The email is foaad@calpoly.edu."

    [`Answer`](#ntfp.ntfp_types.Answer): "foaad@calpoly.edu"
"""

IDK_TYPE = Literal["¯\\_(ツ)_/¯"]
"""IDK_TYPE = `Literal["¯\\_(ツ)_/¯"]`"""

IDK: IDK_TYPE = "¯\\_(ツ)_/¯"
"""IDK: `IDK_TYPE`"""


if __name__ == "__main__":
    question: Question = Question("what is the meaning of life?")
    context: Context = Context("The meaning of life is 42.")
    t: Callable[[Question, Context], Answer] = lambda q, c: Answer("42")
    answer: Answer = t(question, context)
    print(answer)
