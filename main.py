#!/usr/bin/env python3

from nimbus_transformer.question import Question
from nimbus_transformer.query import Query
from nimbus_transformer.result import Results

from ntfp import ntfp
from ntfp import ntfp_types

from typing import Callable

class Context(str):
    """
    `Context`: one large text document containing
        the text content of each url in `Results`.
    """

    pass


class SimpleContext(str):
    """
    `SimpleContext`: one large text document containing
        the text content of the first 10 **html sections** in `Results`
    """

    pass


class Answer(str):
    """
    `Answer`: a segment text found within the given `Context`
        that appropriately answers the given `Question`.
    """

    pass


if __name__ == "__main__":
    print("nimbus_transformer")

    user_input = input("question: ")

    question = Question(user_input)

    query = Query(question)

    print("question...", question)
    print("query...", query)

    google_result = Results(query)

    urls = [u for u in google_result]
    print(urls)

    # print(google_result.BASE_URL)

    # print(google_result.question)
    # print(google_result.query)
    # print(google_result.get_google_result())

    user_input: str = input("question: ")
    question: ntfp_types.Question = ntfp_types.Question(user_input)
    query: ntfp_types.Query = ntfp.create_query(question)
    print("query: ", query, "\n")
    sanitized_query: ntfp_types.SanitizedQuery = ntfp.url_param_sanitize(query)
    print("sanitized_query: ", sanitized_query, "\n")
    x = ntfp.get_google_result_page(sanitized_query)
    y = ntfp.get_google_result_page(query)
    assert x[:5] == y[:5]
    first_ten_urls: ntfp_types.GoogleResultURLs = [
        x for x in ntfp.fetch_google_result_urls(query, limit=10)
    ]
    print("first_ten_urls: ", first_ten_urls)
    type_hint = Callable[[ntfp_types.URL], ntfp_types.WebPage]
    fun: type_hint = ntfp.get_page
    type_hint_2 = ntfp_types.GoogleResultPage
    result_pages: ntfp_types.GoogleResultPages = [
        type_hint_2(fun(url)) for url in first_ten_urls
    ]
