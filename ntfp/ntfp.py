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
from typing import Optional, Union, get_type_hints

import googlesearch
from transformers import pipeline
from typing_extensions import Final

from ntfp.ntfp_types import (
    IDK,
    IDK_TYPE,
    Answer,
    Context,
    GoogleResultPage,
    GoogleResultPageIterataor,
    GoogleResultPages,
    GoogleResultURL,
    GoogleResultURLIterator,
    GoogleResultURLPage,
    GoogleResultURLPageIterator,
    GoogleResultURLPages,
    GoogleResultURLs,
    Query,
    Question,
    SanitizedQuery,
    WebPage,
    WebPageIterataor,
    WebPages,
    URL,
    URLs,
    URLIterataor,
)


def create_query(question: Question) -> Query:
    """
    [//]: # (markdown comment # noqa)

    Describes how to create a new
        [`Query`](ntfp_types.html#ntfp.ntfp_types.Query) string
        from a given [`Question`](ntfp_types.html#ntfp.ntfp_types.Question).

    Args:
        question: A [`Question`](ntfp_types.html#ntfp.ntfp_types.Question) string.

    Returns:
        A [`Query`](ntfp_types.html#ntfp.ntfp_types.Query) string.
    """
    # make a Google query with appropriate scope of domain name
    # by kind-of-sort-of-cast-str-to-Query-via-__init__-but-is-that-really-casting-idk-how-types-work-in-python  # noqa
    query: Query = Query(f"{question} site:calpoly.edu")
    return query


def url_param_sanitize(query: Query) -> SanitizedQuery:
    """Sanitizes the given
        [`Query`](ntfp_types.html#ntfp.ntfp_types.Query) string
        for use in a [`URL`](ntfp_types.html#ntfp.ntfp_types.URL)
        as an HTTP parameter in a HTTP GET request.

    [//]: # (markdown comment # noqa)

    Args:
        query: A [`Query`](ntfp_types.html#ntfp.ntfp_types.Query) string
            that would be typed into the Google Search box,
            which is expected to be used as a URL parameter.

    Example:
        >>> query: Query = Query("what is foaad khosmood's email? site:calpoly.edu")
        >>> url_param_sanitize(query)
        what+is+foaad+khosmood%27s+email%3F+site%3Acalpoly.edu
        >>> url_param_sanitize("a!a@a#a$a%a^a&a*a(a)a_a+a a")
        'a%21a%40a%23a%24a%25a%5Ea%26a%2Aa%28a%29a_a%2Ba+a'

    Returns:
        A [`SanitizedQuery`](ntfp_types.html#ntfp.ntfp_types.SanitizedQuery) \
            string such that spaces are converted to `+` \
                and special characters into their appropriate codes.

    """
    return SanitizedQuery(googlesearch.quote_plus(query))  # pyre-ignore[16]


def get_page(url: URL) -> WebPage:
    """Returns the html \
        [`WebPage`](ntfp_types.html#ntfp.ntfp_types.WebPage) \
        of the given [`URL`](ntfp_types.html#ntfp.ntfp_types.URL).
    """
    return WebPage(googlesearch.get_page(url))


def get_google_result_page(query: Query) -> GoogleResultPage:
    """
    Perform a Google Search and return the html content.

    Args:
        query: A [`Query`](ntfp_types.html#ntfp.ntfp_types.Query) string
            that would be typed into the Google Search box,
            which is expected to be used as a URL parameter.

    Example:
        >>> question: Question = Question("what is foaad email?")
        >>> query: Query = create_query(question)
        >>> query
        ... 'what is foaad email? site:calpoly.edu'
        >>> google_result: GoogleResultPage = get_google_result_page(query)
        >>> google_result
        ... '<html><body><div>...</div></body></html>'
        >>> type(google_result)  # type still str at runtime
        ... <class 'str'>

    Returns:
        A string of HTML representing the [Google Search result][4] \
            [`GoogleResultPage`](ntfp_types.html#ntfp.ntfp_types.GoogleResultPage).

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """
    BASE_GOOGLE_URL: Final[URL] = URL("https://www.google.com/search?q=")

    sanitized_query: SanitizedQuery = url_param_sanitize(query)

    url: URL = URL(f"{BASE_GOOGLE_URL}{sanitized_query}")

    html_page: GoogleResultPage = GoogleResultPage(get_page(url))

    return html_page


