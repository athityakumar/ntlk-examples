__author__ = 'joswin'

import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:postgres@localhost:5432/linkedin_data')

tmp = pd.read_sql('linkedin_company_base_settu_sir',engine)
text_list = list(tmp['description'])
del tmp

from text_processing import word_transformations
tk = word_transformations.Tokenizer()

text_list_lemma = tk.wordnet_lemma_listinput(text_list) # sometimes

from text_processing import extract_phrases
phr = extract_phrases.PhraseExtractor()

grammar = r"""
    NP: {<RB.*>*<DT|JJ|NN.*>+}          # Chunk sequences of DT, JJ, NN
    PP: {<IN><NP>}               # Chunk prepositions followed by NP
    VP: {<RB.*>*<VB.*><NP|PP>+} # Chunk verbs and their arguments
    CLAUSE: {<NP><VP>}           # Chunk NP, VP
    """
from text_processing import chunking
ch = chunking.Chunker()
chunk_list = ch.ne_chunk_listinput(text_list)

from text_processing import grammar
gm = grammar.Grammar()
grammar_list = gm.parse_regex_grammar_listinput(chunk_list)

from text_processing import extract_phrases
pe = extract_phrases.PhraseExtractor()
phr_list = pe.extract_phrase_treelistinput(grammar_list,['NP','PP','VP','CLAUSE'])

phr_list_all = [j for i in phr_list for j in i]
phr_list_all = list(set(phr_list_all))

pm = extract_phrases.PhraseMerger()

text_phrases = pm.merge_phrases_listinput(text_list,phr_list_all,keep_original=True)
