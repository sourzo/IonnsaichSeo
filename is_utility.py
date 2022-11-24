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

def anm(word):
    """add 'an' or 'am' to the front of a word depending on its first letter"""
    if word[0] in ("b","m","f","p"):
        word = "am " + word
    else:
        word = "an " + word
    return word

def gd_common_article(word,sg_pl,gender,case):
    """Add the common article ('the' in English) to a Gaelic word
    sg_pl: sg/pl (singular or plural)
    gender: masc/fem
    case: nom/poss/prep (nominative, possessive, prepositional)
    (no vocative - slenderisation can't be automated) """
    
    vowels = ["a","e","i","o","u","à","è","ì","ò","ù"]
    
    def art_standard(word):
        """The common article pattern used for singular nom-fem, prep, and poss-masc."""
        if word[0].lower() in ("b","c","g","m","p"):
            word = "a' " + lenite(word)
        elif word[0].lower() == "s":
            if word[1].lower in vowels + ["l","n","r"]:
                word = "an t-" + word
        else:
            word = anm(word)
        return word
    
        
    #singular
    if sg_pl == "sg":
        
        #nominal case
        if case == "nom":
            #masculine
            if gender == "masc":
                if word[0].lower() in ("b","m","f","p"):
                    word = "am " + word
                elif word[0].lower() in vowels:
                    word = "an t-" + word
                else:
                    word = anm(word)
            #feminine
            elif gender == "fem":
                word = art_standard(word)
                
        #possessive case
        elif case == "poss":
            #masculine
            if gender == "masc":
                word = art_standard(word)
            #feminine
            elif gender == "fem":
                if word[0].lower() in vowels:
                    word = "na h-" + word
                else:
                    word = "na " + word
                #blah
                
        #prepositional case
        elif case == "prep":
            #both genders
            word = art_standard(word)
                
    #plural
    elif sg_pl == "pl":
        
        #possessive
        if case == "poss":
            if word[0].lower() in ("b","m","f","p"):
                word = "nam " + word
            else:
                word = "nan " + word

        #nominal & prepositional
        else:
            if word[0].lower() in vowels:
                word = "na h-" + word
            else:
                word = "na" + word
                
    return word

#English grammar---
def en_indef_article(word):
    """Add a/an to a word (using vowels)
    Note, a/an is applied in English by sound rather than spelling,
    so this will be wrong sometimes (eg "an unicorn")
    """
    if word[0] in ("a","e","i","o","u"):
        obj_indef = "an " + word
    else:
        obj_indef = "a " + word
    return obj_indef
