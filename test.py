#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import tensorflow as tf
# from tensorflow import keras
import pandas as pd

# print(tf.__version__)
# print(keras.__version__)

<<<<<<< HEAD
df = pd.read_csv('data/df_stats.csv')

# print(list(df))

=======
df = pd.read_csv('data/df_stats.csv', index_col=0)

# print(list(df))

#del df['Unnamed: 0']
>>>>>>> 8d6568af2267da779e0fe4471ee5f002839e2735
del df['title.1']
del df['name.1']
del df['job_group_id']
del df['status']
del df['enabled']
del df['limit_cv']
del df['uppdate']
del df['budgetleft']
del df['employer']

# df['']

df = df.dropna()


# print(df.corr())

# print(df['job_board_id'])

df.to_csv('data/preprocessed_campaigns.csv')

# a = df['job_board_id'].corr(df['title'], method='spearman') # 0.015116500377894835

# print(a)
