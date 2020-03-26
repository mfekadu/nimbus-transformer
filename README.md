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
* `ResultURLs`: the first 10 **URLs** in `Result`
* `Context`: one large text document containing the text content of each url in `ResultURLs`
* `SimpleContext`: one large text document containing the text content of the first 10 **html sections** in `Result`
* `Transformer`/`Transform`: a function that uses one of the fancy langauge models provided in [huggingface/transformers][2]
* `Answer`: a segment text found within the given `Context` that appropriately answers the given `Question`.

**Pipeline**
1. _User_ asks `Question` to a web application.
2. Scrape Google for `Context` limit 10 url results.
3. Store `Context` into database.
4. Transform ( `Question`, `Context` ) >> `Answer`
5. Reply with `Answer`
6. Mark, good/bad answer _to learn from later_.


## TODO
- [ ] a simple web UI with an input box and a section for answers
- [ ] database code for 
  * INSERT `Context`/`Question`/`Answer`/_timestamp_/_good-bad-answer_
  * UPDATE _good-bad-answer_

**Proof of Concept (MVP)**

- [ ] write function `makeQuery( q : Question ) -> Query`
 * given a `Question`, returns a formatted `Query` that conforms to the limitations/assumptions of this program (if need be)

- [ ] write function `getGoogleResult( q : Query ) -> Result`
  * given a `Query`, returns the `Result` as defined above
  * [pip install beautifulsoup4][8]
```python
>>> import googlesearch
>>> from bs4 import BeautifulSoup
>>> 
>>> url_sanitze = lambda q: googlesearch.quote_plus(f"{q}")
>>> base_url = "https://www.google.com/search?q="
>>> query = "what is foaad khosmood's email? site:calpoly.edu"
>>> URL = f"{base_url}{html_sanitize(query)}"
>>> URL
'https://www.google.com/search?q=what+is+foaad+khosmood%27s+email%3F+site%3Acalpoly.edu'
>>> html_page = googlesearch.get_page(URL)
>>> soup = BeautifulSoup(html_page)
>>> print(soup.text)
```

- [ ] write function `getGoogleResultURLs( q : Query ) -> ResultURLs`
  * given a `Query`, returns the `Result` as defined above
  * [`pip install google`][7]
```python
>>> from googlesearch import search
>>> query = "what is foaad khosmood's email? site:calpoly.edu"
>>> for x in search(query, num=10, stop=10):
...     print(x)
...
https://cpe.calpoly.edu/faculty/foaad/
http://users.csc.calpoly.edu/~dekhtyar/466-Spring2012/
https://iatpp.calpoly.edu/organization
https://cpe.calpoly.edu/faculty/
https://lib.calpoly.edu/events/my-tech-journey/
https://lib.calpoly.edu/events/gerrymandering-in-america/
https://www.calpoly.edu/news
https://digitalcommons.calpoly.edu/theses/1623/
https://www.calpoly.edu/news/category/california-impact
https://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=2820&context=theses
```

- [ ] write function `getGoogleContext( urls : ResultURLs ) -> Context`
  * given a `ResultURLs`, returns the `Context` as defined above
  * [pip install beautifulsoup4][8]
```
>>> from bs4 import BeautifulSoup
>>> 
>>> soups = [BeautifulSoup(url) for url in urls]
>>> texts = [s.text for s in soups]
>>> document = "\n\n".join(texts)
```

- [ ] write function `getSimpleGoogleContext( r : Result ) -> SimpleContext`
  * given a `Result`, returns the `SimpleContext` as defined above
  * [`pip install google`][7]
```
>>> import googlesearch
>>> from bs4 import BeautifulSoup
>>> 
>>> # TODO: some fancy bs4 magic to extract the html sections for each result
```

- [ ] write function `transform( question: str, context: str  ) -> Answer`
  * given a `Question` _string_ and a `Context` _string_, returns the `Answer` _string_ as defined above.
  * [`pip install transformers`][2]
  * [pip install spacy][3]
  * see [huggingface/transformers#quick-tour-of-pipelines][9]
```python
from transformers import pipeline

# Allocate a pipeline for sentiment-analysis
nlp = pipeline('sentiment-analysis')
nlp('We are very happy to include pipeline into the transformers repository.')
>>> {'label': 'POSITIVE', 'score': 0.99893874}

# Allocate a pipeline for question-answering
nlp = pipeline('question-answering')
nlp({
    'question': 'What is the name of the repository ?',
    'context': 'Pipeline have been included in the huggingface/transformers repository'
})
>>> {'score': 0.28756016668193496, 'start': 35, 'end': 59, 'answer': 'huggingface/transformers'}
```


## Resources
* [**huggingface/transformers**][2]
* [**explosion/spaCy**][3]
* **Technical Talk:** [Using spaCy with Bert | Hugging Face Transformers | Matthew Honnibal][1]
* [example google search][4]
* [`pip install google` source code][7]
* [`pip install google` tutorial][5]
  * read this in more depth for alternative google search api options
* [`pip install google` geeksforgeeks][6]
* [`pip install beautifulsoup4`][8]

[1]: https://www.youtube.com/watch?v=RB9uDpJPZdc
[2]: https://github.com/huggingface/transformers
[3]: https://github.com/explosion/spaCy
[4]: http://google.com/search?q=what+is+foaad+email?+site:calpoly.edu
[5]: https://towardsdatascience.com/current-google-search-packages-using-python-3-7-a-simple-tutorial-3606e459e0d4
[6]: https://www.geeksforgeeks.org/performing-google-search-using-python-code/
[7]: https://github.com/MarioVilas/googlesearch
[8]: https://pypi.org/project/beautifulsoup4/
[9]: https://github.com/huggingface/transformers#quick-tour-of-pipelines
