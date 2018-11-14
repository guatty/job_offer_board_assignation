# #!/usr/bin/python3
# # -*- coding: utf-8 -*-
#
# # import tensorflow as tf
# # from tensorflow import keras
import pandas as pd
#
# # print(tf.__version__)
# # print(keras.__version__)
#
# df = pd.read_csv('data/df_stats.csv', index_col=0)
#
# # print(list(df))
#
# #del df['Unnamed: 0']
# del df['title.1']
# del df['name.1']
# del df['job_group_id']
# del df['status']
# del df['enabled']
# del df['limit_cv']
# del df['uppdate']
# del df['budgetleft']
# del df['employer']
#
# # df['']
#
# df = df.dropna()
#
#
# # print(df.corr())
#
# # print(df['job_board_id'])
#
# df.to_csv('data/preprocessed_campaigns.csv')
#
# # a = df['job_board_id'].corr(df['title'], method='spearman') # 0.015116500377894835
#
# # print(a)

# import datetime
# import calendar
#
# an = 2018
# mois = 11
# jour = 13
#
# my_date = datetime.date(an, mois, jour).weekday()
# str_date = calendar.day_name[my_date]
# print(str_date)

df = pd.read_csv('data/truc2.csv', delimiter=',', encoding="utf-8")

new_df = df[ df['my_title'].isin(["Administrative Assistant", "Phlebotomist", "Sales Associate"]) ]

new_df.to_csv('data/truc4.csv')

# if (df['title'] == "Administrative Assistant"):
#     print("oui")

# print(df['id'][0])
