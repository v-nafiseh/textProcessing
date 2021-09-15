teamwork with ![Shokoofa Ghods](https://github.com/shokoofa-ghods)
### text processing on imdb top 250 movies

#### quick overview
- extracting keywords from storylines
- maintaining a weighted graph between movies in which the movies' names are nodes & links are common keywords
- saving graph details as csv file

#### details
- scraping the storyline with beautiful soup library and regex
- using textRank algorithm for extracting the keywords
- tokenizing, deleting stopwords, lemmatizing
- producing the weighted graph
- ploting the graph with networkx library

![Alt text](https://github.com/v-nafiseh/textProcessing/blob/main/Figure_1.png?raw=true "Title")

### scraping digikala speciall offer products

#### quick overview
- crawling special offers page
- extracting name, price and sale's amount of product
- showing the results in a web page using django framework

#### details
- scraping with BeautifulSoup library
- using regex for extracting exact details
- saving files into json and csv format
- using django fixtures for populating database with the data derived from previous steps




