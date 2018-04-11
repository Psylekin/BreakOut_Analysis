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

data = pd.read_csv("data_Mitarbeiter-Feedback_2018-04-11_13-05.csv", encoding='utf-16', sep = "\t", na_values=["nicht beantwortet", "nan", -9])
meaning = pd.read_csv("values_Mitarbeiter-Feedback_2018-04-11_13-05.csv", encoding='utf-16', sep = "\t")
questions = pd.read_csv("variables_Mitarbeiter-Feedback_2018-04-11_13-05.csv", encoding='utf-16', sep = "\t")  
data = data.iloc[:,6:73]

#%% Testgrafik

#target = "PB01"
def plot_bar(target):
    printed = data.loc[:, target]
    name = questions.loc[questions.VAR == printed.name, "QUESTION"].values[0]
    sub_name = questions.loc[questions.VAR == printed.name, "LABEL"].values[0]
    target = printed.value_counts()
    meanings = meaning.loc[meaning.VAR == target.name, ["MEANING","RESPONSE"]]
    meanings.index = meanings.RESPONSE
    
    target = pd.DataFrame(target).join(meanings, how = "left")
    target.index = target.MEANING
    target = target.drop("MEANING", axis = 1)
    
    plt.figure(figsize=(20,10))
    plt.title(name)
    plt.suptitle(sub_name)
    plt.xlabel('Antworten')
    plt.ylabel('Häufigkeit')
    plt.xticks(rotation= 30)
    
    plt.bar(target.index, target.iloc[:,0])
    plt.savefig('Ergebnisse/Bilder/' + str(data.loc[:, x].name) + '.png')
    plt.clf()

for x in data.columns:
    try:
        plot_bar(x)
    except:
        print("Fehler bei Grafik", x)
        
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
