from networkx.generators import directed
from nltk.stem import WordNetLemmatizer 
from nltk import pos_tag
import numpy as np
import math
from nltk.util import pr
from numpy.core.fromnumeric import partition
import pandas as pd
import requests
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import networkx as nx

#implementation of textRank
class TextRank:
    def __init__(self,stl):
        self.stl = stl
        pass

    def word_prepration(self):

        #case folding
        lower_text = self.stl.lower()
        
        #del numbers
        clear_text = re.sub("\d+","", lower_text)

        #tokenize words
        tokenized_words = word_tokenize(clear_text)

        #delete stop words
        stop_words = stopwords.words("english")
        non_stops = []
        for word in tokenized_words:
            if word not in stop_words:
                if word not in non_stops:
                    non_stops.append(word)

        wl = WordNetLemmatizer()
        # tags = {"adj":['JJ','JJR','JJS'], "noun":['NN', 'NNS']}
        taged_text = pos_tag(non_stops)
        lemmatized_words = []

        for word in taged_text:
            w = wl.lemmatize(word[0], pos="a")
            w = wl.lemmatize(w, pos="n")
            w = wl.lemmatize(w, pos="v")
            w = wl.lemmatize(w, pos="r")

            lemmatized_words.append(w)
        
        #create vocab
        vocab = list(set(lemmatized_words))
        return vocab



    def matrix_preration(self):

        vocabulary = self.word_prepration()
        vocab_len = len(vocabulary)

        weighted_edge = np.zeros((vocab_len,vocab_len),dtype=np.float32)

        score = np.zeros((vocab_len),dtype=np.float32)
        window_size = 3
        covered_occurrences = []

        for i in range(0,vocab_len):
            score[i]=1
            for j in range(0,vocab_len):
                if j==i:
                    weighted_edge[i][j]=0
                else:
                    for window_start in range(0,(len(vocabulary)-window_size+1)):
                        
                        window_end = window_start+window_size
                        
                        window = vocabulary[window_start:window_end]
                        
                        if (vocabulary[i] in window) and (vocabulary[j] in window):
                            
                            index_of_i = window_start + window.index(vocabulary[i])
                            index_of_j = window_start + window.index(vocabulary[j])
                            
                            if [index_of_i,index_of_j] not in covered_occurrences:
                                weighted_edge[i][j] += 1
                                covered_occurrences.append([index_of_i,index_of_j])
        return weighted_edge,score,vocabulary



    def score_provider(self):

        weighted_edge,score,vocabulary = self.matrix_preration()
        vocab_len = len(vocabulary)

        inout = np.zeros((vocab_len),dtype=np.float32)

        for i in range(0,vocab_len):
            for j in range(0,vocab_len):
                inout[i]+=weighted_edge[i][j]

        dictionary={}

        MAX_ITERATIONS = 50
        d=0.85
        threshold = 0.0001 #convergence threshold

        for iter in range(0,MAX_ITERATIONS):
            prev_score = np.copy(score)
            
            for i in range(0,vocab_len):
                
                summation = 0
                for j in range(0,vocab_len):
                    if weighted_edge[i][j] != 0:
                        summation += (weighted_edge[i][j]/inout[j])*score[j]
                        
                score[i] = (1-d) + d*(summation)
            
            if np.sum(np.fabs(prev_score-score)) <= threshold: #convergence condition
                # print("Converging at iteration "+str(iter)+"....")
                
                score = sorted(score)
                for i in range(0,vocab_len):
                    dictionary[vocabulary[i]] =score[i]
                
                dictionary = {k:v for k,v in sorted(dictionary.items(), key=lambda item: item[1],reverse=True)}
                import itertools
                
                i=0
                for keys,values in dictionary.items():
                    if(i<10):
                        # print("Score of "+keys+": "+str(values))
                        i+=1
                break
        return(list(dictionary.keys()))



url = "https://www.imdb.com/chart/top/"

#make beautifulsoup object
def r_soup(web_url):
    page = requests.get(web_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

# print(soup.prettify())
# print(type(soup))

results = r_soup(url).find_all("td", class_="titleColumn")

links = []
movie_story=[]
movie_keyword={}
new_url = re.sub("/chart/top/","",url)
for result in results:
    link = result.find("a").attrs.get('href')
    complete_link =  new_url + link
    links.append(complete_link)

# print(links) 

def story_line(web_url):
    for url in web_url:
        sub_page = r_soup(url)
        # story_line_txt =sub_page.find("div",id="titleStoryLine").find("div",class_=("inline canwrap")).find("span").text
        story_line_txt = sub_page.find("div", class_ = "Storyline__StorylineWrapper-sc-1b58ttw-0").find("div", class_ = "ipc-overflowText").find("div", class_ = "ipc-html-content").find("div").text
        # title= re.sub(r"[(\d)]","",sub_page.find("div",class_="title_wrapper").find("h1").text)
        t = re.sub(r"[(\d)]", "", sub_page.find("div", class_ = "TitleBlock__TitleContainer-sc-1nlhx7j-1").find("h1").text)
        movie_story.append(dict(title = re.sub("[\...]$","",t), stry=story_line_txt))
    # print(movie_story)
    return movie_story

mvst = story_line(links)
# print(mvst)

d = {} #keeps title and keywords of storyLine
all = [] #adjacency list for weight of each node
labeldict = {} #to be used in networkx for labeling the nodes

for index, movie in enumerate(movie_story):
   title = movie['title']
   labeldict[index]=title
   stry = movie['stry']
   tr = TextRank(stry)
   d[title] = tr.score_provider()

#check for common keywords
for k, v in d.items():
    w = []
    for kk, vv in d.items():
        inter = len(set(v).intersection(set(vv)))
        if k!=kk and inter:
            w.append(inter)
        else:
            w.append(0)

    all.append(w) 


arr = np.array(all) #convert list to numpy array
# print(arr)
# up = np.triu(arr, k=0)
# print(up)
#creating graph 
# G = nx.from_numpy_matrix(np.matrix(up), create_using=nx.DiGraph)
# layout = nx.spring_layout(G)
# nx.draw(G, layout, labels = labeldict, with_labels = True)
# nx.draw_networkx_edge_labels(G, pos=layout)
# #write graph to csv file 
# nx.write_edgelist(G, "edge.csv")
# plt.show()

G = nx.from_numpy_matrix(np.matrix(arr), create_using=nx.Graph)

layout = nx.spring_layout(G)
nx.draw(G, layout, labels = labeldict, with_labels = True)
nx.draw_networkx_edge_labels(G, pos=layout)
#write graph to csv file 
nx.write_edgelist(G, "edge.csv")
plt.show()

