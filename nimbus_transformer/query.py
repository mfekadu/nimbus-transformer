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
            typed into the Google Search box,
            which is expected to be used as a URL parameter.

    [//]: # (markdown comment # noqa)


    FIXME:
        theres a type bug when 2 `Query`s are added

        >>> type( Query("foo") + Query("bar") )
        ... <class 'str'>

        because `Query` inherits from `str` and [the `__add__` method][dunder_add]
        needs to be overridden.

        TODO: [consider the perils of inheritance][ariel_ortiz_inheritance_talk]
            and whether to "favor composition over inheritance".

        The value after `__add__` is also incorrect

        >>> Query("foo") + Query("bar")
        ... 'foo site:calpoly.edubar site:calpoly.edu'

        I would expect something like

        >>> Query("foo") + Query("bar")
        ... 'foobar site:calpoly.edu'

        That's how `Question` works

        >>> Question("foo") + Question("bar")
        ... 'foobar'

        However, this is weird...what does it mean to concatenate two Questions anyway?

        >>> Question("foo?") + Question("bar?")
        ... 'foo?bar?'

        Should it be like this?

        >>> q1 = Question("what's the meaning of life?")
        >>> q2 = Question("what color is the sky?")
        >>> q1 + q2
        ... "what's the meaning of life AND what color is the sky?"

        At this point, the Liskov Substitution Principle makes more sense:

        > [functions that use references to base class objects
        > must be able to use objects of derived classes without
        > knowing it.][ariel_ortiz_LSP_quote]

        In other words,

        > [If it looks like a duck,
        > quacks like a duck,
        > but walks on wheels,
        > you most definitely have
        > the wrong abstraction.][ariel_ortiz_duck_quote]

        So, `Query` is a duck (`str`) that walks on wheels (`site: calpoly.edu`)

        It's pretty much crying out to be composed from an internal string.

        And the [python dunder methods][dunder_methods] can be used when needed,
            rather than behaving as it would on `str`.

        And I'll miss having direct access to the methods under `str.`

        However, those can still be used after extracting the internal string
            of a Query class which is designed with composition instead of inheritance.

        >>> str.
        ... str.capitalize(   str.format(       str.islower(
        ... str.lower(        str.rjust(        str.swapcase(
        ... str.casefold(     str.format_map(   str.isnumeric(
        ... str.lstrip(       str.rpartition(   str.title(
        ... str.center(       str.index(        str.isprintable(
        ... str.maketrans(    str.rsplit(       str.translate(
        ... str.count(        str.isalnum(      str.isspace(
        ... str.mro(          str.rstrip(       str.upper(
        ... str.encode(       str.isalpha(      str.istitle(
        ... str.partition(    str.split(        str.zfill(
        ... str.endswith(     str.isdecimal(    str.isupper(
        ... str.replace(      str.splitlines(
        ... str.expandtabs(   str.isdigit(      str.join(
        ... str.rfind(        str.startswith(
        ... str.find(         str.isidentifier( str.ljust(
        ... str.rindex(       str.strip(
        >>> Query.
        ... Query.capitalize(   Query.format_map(   Query.isprintable(
        ... Query.mro(          Query.split(
        ... Query.casefold(     Query.index(        Query.isspace(
        ... Query.partition(    Query.splitlines(
        ... Query.center(       Query.isalnum(      Query.istitle(
        ... Query.replace(      Query.startswith(
        ... Query.count(        Query.isalpha(      Query.isupper(
        ... Query.rfind(        Query.strip(
        ... Query.encode(       Query.isdecimal(    Query.join(
        ... Query.rindex(       Query.swapcase(
        ... Query.endswith(     Query.isdigit(      Query.ljust(
        ... Query.rjust(        Query.title(
        ... Query.expandtabs(   Query.isidentifier( Query.lower(
        ... Query.rpartition(   Query.translate(
        ... Query.find(         Query.islower(      Query.lstrip(
        ... Query.rsplit(       Query.upper(
        ... Query.format(       Query.isnumeric(    Query.maketrans(
        ... Query.rstrip(       Query.zfill(


        **Lastly**

        This StackOverFlow answer says

        > [Inheriting built-in types is very seldom worth while.
        > You have to deal with several issues
        > and you don't really get much benefit.][stackoverflow_str_inherit_bad]


    Example:
        >>> from nimbus_transformer.question import Question
        >>> from nimbus_transformer.query import Query
        >>> question = Question("what is foaad khosmood's email?")
        >>> query = Query(question)
        >>> query
        ... "what is foaad khosmood's email? site:calpoly.edu"
        >>> query.question == question
        ... True
        >>> query.query_string == str(Query(question))
        ... True
        >>> query.query_string is str(query.query_string)
        ... True

    Resources:
        * Example Google Search:
            * http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu

        * More details about the dunder `__new__` method:
            * https://stackoverflow.com/q/2673651

        * GeeksForGeeks about the dunder `__new__` method:
            * https://www.geeksforgeeks.org/__new__-in-python/

        * Python.org reference on dunder `__new__` method:
            * https://docs.python.org/3/reference/datamodel.html#object.__new__

        * Python.org reference on dunder `__add__` method:
            * https://docs.python.org/3/reference/datamodel.html#object.__add__

        * Ariel Ortiz - The Perils of Inheritance: Why We Should Prefer Composition - PyCon 2019
            * https://youtu.be/YXiaWtc0cgE

    [dunder_add]: https://docs.python.org/3/reference/datamodel.html#object.__add__
    [ariel_ortiz_inheritance_talk]: https://youtu.be/YXiaWtc0cgE
    [ariel_ortiz_LSP_quote]: https://youtu.be/YXiaWtc0cgE?t=1795
    [ariel_ortiz_duck_quote]: https://youtu.be/YXiaWtc0cgE?t=1803
    [dunder_methods]: https://docs.python.org/3/reference/datamodel.html#special-method-names
    [stackoverflow_str_inherit_bad]: https://stackoverflow.com/a/2676367
    """

    def __init__(self, question: Question) -> None:
        print("init")
        # save for future reference
        self.question = question
        self.query_string = f"{question} site:calpoly.edu"
        self = self + self.query_string

    def __new__(cls: type, question: Question) -> object:
        """
        Describes how to create a new `Query` string object
            from a given `nimbus_transformer.question.Question`.

        Args:
            cls: (type(Query)) I'm not really sure but Python needs this.
                Unlike `self`, which is an object, `cls` is a type.
            question: A `nimbus_transformer.question.Question` string.

        Returns:
            A `Query` object.
        """
        print("cls:", cls)
        print("cls:", type(cls))

        # make a Google query with appropriate scope of domain name
        query = f"{question} site:calpoly.edu"

        # use the str.__new__() and rename object as Query
        obj = str.__new__(cls, query)

        # save for future reference
        obj.question = question
        obj.query_string = query

        return obj

    def __repr__(self) -> str:
        return f"Query( query_string = '{self.query_string}' )"
