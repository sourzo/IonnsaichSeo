# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:30:28 2022

@author: Zoe
"""

import random as rd
from sys import platform
import re #regex
import is_csvreader as csvr

en = csvr.read_csv('grammar_english')
numlist = csvr.read_csv('grammar_numbers')
encouragements = csvr.read_csv('conversation_encouragement')
#---------------
#Definitions----
#---------------

vowels = set("aàáeèéiìíoòóuùú")
broad_vowels = set("aàáoòóuùú")
slender_vowels = set("eèéiìí")
labials = set("bmfp")
never_lenite = tuple(vowels) + ("l","r","n","sm","st","sg","sp")
dentals = tuple("dt")
def_articles = tuple(("an ", "na ", "a' ", "a’ ", "am ", "an t-"))

irreg_past = {"rach" : ["chaidh", "deach"],
              "abair" : ["thuirt", "tuirt"],
              "dèan" : ["rinn", "do rinn"],
              "cluinn" : ["chuala", "cuala"],
              "faic" : ["chunnaic", "faca"],
              "thig" : ["thàinig", "tàinig"],
              "thoir" : ["thug", "tug"],
              "ruig" : ["ràinig", "do ràinig"],
              "beir" : ["rug", "do rug"],
              "faigh" : ["fhuair", "d' fhuair"],
              "bi" : ["bha", "robh"]}
irreg_future = {"rach" : ["thèid", "tèid"],
                "abair" : ["canaidh", "can"],
                "dèan" : ["nì", "dèan"],
                "faic" : ["chì", "faic"],
                "thig" : ["thig", "tig"],
                "thoir" : ["bheir", "toir"],
                "faigh" : ["gheibh", "faigh"],
                "bi" : ["bidh", "bi"]}

#---------------------
#General functions----
#---------------------
async def user_input(prompt):
    """This is useful for the browser implementation where asynchronous input is needed
    Note: all ancestor functions need to be asynchronous"""
    if platform == "emscripten":
        import js
        return await js.user_input(prompt)
    else:
        return input(prompt)
    
def encourage():
    """Print a random encouraging phrase in Gaelic and English"""
    choose = rd.randint(0, len(encouragements)-1)
    print(encouragements[choose]["gaelic"].capitalize()+"!",
          encouragements[choose]["english"].capitalize()+"!")


#--------------------
#Helper functions----
#--------------------
def extract_firstword(string):
    """Separate the first word from a string, using space and '-' as delimiters
    Examples:
        an t-seòmar -> an + t-seomar
        an taigh beag -> an + taigh beag
        taigh-beag -> taigh + beag"""
    split_st = re.split("-| ", string, maxsplit=1)
    if len(split_st) == 2:
        s1 = split_st[0]
        s2 = " " + split_st[1]
    else:
        s1 = string
        s2 = ""
    return (s1, s2)

def end_width(word):
    """Does a word end with a broad or slender vowel?"""
    w = word.lower()
    test = [char for char in w if char in vowels]
    if test[-1] in broad_vowels:
        return "broad"
    elif test[-1] in slender_vowels:
        return "slender"

def contains_articles(vocab_sample):
    """Checks if a vocab file contains definite articles in the nom_sing/place_gd column.
    You can't add the definite article to place-names if they don't already have a def art."""
    if "nom_sing" in vocab_sample[0]:
        colname = "nom_sing"
    elif "place_gd" in vocab_sample[0]:
        colname = "place_gd"
    for entry in vocab_sample:
        if entry[colname].lower().startswith(def_articles):
            return True
    return False

def remove_articles(word):
    """Remove the definite article from a word"""
    if word.lower().startswith(def_articles):
        stripword = word.split(" ", maxsplit=1)[1]
        if stripword.lower().startswith("t-"):
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
                w.startswith("an t-s") and w[6] in vowels.union(set("lrn")),
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

def lenite(word, extras = ()):
    """lenite words - can add other letters which should not lenite, eg dentals"""
    w = word.lower()
    if not w.startswith(never_lenite + extras):
            if w[1] != "h":
                word = word[0] + "h" + word[1:]
    return word

def slenderise(word):
    """This is not perfect, even with the exceptions -
    I am not sure whether to do some general rules, eg '...each' -> '...ich'...
    ... also do this before lenition because of list matching for exceptions."""
    ##Only slenderise the first word in the string
    w1, w2 = extract_firstword(word)
    ##Only slenderise broad words
    if end_width(w1) == "broad":
        ##Some words are exceptions to the usual slenderisation rules
        slender_exceptions = csvr.read_csv('grammar_slenderisation')
        exceptions = slender_exceptions["broad"]
        if w1 in exceptions:
            return slender_exceptions[exceptions.index(w1)]["slender"] + w2
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

def shorten(word):
    """Removes the last set of vowels from a word, and changes nn to n"""
    if word.endswith(("il","in","ir")):
        consonants = [char for char in word if char not in vowels]
        cut_pos = word.rfind(consonants[-2]) + 1
        return word[:cut_pos] + word[-1]
    elif word.endswith(("inn")):
        consonants = [char for char in word if char not in vowels]
        cut_pos = word.rfind(consonants[-3]) + 1
        return word[:cut_pos] + "n"
    else:
        return word

def anm(word):
    """add 'an' or 'am' to the front of a word depending on its first letter"""
    w = word.lower()
    if w.startswith(def_articles) == False:
        if w[0] in labials:
            word = "am " + word
        else:
            word = "an " + word
    return word

def cha(word):
    """Add 'cha' or 'chan' to the front of a word"""
    w = word.lower()
    if w[0] in vowels:
        word = "chan " + word
    elif w[0] == "f" and w[1] in vowels:
        word = "chan fh" + word[1:]
    else:
        word = "cha " + lenite(word, extras = dentals)
    return word

def digits_to_gd(n):
    num_unit = str(n)[-1]
    num_unit_gd = csvr.filter_matches(numlist, "number", num_unit)[0]["cardinal"]
    if n <= 10: # 0-9
        return csvr.filter_matches(numlist, "number", str(n))[0]["cardinal"]
    elif n == 12:
        return "dà dheug" #lenition
    elif n < 20: #11-19
        return num_unit_gd + " deug"
    elif n < 100: #20-99
        num_ten = str(n)[-2] + "0"
        num_ten_gd = csvr.filter_matches(numlist, "number", num_ten)[0]["cardinal"]
        if num_unit == "0":
            return num_ten_gd
        else:
            if num_unit in ("1","8"):
                return num_ten_gd + " 's a h-" + num_unit_gd
            else:
                return num_ten_gd + " 's a " + num_unit_gd

def art_standard(word):
    """The common article pattern used for singular nom-fem, prep, and gen-masc."""
    w = word.lower()
    if w[0] in {"b","c","g","m","p"}:
        return "a' " + lenite(word, dentals)
    elif w[0] == "s":
        if w[1] in vowels.union({"l","n","r"}):
            return "an t-" + word
        else:
            return "an " + word #Does this lenite??
    elif w[0] == "f":
        return "an " + lenite(word)
    else:
        return anm(word)

def gd_common_article(word,sg_pl,gender,case):
    """Add the common article ('the' in English) to a Gaelic word with no article
    sg_pl: sg/pl (singular or plural)
    gender: masc/fem
    case: nom/gen/prep (nominative, genitive, prepositional)
    (no vocative - slenderisation can't be automated) """
    word = remove_articles(word)
    word_lower = word.lower()
    #singular
    if sg_pl == "sg":
        
        #nominal case
        if case == "nom":
            #masculine
            if gender == "masc":
                if word_lower[0] in labials:
                    word = "am " + word
                elif word_lower[0] in vowels:
                    word = "an t-" + word
                else:
                    word = anm(word)
            #feminine
            elif gender == "fem":
                word = art_standard(word)
                
        #genitive case
        elif case == "gen":
            #masculine
            if gender == "masc":
                word = art_standard(word)
            #feminine
            elif gender == "fem":
                if word_lower[0] in vowels:
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
        
        #genitive
        if case == "gen":
            if word_lower[0] in labials:
                word = "nam " + word
            else:
                word = "nan " + word

        #nominal & prepositional
        else:
            if word_lower[0] in vowels:
                word = "na h-" + word
            else:
                word = "na " + word
                
    return word

def prep_def(df,row_num):
    """Turn a word with the definite article into prepositional"""
    ##get word
    word = df[row_num]["nom_sing"]
    word_lower = word.lower()
    ##get gender
    gender = df[row_num]["gender"]
    if gender not in ("masc", "fem"):
        gender = guess_gender(word_lower)
    ##get sing/pl
    if word_lower.startswith("na "):
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

def transform_verb(root, tense, negative, question):
    """Simple past/future tense of a verb"""
    root = root.lower()
    if tense == "past":
        if root in irreg_past:
            if question == False and negative == False:
                ##Primary form
                verb = irreg_past[root][0]
            else:
                #Secondary form
                verb = irreg_past[root][1]
        else:
            #regular past
            if root[0] in vowels:
                verb = "dh'" + root
            elif root[0] == "f" and root[1] in vowels:
                verb = "dh'fh" + root[1:]
            else: 
                verb = lenite(root)
            #secondary form
            if question == True or negative == True:
                verb = "do " + verb
    
    elif tense == "future":
        if root in irreg_future:
            if question == False and negative == False:
                ##Primary form
                verb = irreg_future[root][0]
            else:
                #Secondary form
                verb = irreg_future[root][1]
        else:
            #regular future
            if question == False and negative == False:
                #primary form
                if end_width(root) == "broad":
                    verb = root + "aidh"
                else:
                    verb = shorten(root) + "idh" #some slender-ended verbs need shortening
            else:
                #secondary form
                if question == False:
                    verb = lenite(root)
                else:
                    verb = root
    elif tense == "present":
        if root == "bi":
            if question == False and negative == False:
                #primary form
                verb = "tha"
            else:
                #secondary form
                verb = "eil"
    
    ##Negative prefixes
    if negative == True:
        if question == True:
            if verb == "faca":
                verb = "nach fhaca"
            else:
                verb = "nach " + verb
        else:
            verb = cha(verb)
    
    #Positive prefixes
    else:
        if question == True:
            if verb != "eil":
                verb = anm(verb)
            else:
                verb = "a bh" + verb
    return verb

def verbal_noun(vn, person, tense, negative, question):
    if tense in ("vn_past", "vn_future"):
        tense = tense[3:]
    """Verbal noun tense of given verb, vn.
    Input must be the verbal noun form."""
    bi = transform_verb("bi", tense, negative, question)
    if vn[0] in vowels:
        vn = "ag " + vn
    else:
        vn = "a' " + vn
    return bi + " " + person + " " + vn

def relative_time(relative_en, time_unit_en):
    """Last/this/next/(all)/every day/month/year etc
    Note the time unit must be in the datetime units csv
    This function is unfinished and unused"""
    #gd_common_article(word,sg_pl,gender,case)
    print("Warning - the relative time function is unfinished")
    time_units = csvr.read_csv("datetime_units")
    gender = csvr.filter_matches(time_units, "english", time_unit_en)[0]["gender"]
    time_unit_gd = csvr.filter_matches(time_units, "english", time_unit_en)[0]["nom_sing"]
    if relative_en == "last":
        when_gd = gd_common_article(time_unit_gd, "sg", gender, "nom") + " seo chaidh"
    elif relative_en == "this":
        when_gd = gd_common_article(time_unit_gd, "sg", gender, "nom") + " seo"
    elif relative_en == "next":
        when_gd = "an ath " + lenite(time_unit_gd)
    #elif relative_en == "all":   #Genitive case - I'll do this when I've learned it
    #    when_gd = ""
    elif relative_en == "every":
        if time_unit_gd[0] in vowels:
            time_unit_gd = "h-" + time_unit_gd
        when_gd = "a h-uile " + time_unit_gd
    return when_gd

#------------------
#English grammar---
#------------------

def en_indef_article(word):
    """Add a/an to a word (using vowels)
    Note, a/an is applied in English by sound rather than spelling,
    so this will be wrong sometimes (eg "an unicorn")
    """
    if word[0] in vowels:
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
    elif word[-1] == "y" and word[-2] not in vowels:
        return word[0:-1] + "ies"
    elif word[-6:] == "person":
        return word[:-6] + "people"
    elif word[-5:] == "child":
        return word[:-5] + "children"
    elif word[-3:] == "man":
        return word[:-3] + "men"
    elif word[-1] in ("s","x","z") or (word[-2:] in ("sh","ch") and word != "stomach"):
        return word + "es"
    elif word[-1] == "o" and word[-2] not in vowels:
        return word + "es"
    elif word[-2:] == "fe":
        return word[:-2] + "ves"
    elif word[-1] == "f" and word[-2] != "f" and word not in ("roof", "chef", "belief", "chief"):
        return word[:-1] + "ves"
    else:
        return word + "s"

def en_verb(vocab_sample, item, pronoun, tense, negative, question):
    global en
    
    if question == False:
        if negative == True:
            neg = " not "
        else:
            neg = " "

        if tense == "present":
            return pronoun + " " + csvr.filter_matches(en, "en_subj", pronoun)[0]["be_pres"] + neg + vocab_sample[item]["en_vn"]
        elif tense == "past":
            if negative == False:
                return pronoun + " " + vocab_sample[item]["en_past"]
            else:
                return pronoun + " did not " + vocab_sample[item]["english"]
        elif tense == "vn_past":
            return pronoun + " " + csvr.filter_matches(en, "en_subj", pronoun)[0]["be_past"] + neg + vocab_sample[item]["en_vn"]
        elif tense == "future":
            return pronoun + " will" + neg + vocab_sample[item]["english"]
        elif tense == "vn_future":
            return pronoun + " will" + neg + "be " + vocab_sample[item]["en_vn"]
    else:
        if negative == True:
            neg = "n't "
        else:
            neg = " "

        if tense == "present":
            if pronoun.lower() == "i" and negative == True:
                return "Aren't " + pronoun + " " +  vocab_sample[item]["en_vn"]
            else:
                return csvr.filter_matches(en, "en_subj", pronoun)[0]["be_pres"] + neg + pronoun + " " +  vocab_sample[item]["en_vn"]
        elif tense == "past":
            return "Did" + neg + pronoun + " " + vocab_sample[item]["english"]
        elif tense == "vn_past":
            return csvr.filter_matches(en, "en_subj", pronoun)[0]["be_past"] + neg + pronoun + " " +  vocab_sample[item]["en_vn"]
        else:
            if negative == True:
                start = "Will "
            else:
                start = "Won't "
            if tense == "future":
                return start + pronoun + " " + vocab_sample[item]["english"]
            elif tense == "vn_future":
                return start + pronoun + " be " + vocab_sample[item]["en_vn"]
