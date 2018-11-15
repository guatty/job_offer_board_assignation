#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 18:13:26 2018

@author: geoffrey
"""

import pandas as pd # manipulation de csv
import frequency_terms as freq
from keras.preprocessing.text import Tokenizer


# tf_idf
import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
###

from nltk.corpus import stopwords  # text preproccess
import html2text

import csv
import tqdm



class vectorisation:

    def __init__(self, job_offer_df, nb_keywords_to_consider=1000, nb_keywords_per_desc=10):
        self.total_kw = nb_keywords_to_consider
        self.kw_per_data = nb_keywords_per_desc
        self.df = job_offer_df
        self._set_stopwords()


    def do_columns(self, cols=["description"]):
        for col in cols:
            self._do(col)

    def _do(self, col):

        self.remove_html_pattern(col)
        self.remove_stopwords_in(col)
        self.vectorize_for(col)

        # vector_description, word_index = vectorize_column(clean_description_column)

    def vectorize_for(self, column_name):
        tokenizer = Tokenizer(num_words=self.total_kw)
        tokenizer.fit_on_texts(data_column)
        word_index = tokenizer.word_index
        vector_data = tokenizer.texts_to_sequences(data_column)


def vectorize_column(data_column):
    tokenizer = Tokenizer(num_words=self.total_kw)
    tokenizer.fit_on_texts(data_column)
    word_index = tokenizer.word_index
    vector_data = tokenizer.texts_to_sequences(data_column)
    return vector_data,word_index



with open('data/truc2.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    my_header = []
    for mot in word_index.keys():
        my_header.append(mot)
    spamwriter.writerow(my_header)
    for description in vector_description:
        liste_binaire=[]
        for i in range(len(word_index)) :
            if i in description:
                liste_binaire.append(1)
            else:
                liste_binaire.append(0)
        spamwriter.writerow(liste_binaire)





    def remove_html_pattern(self, column_name):
        df[column_name] = df[column_name].apply( html2text.html2text )


    def remove_stopwords_in(self, column_name):
        def filter_stopwords(text):
            text = text.strip().lower().split()
            text = filter(lambda word: word not in self.english_sw, text)
            text = filter(lambda word: word not in self.french_sw, text)
            text = filter(lambda word: len(word) > 3, text)
            return " ".join(text)

        df[column_name] = df[column_name].apply( filter_stopwords )

        

    def export_to_csv(self, path="data/vectorized_campaigns.csv"):
        self.df.to_csv(path)

    def _set_stopwords(self):
        self.english_sw = set(stopwords.words("english"))
        self.french_sw = set(stopwords.words("french"))
        self.french_sw.add('dont')
        self.french_sw.add('votre')
        self.french_sw.add('notre')
        self.french_sw.add('autres')
        self.french_sw.add('autre')
        self.french_sw.add('sans')
        self.french_sw.add('leurs')
        self.french_sw.add('desormais')
        self.french_sw.add('nous')
        self.french_sw.add('si')
        self.french_sw.add('les')
        self.french_sw.add('lui')


def replace_text_by_vector(dataframe,column_to_remove,column_to_add,name_column_to_add):
    del dataframe[column_to_remove]
    dataframe[name_column_to_add] = pd.Series(column_to_add, index = dataframe.index)
    return dataframe


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
    keywords=freq.extract_topn_from_vector(feature_names,sorted_items,15)
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



if __name__ == '__main__':
    df = pd.read_csv('small_data.csv', delimiter=',', encoding="utf-8")
    vec = vectorisation(df)

    vec.do_columns(['description'])




'''
cv, word_count_vec, feature_names = prepare_tf_idf(clean_description_column)
keywords = compute_tf_idf_column(clean_description_column,word_count_vec,cv,feature_names)


keys = get_keys(keywords)
'''
'''
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
