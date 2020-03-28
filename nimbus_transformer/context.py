"""Defines the Google Search `Context` object.

A Google Search `Context` is one large text document of the text content of the
first 10 `ResultURLs` from a Google Search `nimbus_transformer.query.Query`.


Typical usage example:

    from nimbus_transformer.question import Question
    from nimbus_transformer.query import Query
    from nimbus_transformer.result import Result
    # TODO: somehow get the ResultURLs
    # TODO: ResultURLs is a property of Result
    from nimbus_transformer.context import Context
    question = Question("what is foaad khosmood's email?")
    query = Query(question)
    google_result = Result(query)
    # TODO: finish this example
    >>> # TODO: finish this example

[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
"""


class Context(str):
    """
    A `Context` is one large text document of the text content of the
    first 10 `ResultURLs` from a Google Search `nimbus_transformer.query.Query`

    Attributes:
        # TODO: ???

    # TODO: SimpleContext is a property of Context
    """

    pass
