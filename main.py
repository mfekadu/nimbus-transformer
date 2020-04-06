#!/usr/bin/env python3
from typing import Callable, List

from ntfp.ntfp import (
    create_query,
    extract_webpage_context,
    fetch_google_result_urls,
    get_google_page,
    get_page,
    url_param_sanitize,
    transformer,
)
from ntfp.ntfp_types import (
    IDK,
    IDK_TYPE,
    URL,
    Answer,
    Context,
    GooglePage,
    GooglePages,
    GoogleResultURL,
    GoogleResultURLIterator,
    GoogleResultURLs,
    Query,
    Question,
    SanitizedQuery,
    WebPage,
    WebPageContext,
)

if __name__ == "__main__":
    print("nimbus_transformer")

    user_input: str = input("question: ")
    question: Question = Question(user_input)

    query: Query = create_query(question)
    print("query: ", query, "\n")

    # first_ten_urls: GoogleResultURLs = [
    #     x for x in fetch_google_result_urls(query, limit=10)
    # ]
    # print("first_ten_urls: ", first_ten_urls)

    # google_page: GooglePage = get_google_page(query)

    # f: Callable[[URL], WebPage] = get_page
    # result_pages: List[WebPage] = [f(url) for url in first_ten_urls]

    # f: Callable[[WebPage], WebPageContext] = extract_webpage_context
    # contexts: List[WebPageContext] = [f(page) for page in result_pages]

    # large_context: Context = Context("\n\n".join(contexts))

    # print(large_context)

    def generate_data(query, verbose=False):
        sanitized_query: SanitizedQuery = url_param_sanitize(query)
        print("sanitized_query: ", sanitized_query, "\n")

        large_context: str = ""

        for url in fetch_google_result_urls(query, limit=10):
            if verbose:
                print(f"getting data for url: {url}...")
            page: WebPage = get_page(url, verbose=verbose)
            context: WebPageContext = extract_webpage_context(page)
            large_context += context + "\n\n"
            yield (url, page, context)

        return large_context

    def handle_return(generator, func):
        """
        https://stackoverflow.com/a/41875793
        """
        returned = yield from generator
        func(returned)

    gen = generate_data(query)  # , verbose=True)

    def fun(return_value):
        print(f"type(return_value): {type(return_value)}")
        print(f"len(return_value): {len(return_value)}")

    def print_answer(question):
        def func(large_context):
            answer: Answer = transformer(question, context)
            print("\n\n")
            print("question: ", question)
            print("context[:25]", large_context[:25])
            print("answer: ", answer)

        return func

    fun2 = print_answer(question)

    for url, page, context in handle_return(gen, fun2):
        print("got data\n")
