import pandas as pd

df = pd.read_csv('./preprocessed_campaigns.csv')

print(list(df))

i=0
new_df = pd.DataFrame(columns=['id', 'title', 'category', 'country', 'cpc', 'name', 'keywords', 'description', 'job_type', 'employer', 'job', 'job_board_id', 'amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'budgetmax', 'budgetleft', 'creation'])
for row in df.groupby(['id', 'creation']):
    print(row[1])
    print(row[1]['id'])
    print(type(row[1]))
    # df.loc[i] = [row[1]['id'], row[1]['id'], row[1]['id'], row[1]['id']]
    i+=1
    break
