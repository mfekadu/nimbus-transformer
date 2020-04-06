#!/usr/bin/env python3

from ntfp import ntfp
from ntfp import ntfp_types

from typing import Callable, List

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
)

if __name__ == "__main__":
    print("nimbus_transformer")

    user_input: str = input("question: ")
    question: ntfp_types.Question = ntfp_types.Question(user_input)
    query: ntfp_types.Query = ntfp.create_query(question)
    print("query: ", query, "\n")
    sanitized_query: ntfp_types.SanitizedQuery = ntfp.url_param_sanitize(query)
    print("sanitized_query: ", sanitized_query, "\n")
    first_ten_urls: ntfp_types.GoogleResultURLs = [
        x for x in ntfp.fetch_google_result_urls(query, limit=10)
    ]
    print("first_ten_urls: ", first_ten_urls)
    type_hint = Callable[[ntfp_types.URL], ntfp_types.WebPage]
    fun: type_hint = ntfp.get_page
    type_hint_2 = ntfp_types.GooglePage
    result_pages: ntfp_types.GooglePages = [
        type_hint_2(fun(url)) for url in first_ten_urls
    ]

    google_page: ntfp_types.GooglePage = ntfp.get_google_page(query)

    f: Callable[[ntfp_types.URL], ntfp_types.WebPage] = ntfp.get_page
    result_pages: List[ntfp_types.WebPage] = [f(url) for url in first_ten_urls]

    WP = ntfp_types.WebPage
    WPC = ntfp_types.WebPageContext
    f: Callable[[WP], WPC] = ntfp.extract_webpage_context
    contexts: List[WPC] = [f(page) for page in result_pages]

    C = ntfp_types.Context
    large_context: C = ntfp_types.Context("\n\n".join(contexts))

    print(large_context)
