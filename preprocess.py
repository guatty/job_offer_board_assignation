#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import tensorflow as tf
# from tensorflow import keras
import pandas as pd
from math import sqrt

from tqdm import tqdm

import datetime
import calendar

# print(tf.__version__)
# print(keras.__version__)
df = pd.read_csv('data/df_stats.csv', index_col=0)


#del df['Unnamed: 0'] # Not del'd since used as index.
del df['title.1']
del df['name.1']
del df['job_group_id']
del df['status']
del df['keywords']
del df['enabled']
del df['limit_cv']
del df['uppdate']
del df['budgetleft']
del df['employer']

df = df.dropna()

# df.to_csv('data/preprocessed_campaigns.csv')


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


#df = pd.read_csv('data/preprocessed_campaigns.csv')

legacy_columns = ['id', 'title', 'category', 'country', 'name', 'keywords', 'description', 'job_type', 'job', 'job_board_id', 'budgetmax', 'creation']
new_columns = ['amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'total_cost', 'true_cpc', 'taux_conversion', "taux_conversion_pondere", "volume_conversion", 'creation_an', 'creation_mois', 'creation_jour', 'weekday']

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
            my_date = datetime.date(int(an), int(mois), int(jour)).weekday()
            str_date = calendar.day_name[my_date]
            line['weekday'] = str_date


    for index, row in result[1].iterrows():
        action_id = row['action']
        if action_id in range(5):
            line['amount_action_' + str(int(action_id))] += row['amount_action']
        line['total_cost'] += row['cpc']

    conversion_volume = line['amount_action_2'] + line['amount_action_3']
    line['volume_conversion'] = conversion_volume
    if line['amount_action_0'] != 0 and conversion_volume <= line['amount_action_0']:
        line['taux_conversion'] = conversion_volume / line['amount_action_0']
        line['taux_conversion_pondere'] = line['taux_conversion'] * sqrt(conversion_volume)
        line['true_cpc'] = line['total_cost'] / line['amount_action_0']

        line['job_type'] = unify_job_types(line['job_type'])

        df_line  = pd.DataFrame(line, columns=new_df.columns, index=[0])
        new_df = pd.concat([new_df, df_line])


new_df.to_csv('data/cleaned_preprocessed_campaigns.csv')
