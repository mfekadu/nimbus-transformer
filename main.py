#!/usr/bin/env python3

from nimbus_transformer.question import Question
from nimbus_transformer.query import Query
from nimbus_transformer.result import Results


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

    for url in google_result:
        print(url)

    # print(google_result.BASE_URL)

    # print(google_result.question)
    # print(google_result.query)
    # print(google_result.get_google_result())
