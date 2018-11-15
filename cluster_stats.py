#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import tensorflow as tf
# from tensorflow import keras
import pandas as pd
import datetime
from tqdm import tqdm

considered_columns = ['id', 'job_board_id', 'true_cpc', 'total_cost', 'volume_conversion', 'creation', 'taux_conversion', "taux_conversion_pondere"]

#['id', 'title', 'category', 'country', 'cpc', 'name',
# 'keywords', 'description', 'job_type', 'job', 'job_board_id', 'budgetmax']
#['amount_action_0', 'amount_action_1', 'amount_action_2',
# 'amount_action_3', 'amount_action_4', 'taux_conversion',
# "taux_conversion_pondere", 'creation_an', 'creation_mois', 'creation_jour']


dateparser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d')
df = pd.read_csv('data/cleaned_preprocessed_campaigns.csv', index_col=0, parse_dates=['creation'], date_parser=dateparser)


#print(df[ df['id'] == 4717 ])

def get_stat(job_offer_id):

    stats_all_job_offers = pd.DataFrame(columns=['campaign_duration', 'total_cost', 'volume_conversion', 'true_cpc', 'taux_conversion', "taux_conversion_pondere"])

    for job_offer_log in tqdm(df[ df['id'] == job_offer_id ].groupby('job_board_id'), desc="Stats on job offer: "):

        job_offer_log = job_offer_log[1]
        #print(job_offer_log)
        campaign_start_date = job_offer_log['creation'].min()
        campaign_duration = ( job_offer_log['creation'].max() - campaign_start_date ).days + 1

        jor =  job_offer_log[ considered_columns ]
        if campaign_duration > 1 / 0.8 :
            date_a_80_pct_gauss =  campaign_start_date + datetime.timedelta( 0.8 * campaign_duration )
            gauss_eighty_most_significant = jor[ jor['creation'] < date_a_80_pct_gauss ]
        else:
            gauss_eighty_most_significant = jor

        del gauss_eighty_most_significant['creation']
        #stats = gauss_eighty_most_significant[['total_cost', 'volume_conversion']].sum(axis=0)
        #stats = stats[['true_cpc', 'taux_conversion', "taux_conversion_pondere"]].mean(axis=0)
        agg_sum = { key: 'sum' for key in ['total_cost', 'volume_conversion'] }
        agg_mean = { key: 'mean' for key in ['true_cpc', 'taux_conversion', "taux_conversion_pondere"] }
        agg_sum.update(agg_mean)

        stats = gauss_eighty_most_significant.agg( agg_sum )

        stats['campaign_duration'] = 0.8 * campaign_duration
        statss = pd.DataFrame(stats.transpose())
        print(statss.T)
        stats_all_job_offers = pd.concat([stats_all_job_offers, statss.T])

    return stats_all_job_offers


print(get_stat(4717))


def stats_cluster(liste_job_id):
    stats_cluster = dataframe()
    for job_id in liste_job_id:
        stats_cluster.append( get_stat( job_id ) )

    return stats_cluster.mean()

