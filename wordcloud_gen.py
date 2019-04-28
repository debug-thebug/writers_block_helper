# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:31:48 2019

@author: Patrick Kwon
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud


class WordCloudGenerator:
    def __init__(self, text):
        self.text = text
        
    def get_wc(self, name):
        wordcloud = WordCloud(max_font_size=40).generate(self.text)
        plt.figure()
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(name, figsize=(200,100), dpi=100)
        
text1 = "Your Thanksgiving dinner tasted delicious. Thank you so much, and I hope to come again next year!"
wC = WordCloudGenerator(text1)
print(wC.get_wc('save_fig.jpg'))
