#!/usr/bin/env python3

import googlesearch


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


def url_param_sanitize(q: Query) -> str:
    """
    Args:
        q: A `Query` string that would be
            typed into the Google search box,
            which is expected to be used as a URL parameter.

    Example:
        >>> q = "what is foaad khosmood's email? site:calpoly.edu"
        >>> url_param_sanitize(q)
        what+is+foaad+khosmood%27s+email%3F+site%3Acalpoly.edu
        >>> url_param_sanitize("a!a@a#a$a%a^a&a*a(a)a_a+a a")
        'a%21a%40a%23a%24a%25a%5Ea%26a%2Aa%28a%29a_a%2Ba+a'

    Returns:
        A string such that spaces are converted to `+` and special characters
            into their appropriate codes.
    """
    return googlesearch.quote_plus(str(q))


class Result(str):
    """
    A `Result` is the Google html page for a given `Query`.

    For example [this page][4].

    Attributes:
        query: A `Query` string that would be
            typed into the Google search box,
            which is expected to be used as a URL parameter.

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """

    # static variable
    BASE_URL = "https://www.google.com/search?q="

    def __init__(self, query: Query) -> None:
        super().__init__()
        self.query = query

    def get_google_result(self) -> str:
        """
        Perform a Google search and return the html content.

        Example:
            >>> from nimbus_transformer import Question, Query, Result
            >>> question = Question("what is foaad khosmood's email?")
            >>> query = Query(question)
            >>> google_result = Result(query)
            >>> google_result.get_google_result()
            '<html><body><div>...</div></body></html>'

        Returns:
            A string of HTML representing the [Google search result][4] page.

        [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
        """
        URL = f"{self.BASE_URL}{url_param_sanitize(self.query)}"
        html_page = googlesearch.get_page(URL)
        return html_page

    @property
    def question(self):
        """
        Gets the original `Question` that leads to this `Result`
        """
        return self.query.question


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

    google_result = Result(query)

    print(google_result.BASE_URL)

    print(google_result.question)
    print(google_result.query)
    print(google_result.get_google_result())