# fmt:off
def fetch_google_result_urls(query: Query, limit: Optional[int] = None) -> GoogleResultURLIterator:  # noqa
    """Fetches [`GoogleResultURL`](ntfp_types.html#ntfp.ntfp_types.GoogleResultURL)s \
        from [large list of Google Search results][4].

    [//]: # (markdown comment # noqa)

    Retrieves strings of \
        [`GoogleResultURL`](ntfp_types.html#ntfp.ntfp_types.GoogleResultURL)s \
        pertaining to the given [`Query`](ntfp_types.html#ntfp.ntfp_types.Query).

    Args:
        query: A [`Query`](ntfp_types.html#ntfp.ntfp_types.Query) string
            that would be typed into the Google Search box,
            which is expected to be used as a URL parameter.

        limit: An optional integer for the total number of results to fetch.
            By default `None` means fetch all results that google offers.

    Yields:
        A single \
            [`GoogleResultURL`](ntfp_types.html#ntfp.ntfp_types.GoogleResultURL)
            from the Google Search
            [`GoogleResultPage`](ntfp_types.html#ntfp.ntfp_types.GoogleResultPage).

    Resources:
        * How to type annotate Generators
            * https://stackoverflow.com/q/27264250
            * https://docs.python.org/3/library/typing.html#typing.Generator

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """
    # fmt: on
    for url in googlesearch.search(
        query,
        num=10,
        stop=limit,  # allows for infinite-ish generation of google results
        country="",  # TODO: consider setting San Luis Obispo if possible?
    ):
        yield GoogleResultURL(url)


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
    # reveal_type(IDK)

    print("type(IDK): ", type(IDK), "\n")
    # reveal_type(type(IDK))

    print("IDK_TYPE: ", IDK_TYPE, "\n")
    # reveal_type(IDK_TYPE)

    print("type(IDK_TYPE): ", type(IDK_TYPE), "\n")
    # reveal_type(type(IDK_TYPE))

    # print("IDK_TYPE_TypeVar: ", IDK_TYPE_TypeVar, "\n")
    # # reveal_type(IDK_TYPE_TypeVar)

    # print("type(IDK_TYPE_TypeVar): ", type(IDK_TYPE_TypeVar), "\n")
    # # reveal_type(type(IDK_TYPE_TypeVar))

    # print('IDK_TYPE("hello"): ', IDK_TYPE("hello"), "\n")

    # print('type(IDK_TYPE("hello")): ', type(IDK_TYPE("hello")), "\n")

    print("transformer: ", transformer, "\n")
    # reveal_type(transformer)

    print("type(transformer): ", type(transformer), "\n")
    # reveal_type(type(transformer))

    # print("Transformer: ", Transformer, "\n")
    # # reveal_type(Transformer)

    # print("type(Transformer): ", type(Transformer), "\n")
    # # reveal_type(type(Transformer))

    print("get_type_hints(transformer): ", get_type_hints(transformer), "\n")
    # reveal_type(get_type_hints(transformer))

    print()

    user_input: str = input("question: ")
    # reveal_type(user_input)

    question: Question = Question(user_input)
    # reveal_type(question)

    query: Query = create_query(question)
    print("query: ", query, "\n")
    print("type(query) == str: ", type(query) == str, "\n")
    # this typing module is not intuitive sometimes.
    # i suppose the reason is that the type checker is static
    # and has no affect on runtime values.
    print("type(query) != Query: ", type(query) != Query, "\n")
    # reveal_type(query)
    # reveal_type(type(query))
    # reveal_type(Query)

    sanitized_query: SanitizedQuery = url_param_sanitize(query)
    print("sanitized_query: ", sanitized_query, "\n")
    # reveal_type(sanitized_query)

    x = get_google_result_page(sanitized_query)
    y = get_google_result_page(query)
    assert x[:5] == y[:5]
    # reveal_type(x)
    # reveal_type(y)

    first_ten_urls: GoogleResultURLs = [x for x in fetch_google_result_urls(query, limit=10)]  # noqa
    print("first_ten_urls: ", first_ten_urls)
    # reveal_type(first_ten_urls)

    result_pages: GoogleResultPages = [GoogleResultPage(get_page(url)) for url in first_ten_urls]  # noqa
    # reveal_type(result_pages)

    # print(": ", transformer("ok", "cool"))
