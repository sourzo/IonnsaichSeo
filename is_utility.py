# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:30:28 2022

@author: Zoe
"""
#General stuff----
def encourage():
    """Print a random encouraging phrase in Gaelic and English"""
    import pandas as pd
    import random as rd
    encouragements = pd.read_csv('Vocabulary/conversation_encouragement.csv')
    choose = rd.randint(0, len(encouragements)-1)
    print(encouragements.loc[choose,"gaelic"].capitalize()+"!",
          encouragements.loc[choose,"english"].capitalize()+"!")

#Gaelic grammar----
def lenite(word):
    """lenite words"""
    if word[0].lower() not in ("l","n","r","a","e","i","o","u","à","è","ì","ò","ù"):
        if word[0:2].lower() not in ("sm","st","sg","sp"):
            word = word[0] + "h" + word[1:]
            
    return word

#English grammar---
def indef_article(word):
    if word[0] in ("a","e","i","o","u"):
        obj_indef = "an " + word
    else:
        obj_indef = "a " + word
    return obj_indef
