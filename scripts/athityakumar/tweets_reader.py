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
import tweets_database as td

def database_login() :
  return MySQLdb.connect(td.host(),td.user(),td.password(),td.database()) 
  
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
