#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 00:00:22 2019

@author: vasudharengarajan
"""

#from grammarbot import GrammarBotClient
from spacy.lang.en import English
from collections import OrderedDict

#from urlparse import urljoin
from urllib.parse import urljoin

import requests


class GrammarBotClient:
    """
    A GrammarBot-API wrapper client.
    """

    def __init__(self, base_uri='http://api.grammarbot.io/', api_key='python-default'):
        self._api_key = api_key
        self._base_uri = base_uri
        self._endpoint = urljoin(base_uri, '/v2/check')

    def check(self, text, lang='en-US'):
        """
        Check a given piece of text for grammatical errors.

        :param text:
            Text to be checked using the API.
        :param lang:
            Language code for the text language.
        """
        params = {
            'language': lang,
            'text': text,
            'api_key': self._api_key
        }
        res = requests.get(self._endpoint, params=params)
        json = res.json()
        return GrammarBotApiResponse(json)

    def __repr__(self):
        return 'GrammarBotClient(base_uri={}, api_key={})'.format(
            self._base_uri, self._api_key)


class GrammarBotMatch:
    """
    Represents a GrammarBot match detected by the API.
    """

    def __init__(self, match_json):
        self._match_json = match_json

    @property
    def message(self):
        """
        Returns the message for the given match.
        """
        return self._match_json["message"]

    @property
    def category(self):
        """
        Gives the rule category.
        """
        return self._match_json["rule"]["category"]["id"]

    @property
    def replacement_offset(self):
        """
        Gives the offset at which the replacement should be made.
        """
        return self._match_json["offset"]

    @property
    def replacement_length(self):
        """
        Gives the length of the string that has to be replaced.
        """
        return self._match_json["length"]

    @property
    def replacements(self):
        """
        Gives a list of possible replacements.
        """
        return [mjson["value"] for mjson in self._match_json["replacements"]]

    @property
    def corrections(self):
        """
        Gives a list of possibly correct variation of the input text.
        """
        sentence = self._match_json["sentence"]
        left = sentence[:self.replacement_offset]
        right = sentence[self.replacement_offset + self.replacement_length:]
        return [
            '{left}{replacement}{right}'.format(
                left=left, replacement=replacement, right=right)
                for replacement in self.replacements
        ]

    @property
    def rule(self):
        """
        Gives the rule ID which applies for this match.
        """
        return self._match_json["rule"]["id"]

    @property
    def type(self):
        """
        Gives the type of match.
        """
        return self._match_json["type"]["typeName"]

    def __repr__(self):
        return (
            'GrammarBotMatch(offset={offset}, length={length}, rule={rule}, '
            'category={category})'
        ).format(
            offset=self.replacement_offset,
            length=self.replacement_length,
            rule={self.rule},
            category={self.category}
        )


class GrammarBotApiResponse:
    """
    Represents the JSON API returned by the server.
    """

    def __init__(self, json):
        self._json = json

    @property
    def raw_json(self):
        """
        Returns the raw JSON response that was returned by the server.
        """
        return self._json

    @property
    def detected_language(self):
        """
        Gives the language code for the detected langauge.
        """
        return self._json["language"]["detectedLanguage"]["code"]

    @property
    def result_is_incomplete(self):
        """
        States whether these results are complete or incomplete.
        """
        return self._json["warnings"]["incompleteResults"]

    @property
    def matches(self):
        """
        Different matches detected by the GrammarBot API.
        """
        return [GrammarBotMatch(mjson) for mjson in self._json["matches"]]

    def __repr__(self):
        return 'GrammarBotApiResponse(matches={})'.format(self.matches)


class ValidityChecker:
    def __init__(self):
        self.nlp = English()
        self.nlp.add_pipe(self.nlp.create_pipe('sentencizer'))
        self.client = GrammarBotClient()

    def len_corrections(self, corrections):
        for k, vs in corrections.items():
            if len(vs) > 0:
                return 1
        return 0
            
    def corrections(self, text):
        doc = self.nlp(text)
        self.sentences = [sent.string.strip() for sent in doc.sents]
        sentence_corrections_dict = OrderedDict()
        
        for sentence in self.sentences:
            self.res = self.client.check(sentence)
            list_of_corrections = [match.message for match in self.res.matches]
            sentence_corrections_dict[sentence] = list_of_corrections
            
        return sentence_corrections_dict
    
text1 = "Yur Thanksgiving dinner was delicious. Thank you soo much, and hope too join you next year!"
text2 = "I cant remember how to go their."
# checker = ValidityChecker()
# print(checker.corrections(text=text1))
# print(checker.corrections(text=text2))
