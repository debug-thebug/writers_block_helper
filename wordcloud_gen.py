# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 09:31:48 2019

@author: Patrick Kwon
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud

text = open('sample_text.txt').read()

wordcloud = WordCloud(max_font_size=40).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

plt.savefig('sample_img.jpg', figsize=(200,100), dpi=100)