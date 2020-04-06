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
from typing import Optional, get_type_hints
from bs4 import BeautifulSoup
import googlesearch
from fuzzywuzzy import fuzz
from requests import get
from requests.models import Response
from transformers import pipeline
from typing_extensions import Final
from typing import List, Callable, Iterator, Tuple
from ntfp.ntfp_types import (
    IDK,
    IDK_TYPE,
    Answer,
    Context,
    WebPageContext,
    GooglePage,
    GoogleResultURL,
    GoogleResultURLIterator,
    Query,
    Question,
    SanitizedQuery,
    WebPage,
    URL,
    ExtraDataDict,
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


def get_page(url: URL, verbose=False) -> WebPage:
    """Returns the html \
        [`WebPage`](ntfp_types.html#ntfp.ntfp_types.WebPage) \
        of the given [`URL`](ntfp_types.html#ntfp.ntfp_types.URL).
    """
    if url.endswith("pdf"):
        if verbose:
            print("skipping PDF file && returning empty WebPage...")
        # TODO: consider returning None? but then return is Optional[WebPage]
        # TODO: consider having create_query avoid PDFs via "-filetype:pdf"
        # TODO: but also consider that Google can get GoogleContext from PDFs,
        #     :    which is good
        # TODO: but for sure get_page should avoid PDFs.
        #     :    unless we can import some fancy PDF OCR package to handle it
        return WebPage("")
    response: Response = get(url)
    html: str = response.text
    return WebPage(html)


def get_google_page(query: Query) -> GooglePage:
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
        >>> google_page: GooglePage = get_google_page_page(query)
        >>> google_page
        ... '<html><body><div>...Google...foaad...email...</div></body></html>'
        >>> type(google_page)  # type still str at runtime
        ... <class 'str'>

    Returns:
        A string of HTML representing the [Google Search result][4] \
            [`GooglePage`](ntfp_types.html#ntfp.ntfp_types.GooglePage).

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """
    BASE_GOOGLE_URL: Final[URL] = URL("https://www.google.com/search?q=")

    sanitized_query: SanitizedQuery = url_param_sanitize(query)

    url: URL = URL(f"{BASE_GOOGLE_URL}{sanitized_query}")

    html_page: GooglePage = GooglePage(get_page(url))

    return html_page


def fetch_google_result_urls(
    query: Query, limit: Optional[int] = None
) -> GoogleResultURLIterator:
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
            [`GooglePage`](ntfp_types.html#ntfp.ntfp_types.GooglePage).

    Resources:
        * How to type annotate Generators
            * https://stackoverflow.com/q/27264250
            * https://docs.python.org/3/library/typing.html#typing.Generator

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """
    for url in googlesearch.search(
        query,
        num=10,
        stop=limit,  # allows for infinite-ish generation of google results
        country="",  # TODO: consider setting San Luis Obispo if possible?
    ):
        yield GoogleResultURL(url)


def transformer(q: Question, c: Context) -> Tuple[Answer, ExtraDataDict]:
    """transformer

    [//]: # (markdown comment # noqa)

    Resources:
        * HuggingFace Transformers pipelines
            * https://github.com/huggingface/transformers#quick-tour-of-pipelines
    """
    if len(c) <= 0:
        extra_data: ExtraDataDict = {
            "score": -1.0,
            "start": -1,
            "end": -1,
            "tokenizer": "NA_SKIPPED_TRANSFORMER",
            "model": "NA_SKIPPED_TRANSFORMER",
        }
        return (
            Answer(IDK),
            extra_data,
        )
    # FIXME: this line below needs an internet connection!
    nlp = pipeline("question-answering")
    input_data = {"question": q, "context": c}
    answer = nlp(input_data)
    extra_data: ExtraDataDict = {
        "score": answer.get("score", -1.0),
        "start": answer.get("start", -1),
        "end": answer.get("end", -1),
        "tokenizer": nlp.tokenizer.__class__.__name__,
        "model": nlp.model.__class__.__name__,
    }
    return (answer.get("answer", IDK), extra_data)


def extract_webpage_context(
    page: WebPage, only_paragraphs: Optional[bool] = False
) -> WebPageContext:
    """Extracts the text from a given HTML \
        [`WebPage`](ntfp_types.html#ntfp.ntfp_types.WebPage) and returns it as a \
        [`WebPageContext`](ntfp_types.html#ntfp.ntfp_types.WebPageContext).

    [//]: # (markdown comment # noqa)

    Args:
        page: A [`WebPage`](ntfp_types.html#ntfp.ntfp_types.WebPage) HTML string.
        only_paragraphs: An Optional boolean value to specify whether to only \
            look at paragraph tags `<p>`. (Default = False).

    Returns:
        The [`WebPageContext`](ntfp_types.html#ntfp.ntfp_types.WebPageContext) string.

    Example:
        >>> html = "<html><div>Hello World!</div><code>126/3==42</code></html>"
        >>> p: WebPage = WebPage(html)
        >>> wpc: WebPageContext = extract_webpage_context(p)
        >>> wpc
        ... 'Hello World!126/3==42'

    Resources:
        * BeautifulSoup4
            * https://pypi.org/project/beautifulsoup4/
    """
    soup: BeautifulSoup = BeautifulSoup(markup=page, features="html.parser")
    if only_paragraphs is True:
        paragraph_text: str = "".join([p.text for p in soup.find_all("p")])
        return WebPageContext(Context(paragraph_text))
    text: Context = Context(str(soup.text))
    return WebPageContext(text)


def extract_relevant_context(page: WebPage, question: Question) -> Context:
    soup: BeautifulSoup = BeautifulSoup(markup=page, features="html.parser")

    txt_lst: List[str] = [x for x in soup.stripped_strings]

    def relevance(to):
        original_question = to

        def filter_func(text):
            # TODO: make smarter filter rules
            FUZZ_THRESHOLD = 30
            LEN_THRESHOLD = 2
            if original_question in text:
                # ASSUME: that answer would not include original_question
                return False
            if fuzz.ratio(text, original_question) < FUZZ_THRESHOLD:
                # ASSUME: some lexical similarity question with answer
                return False
            if len(text) < LEN_THRESHOLD:
                # ASSUME: answer is not short
                return False
            return True

        return filter_func

    # Filter by relevance to the question
    relevant_text_list: Iterator[str] = filter(relevance(to=question), txt_lst)

    return Context("\n".join(relevant_text_list))


def get_context(
    question: Question, use_google: bool = True, verbose: bool = False
) -> Tuple[Query, WebPage, Context]:
    if use_google:
        query: Query = create_query(question)
        page: GooglePage = get_google_page(query)
        if verbose:
            print("query: ", query, "\n")
            print("len(page): ", len(page), "\n")
        context: Context = extract_relevant_context(page, question)
        return query, page, context
    else:
        raise NotImplementedError


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

    # x = get_google_page(sanitized_query)
    # y = get_google_page(query)
    # assert x[:5] == y[:5]
    # # reveal_type(x)
    # # reveal_type(y)

    google_page: GooglePage = get_google_page(query)

    first_ten_urls: List[GoogleResultURL] = [
        x for x in fetch_google_result_urls(query, limit=10)
    ]  # noqa
    print("first_ten_urls: ", first_ten_urls)
    # reveal_type(first_ten_urls)

    f: Callable[[URL], WebPage] = get_page
    result_pages: List[WebPage] = [f(url) for url in first_ten_urls]
    # reveal_type(result_pages)

    f: Callable[[WebPage], WebPageContext] = extract_webpage_context
    contexts: List[WebPageContext] = [f(page) for page in result_pages]

    large_context: Context = Context("\n\n".join(contexts))

    print(large_context)
    # print(": ", transformer("ok", "cool"))
