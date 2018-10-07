#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 13:02:04 2018

@author: psylekin
"""

import os as os
import matplotlib.pyplot as plt
import pandas as pd


def create_report():
    with open ('Ergebnisse/Bericht.txt', 'w') as log:
        for variable in data.columns:
            try:
                log.write(write_report_by_type(variable))
            except:
                print("Fehler bei: "+variable)
    print("I´m not finished")
    
def write_report_by_type(variable):
    if gettype(variable) == "TEXT":
        report = write_text_report(variable)
    elif gettype(variable) == "ORDINAL":
        report = write_ordinal_report(variable)
    elif gettype(variable) == "NOMINAL":
        report = write_nominal_report(variable)
    elif gettype(variable) == "DICHOTOMOUS":
        report = write_dichotomous_report(variable)
    else:
        print("Error: Type was not found!")
    return report
        
def gettype(variable):
    type = metaData.loc[variable,"TYPE"]
    return type

def write_text_report(variable):
    report = 'Text report\n'
    report = write_header(variable)
    for i, answer in enumerate(data.loc[:,variable].dropna()): #doesn´t show nans
        report += "{}) {}\n".format(i,answer)
    return report

def write_ordinal_report(variable):
    #Testing with BA01_01
    report = write_header(variable)
    report += report_mean_and_std(variable)
    #report += report_value_meanings()
    return report

def write_nominal_report(variable):
    report = 'Nominal report\n'
    report += write_header(variable)
    return report

def write_dichotomous_report(variable):
    report = 'Dichotomous report\n'
    report += write_header(variable)
    return report

def write_header(variable):
    header = "{}\n{}\n"
    header = header.format(metaData.loc[variable,"LABEL"].encode('utf-8'), #I don´t know why this is necessary!
                           metaData.loc[variable,"QUESTION"])
    return header

def report_mean_and_std(variable):
    report = "Mittelwert: {}\nStd: {}\n".format(get_mean(variable),get_std(variable))
    return report

def get_mean(variable):
    mean = data.loc[:,variable].mean()
    return mean

def get_std(variable):
    std = data.loc[:,variable].std()
    return std

def create_named_dataframe():
    namedDataframe = data.replace(numbersToTextDict)
    
    return namedDataframe
    
def create_numbersToTextDict():
    numbersToTextDict = dict()
    
    for variable in answerCodes.index.unique():
        variable_meaning = answerCodes.loc[answerCodes.index == variable,"RESPONSE":].set_index("RESPONSE").to_dict()
        variable_meaning[variable] = variable_meaning.pop("MEANING")
        numbersToTextDict.update(variable_meaning)
        
    return numbersToTextDict

def delete_uninteresting_variables(data, metaData):
    data = data.iloc[:,6:-23]
    metaData = metaData.iloc[6:-23,:]
    return data, metaData

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

#%% Vorbereitung
create_folder("Ergebnisse")
create_folder("Ergebnisse/Bilder")

dataFileLocations = [
            "data_Mitarbeiter-Feedback_2018-09-13_10-31.csv",
            "values_Mitarbeiter-Feedback_2018-09-13_10-31.csv",
            "variables_Mitarbeiter-Feedback_2018-09-13_10-31.csv"]

na_values = ["nicht beantwortet", "nan", -9]

data = pd.read_csv(dataFileLocations[0], encoding='utf-16', sep = "\t", na_values=na_values)
answerCodes = pd.read_csv(dataFileLocations[1], encoding='utf-16', sep = "\t").set_index("VAR")
metaData = pd.read_csv(dataFileLocations[2], encoding='utf-16', sep = "\t").set_index("VAR").drop("INPUT",axis = 1)

data, metaData = delete_uninteresting_variables(data, metaData)
numbersToTextDict = create_numbersToTextDict()
namedDataframe = create_named_dataframe()

create_report()
"""
#%%

with open ('Ergebnisse/Verteilung.txt', 'w') as log:
    for variable in data.columns:
        output = "{} - {} \n {} \n {} \n\n"
        log.write(output.format(variable, 
                                metaData.loc[variable,"LABEL"].encode('utf-8'), 
                                metaData.loc[variable,"QUESTION"],
                                data.loc[:,variable].value_counts().sort_index()))


#%%


#%% Grafiken
plt.figure(figsize=(20, 10))
for x in data.columns:
    target = data.loc[:, x].value_counts().sort_index()
    target.plot.bar(width=1, title=data.loc[:, x].name)
    plt.savefig('Ergebnisse/Bilder/' + str(data.loc[:, x].name) + '.png')
    plt.clf()
            
 """
