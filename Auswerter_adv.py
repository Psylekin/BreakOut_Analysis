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
        for variable in metaData.index:
            try:
                log.write(write_report_by_type(variable))
            except Exception as e:
                errormassage = "Fehler bei: {}\n {}\n"
                print(errormassage.format(variable, e))
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

def write_absolut_distribution(variable):
    report = str(get_absolut_distribution(variable))
    report = remove_last_line_from_string(report)
    report = remove_first_line_from_string(report)
        
    return report

def get_absolut_distribution(variable):
    distribution = data.loc[:,variable].value_counts()
    meaning = pd.Series(numbersToTextDict[variable])
    
    result = pd.DataFrame(meaning).join(distribution, how = 'outer')
    result.columns = ["meaning", "distribution"]
    result.meaning = result.meaning.fillna('-')
    result.distribution = result.distribution.fillna(0)
    
    return result

def remove_last_line_from_string(string):
    return string[:string.rfind('\n')]

def remove_first_line_from_string(string):
    return string[string.find('\n'):]

def get_label(variable):
    label = metaData.loc[variable,"LABEL"] 
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
    
def create_numbersToTextDict():
    numbersToTextDict = dict()
    
    for variable in answerCodes.index.unique():
        variable_meaning = answerCodes.loc[answerCodes.index == variable,"RESPONSE":]
        variable_meaning = variable_meaning.set_index("RESPONSE").to_dict()
        variable_meaning[variable] = variable_meaning.pop("MEANING")
        numbersToTextDict.update(variable_meaning)
        
    return numbersToTextDict

def delete_system_variables(data, metaData):
    kriteria_for_deletion = list(metaData.loc[:,"INPUT"] != "SYSTEM")
    
    data = data.iloc[:,kriteria_for_deletion]
    metaData = metaData.iloc[kriteria_for_deletion,:]
    
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
    absolutDistribution.index = absolutDistribution.meaning
    
    absolutDistribution.distribution.plot.bar(rot= 30, 
                                 figsize=(18,10),
                                 title = get_question(variable))
    plt.suptitle(get_label(variable))
    plt.savefig('Ergebnisse/Bilder/' + variable + '.png')
    plt.close()
    



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
metaData = pd.read_csv(dataFileLocations[2], encoding='utf-16', sep = "\t").set_index("VAR")

data, metaData = delete_system_variables(data, metaData)
numbersToTextDict = create_numbersToTextDict()

create_txt_report()
create_barplots()

#TODO: Get SosciSurvey-Data in UTF-8 !!!

print("Done!")