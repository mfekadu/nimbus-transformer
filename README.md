# nimbus-transformer
it's like Nimbus but uses a transformer language model

## A Simple Program

**Assumptions**
* Limited to Cal Poly

**Definitions**
* _User_: anyone with access to the internet.
* `Question`: a sentence that elicits information about Cal Poly staff/clubs/etc. 
  * e.g. `"What is Foaad Khosmood's email?"`
  * e.g. `"What is Foaad's office?"`
  * e.g. `"What courses does Foaad Khosmood teach this quarter?"`
* `Query`: a string of text to pass into Google search
  * `{Question}` or 
  * `{Question} site:calpoly.edu`
* `Result`: the Google html page for a given `Query`
  * e.g. [this page][4]
* `Context`: the text content of the first 10 **URLs** in `Result`
* `SimpleContext`: the text content of the first 10 **html sections** in `Result`
* `Answer`: an appropriate response to a given `Question`
* `Transformer`/`Transform`: a function that uses one of the fancy langauge models provided in [huggingface/transformers][2]

**Pipeline**
1. _User_ asks `Question` to a web application.
2. Scrape google for `Context` limit 10 url results.
3. Store `Context` into database.
4. Transform ( `Question`, `Context` ) >> `Answer`
5. Reply with `Answer`
6. Mark, good/bad answer _to learn from later_.


## Resources
* [**huggingface/transformers**][2]
* [**explosion/spaCy**][3]
* **Technical Talk:** [Using spaCy with Bert | Hugging Face Transformers | Matthew Honnibal][1]

[1]: https://www.youtube.com/watch?v=RB9uDpJPZdc
[2]: https://github.com/huggingface/transformers
[3]: https://github.com/explosion/spaCy
[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
