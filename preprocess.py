#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import tensorflow as tf
# from tensorflow import keras
import pandas as pd
from math import sqrt

from tqdm import tqdm

# print(tf.__version__)
# print(keras.__version__)
"""

df = pd.read_csv('data/df_stats.csv', index_col=0)

# print(list(df))

#del df['Unnamed: 0'] # Not del'd since used as index.
del df['title.1']
del df['name.1']
del df['job_group_id']
del df['status']
del df['enabled']
del df['limit_cv']
del df['uppdate']
del df['budgetleft']
del df['employer']

df = df.dropna()


# print(df.corr())

# print(df['job_board_id'])

df.to_csv('data/preprocessed_campaigns.csv')

# a = df['job_board_id'].corr(df['title'], method='spearman') # 0.015116500377894835

# print(a)

"""

def unify_job_types(jt):
    if jt == "Apprenticeship":
        return "Alternance"
    elif jt == "Internship":
        return "Stage"
    elif jt in ["Other", "Autres"]:
        return "Autre"
    elif jt == "Permanent contract":
        return "CDI"
    else:
        return jt


df = pd.read_csv('data/preprocessed_campaigns.csv')
# print(list(df))

i=0
legacy_columns = ['id', 'title', 'category', 'country', 'cpc', 'name', 'keywords', 'description', 'job_type', 'job', 'job_board_id', 'budgetmax']
new_columns = ['amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'taux_conversion', "taux_conversion_pondere", 'creation_an', 'creation_mois', 'creation_jour']

new_df = pd.DataFrame(columns=legacy_columns + new_columns)
for result in tqdm(df.groupby(['id', 'creation']), desc="Preprocessing: "):

    line = {}

    for col_name in new_columns:
        line[col_name] = 0

    for col_name, column_value in result[1].iloc[0].iteritems():
        if col_name in legacy_columns:
            line[col_name] = column_value

        if col_name == "creation":
            an, mois, jour = column_value.split('-')
            line['creation_an'] = an
            line['creation_mois'] = mois
            line['creation_jour'] = jour


    for index, row in result[1].iterrows():
        action_id = row['action'] 
        if action_id in range(5):
            line['amount_action_' + str(int(action_id))] += row['amount_action']
        line['cpc'] += row['cpc']

    conversion_volume = line['amount_action_2'] + line['amount_action_3'] 
    if line['amount_action_0'] != 0 and conversion_volume <= line['amount_action_0']:
        line['taux_conversion'] = conversion_volume / line['amount_action_0'] 
        line['taux_conversion_pondere'] = line['taux_conversion'] * sqrt(conversion_volume)

    line['job_type'] = unify_job_types(line['job_type'])

    df_line  = pd.DataFrame(line, columns=new_df.columns, index=[0])
    new_df = pd.concat([new_df, df_line])


new_df.to_csv('data/cleaned_preprocessed_campaigns.csv')


#new_df = pd.DataFrame(columns=['id', 'title', 'category', 'country', 'cpc', 'name', 'keywords', 'description', 'job_type', 'employer', 'job', 'job_board_id', 'amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'budgetmax', 'budgetleft', 'creation'])
#for row in df.groupby(['id', 'creation']):

# def fuse_action_row_into_columns(df):
#     print(df)
#     if df['action'] in [0, 1, 2, 3, 4]:
#         print(df[''])
#     if 'Fruit' in df.values:
#        num_val = df[df['Property'] == 'Red']['Numerical_value'].values[0]
#        return pd.Series({'Red&Fruit': '1', 'Num_val': num_val})
#     elif 'Red' in df.values:
#        num_val= df[df['Property'] == 'Red']['Num_val'].values[0]
#        return pd.Series({'Just_red': '1', 'Num_val': num_val})
#     else:
#        return pd.Series({'Other': '1', 'Num_val': 0})

# grouped = df.groupby(['id', 'creation'])['action', 'amount_action'].apply(fuse_action_row_into_columns)

# def f(row, action):
#     if row['action'] == action:
#         return row['amount_action']

# for action in range(5):
#     df['amount_action_'+str(action)] = df.apply( lambda row: f(row, action), axis=1)

# del df['action']
# del df['amount_action']

# grouped = df.groupby(['id', 'creation']).sum()
# #grouped = df.drop_duplicates(["creation", "id"])
# print(grouped)

# grouped.to_csv("data/grouped.csv")
