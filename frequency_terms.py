#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 19:38:18 2018

@author: geoffrey
"""

import nltk
from collections import Counter
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer




def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    score_vals = []
    feature_vals = []
    
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])
 
    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results




def prepare_tf_idf(tab):
    cv=CountVectorizer(max_df=0.85)
    word_count_vector=cv.fit_transform(tab)
    feature_names=cv.get_feature_names()
    
    

phrase =["adista developpe offre services particulierement pertinente innovante autour l'hebergement systemes d'information, l'exploitation reseaux thd livrer entreprises services informatiques telecommunications. cette offre rencontre d'autant plus succes les dirigeants d'entreprises recherche d'un si adapte strategie, utilise mode service, vision type 'cloud'. **les missions responsabilit :** rattache l'agence cesson-sevigne, etes charge developpement commercial offres region bretagne, cible pme / eti collectivites. mission developpement actions commerciales l'appui service marketing service avant-vente l'entreprise reporterez direction commerciale. egalement charge developper reseau partenaire secteur. **qualites candidat:** * disposez deja d'une experience reussie vente solutions complexes directions metiers (dg/dsi/marketing…). * sentez veritable developpeur commercial l'ame forte envie reussir. * bonne maitrise vente solutions autour si btob (hebergement). diplome bac+ 2 minimum / permis b obligatoire poste necessite candidat disposant quelques annees d'experience domaine l'integration systemes, desireux donner nouvel elan carriere, integrant adista commercialiser vision nouvelle systeme d'information. remuneration selon profil composee d'un fixe d'un variable evolutif. **description compagnie :** c'est l'esprit l'entreprise. adista fait partie 150 plus belles entreprises françaises independantes annonce objectif 2018 100 millions € ca 500 collaborateurs. adista dispose d'une moyenne d'age jeune, collaborateurs travaillent projets motivants, essentiels pme, eti grandes entreprises, grandes collectivites. considerons clef succes reside facteur humain. les collaborateurs 1ere richesse l'entreprise. donnant toutes les conditions innover, bonifier solutions, creer nouvelles…adista permet d'exprimer tout potentiel. investissant tous les ans part importante revenus, proposant l'innovation clients, l'entreprise cree cadre travail tres motivant collaborateurs traduit quotidien les outils communication collaboration mis disposition.", "adista developpe offre services particulierement pertinente innovante autour l'hebergement systemes d'information, l'exploitation reseaux thd livrer entreprises services informatiques telecommunications. cette offre rencontre d'autant plus succes les dirigeants d'entreprises recherche d'un si adapte strategie, utilise mode service, vision type 'cloud'. **les missions responsabilit :** rattache l'agence cesson-sevigne, etes charge developpement commercial offres region bretagne, cible pme / eti collectivites. mission developpement actions commerciales l'appui service marketing service avant-vente l'entreprise reporterez direction commerciale. egalement charge developper reseau partenaire secteur. **qualites candidat:** * disposez deja d'une experience reussie vente solutions complexes directions metiers (dg/dsi/marketing…). * sentez veritable developpeur commercial l'ame forte envie reussir. * bonne maitrise vente solutions autour si btob (hebergement). diplome bac+ 2 minimum / permis b obligatoire poste necessite candidat disposant quelques annees d'experience domaine l'integration systemes, desireux donner nouvel elan carriere, integrant adista commercialiser vision nouvelle systeme d'information. remuneration selon profil composee d'un fixe d'un variable evolutif. **description compagnie :** c'est l'esprit l'entreprise. adista fait partie 150 plus belles entreprises françaises independantes annonce objectif 2018 100 millions € ca 500 collaborateurs. adista dispose d'une moyenne d'age jeune, collaborateurs travaillent projets motivants, essentiels pme, eti grandes entreprises, grandes collectivites. considerons clef succes reside facteur humain. les collaborateurs 1ere richesse l'entreprise. donnant toutes les conditions innover, bonifier solutions, creer nouvelles…adista permet d'exprimer tout potentiel. investissant tous les ans part importante revenus, proposant l'innovation clients, l'entreprise cree cadre travail tres motivant collaborateurs traduit quotidien les outils communication collaboration mis disposition.", "**votre vie d'ingenieur(e) commercial(e) chez fiparc 2 elements cles :** 1. chasseur reseauteur : chasseur(euse) avant tout, c'est conquete commerciale attire. convaincu(e) qualite solutions fiparc, faites ouvrir les portes societes interessent. reseauteur(euse) plaisir, aimez rencontrer les gens, decouvrir les metiers rendre sincerement service. mettre relation les meilleures conditions futurs clients, fonctionnez naturellement reseaux. 2. batisseur commercial : pensez long-terme. prenez plus grand soin relations creez les dg les daf belles pme cibles. fidelisez les clients conquis constance presence qualite prestations fiparc laquelle contribuez. employez repondre precision attentes. approfondissez connaissance metiers secteurs. batissez ainsi portefeuille clients satisfaction l'une fiertes. d'ailleurs, prenez plaisir les mettre relation entre eux. **concr etement ?**nous confions portefeuille prospects ile france conquerir. ils connaissent doute encore car equipe justement besoin s'etoffer commercialement. disposez d'une gamme large tres ciblee solutions location financiere certains produits tres novateurs. les aidez financer investissements industriels informatiques les meilleures conditions, banquiers. 200 clients 8 societes cac40 temoignent. **vos moyens reussir** manager tres proche vous, commercial lui-meme. objectif permettre progresser reussir mieux possible. supervise formation initiale metier location financiere, produits fiparc methodes vente solidement eprouvees. l'equipe fiparc, soudee solidaire, experimentee metiers, aide quotidien proposer valider les meilleures solutions clients. les clients fiparc montrent aussi parfois d'excellents ambassadeurs ! organiser actions, disposez tous les outils crm utiles realisation business. etes egalement equipe(e) d'un ordinateur fixe d'un telephone mobile. **votre entreprise taille humaine :** fiparc fete 15 ans cette annee realise ca 11 m€ equipe 8 personnes. independante tout organisme bancaire financier, certifiee iso 9001. stade aventure, place conquete commerciale premier rang priorites. **votre profil :** si pouvez demontrer tres bonnes competences batisseur commercial chasseur-reseauteur citees plus haut, suppose quelques annees d'experience, si aimez apprendre apprendre autres, si apprecie souvent culture generale, si pratiquez les relations commerciales niveau directions pme, alors dites-nous plus ! si outre culture financiere, saurons naturellement l'apprecier. formation, attendons niveau d'etudes type bac+3 4, totalement ouverts d'autres parcours. seules competences envie mesurees. **votre remuneration:** fiparc offre package salarial tres attractif non plafonne : salaire fixe + variable mensuel. poste evidemment propose cdi."]

# get the document that we want to extract keywords from


def compute_tf_idf(text,wd,cv,feature_names):
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(wd)
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([text]))
    sorted_items=sort_coo(tf_idf_vector.tocoo())
    keywords=extract_topn_from_vector(feature_names,sorted_items,15)
    return keywords


    
    


























'''fdist = nltk.FreqDist(['Gab','Geoffrey','Geoffrey','Romain','alors','bateau','alors','bien']) # creates a frequency distribution from a list
count = Counter(fdist)
    
print(count)'''