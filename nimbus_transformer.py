#!/usr/bin/env python3


class Question(str):
    """
    A `Question` is a sentence that elicits information
    about Cal Poly staff/clubs/etc. This class merely wraps the `str` type
    for increased readablility of the code below. # noqa

    TODO: consider adding functions to this class like:

    * classify - maps a given `Question` to a known `Question` with
        - [`sklearn.neighbors.KNeighborsClassifier` as used by Cal Poly CSAI][1]

    * paraphrase - kind of like classify, but use a technique
        - known as Question Paraphrasing coined by Gan et al.
        - https://www.aclweb.org/anthology/P19-1610/

    * normalize - transform the given `Question` string to all lowercase, etc.

    Example:
        >>> Question("What is Foaad Khosmood's email?")
        "What is Foaad Khosmood's email?"
        >>> Question("What is Foaad's office?")
        "What is Foaad's office?"
        >>> Question("What courses does Foaad Khosmood teach this quarter?")
        'What courses does Foaad Khosmood teach this quarter?'

    [1]: https://github.com/calpoly-csai/api/blob/7e24774fccc6f835c59c4b6d3414b79c1ba1fd0b/nimbus_nlp/question_classifier.py#L5
    """

    pass


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
            from a given `Question`.

        Args:
            question: A `Question` string.

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
