# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:31:48 2019

@author: Patrick Kwon
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud


class WordCloudGenerator:
    def __init__(self):
        self.wordcloud = WordCloud(max_font_size=40)
        
    def generate_wc(self, text, fname):
        self.wordcloud.generate(text)
        plt.figure()
        plt.imshow(self.wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(fname, figsize=(200,100), dpi=100)
        
# text1 = "Your Thanksgiving dinner tasted delicious. Thank you so much, and I hope to come again next year!"
# wC = WordCloudGenerator()
# wC.generate_wc(text=text1, fname='save_fig.jpg')
