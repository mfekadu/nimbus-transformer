"""Defines the Google Search `Results` object.

A Google `Results` is an HTML page [like this page][4].

[//]: # (markdown comment # noqa)
A GET request to the corresponding Query URL of a Google Search `nimbus_transformer.query.Query`
is needed to extract the HTML page and later the `nimbus_transformer.context.Context`.

Example Query URL:
```
'http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu'
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

    print(google_result.result)
    >>> '<html><body><div>...</div></body></html>'

Iterator Example:

    for url in google_result:
        print(url)
    >>> 'https://cpe.calpoly.edu/faculty/foaad/'
    >>> 'http://users.csc.calpoly.edu/~dekhtyar/466-Spring2012/'
    >>> 'https://iatpp.calpoly.edu/organization'
    >>> 'https://lib.calpoly.edu/events/my-tech-journey/'
    >>> 'https://cpe.calpoly.edu/faculty/'
    >>> 'https://lib.calpoly.edu/events/gerrymandering-in-america/'
    >>> 'https://lib.calpoly.edu/events/open-access-and-government-transparency/'
    >>> 'https://www.calpoly.edu/news/cal-poly-and-university-miami-team-help-newspapers-using-ai'
    >>> 'https://digitalcommons.calpoly.edu/theses/1623/'
    >>> 'https://www.calpoly.edu/'

    urls = [u for u in google_result]
    print(urls)
    >>> ['https://cpe.calpoly.edu/faculty/foaad/', 'http://users.csc.calpoly.edu/~dekhtyar/466-Spring2012/', 'https://iatpp.calpoly.edu/organization', 'https://lib.calpoly.edu/events/my-tech-journey/', 'https://cpe.calpoly.edu/faculty/', 'https://lib.calpoly.edu/events/gerrymandering-in-america/', 'https://lib.calpoly.edu/events/open-access-and-government-transparency/', 'https://www.calpoly.edu/news/cal-poly-and-university-miami-team-help-newspapers-using-ai', 'https://digitalcommons.calpoly.edu/theses/1623/', 'https://www.calpoly.edu/']


[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
"""

import googlesearch
from nimbus_transformer.query import Query
from nimbus_transformer.question import Question
from typing import Iterator


def url_param_sanitize(q: Query) -> str:
    """Sanitizes string for use in a URL for an HTTP GET request.

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
    return googlesearch.quote_plus(str(q))  # pyre-ignore[16]


class Results:
    """
    [//]: # (markdown comment # noqa)
    A `Results` is the Google html page for a given `nimbus_transformer.query.Query`.

    For example [this page][4].

    # TODO: ResultsURLs is a property of Results

    Attributes:
        query: A `nimbus_transformer.query.Query` string that would be
            typed into the Google Search box,
            which is expected to be used as a URL parameter.


    Resources:
        * How to assert string is HTML
            * https://stackoverflow.com/q/24856035
            * TODO: write tests

    [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
    """

    # class variables
    BASE_URL = "https://www.google.com/search?q="
    query = None

    def __init__(self, query: Query) -> None:
        super().__init__()
        self.query = query
        self._html_page = self.get_google_result()
        self._first_ten_urls = [u for u in self.fetch_result_urls(limit=10)]

    def fetch_result_urls(self, limit=None) -> Iterator[str]:
        """Fetches result URLs from [large list of Google Search results][4].

        [//]: # (markdown comment # noqa)

        Retrieves strings of URLs pertaining to the `Results.query`

        Yields:
            A single url from the Google Search `Results`.

        Resources:
            * How to type annotate Generators
                * https://stackoverflow.com/q/27264250
                * https://docs.python.org/3/library/typing.html#typing.Generator

        [4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
        """
        for url in googlesearch.search(
            self.query,
            num=10,
            stop=limit,  # allows for infinite-ish generation of google results
            country="",  # TODO: consider setting San Luis Obispo if possible?
        ):
            yield url

    def __len__(self):
        return len(self._first_ten_urls)

    def __getitem__(self, position):
        return self._first_ten_urls[position]

    @property
    def result(self) -> str:
        """
        `Results.get_google_result`
        """
        return self.get_google_result()

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
