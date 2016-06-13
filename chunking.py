__author__ = 'joswin'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk
from tagging_methods import get_postag_listinput

class Chunker(object):
    '''
    '''
    def __init__(self):
        '''
        :return:
        '''
        pass

    def ne_chunk_textinput(self,text):
        '''
        :param text:
        :return:
        '''
        tagged_sent = nltk.pos_tag(nltk.word_tokenize(text))
        tagged_sent_new=nltk.ne_chunk(tagged_sent)
        return tagged_sent_new

    def ne_chunk_listinput(self,text_list):
        '''
        :param text_list: [sent1,sent2,..]
        :return:
        '''
        tag_list = get_postag_listinput(text_list)
        chunked_list = [nltk.ne_chunk(sent) for sent in tag_list]
        return chunked_list




