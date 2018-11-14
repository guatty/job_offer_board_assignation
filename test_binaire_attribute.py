#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 13:53:38 2018

@author: geoffrey
"""


import csv
import pandas as pd # manipulation de csv


df = pd.read_csv('truc4.csv', delimiter=',', encoding="utf-8")

columnes = df.columns

attributs_key_words = columnes[3:]

tab_key_words = []

def extract_diffrent_words(column):
    for word in column :
        if not word in tab_key_words:
            tab_key_words.append(word)

        


def foreach_column():
    for colonne in attributs_key_words:
        extract_diffrent_words(df[colonne])
    
        


a = foreach_column()



with open('truc5.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    spamwriter.writerow(tab_key_words)
    with open('truc4.csv', 'r') as csvfile2:
        reader = csv.reader(csvfile2)
        for row in reader :
            liste = []
            for key in tab_key_words:
                found = False
                for mot in row[3:] :
                    if key == mot:
                        liste.append(1)
                        found = True
                if not found:
                    liste.append("?")
            spamwriter.writerow(liste)



























