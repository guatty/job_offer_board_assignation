#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 18:13:26 2018

@author: geoffrey
"""

import pandas as pd # manipulation de csv
import frequency_terms as freq
from tensorflow.keras.preprocessing.text import Tokenizer


# tf_idf
import nltk
# nltk.download('stopwords')
from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
###

from nltk.corpus import stopwords  # text preproccess
import html2text

import csv
import tqdm

ENGLISH_STOPWORDS = set(stopwords.words("english"))
FRENCH_STOPWORDS = set(stopwords.words("french"))
FRENCH_STOPWORDS.add('dont')
FRENCH_STOPWORDS.add('votre')
FRENCH_STOPWORDS.add('notre')
FRENCH_STOPWORDS.add('autres')
FRENCH_STOPWORDS.add('autre')
FRENCH_STOPWORDS.add('sans')
FRENCH_STOPWORDS.add('leurs')
FRENCH_STOPWORDS.add('desormais')
FRENCH_STOPWORDS.add('nous')
FRENCH_STOPWORDS.add('si')

MAX_NB_WORDS= 200000

NB_KEYWORDS = 42

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

def replace_text_by_vector(dataframe,column_to_remove,column_to_add,name_column_to_add):
    del dataframe[column_to_remove]
    dataframe[name_column_to_add] = pd.Series(column_to_add, index = dataframe.index)
    return dataframe

def convert_df_to_csv(dataframe):
    dataframe.to_csv('vectorized_campaigns.csv')

#=================================================================
# tf_idf functions
#=================================================================
def prepare_tf_idf(tab):
    cv=CountVectorizer(max_df=0.85)
    word_count_vector=cv.fit_transform(tab)
    feature_names=cv.get_feature_names()
    return cv,word_count_vector,feature_names

def compute_tf_idf(text,wd,cv,feature_names):
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(wd)
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([text]))
    sorted_items=freq.sort_coo(tf_idf_vector.tocoo())
    keywords=freq.extract_topn_from_vector(feature_names,sorted_items,NB_KEYWORDS)
    return keywords

def compute_tf_idf_column(column,wd,cv,feature_names):
    tab_tf_idf_text = []
    for text in column :
        tf_idf = compute_tf_idf(text,wd,cv,feature_names)
        tab_tf_idf_text.append(tf_idf)
    return tab_tf_idf_text

def get_keys(array_of_tf_idf):
    tab_keys =[]
    for dictionnaire in array_of_tf_idf:
        keys = dictionnaire.keys()
        tab_keys.append(keys)
    return tab_keys




#=================================================================
# test
#=================================================================



df = pd.read_csv('data/cleaned_preprocessed_campaigns.csv', delimiter=',', encoding="utf-8")

# Vectorization of description column

description_column = df["description"]
clean_description_column = remove_html_pattern(description_column)
clean_description_column = clean_tab(clean_description_column)

cv, word_count_vec, feature_names = prepare_tf_idf(clean_description_column)
keywords = compute_tf_idf_column(clean_description_column,word_count_vec,cv,feature_names)
keys = get_keys(keywords)

print("a")

all_ids = []
# all_words = []
# for words in keys:
#     for key in words:
#         if not (key in all_words):
#             all_words.append(key)
#
# print(len(all_words))

with open('data/truc2.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    my_header = []
    my_header.append("my_id")
    my_header.append("my_title")
    for i in range(NB_KEYWORDS):
        my_header.append("keyword_"+str(i))
    # for word in all_words:
    #     my_header.append(word)
    spamwriter.writerow(my_header)
    for index in range(len(keywords)):
        if not (df['id'][index] in all_ids):
            final_list = []
            all_ids.append(df['id'][index])
            final_list.append(df['id'][index])
            final_list.append(df['title'][index].replace('"', ''))
            # for word in all_words:
            #     found = False
            #     for key in keys[index]:
            #         if (key == word):
            #             final_list.append(1)
            #             found = True
            #         if not found:
            #             final_list.append("?")
            # spamwriter.writerow(final_list)
            for key in keys[index]:
                    final_list.append(key)
            if (len(keys[index]) == NB_KEYWORDS):
                spamwriter.writerow(final_list)

'''
vector_description = vectorize_column(clean_description_column)
df = replace_text_by_vector(df,"description",vector_description,"vector_description")


# Vectorization of title column

title_column = df["title"]
vector_title = vectorize_column(title_column)
df = replace_text_by_vector(df,"title",vector_title,"vector_title")


# Vectorization of category column

category_column = df["category"]
vector_category = vectorize_column(category_column)
df = replace_text_by_vector(df,"category",vector_category,"vector_category")


# Vectorization of country column

country_column = df["country"]
vector_country = vectorize_column(country_column)
df = replace_text_by_vector(df,"country",vector_country,"vector_country")


# Vectorization of name column

name_column = df["name"]
vector_name = vectorize_column(name_column)
df = replace_text_by_vector(df,"name",vector_name,"vector_name")

# Vectorization of job_type column

job_type_column = df["job_type"]
vector_job_type = vectorize_column(job_type_column)
df = replace_text_by_vector(df,"job_type",vector_job_type,"vector_job_type")

convert_df_to_csv(df)
'''
