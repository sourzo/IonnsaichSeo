import csv
import random as rd
def read_csv(filename):
    """Read a csv file and return it as a vocab dict: a dictionary of lists,
    where each dictionary item is a column of the csv file
    and each list is the items in that column"""
    with open(f"Vocabulary/{filename}.csv", 'r', encoding = "utf-8") as infile:
        csvfile = csv.DictReader(infile)
        newdict=dict.fromkeys(csvfile.fieldnames)
        for k in newdict:
            newdict[k] = list()
        for line in csvfile:
            for key, value in line.items():
                newdict[key].append(value)
    return newdict

def rename_column(vocabdict, oldname, newname):
    vocabdict[newname] = vocabdict.pop(oldname)

def filter_matches(vocabdict, colname, matchword):
    """Create a new vocab dict where values in the 
    specified column match the specified matchword"""
    newdict = dict.fromkeys(vocabdict)
    for k in newdict:
        newdict[k] = list()
    searchlist = vocabdict[colname]
    matchlist = []
    for index, item in enumerate(searchlist):
        if item.lower() == matchword.lower():
            matchlist.append(index)
    for item in newdict:
        for index in matchlist:
            newdict[item].append(vocabdict[item][index])
    return newdict

def filter_rows(vocabdict, rowlist):
    """Create a new vocab dict where values in the 
    specified column match the specified matchword"""
    newdict = dict.fromkeys(vocabdict)
    for k in newdict:
        newdict[k] = list()
    for item in newdict:
        for index in rowlist:
            newdict[item].append(vocabdict[item][index])
    return newdict

def random_sample(vocabdict, size):
    """Create a new vocab dict which is a 
    random sample of items from the original"""
    newdict = dict.fromkeys(vocabdict)
    for k in newdict:
        newdict[k] = list()
    matchlist = rd.sample(range(length(vocabdict)), size)
    for item in newdict:
        for index in matchlist:
            newdict[item].append(vocabdict[item][index])
    return newdict

def length(vocabdict):
    """Find the number of items in a vocab dict"""
    return len(vocabdict[list(vocabdict.keys())[0]])

def firstcol(vocabdict):
    """Find the first column name in a vocab dict"""
    return list(vocabdict.keys())[0]