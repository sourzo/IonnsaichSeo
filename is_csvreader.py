# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 17:55:11 2023

@author: Zoe
"""

import csv
def read_csv(filename):
    """Read a csv file and return it as a list of dictionaries:
    where each list item is a row of the csv file"""
    with open(f"Vocabulary/{filename}.csv", 'r', encoding = "utf-8") as infile:
        return [x for x in csv.DictReader(infile)]

def rename_column(vocablist, oldname, newname):
    """Rename a column - note this changes the order of the columns,
    but if this is a problem we can switch to using OrderedDict."""
    for index, row in enumerate(vocablist):
        vocablist[index][newname] = vocablist[index].pop(oldname)

def filter_matches(vocablist, colname, matchword):
    """Create a new vocab list where values in the 
    specified column match the specified matchword"""
    return [x for x in vocablist if x[colname] == matchword]

def filter_rows(vocablist, rowlist):
    """Filter the vocab list by row numbers"""
    newlist = []
    for x in rowlist:
        newlist.append(vocablist[x])
    return newlist

def getcol(vocablist, colname):
    return [x[colname] for x in vocablist]
