#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
from math import sqrt

from tqdm import tqdm

import datetime
import calendar


class Preprocess:



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
        self.line = {}
        self.init_new_line()
        self.calculate_amount_action_and_cost(result)
        conversion_volume = self.line['amount_action_2'] + self.line['amount_action_3']
        if self.line['amount_action_0'] != 0 and conversion_volume <= self.line['amount_action_0']:

            for col_name, column_value in result[1].iloc[0].iteritems():
                self.set_job_offer_info(column_value, col_name)

            self.set_additional_indicators(result, conversion_volume)
            self.line['job_type'] = self.unify_job_types(self.line['job_type'])

            # inputs line
            df_line = pd.DataFrame(columns=self.new_df.columns, index=[0])
            self.new_df = pd.concat([self.new_df, df_line])


    def init_new_line(self):
        for col_name in self.new_columns:
            self.line[col_name] = 0

    def set_job_offer_info(self, column_value, col_name):
        if col_name in self.legacy_columns:
            self.line[col_name] = column_value

        if col_name == "creation":
            an, mois, jour = column_value.split('-')
            self.line['creation_an'] = an
            self.line['creation_mois'] = mois
            self.line['creation_jour'] = jour
            my_date = datetime.date(int(an), int(mois), int(jour)).weekday()
            str_date = calendar.day_name[my_date]
            self.line['weekday'] = str_date

    def calculate_amount_action_and_cost(self, result):
        for index, row in result[1].iterrows():
            action_id = row['action']
            if action_id in range(5):
                self.line['amount_action_' + str(int(action_id))] += row['amount_action']
            self.line['total_cost'] += row['cpc']

    def set_additional_indicators(self, result, conversion_volume):
        self.line['volume_conversion'] = conversion_volume
        self.line['taux_conversion'] = conversion_volume / self.line['amount_action_0']
        self.line['taux_conversion_pondere'] = self.line['taux_conversion'] * sqrt(conversion_volume)
        self.line['true_cpc'] = self.line['total_cost'] / self.line['amount_action_0']

if __name__ == '__main__':
    pp = Preprocess()
    preprocess.execute_standard()
