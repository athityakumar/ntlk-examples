#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'joswin'

import nltk

class Grammar(object):
    '''
    '''
    def __init__(self):
        '''
        :return:
        '''
        self.grammar = r"""
	NP: {<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
	PP: {<IN><NP>}               # Chunk prepositions followed by NP
	VP: {<VB.*><NP|PP>+} # Chunk verbs and their arguments
	CLAUSE: {<NP><VP>}           # Chunk NP, VP
  	"""

    def parse_regex_grammar_textinput(self,chunked_sent,grammar=None,loop=1):
        '''
        :param chunked_sent: output of nltk.ne_chunk
        :return:
        '''
        if not grammar:
            grammar = self.grammar
        cp = nltk.RegexpParser(grammar,loop=loop)
        result = cp.parse(chunked_sent)
        return result

    def parse_regex_grammar_listinput(self,chunks_list,grammar=None,loop=1):
        '''
        :param chunks_list:
        :param grammar:
        :return:
        '''
        result = []
        for chunk in chunks_list:
            result.append(self.parse_regex_grammar_textinput(chunk,grammar,loop))
        return result
