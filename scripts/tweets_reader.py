__author__ = 'athityakumar'
#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import numpy as np
import MySQLdb
import string
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF

def database_login() :
  return MySQLdb.connect(host="localhost",user="root",passwd="password",db="database") 
  
def database_read(table_name) :
  cur = database_login().cursor()
  cur.execute("SELECT * FROM "+table_name)
  return cur.fetchall()

def database_end() :
  database_login().close()

def remove_link(tweet) :
  while tweet.find("https://t.co/") != -1 :
    link = tweet[tweet.find("https://t.co/"):tweet.find("https://t.co/")+23]
    tweet = string.replace(tweet,link,"")
  return tweet
 
# print all the first cell of all the rows
def get_all_tweets() :
  tweets = {}
  for row in database_read("twitter_tweets"):
      hashtag =  row[2]
      mention = row[10]
      raw_tweet = row[1]
      clean_tweet = raw_tweet
      if hashtag != None :
          clean_tweet = string.replace(clean_tweet,hashtag,"")
          clean_tweet = string.replace(clean_tweet,"#","")
      if mention != None :
          clean_tweet = string.replace(clean_tweet,mention,"")
          clean_tweet = string.replace(clean_tweet,"@","")
      
      clean_tweet = remove_link(clean_tweet)
      id = row[0]
      tweets[id] = { "clean_tweet": clean_tweet , "hashtag": hashtag , "mention" : mention }
  database_end()
  return tweets

def clean(model,index) :
  index = index + 1
  dirty = ["+",".","*"]
  while model.find("0.") != -1 :
    prob = model[model.find("0."):model.find("0.")+6]
    model = string.replace(model,prob,"")
  for element in dirty :    
    model = string.replace(model,element,"")
  model = "Topic #"+str(index)+": "+model
  return model

all_tweets = get_all_tweets()  
doc_set = []
count = 0
for index in all_tweets :
  doc_set.append(all_tweets[index]["clean_tweet"])
  count = count + 1

tokenizer = RegexpTokenizer(r'\w+')
en_stop = get_stop_words('en')
en_stop.extend(["s","t","rs","http","amp","rt","https","0","1","2","3","4","5","6","7","8","9"])
p_stemmer = PorterStemmer()  
texts = []

# loop through document list
for i in doc_set:
    
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i.lower() in en_stop]
    
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

#generate LDA model
num_topics = 20
num_words = 10
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word = dictionary)

i = 0
while i < num_topics:
  print(clean(ldamodel.print_topics(num_topics=num_topics,num_words=num_words)[i][1],i))
  i = i+1
