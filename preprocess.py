#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
from math import sqrt

from tqdm import tqdm

import datetime
import calendar
import html2text
from nltk.corpus import stopwords
import re
from nltk.stem.snowball import FrenchStemmer

class Preprocess:





    def __init__(self, raw_data_path = 'data/df_stats.csv', output_filepath='data/cleaned_preprocessed_campaigns.csv', joi_output='data/joi.csv'):
        self.raw_data_path = raw_data_path
        self.output_filepath = output_filepath
        self.joi_output = joi_output
        self.legacy_columns = ['id', 'title', 'category', 'country', 'name', 'description', 'job_type', 'job_board_id', 'budgetmax', 'creation']
        self.new_columns = ["job_board_name", 'amount_action_0', 'amount_action_1', 'amount_action_2', 'amount_action_3', 'amount_action_4', 'total_cost', 'true_cpc', 'taux_conversion', "taux_conversion_pondere", "volume_conversion", 'creation_an', 'creation_mois', 'creation_jour', 'weekday']
        self.jobboard_name_for_id = { 31 : "AdformProgrammaticFR", 75 : "AdformProgrammaticGermany", 73 : "AdformProgrammaticNL", 74 : "AdformProgrammaticSwitzerland", 87 : "AdformProgrammaticUK", 76 : "AdformProgrammaticUS", 24 : "Adwords", 96 : "AdwordsFR", 102: "adwords-Switzerland", 101: "AdwordsUS", 4  : "Adzuna", 52 : "Adzuna US", 169: "APEC", 12 : "capital", 25 : "CV Library", 59 : "DoubleclickFR", 58 : "DoubleclickUK", 99 : "Facebook-Austria", 77 : "FacebookFR", 79 : "FacebookGermany", 81 : "Facebook-Netherlands", 80 : "Facebookswitzerland", 16 : "FaceBookUK", 78 : "FacebookUS", 98 : "Gigajob-Austria", 35 : "GigaJobFR", 68 : "Gigajob- Germany", 67 : "GigaJob - Netherlands", 69 : "Gigajob- switzerland", 34 : "GigaJobUK", 54 : "GigaJob US", 10 : "Github", 168: "GoogleJobDiscovery", 1  : "Indeed", 146: "Jobbird-Austria", 147: "Jobbird-Belgium", 156: "jobbird-Canada", 151: "Jobbird-France", 152: "Jobbird-Germany", 148: "Jobbird-India", 145: "Jobbird-Netherlands", 150: "Jobbird-Newzealand", 153: "Jobbird-Spain", 155: "jobbird-Switzerland", 149: "Jobbird-Turkey", 143: "Jobbird-UK", 144: "jobbird-US", 154: "jobboard-Switzerland", 14 : "Jobijoba", 9  : "Jobintree", 36 : "JobisJob", 57 : "JobisJob US", 97 : "Joblift-Austria", 131: "joblift-Belgium", 133: "joblift-Canada", 40 : "Joblift FR", 65 : "Joblift - Germany", 159: "joblift-Germany-d.jobmonitor.com", 158: "joblift-Germany-Muenchener", 136: "joblift-India", 61 : "Joblift-Netherlands", 135: "joblift-newzealand", 132: "joblift-Spain", 66 : "Joblift - Switzerland", 134: "joblift-Turkey", 37 : "JobLift UK", 50 : "Joblift US", 3  : "Jobrapido", 161: "jobrapidoGermany-Jobmonitor", 162: "jobrapidoGermany-muenchener", 60 : "jobrapidoProgrammaticTrendingJobs", 53 : "JobRapido US", 13 : "Jobtome", 157: "JobtomeGermany - de.jobmonitor.com", 88 : "JobtomeGermany - muenchener", 165: "Jobtomeprogrammatic", 39 : "Jobtome UK", 56 : "Jobtome US", 166: "kudos", 26 : "LApec", 7  : "Leboncoin", 19 : "Leboncoin Marque employeur", 100: "Linkedin-Austria", 82 : "LinkedinFR", 83 : "LinkedinGermany", 85 : "Linkedinnetherlands", 84 : "Linkedinswitzerland", 8  : "LinkedinUK", 86 : "LinkedinUS", 18 : "LinkUp", 47 : "LoadTestBoard", 167: "Match2one", 163: "Meteojob", 48 : "Monster", 43 : "MyJobHelper FR", 71 : "Myjobhelper-Germany", 70 : "MyJobHelper - Netherlands", 72 : "MyJobHelper - switzerland", 41 : "MyJobHelper UK", 55 : "MyJobHelper US", 28 : "Name", 42 : "Name", 33 : "Neuvoo", 90 : "NeuvooAustria-Jobleads", 137: "NeuvooBelgium-jobleads", 139: "NeuvooCanada-Jobleads", 93 : "NeuvooFrance-Jobleads", 89 : "NeuvooGermanyjobleads", 95 : "NeuvooGermany-Jobmonitor", 160: "NeuvooGermany-muenchener", 94 : "NeuvooHolland-Jobleads", 140: "NeuvooIndia-Jobleads", 142: "NeuvooNewzealand-jobleads", 138: "NeuvooSpain-jobleads", 91 : "Neuvooswitzerland-Jobleads", 141: "NeuvooTurkey-jobleads", 92 : "NeuvooUK-Jobleads", 51 : "NeuvooUSJobleads", 45 : "Nominal Technology", 2  : "Optioncarriere", 164: "ProgrammaticAppnexus", 113: "restorationmedia-UK", 112: "restorationmedia-US", 104: "ResultsGeneration-UK", 103: "Resultsgeneration -US", 27 : "Sites gratuits TP", 11 : "Stackoverflow", 5  : "Test", 29 : "[test] Job board 31671", 30 : "[test] Job board 73347", 115: "Trendingjobs-UK", 114: "Trendingjobs-US", 6  : "Trovit", 63 : "Trovit- Germany", 62 : "Trovit - Netherlands", 64 : "Trovit- Switzerland", 38 : "Trovit UK", 49 : "Trovit US", 17 : "Twitter", 15 : "Vivastreet", 120: "xpat-Austria", 125: "xpat-Belgium", 128: "xpat-Canada", 119: "xpat-France", 121: "xpat-Germany", 126: "xpat-India", 118: "xpat-Netherlands", 130: "xpat-newzealand", 127: "xpat-Spain", 122: "xpat-Switzerland", 129: "xpat-Turkey", 117: "xpat-UK", 116: "xpat-US", 109: "Yahoo-Austria", 108: "Yahoo-France", 107: "Yahoo-Germany", 110: "Yahoo-Netherlands", 111: "Yahoo-Switzerland", 106: "Yahoo-UK", 105: "Yahoo-US", 46 : "ZipRecruiter-France", 124: "ZipRecruiter-UK", 123: "ZipRecruiter-US"}
        self.stemmer = FrenchStemmer()
        self._set_stopwords()

    def reprocess_df_stats(self, raw=None, output=None):
        if raw is None:
            raw = self.raw_data_path
        if output is None:
            output = self.output_filepath
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
        #del self.df['Unnamed: 0'] # Not del'd since used as index.
        del self.df['title.1']
        del self.df['name.1']
        del self.df['job_group_id']
        del self.df['status']
        del self.df['keywords']
        del self.df['enabled']
        del self.df['limit_cv']
        del self.df['uppdate']
        del self.df['budgetleft']
        del self.df['employer']
        del self.df['job']

        self.df = self.df.dropna()

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
            df_line = pd.DataFrame(self.line, columns=self.new_df.columns, index=[0])
            self.new_df = pd.concat([self.new_df, df_line])


    def init_new_line(self):
        for col_name in self.new_columns:
            self.line[col_name] = 0

    def set_job_offer_info(self, column_value, col_name):
        if col_name in self.legacy_columns:
            if col_name == "description":
                def clean_desc(text):
                    text = html2text.html2text(text)
                    pattern = re.compile('[\W_]+', re.UNICODE)
                    text = pattern.sub(' ', text)
                    text = text.strip().lower().split()
                    text = filter(lambda word: word not in self.english_sw, text)
                    text = filter(lambda word: word not in self.french_sw, text)
                    text = filter(lambda word: len(word) >= 3, text)
                    text = [ self.stemmer.stem(t) for t in text ]
                    text = " ".join(text)

                    return text

                self.line[col_name] = clean_desc(column_value)
            elif col_name == "job_board_id":
                self.line["job_board_name"] = self.jobboard_name_for_id[int( column_value )]
            else:
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

    def get_unique_descriptions(self, output=None):
        if output is None:
            output = self.joi_output
        to_keep = ['id', 'title', 'category', 'country', 'name', 'description', 'job_type', 'budgetmax']
        # agg_first = { key: 'first' for key in to_keep }
        # job_offers_information = self.df.agg( agg_first )
        job_offers_information = self.new_df[ to_keep ].groupby('id').first()
        job_offers_information.to_csv(output)

    def _set_stopwords(self):
        self.english_sw = set(stopwords.words("english"))
        self.french_sw = set(stopwords.words("french"))
        self.french_sw.add('dont')
        self.french_sw.add('votre')
        self.french_sw.add('notre')
        self.french_sw.add('autres')
        self.french_sw.add('autre')
        self.french_sw.add('sans')
        self.french_sw.add('leurs')
        self.french_sw.add('desormais')
        self.french_sw.add('nous')
        self.french_sw.add('si')
        self.french_sw.add('les')
        self.french_sw.add('lui')



if __name__ == '__main__':
    pp = Preprocess()

    pp.reprocess_df_stats()
    pp.get_unique_descriptions()
