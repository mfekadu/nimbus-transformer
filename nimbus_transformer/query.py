"""Defines the Google Search `Query` object.

A Google `Query` can become [quite advanced][1]. For the use case of this
`nimbus_transformer` program, we make use of the `site:` keyword to
limit our results to the calpoly.edu domain.

Typical usage example:

    from nimbus_transformer.question import Question
    from nimbus_transformer.query import Query
    question = Question("what?")
    query = Query(question)
    print(query)
    >>> "what? site:calpoly.edu"

[1]: https://www.google.com/advanced_search
"""

from nimbus_transformer.question import Question


class Query(str):
    """
    A `Query` is a string that would be
            typed into the Google search box,
            which is expected to be used as a URL parameter.

    Example:
        >>> question = Question("what is foaad khosmood's email?")
        >>> Query(question)
        "what is foaad khosmood's email? site:calpoly.edu"

    Resources:
        * Example Google Search:
            * http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu

        * More details about the dunder `__new__` method:
            * https://stackoverflow.com/q/2673651
    """

    def __new__(cls, question: Question):
        """
        Describes how to create a new `Query` string object
            from a given `nimbus_transformer.question.Question`.

        Args:
            question: A `nimbus_transformer.question.Question` string.

        Returns:
            A `Query` object.
        """

        # make a Google query with appropriate scope of domain name
        query = f"{question} site:calpoly.edu"

        # use the str.__new__() and rename object as Query
        obj = super(Query, cls).__new__(cls, query)

        # save for future reference
        obj.question = question
        obj.query = query

        return obj
