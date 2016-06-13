__author__ = 'joswin'
#!/usr/bin/python
# -*- coding: utf-8 -*-

import nltk

def get_postag_listinput(text_list):
        '''
        This method tries to tag a list of sentences. Doing it separately is slow. So, here this method
        combines all the sentences, and tag them together, then split the sentences back.
        text_list is a list of sentences
        '''
        list_split_code = ' spl_cd_X3ffty. '
        pos_list_split = 'spl_cd_X3ffty'
        tmp = list_split_code.join(text_list)
        doc_tags = nltk.pos_tag(nltk.word_tokenize(tmp))
        out_list = []
        row_list = []
        prev_tag_splitcode = False
        for i in doc_tags:
            if i[0] == pos_list_split:
                out_list.append(row_list)
                row_list = []
                prev_tag_splitcode = True
            elif prev_tag_splitcode:
                prev_tag_splitcode = False
                continue
            else:
                row_list.append(i)
        out_list.append(row_list)
        out_list = out_list[:len(text_list)]
        return out_list

