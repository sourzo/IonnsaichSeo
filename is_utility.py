# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:30:28 2022

@author: Zoe
"""

import pandas as pd
import random as rd
import re

#-----------------
#General stuff----
#-----------------
def encourage():
    """Print a random encouraging phrase in Gaelic and English"""
    encouragements = pd.read_csv('Vocabulary/conversation_encouragement.csv')
    choose = rd.randint(0, len(encouragements)-1)
    print(encouragements.loc[choose,"gaelic"].capitalize()+"!",
          encouragements.loc[choose,"english"].capitalize()+"!")

vowels = ["a","e","i","o","u",
          "à","è","ì","ò","ù",
          "á","é","í","ó","ú"]
broad_vowels = ["a","o","u","à","ò","ù","á","ó","ú"]
slender_vowels = ["e","i","è","ì","é","í"]
def_articles = ("an ", "na ", "a' ", "a’ ", "am ", "an t-")

#--------------------
#Helper functions----
#--------------------
def extract_firstword(string):
    """Extract the first word from a string, using space and - as delimiters
    Examples:
        an t-seòmar -> an + t-seomar
        an taigh beag -> an + taigh beag
        taigh-beag -> taigh + beag"""
    split_st = re.split("-| ", string, maxsplit=1)
    if len(split_st) == 2:
        s1 = split_st[0]
        s2 = " " + split_st[1]
    else:
        s1 = string.lower()
        s2 = ""
    return (s1, s2)

def end_width(word):
    w = word.lower()
    test = [char for char in w if char in vowels]
    if test[-1] in broad_vowels:
        return "broad"
    elif test[-1] in slender_vowels:
        return "slender"

def remove_articles(word):
    if word.startswith(def_articles):
        stripword = word[3:]
        if stripword.startswith("t-"):
            stripword = stripword[2:]
        return stripword
    else:
        return word

def guess_gender(word):
    """Note this does not always guess correctly -
    words starting 'an ' + (d,l,r,n,sg,sp,st,sm)
    might be masc or fem, so it tries to guess without the article.
    Also it does not check context (eg does it describe a person, is it a country)"""
    w = word.lower().strip()
    #definite articles may help
    if w.startswith(def_articles):
        if any((w.startswith(("a' ", "an fh")),
                w.startswith("an t-s") and w[6] in vowels + ["l","r","n"],
                w.startswith("an ") and w[3] in vowels)):
            return "fem"
        else:
            return guess_gender(remove_articles(w))
    #no definite articles
    else:
        w1, w2 = extract_firstword(w)
        if any((w1.endswith(("ag","achd")),
                w1 == "cailleach")):
            return "fem"
        elif w1 in ("caraid","nàmhaid"):
            return "masc"
        elif end_width(w1) == "slender":
            return "fem"
        else: #broad endings not otherwise specified
            return "masc"

#------------------
#Gaelic grammar----
#------------------

##Note - some of these things assume a 'word' not a string. Might need to put error message in.

def lenite(word):
    """lenite words"""
    w = word.lower()
    if w[0] not in ("l","n","r","a","e","i","o","u","à","è","ì","ò","ù"):
        if w[0:2] not in ("sm","st","sg","sp"):
            if w[1] != "h":
                word = word[0] + "h" + word[1:]
            
    return word

def lenite_dt(word):
    """lenite words - but not d and t words"""
    w = word.lower()
    if w[0] not in ("d","t","l","n","r","a","e","i","o","u","à","è","ì","ò","ù"):
        if w[0:2] not in ("sm","st","sg","sp"):
            if w[1] != "h":
                word = word[0] + "h" + word[1:]
    return word

def slenderise(word):
    """This is not perfect, even with the exceptions -
    I am not sure whether to do some general rules, eg '...each' -> '...ich'...
    ... also do this before lenition because of list matching."""
    ##Only slenderise the first word in the string
    w1, w2 = extract_firstword(word)
    ##Only slenderise broad words
    if end_width(w1) == "broad":
        ##Some words are exceptions to the usual slenderisation rules
        slender_exceptions = pd.read_csv('Vocabulary/grammar_slenderisation.csv')
        exceptions = list(slender_exceptions["broad"])
        if w1 in exceptions:
            return slender_exceptions.loc[exceptions.index(w1),"slender"] + w2
        ##Regular slenderisation is adding an i after last vowel
        else:
            bv = [char for char in w1 if char in broad_vowels]
            i_pos = w1.rfind(bv[-1]) + 1
            if i_pos <= len(w1):
                return word[:i_pos] + "i" + word[i_pos:] + w2
            else:
                return word
    else:
        return word

def anm(word):
    """add 'an' or 'am' to the front of a word depending on its first letter"""
    if word[0] in ("b","m","f","p"):
        word = "am " + word
    else:
        word = "an " + word
    return word

def art_standard(word):
    """The common article pattern used for singular nom-fem, prep, and poss-masc."""
    if word[0].lower() in ("b","c","g","m","p"):
        return "a' " + lenite_dt(word)
    elif word[0].lower() == "s":
        if word[1].lower() in vowels + ["l","n","r"]:
            return "an t-" + word
    elif word[0].lower() == "f":
        return "an fh" + word[1:]
    else:
        return anm(word)

def gd_common_article(word,sg_pl,gender,case):
    """Add the common article ('the' in English) to a Gaelic word with no article
    sg_pl: sg/pl (singular or plural)
    gender: masc/fem
    case: nom/poss/prep (nominative, possessive, prepositional)
    (no vocative - slenderisation can't be automated) """
    
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

def prep_def(df,row_num):
    """Turn a word with the definite article into prepositional"""
    ##get word
    word = df.loc[row_num,"nom_sing"]
    ##get gender
    gender = df.loc[row_num,"gender"]
    if gender not in ("masc", "fem"):
        gender = guess_gender()
    ##get sing/pl
    if word.startswith("na "):
        sg_pl = "pl"
    else:
        sg_pl = "sg"
    ##get prepositional form depending on gender
    if gender == "masc":
        word = remove_articles(word)
        word = gd_common_article(word, sg_pl, "masc", "prep")
    elif gender == "fem":
        word = remove_articles(word)
        word = slenderise(word)
        word = gd_common_article(word, sg_pl, "masc", "prep")
    return word

#------------------
#English grammar---
#------------------

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

def en_verb(pronoun, word):
    if pronoun.lower() in ("he", "she", "name"):
        return word + "s"
    else:
        return word