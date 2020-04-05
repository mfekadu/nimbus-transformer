"""it's like [Nimbus][1] but uses [a transformer language model][2]

[READ MORE ON GITHUB][3]

**Pipeline**

1. _User_ asks `nimbus_transformer.question.Question` to a web application.

2. Scrape Google for `Context` limit 10 url results.

3. Store `Context` into database.

4. Transform ( `nimbus_transformer.question.Question`, `Context` ) >> `Answer`

5. Reply with `Answer`

6. Mark, good/bad answer _to learn from later_.

[1]: http://github.com/calpoly-csai/api
[2]: https://github.com/huggingface/transformers
[3]: http://github.com/mfekadu/nimbus-transformer
"""
