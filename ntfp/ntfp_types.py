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

Just a string of HTML.

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

The actual Google search page with results.

Example:
    ```
    "<html><body><div>...Google.com...</div></body></html>"
    ```

    [**Click here for an example GoogleResultPage**][4]

[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
"""
GoogleResultPages = List[GoogleResultPage]
GoogleResultPageIterataor = Iterator[GoogleResultPage]

GoogleResultURL = NewType("GoogleResultURL", URL)
"""GoogleResultURL"""
__pdoc__[
    "GoogleResultURL"
] = """A GoogleResultURL type

Has _supertype_ [`URL`](#ntfp.ntfp_types.URL).

A URL found in a [`GoogleResultPage`](#ntfp.ntfp_types.GoogleResultPage) like:

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

    ### Image Example
    The GoogleResultURLs are the clickable purple or blue text in the image below.
    <br>
    The first example GoogleResultURL below is _"https://cpe.calpoly.edu/faculty/foaad/"_
    <br>
    <img src="../google.png"
         alt="google.png"
         width="400px"
         title="the GoogleResultURLs are the clickable purple or blue text in this image."/>
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

    ### Image Example
    [**Clicking on the first link**][1] in the below image of a Google search would then display a GoogleResultURLPage.
    <br>
    <img src="../google.png"
         alt="google.png"
         width="400px"
         title="..."/>

[1]: https://cpe.calpoly.edu/faculty/foaad/
"""
GoogleResultURLPages = List[GoogleResultURLPage]
GoogleResultURLPageIterator = Iterator[GoogleResultURLPage]

Context = NewType("Context", str)
"""Context"""
__pdoc__[
    "Context"
] = """A Context type

Has _subtype_ [`GoogleContext`](#ntfp.ntfp_types.GoogleContext).

Has _subtype_ [`FullContext`](#ntfp.ntfp_types.FullContext).

Example:
    [`Question`](#ntfp.ntfp_types.Question): "what is foaad khosmood's email?"

    [`Query`](#ntfp.ntfp_types.Query): "what is foaad khosmood's email? site:calpoly.edu"

    [`Context`](#ntfp.ntfp_types.Context): "The email is foaad@calpoly.edu."

    [`Answer`](#ntfp.ntfp_types.Answer): "foaad@calpoly.edu"
"""

GoogleContext = NewType("GoogleContext", Context)
"""GoogleContext"""
__pdoc__[
    "GoogleContext"
] = """A GoogleContext type

Has _supertype_ [`Context`](#ntfp.ntfp_types.Context).

The short preview text that Google shows within the \
    [`GoogleResultPage`](#ntfp.ntfp_types.GoogleResultPage) \
    just below the [`GoogleResultURL`](#ntfp.ntfp_types.GoogleResultURL).

That text often contains words that Google has deemed most _relevant_ to \
    the query, and sometimes sufficiently answers the question.

Example:
    [Click here for an example Google Search][4] and determine for yourself \
        if the short block of text below each \
            [`GoogleResultURL`](#ntfp.ntfp_types.GoogleResultURL) \
            sufficiently answers the question.

    ### Image Example
    See the highlighted text below.
    <br>
    <img src="../google.png"
         alt="google.png"
         width="400px"
         title="the highlighted text is a GoogleContext"/>

[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
"""

FullContext = NewType("FullContext", Context)
"""FullContext"""
__pdoc__[
    "FullContext"
] = """A FullContext type

Has _supertype_ [`Context`](#ntfp.ntfp_types.Context)

**The text content of a [`GoogleResultURLPage`](#ntfp.ntfp_types.GoogleResultURLPage).**
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
