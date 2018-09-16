#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 13:02:04 2018

@author: psylekin
"""

import os as os
import matplotlib.pyplot as plt
import pandas as pd

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
       
def get_distribution(target):
    printed = data.loc[:,target]
    name = questions.loc[questions.VAR == printed.name, "QUESTION"].values[0]
    sub_name = questions.loc[questions.VAR == printed.name, "LABEL"].values[0]
    stats = printed.value_counts().sort_index()
    return sub_name, name, stats

def get_stats(target):
    printed = data.loc[:,target]
    name = questions.loc[questions.VAR == printed.name, "QUESTION"].values[0]
    sub_name = questions.loc[questions.VAR == printed.name, "LABEL"].values[0]
    stats = printed.describe()
    return sub_name, name, stats

#%% Vorbereitung
create_folder("Ergebnisse")
create_folder("Ergebnisse/Bilder")

datalist = ["data_Mitarbeiter-Feedback_2018-09-13_10-31.csv",
            "values_Mitarbeiter-Feedback_2018-09-13_10-31.csv",
            "variables_Mitarbeiter-Feedback_2018-09-13_10-31.csv"]

def loadData(datalist):
    data = pd.read_csv(datalist[0], encoding='utf-16', sep = "\t", na_values=["nicht beantwortet", "nan", -9])
    answerCodes = pd.read_csv(datalist[1], encoding='utf-16', sep = "\t").set_index("VAR")
    metaData = pd.read_csv(datalist[2], encoding='utf-16', sep = "\t").drop("INPUT",axis = 1).set_index("VAR")
    meaninglist = dict()
    
    for variable in answerCodes.index.unique():
        meaningDict = answerCodes.loc[answerCodes.index == variable,"RESPONSE":].set_index("RESPONSE").to_dict()
        meaningDict[variable] = meaningDict.pop("MEANING")
        meaninglist.update(meaningDict)
        
    return metaData, data, meaninglist

metaData, data, meaninglist = loadData(datalist)

#%%

with open ('Ergebnisse/Verteilung.txt', 'w') as log:
    for variable in data.columns:
        output = "{} - {} \n"
        log.write(output.format(variable, 
                                metaData.loc[variable,"QUESTION"]))


#%%

"""
#%% Grafiken
plt.figure(figsize=(20, 10))
for x in data.columns:
    target = data.loc[:, x].value_counts().sort_index()
    target.plot.bar(width=1, title=data.loc[:, x].name)
    plt.savefig('Ergebnisse/Bilder/' + str(data.loc[:, x].name) + '.png')
    plt.clf()
    
#%% Verteilung
with open ('Ergebnisse/Verteilung.txt', 'w') as log:
    for x in data.columns:
        output = get_distribution(x)[0], "\n",get_distribution(x)[1], "\n",get_distribution(x)[2], "\n+++++\n\n"
        for y in output:
            log.write(str(y))

#%% Statistik
with open ('Ergebnisse/Statistik.txt', 'w') as log:
    for x in data.columns:
        output = get_stats(x)[0], "\n",get_stats(x)[1], "\n",get_stats(x)[2], "\n+++++\n\n"
        for y in output:
            log.write(str(y))
            
 """
