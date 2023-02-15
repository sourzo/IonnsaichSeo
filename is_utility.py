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

def lenite_dt(word):
    """lenite words - but not d and t words"""
    if word[0].lower() not in ("d","t","l","n","r","a","e","i","o","u","à","è","ì","ò","ù"):
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

def end_width(word):
    vowels = {"a","e","i","o","u","à","è","ì","ò","ù"}
    test = [char for char in word if char in vowels]
    if test[-1] in {"a","o","u","à","ò","ù"}:
        return "broad"
    elif test[-1] in {"e","i","è","ì"}:
        return "slender"

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

def en_pl(word):
    """Turn a word into the plural form"""
    if word in ("sheep", "deer", "fish", "trousers", "glasses"):
        return word
    elif word in ("tooth", "foot", "goose"):
        return word[0] + "ee" + word[3:]
    elif word == "mouse":
        return "mice"
    elif word[-1] == "y" and word[-2] not in ("a", "e", "i", "o", "u"):
        return word[0:-1] + "ies"
    elif word[-6:] == "person":
        return word[:-6] + "people"
    elif word[-3:] == "man":
        return word[:-3] + "men"
    elif word[-1] in ("s","x","z") or word[-2:] in ("sh","ch"):
        return word + "es"
    elif word[-1] == "o" and word[-2] not in ("a", "e", "i", "o", "u"):
        return word + "es"
    elif word[-2:] == "fe":
        return word[:-2] + "ves"
    elif word[-1] == "f" and word[-2] != "f" and word not in ("roof", "chef", "belief", "chief"):
        return word[:-1] + "ves"
    else:
        return word + "s"