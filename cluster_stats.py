#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import tensorflow as tf
# from tensorflow import keras
import pandas as pd

considered_columns = ['id', 'true_cpc', 'sum_cpc', 'volume_conversion', 'creation', 'taux_conversion', "taux_conversion_pondere"]

#['id', 'title', 'category', 'country', 'cpc', 'name', 
# 'keywords', 'description', 'job_type', 'job', 'job_board_id', 'budgetmax']
#['amount_action_0', 'amount_action_1', 'amount_action_2', 
# 'amount_action_3', 'amount_action_4', 'taux_conversion', 
# "taux_conversion_pondere", 'creation_an', 'creation_mois', 'creation_jour']


df = pd.read_csv('data/cleaned_preprocessed_campaigns.csv', index_col=0, columns = considered_columns)

def get_stat(job_offer_id):
    job_offer_log = df[ df['id'] == job_offer_id ]

    #for col in considered_columns:
    #    stats[col] = job_offer_log[].mean(axis=0)
    jor =  job_offer_log[ considered_columns ]

    campaign_start_date = job_offer_log['creation'].min().date()
    campaign_duration = ( job_offer_log['creation'].max().date() - campaign_start_date ).days
    
    gauss_eighty_most_significant = jor[ ( jor['creation'].date() - campaign_start_date ).days  > 0.8 * campaign_duration ]
    
    del gauss_eighty_most_significant['creation']
    stats = gauss_eighty_most_significant.sum(axis=0)

    stats['campaign_duration'] = 0.8 * campaign_duration
    

            

    return stats


print(get_stat(4717))