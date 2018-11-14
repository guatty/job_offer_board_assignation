#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
from math import sqrt

from tqdm import tqdm

import datetime
import calendar


class preprocess:



    def __init__(self, raw_data_path = 'data/df_stats.csv', output_filepath='data/cleaned_preprocessed_campaigns.csv'):
        self.legacy_columns = ['id', 'title', 'category', 'country', 'name', 'keywords', 'description', 'job_type', 'job', 'job_board_id', 'budgetmax', 'creation']
        self.new_columns = ['amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'total_cost', 'true_cpc', 'taux_conversion', "taux_conversion_pondere", "volume_conversion", 'creation_an', 'creation_mois', 'creation_jour', 'weekday']
        
        self.execute_standard(raw_data_path, output_filepath)


    def execute_standard(self, raw, output):
        self.df = pd.read_csv(raw, index_col=0)
        self.remove_useless_data()

        self.new_df = pd.DataFrame(columns=self.legacy_columns + self.new_columns)

        for result in tqdm(self.df.groupby(['id', 'creation']), desc="Preprocessing: "):
            self.preprocess_line(result)

        self.new_df.to_csv(output)

    def unify_job_types(self, jt):
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

    def remove_useless_data(self):
        df = self.df
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
        return df

    def preprocess_line(self, result):
        line = self.init_new_line()
        line = self.calculate_amount_action_and_cost(result, line)
        conversion_volume = line['amount_action_2'] + line['amount_action_3']
        if line['amount_action_0'] != 0 and conversion_volume <= line['amount_action_0']:

            for col_name, column_value in result[1].iloc[0].iteritems():
                line = self.set_job_offer_info(line, column_value, col_name)

            line = self.set_additional_indicators(result, line, conversion_volume)
            line['job_type'] = self.unify_job_types(line['job_type'])

            # inputs line
            df_line  = pd.DataFrame(line, columns=self.new_df.columns, index=[0])
            self.new_df = pd.concat([self.new_df, df_line])


    def init_new_line(self):
        line = {}
        for col_name in self.new_columns:
            line[col_name] = 0
        return line

    def set_job_offer_info(self, line, column_value, col_name):
        if col_name in self.legacy_columns:
            line[col_name] = column_value

        if col_name == "creation":
            an, mois, jour = column_value.split('-')
            line['creation_an'] = an
            line['creation_mois'] = mois
            line['creation_jour'] = jour
            my_date = datetime.date(int(an), int(mois), int(jour)).weekday()
            str_date = calendar.day_name[my_date]
            line['weekday'] = str_date

        return line

    def calculate_amount_action_and_cost(self, result, line):
        for index, row in result[1].iterrows():
            action_id = row['action']
            if action_id in range(5):
                line['amount_action_' + str(int(action_id))] += row['amount_action']
            line['total_cost'] += row['cpc']
        return line

    def set_additional_indicators(self, result, line, conversion_volume):
        line['volume_conversion'] = conversion_volume
        line['taux_conversion'] = conversion_volume / line['amount_action_0']
        line['taux_conversion_pondere'] = line['taux_conversion'] * sqrt(conversion_volume)
        line['true_cpc'] = line['total_cost'] / line['amount_action_0']
        return line

if __name__ == '__main__':
    pp = preprocess()
    preprocess.execute_standard()
