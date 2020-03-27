#!/usr/bin/env python3


class Question(str):
    """
    `Question`: a sentence that elicits information
        about Cal Poly staff/clubs/etc.
    e.g. `"What is Foaad Khosmood's email?"`
    e.g. `"What is Foaad's office?"`
    e.g. `"What courses does Foaad Khosmood teach this quarter?"`
    """

    pass


class Query(str):
    """
    `Query`: a string of text to pass into Google search
    `{Question}` or
    `{Question} site:calpoly.edu`

    Resources:
        * https://stackoverflow.com/q/2673651
    """

    def __new__(cls, question: Question):
        """Describes how to create a new Query string object"""

        # make a Google query with appropriate scope of domain name
        query = f"{question} site:calpoly.edu"

        # use the str.__new__() and rename object as Query
        obj = super(Query, cls).__new__(cls, query)

        # save for future reference
        obj.question = question
        obj.query = query

        return obj


class Result(str):
    """
    `Result`: the Google html page for a given `Query`
    e.g. [this page][4]

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """

    pass


class ResultURL(str):
    """
    `ResultURLs`: the first 10 **URLs** in `Result`
    """

    pass


class Context(str):
    """
    `Context`: one large text document containing
        the text content of each url in `ResultURLs`.
    """

    pass


class SimpleContext(str):
    """
    `SimpleContext`: one large text document containing
        the text content of the first 10 **html sections** in `Result`
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
