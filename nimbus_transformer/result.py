"""Defines the Google Search `Results` object.

A Google `Results` is an HTML page [like this page][4].

[//]: # (markdown comment # noqa)
A GET request to the corresponding URL of a Google Search `nimbus_transformer.query.Query`
is needed to extract the HTML page and later the `nimbus_transformer.context.Context`.

```
http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
```

Typical usage example:

    from nimbus_transformer.question import Question
    from nimbus_transformer.query import Query
    from nimbus_transformer.result import Results
    question = Question("what is foaad khosmood's email?")
    query = Query(question)
    google_result = Results(query)
    print(google_result.get_google_result())
    >>> '<html><body><div>...</div></body></html>'

[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
"""

import googlesearch
from nimbus_transformer.query import Query
from nimbus_transformer.question import Question


def url_param_sanitize(q: Query) -> str:
    """
    Args:
        q: A `nimbus_transformer.query.Query` string that would be
            typed into the Google Search box,
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


class Results(str):
    """
    [//]: # (markdown comment # noqa)
    A `Results` is the Google html page for a given `nimbus_transformer.query.Query`.

    For example [this page][4].

    # TODO: ResultsURLs is a property of Results

    Attributes:
        query: A `nimbus_transformer.query.Query` string that would be
            typed into the Google Search box,
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
        Perform a Google Search and return the html content.

        Example:
            >>> from nimbus_transformer import Question, Query, Results
            >>> question = Question("what is foaad khosmood's email?")
            >>> query = Query(question)
            >>> google_result = Results(query)
            >>> google_result.get_google_result()
            '<html><body><div>...</div></body></html>'

        Returns:
            A string of HTML representing the [Google Search result][4] page.

        [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
        """
        URL = f"{self.BASE_URL}{url_param_sanitize(self.query)}"
        html_page = googlesearch.get_page(URL)
        return html_page

    @property
    def question(self) -> Question:
        """
        Gets the original `nimbus_transformer.question.Question` that leads to this `Results`
        """
        return self.query.question
