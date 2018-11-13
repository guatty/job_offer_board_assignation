import pandas as pd

df = pd.read_csv('data/preprocessed_campaigns.csv')

# print(list(df))

i=0
columns_name = ['id', 'title', 'category', 'country', 'cpc', 'name', 'keywords', 'description', 'job_type', 'job', 'job_board_id', 'amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'budgetmax', 'creation']
new_df = pd.DataFrame(columns=columns_name)
for row in df.groupby(['id', 'creation']):
    if i % 1000 == 0:
        print(i)
    # print(row[1])
    # print(row[1]['id'].iloc[0])
    # print(type(row[1]['id']))
    line = [0] * len(columns_name)
    j = 0
    for column in columns_name:
        if column == "amount_action_0":
            if not (row[1][row[1]['action'] == 0].empty):
                line[j] = row[1][row[1]['action'] == 0 ]['amount_action'].iloc[0]
            else:
                line[j] = 0
        elif column == "amount_action_1":
            if not (row[1][row[1]['action'] == 1].empty):
                line[j] = row[1][row[1]['action'] == 1 ]['amount_action'].iloc[0]
            else:
                line[j] = 0
        elif column == "amount_action_2":
            if not (row[1][row[1]['action'] == 2].empty):
                line[j] = row[1][row[1]['action'] == 2 ]['amount_action'].iloc[0]
            else:
                line[j] = 0
        elif column == "amount_action_3":
            if not (row[1][row[1]['action'] == 3].empty):
                line[j] = row[1][row[1]['action'] == 3 ]['amount_action'].iloc[0]
            else:
                line[j] = 0
        elif column == "amount_action_4":
            if not (row[1][row[1]['action'] == 4].empty):
                line[j] = row[1][row[1]['action'] == 4 ]['amount_action'].iloc[0]
            else:
                line[j] = 0
            # print(row[1][row[1]['action'] == 1 ]['amount_action'].iloc[0])
            # print(row[1][row[1]['action'] == 1 ]['action'].iloc[0] == 1)
            # YYY = df[ df['action'] == 1 ]['amount_action']
        else:
            # print(line.append(row[1]['id'].iloc[0]))
            line[j] = row[1][column].iloc[0]
        j+=1
    new_df.loc[i] = line
    i+=1

new_df.to_csv('data/cleaned_preprocessed_campaigns.csv')
