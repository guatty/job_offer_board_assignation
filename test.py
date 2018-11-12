# import tensorflow as tf
# from tensorflow import keras
import pandas as pd

# print(tf.__version__)
# print(keras.__version__)

df = pd.read_csv('../df_stats.csv')

# print(list(df))

del df['Unnamed: 0']
del df['title.1']
del df['name.1']
del df['job_group_id']
del df['status']
del df['enabled']
del df['limit_cv']
del df['uppdate']

# print(df['job_board_id'])

df.to_csv('./preprocessed_campaigns.csv')

# a = df['job_board_id'].corr(df['title'], method='spearman') # 0.015116500377894835

# print(a)
