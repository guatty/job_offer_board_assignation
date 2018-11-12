#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd

df = pd.read_csv('data/preprocessed_campaigns.csv')


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

def f(row, action):
    if row['action'] == action:
        return row['amount_action']

for action in range(5):
    df['amount_action_'+str(action)] = df.apply( lambda row: f(row, action), axis=1)

del df['action']
del df['amount_action']

grouped = df.groupby(['id', 'creation'])

print(grouped)

grouped.to_csv("data/grouped.csv")