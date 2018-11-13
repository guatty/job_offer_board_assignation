#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 18:13:26 2018

@author: geoffrey
"""

import pandas as pd # manipulation de csv

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

from nltk.corpus import stopwords  # text preproccess
import html2text


ENGLISH_STOPWORDS = set(stopwords.words("english"))
FRENCH_STOPWORDS = set(stopwords.words("french"))

MAX_NB_WORDS= 200000
#print(html2text.html2text(contenu_col))
#df = pd.read_csv('test_correl.csv', delimiter=',', encoding="utf-8-sig")

#a = df['number'].corr(df['number2'], method= 'spearman')

#=================================================================
# preprocess functions
#=================================================================


def preprocess(text):
    text = text.strip().lower().split()
    text = filter(lambda word: word not in ENGLISH_STOPWORDS, text)
    text = filter(lambda word: word not in FRENCH_STOPWORDS, text)
    return " ".join(text)
    

def clean_tab(tab):
    for i in range(len(tab)):
       tab[i] = preprocess(tab[i])
    return tab


def remove_html_pattern(column):
    without_html_tab = []
    for element in column:
        element_without_html = html2text.html2text(element)
        without_html_tab.append(element_without_html)
    return without_html_tab
        

def vectorize_column(data_column):
    tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
    tokenizer.fit_on_texts(data_column)
    vector_data = tokenizer.texts_to_sequences(data_column)
    return vector_data

def replace_text_by_vector(dataframe,column_to_remove,name_column_to_add,column_to_add):
    del dataframe[column_to_remove]
    dataframe[name_column_to_add] = pd.Series(column_to_add, index = dataframe.index)
    #dataframe.to_csv('vector.csv') 
    return dataframe

#=================================================================
# test
#=================================================================

df = pd.read_csv('small_data.csv', delimiter=',', encoding="utf-8")

# Vectorization of description column

description_column = df["description"]
clean_description_column = clean_tab(description_column)
clean_description_column = remove_html_pattern(clean_description_column)
vector_description = vectorize_column(clean_description_column)
df = replace_text_by_vector(df,"description",vector_description,"vector_description")

# Vectorization of title column

title_column = df["title"]
clean_title_column = clean_tab(title_column)
clean_title_column = remove_html_pattern(clean_title_column)
vector_title = vectorize_column(clean_title_column)
df = replace_text_by_vector(df,"title",vector_description,"vector_title")

# Vectorization of title column





















