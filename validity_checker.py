#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 00:00:22 2019

@author: vasudharengarajan
"""

from grammarbot import GrammarBotClient
from spacy.lang.en import English
from collections import OrderedDict


class ValidityChecker:
    def __init__(self, text):
        nlp = English()
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        self.client = GrammarBotClient()
        doc = nlp(text)
        self.sentences = [sent.string.strip() for sent in doc.sents]
            
    def corrections(self):
        sentence_corrections_dict = OrderedDict()
        
        for sentence in self.sentences:
            self.res = self.client.check(sentence)
            list_of_corrections = [match.message for match in self.res.matches]
            sentence_corrections_dict[sentence] = list_of_corrections
            
        return sentence_corrections_dict
    
text1 = "Yur Thanksgiving dinner was delicious. Thank you soo much, and hope too join you next year!"
text2 = "I cant remember how to go their."
checker = ValidityChecker(text2)
print(checker.corrections())
