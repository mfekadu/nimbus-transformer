"""Defines the Cal Poly `Question` object.

A Cal Poly `Question` is a sentence that elicits information
about Cal Poly staff/clubs/etc.

Typical usage example:

    from nimbus_transformer.question import Question
    question = Question("what?")
    print(question)
    >>> "what?"

[1]: https://www.google.com/advanced_search
"""


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
