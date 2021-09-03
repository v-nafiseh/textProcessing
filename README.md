### text processing on imdb top 250 movies

#### quik overview:
- extracting keywords from storylines
- maintaining a weighted graph between movies in which the movies' names are nodes & links are common keywords
- saving graph details as csv file

#### details:
- scraping the storyline with beautiful soup library and regex
- using textRank algorithm for extracting the keywords
- tokenizing, deleting stopwords, lemmatizing
- producing the weighted graph
- ploting the graph with networkx library



