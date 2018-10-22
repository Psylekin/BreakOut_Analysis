#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 13:02:04 2018

@author: psylekin
"""

import os as os
import matplotlib.pyplot as plt
import pandas as pd

def create_txt_report():
    with open ('Ergebnisse/Bericht.txt', 'w') as log:
        for variable in data.columns:
            try:
                log.write(write_report_by_type(variable))
            except:
                print("Fehler bei: "+variable)
    print("Textreport created!")
    
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
    report = write_header(variable)
    for i, answer in enumerate(data.loc[:,variable].dropna()):
        report += "{}) {}\n".format(i,answer)
    report += "\n"
    return report

def write_ordinal_report(variable):
    report = write_header(variable)
    report += report_mean_and_std(variable)
    report += write_absolut_distribution(variable)
    report += "\n\n"
    return report

def write_nominal_report(variable):
    report = write_header(variable)
    report += write_absolut_distribution(variable)
    report += '\n\n'
    return report

def write_dichotomous_report(variable):
    report = write_header(variable)
    report += write_absolut_distribution(variable)
    report += '\n\n'
    return report

def write_header(variable):
    header = "{} - {}\n"
    header = header.format(get_label(variable), 
                           get_question(variable))
    return header

def get_label(variable):
    label = metaData.loc[variable,"LABEL"] #I don´t know why this is necessary!
    return label

def get_question(variable):
    question = metaData.loc[variable,"QUESTION"]
    return question

def report_mean_and_std(variable):
    report = "Mittelwert: {:03.2f}\nStd: {:03.2f}\n\n"
    report = report.format(get_mean(variable),get_std(variable))
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
        variable_meaning = answerCodes.loc[answerCodes.index == variable,"RESPONSE":]
        variable_meaning = variable_meaning.set_index("RESPONSE").to_dict()
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
        
def create_barplots():
    for variable in metaData.loc[metaData.TYPE != 'TEXT',:].index:
        try: 
            create_barplot(variable)
        except:
            print("Fehler bei: " + variable)
    print("Barplots created!")

def create_barplot(variable):
    absolutDistribution = get_absolut_distribution(variable)
    
    absolutDistribution.plot.bar(rot= 30, 
                                 figsize=(18,10),
                                 title = get_question(variable))
    plt.suptitle(get_label(variable))
    plt.savefig('Ergebnisse/Bilder/' + variable + '.png')
    plt.close()
    
def write_absolut_distribution(variable):
    report = str(get_absolut_distribution(variable))
    return report
    
def get_absolut_distribution(variable):
    graph_data = data.loc[:,variable].value_counts()
    meaning = pd.Series(numbersToTextDict[variable])
    
    result = pd.DataFrame([graph_data,meaning]).T
    result.index = result.iloc[:,1]
    result.index.name = variable
    result = result.iloc[:,0]
    result.index = result.index.fillna("-")
    result = result.fillna(0, downcast="infer")
    
    return result

#%% Programm
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

create_txt_report()
#TODO: Make value report less ugly (top and bottom line)
#TODO: Add number values to absolut distribution (otherwise you dont understand the mean and std)
create_barplots()

print("Done!")