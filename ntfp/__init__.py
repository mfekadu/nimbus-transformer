"""it's like [Nimbus][1] but uses [a transformer language model][2]

Implemented in a [functional programming style][4]

[//]: # (markdown comment # noqa)

Resources:
    * [import typing][python3_typing]
    * [import functools][python3_functools]
    * [Functional Design Patterns - Scott Wlaschin][wlaschin_talk]
    * ["Types are not classes... they're sort of like Sets"][wlaschin_talk_types]
    * [Why Isn't Functional Programming the Norm? – Richard Feldman][richard_feldman_talk]
    * ["NewType declares one type to be a _subtype_ of another"][new_type]
        * _subtype_ means the same thing as _subclass_ in this context
    * [__pdoc__override]
    * [pyre-check error suppression][5]
    * [mypy type hints cheat sheet][6]
    * [Carl Meyer - Type-checked Python in the real world - PyCon 2018][carl_myer_pycon2018]

[1]: http://github.com/calpoly-csai/api
[2]: https://github.com/huggingface/transformers
[3]: http://github.com/mfekadu/nimbus-transformer

[4]: https://realpython.com/courses/functional-programming-python/

[5]: https://pyre-check.org/docs/error-suppression.html

[6]: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

[carl_myer_pycon2018]: https://youtu.be/pMgmKJyWKn8

[python3_typing]: https://docs.python.org/3/library/typing.html
[python3_functools]: https://docs.python.org/3/library/functools.html

[wlaschin_talk]: https://youtu.be/ucnWLfBA1dc
[wlaschin_talk_types]: https://youtu.be/ucnWLfBA1dc?t=685

[richard_feldman_talk]: https://youtu.be/QyJZzq0v7Z4

[new_type]: https://docs.python.org/3/library/typing.html#newtype

[__pdoc__override]: https://pdoc3.github.io/pdoc/doc/pdoc/#overriding-docstrings-with-__pdoc__
"""
