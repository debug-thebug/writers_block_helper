#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:27:54 2019

@author: vasudharengarajan
"""
from nltk.wsd import lesk
import nltk
from thesaurus import Word
from nltk.corpus import wordnet
from pattern.en import pluralize, singularize, comparative, superlative, conjugate, PAST


acceptable_pos = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'NN', 'NNS', 'JJ', 'JJR', 'JJS']
pos_dict_thesaurus = {'VB': 'verb', 
            'VBD': 'verb', 
            'VBG': 'verb', 
            'VBN': 'verb',  
            'VBP': 'verb',  
            'VBZ': 'verb',
            'NN': 'noun', 
            'NNS': 'noun',  
            'JJ': 'adj', 
            'JJR': 'adj',  
            'JJS': 'adj'}

pos_dict = {'VB': wordnet.VERB, 
            'VBD': wordnet.VERB,
            'VBG': wordnet.VERB,
            'VBN': wordnet.VERB,  
            'VBP': wordnet.VERB, 
            'VBZ': wordnet.VERB,
            'NN': wordnet.NOUN, 
            'NNS': wordnet.NOUN,  
            'JJ': wordnet.ADJ, 
            'JJR': wordnet.ADJ, 
            'JJS': wordnet.ADJ}

class SynonymGenerator:
    def __init__(self, text):
        self.text = text
        self.tokenized_text = nltk.word_tokenize(self.text)
    
    def get_important_words(self):
        tagged = nltk.pos_tag(self.tokenized_text)
        word_to_pos = {}
        for tup in tagged:
            if tup[1] in acceptable_pos:
                word_to_pos[tup[0]] = tup[1]
        return word_to_pos
    
#    def choose_best_few(self, word, pos, syns):
#        flat_list = [item for sublist in syns for item in sublist]
#        
#        print(flat_list)
#        if len(flat_list) == 0:
#            return []
#        
#        to_return = []
#        for word2 in flat_list:
#            orig = wordnet.synsets(word, pos=pos)
#            syn = wordnet.synsets(word, pos=pos)
#            if orig and syn: #Thanks to @alexis' note
#               s = orig[0].wup_similarity(syn[0])
#                to_return.append(s)
#
#        print(max(to_return))
        
    
    #def change_lemma_to_pos(self, lemma):

#    def get_word_to_synonyms_dict(self): 
#        word_to_syns_dict = {}
#        word_to_pos = self.get_important_words()    
#        for w in self.tokenized_text:
#            if w in word_to_pos:
#                original_synset = lesk(self.text, w)
#                if original_synset: 
#                    for l in original_synset.lemmas():
#                        if l.name() != w:
#                            #print(w, " -> ", l)
#                            candidate_synsets = wordnet.synsets(l.name(), pos=pos_dict[word_to_pos[w]])
#                            #print("ORIGINAL SYNSET: ", original_synset)
#                            #print("CANDIDATE SYNSETS: ", candidate_synsets)
#                            if len(candidate_synsets) > 0:
#                                #newlist = sorted(candidate_synsets, key=lambda x: original_synset.wup_similarity(x))
#                                minSim = max([original_synset.wup_similarity(x) for x in candidate_synsets])
#                                #print(w, l.name(), minSim)
#
#                                if w in word_to_syns_dict:
#                                    word_to_syns_dict[w].append((l.name(), minSim))
#                                else:
#                                    word_to_syns_dict[w] = [(l.name(), minSim)]
#        return word_to_syns_dict
                                        
                                    
    def get_word_to_synonyms_dict(self, n):
        word_to_syns_dict = {}
        word_to_pos = self.get_important_words()    
        
        for w in self.tokenized_text:
            
            if w in word_to_pos:
                list_of_syns_for_w = []
                original_synset = lesk(self.text, w)
                word = Word(w)
                p_o_s = pos_dict_thesaurus[word_to_pos[w]]
                #print(w, word_to_pos[w], p_o_s)
                syns = word.synonyms('all', partOfSpeech=p_o_s)
                flat_list = [item for sublist in syns for item in sublist]
                for candidate_syn in flat_list:
                    candidate_synsets = wordnet.synsets(candidate_syn, pos=pos_dict[word_to_pos[w]])
                    #print(candidate_syn, ":", candidate_synsets)
                    #print(candidate_syn)
                    if len(candidate_synsets) > 0:
                        list_sims = [original_synset.wup_similarity(x) for x in candidate_synsets if original_synset.wup_similarity(x)]
                        if len(list_sims) > 0:
                            maxSim = max(list_sims)
                            list_of_syns_for_w.append((candidate_syn, maxSim))
                if list_of_syns_for_w:
                    list_of_syns_for_w.sort(key=lambda x: x[1], reverse=True)
                    n_truncate = n if n <= len(list_of_syns_for_w) else len(list_of_syns_for_w)
                    word_to_syns_dict[(w, word_to_pos[w])] = list_of_syns_for_w[:n_truncate]
        return word_to_syns_dict
    
    def get_tense_plurality_dict(self, n):
        correct_tense_number_dict = {}
        wordpos_to_syns_dict = self.get_word_to_synonyms_dict(n)
        #print(wordpos_to_syns_dict)
        #print()
        for (word, pos), list_syns in wordpos_to_syns_dict.items():
            #print(word, pos, list_syns)
            #if pos == 'VB':
            if pos == 'VBD':
                correct_tense_number_dict[word] = [conjugate(tup[0], tense=PAST) for tup in list_syns]
            #if pos == 'VBG':
            #if pos == 'VBN':
            #if pos == 'VBP':
            #if pos == 'VBZ':
            #if pos == 'NN':
            #if pos == 'NNS':
            #if pos == 'JJ':
            #if pos == 'JJR':
            #    correct_tense_number_dict[word] = [comparative(tup[0]) for tup in list_syns]
            #if pos == 'JJS':
            #    correct_tense_number_dict[word] = [superlative(tup[0]) for tup in list_syns]
            else:
                correct_tense_number_dict[word] = [tup[0] for tup in list_syns]
        return correct_tense_number_dict
    
    def get_sentence(self, n):
        alternate_sentences = []
        d = self.get_tense_plurality_dict(n)
    
        for i in range(n-1, 0, -1):
            alternate_sentence = self.text
            for key in d:
                i_new = i if i <= len(d[key]) else len(d[key])
                alternate_sentence = alternate_sentence.replace(key, d[key][i_new])
            alternate_sentences.append(alternate_sentence)
        return alternate_sentences
            

text1 = "Your Thanksgiving dinner tasted delicious. Thank you so much, and I hope to come again next year!"
text2 = "I can't remember how to go there."
synonym_gen = SynonymGenerator(text1)
print(synonym_gen.get_sentence(3))


#w = Word('tasted')
#syns = w.synonyms('all', partOfSpeech='verb')
#print(syns)