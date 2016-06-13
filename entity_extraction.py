
# from corenlp import StanfordCoreNLP
import nltk
from nltk.tag.stanford import StanfordNERTagger

def sent_tokenize_withnewline(text):
    '''default tokenizer do not consider new line as sentence delimiter.
     In our case, it makes sense to do so. '''
    sentences = [] 
    for para in text.split('\n'): 
        sentences.extend(nltk.sent_tokenize(para))
    return sentences 

class StanfordNERTaggerExtractor(object):
    """docstring for ClassName"""
    def __init__(self):
        self.st = StanfordNERTagger('intent_class_models/stanford-jars/english.all.3class.distsim.crf.ser.gz' ,
            "intent_class_models/stanford-jars/stanford-ner.jar" )
        # self.st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz' ,
        #     'stanford-ner.jar' )

    def tag_text_single(self,text):
        '''
        :param text:
        :return:
        '''
        # assert type(text) == str
        sents = self.st.tag(nltk.word_tokenize(text))
        return sents

    def identify_NER_tags_single(self,text_tag,tag_to_find):
        '''
        :param text_tag: Tagged text
        :param tag_to_find:
        :return:
        '''
        tag_strs = []
        prev_wrd_tag = False
        for wrd,tag in text_tag:
            if tag == tag_to_find:
                if not prev_wrd_tag:
                    tag_strs.append(wrd)
                else:
                    prev_wrd = tag_strs.pop()
                    new_wrd = prev_wrd+' '+wrd
                    tag_strs.append(new_wrd)
                prev_wrd_tag = True
            else:
                prev_wrd_tag = False
        tags_final = []
        for wrd in tag_strs:
            if wrd not in tags_final:
                tags_final.append(wrd)
        return tags_final

    def tag_text_multi(self,text):
        ''' '''
        tokenized_sents = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text)]
        return self.st.tag_sents(tokenized_sents)

    def identify_NER_tags_multi(self,text_tag,tag_to_find):
        ''' '''
        tag_strs = []
        for sent_tag in text_tag:
            for wrd in self.identify_NER_tags_single(sent_tag,tag_to_find):
                if wrd not in tag_strs:
                    tag_strs.append(wrd)
        return tag_strs

    def tag_text_multi_from_single(self,ner_tags):
        ''' converting a huge single text tags into sentence based tags
        this is done because tagging sentence wise is slow. so we tag the entire text
        and split them after'''
        sents = ''
        for wrd,_ in ner_tags:
            sents += wrd+' '
        sent_tags = [nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(sents)]
        cnt = 0
        final_tags = []
        for sent_ind in range(len(sent_tags)):
            sent_tag_list = []
            for wrd_ind in range(len(sent_tags[sent_ind])):
                try:
                    sent_tag_list.append(ner_tags[cnt])
                    cnt += 1
                except:
                    break
            final_tags.append(sent_tag_list)
        return final_tags

