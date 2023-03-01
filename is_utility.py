# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 17:30:28 2022

@author: Zoe
"""

import pandas as pd
import random as rd
from os import listdir
import re #regex
en = pd.read_csv('Vocabulary/grammar_english.csv')

#---------------
#Definitions----
#---------------
required_columns = {"give_get" : ("english", "nom_sing"),
                    "possession_aig" : ("english", "nom_sing"),
                    "gender" : ("english", "nom_sing", "gender"),
                    "numbers" : ("english", "nom_sing", "nom_pl"),
                    "learn_nouns" : ("english", "nom_sing"),
                    "preferences" : ("english", "nom_sing"),
                    "verb_tenses" : ("english", "en_past", "en_vn", "root", "verbal_noun"),
                    "professions_annan" : (),
                    "emphasis_adjectives" : ("english", "adj_gd"),
                    "possession_mo" : ("english", "nom_sing", "nom_pl"),
                    "where_from" : ("english", "nom_sing", "gender"),
                    "where_in" : ("english", "nom_sing", "gender"),
                    "comparisons" : (),
                    "comparatives_superlatives": ("english", "nom_sing", "gender")}

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
    """This is useful for the browser implementation where asynchronous input is needed"""
    return input(prompt)
    
def encourage():
    """Print a random encouraging phrase in Gaelic and English"""
    encouragements = pd.read_csv('Vocabulary/conversation_encouragement.csv')
    choose = rd.randint(0, len(encouragements)-1)
    print(encouragements.loc[choose,"gaelic"].capitalize()+"!",
          encouragements.loc[choose,"english"].capitalize()+"!")

def check_vocab(lesson_name, vocab_sample, messages = True):
    """Check that the chosen vocab file has the right columns for the lesson"""

    list_ok = True
    if len(required_columns[lesson_name]) > 0:
        for column in required_columns[lesson_name]:
            if column not in vocab_sample.columns:
                list_ok = False
                if messages == True:
                    print()
                    print("Error: Chosen vocabulary list must contain column {} (lower-case)".format(column))
    if list_ok == False and messages == True:
        print("Try another vocabulary list or add the required columns and try again")
    return list_ok

async def select_vocab(lesson, options):
    """Select vocabulary file to use in lesson"""
    if len(required_columns[lesson.__name__]) == 0:
        return pd.DataFrame() #no vocab file needed
    elif lesson.__name__ == "numbers" and options["num_mode"] in ("1","2"):
            return pd.DataFrame({"a" : [1]}) #dummy vocab file
    elif lesson.__name__ == "possession_mo":
        vocab_num = ""
        while vocab_num not in ("x","1","2","3"):
            print()
            print("Select topic")
            print("1: Body parts")
            print("2: Clothes")
            print("3: Family")
            print("X: Exit")
            vocab_num = (await user_input("Practice mode: ")).lower().strip()
        if vocab_num == "x":
            return "x"
        elif vocab_num == "1":
            return pd.read_csv('Vocabulary/people_body.csv')
        elif vocab_num == "2":
            return pd.read_csv('Vocabulary/people_clothes.csv')
        elif vocab_num == "3":
            return pd.read_csv('Vocabulary/people_family.csv')
    elif lesson.__name__ == "where_from":
        vocab_num = ""
        while vocab_num not in ("x","1","2"):
            print()
            print("Select geography")
            print("1: Countries")
            print("2: Places in Scotland")
            print("X: Exit")
            vocab_num = (await user_input("Practice mode: ")).lower().strip()
        if vocab_num == "x":
            return "x"
        elif vocab_num == "1":
            return pd.read_csv('Vocabulary/places_world.csv')
        elif vocab_num == "2":
            return pd.read_csv('Vocabulary/places_scotland.csv')
    elif lesson.__name__ == "where_in":
        vocab_num = ""
        while vocab_num not in ("x","1","2","3","4"):
            print()
            print("Select places")
            print("1: Countries")
            print("2: Places in Scotland")
            print("3: Around town")
            print("4: In the house")
            print("X: Exit")
            vocab_num = (await user_input("Practice mode: ")).lower().strip()
        if vocab_num == "x":
            return "x"
        elif vocab_num == "1":
            options["contains_articles"] = True
            return pd.read_csv('Vocabulary/places_world.csv')
        elif vocab_num == "2":
            options["contains_articles"] = True
            return pd.read_csv('Vocabulary/places_scotland.csv')
        elif vocab_num == "3":
            options["contains_articles"] = False
            return pd.read_csv('Vocabulary/places_town.csv')
        elif vocab_num == "4":
            options["contains_articles"] = False
            return pd.read_csv('Vocabulary/places_home.csv')
    else:
        from os.path import exists
        vocab_file = ""
        suitable = False
        print()
        print("Name the vocabulary list to use in practice")
        print("or type 'help' to list all possible vocabulary lists")
        print("or X to exit")
        while exists("Vocabulary/{}.csv".format(vocab_file)) == False or suitable == False:
            print()
            vocab_file = (await user_input("Vocabulary list: ")).lower().strip()
            if vocab_file == "x":
                return "x"
            elif vocab_file == "help":
                suggest_vocab(lesson.__name__)
            elif exists("Vocabulary/{}.csv".format(vocab_file))==False:
                print()
                print("File not found: Check vocabulary list is a CSV file in the Vocabulary folder")
            else:
                vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
                suitable = check_vocab(lesson.__name__, vocab_list)
        return vocab_list

def suggest_vocab(lesson_name):
    allfiles = listdir("Vocabulary/")
    for filename in allfiles:
        checkfile = pd.read_csv("Vocabulary/"+filename)
        if check_vocab(lesson_name, checkfile, messages=False) == True:
            print(filename[:-4])

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
    """Does a word end with a broad or slender vowel?"""
    w = word.lower()
    test = [char for char in w if char in vowels]
    if test[-1] in broad_vowels:
        return "broad"
    elif test[-1] in slender_vowels:
        return "slender"

def remove_articles(word):
    """Remove the definite article from a word"""
    if word.startswith(def_articles):
        stripword = word.split()[1]
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


def art_standard(word):
    """The common article pattern used for singular nom-fem, prep, and gen-masc."""
    w = word.lower()
    if w[0] in {"b","c","g","m","p"}:
        return "a' " + lenite(word, dentals)
    elif w[0] == "s":
        if w[1] in vowels.union({"l","n","r"}):
            return "an t-" + w
        else:
            return "an " + w #Does this lenite??
    elif w[0] == "f":
        return "an fh" + w[1:]
    else:
        return anm(word)

def gd_common_article(word,sg_pl,gender,case):
    """Add the common article ('the' in English) to a Gaelic word with no article
    sg_pl: sg/pl (singular or plural)
    gender: masc/fem
    case: nom/gen/prep (nominative, genitive, prepositional)
    (no vocative - slenderisation can't be automated) """
    
    #singular
    if sg_pl == "sg":
        
        #nominal case
        if case == "nom":
            #masculine
            if gender == "masc":
                if word[0].lower() in labials:
                    word = "am " + word
                elif word[0].lower() in vowels:
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
        
        #genitive
        if case == "gen":
            if word[0].lower() in labials:
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
    Note the time unit must be in the datetime units csv"""
   # gd_common_article(word,sg_pl,gender,case)
    time_units = pd.read_csv("Vocabulary/datetime_units.csv")
    gender = time_units.loc[time_units["english"] == time_unit_en,"gender"].values[0]
    time_unit_gd = time_units.loc[time_units["english"] == time_unit_en,"nom_sing"].values[0]
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
    elif word[-3:] == "man":
        return word[:-3] + "men"
    elif word[-1] in ("s","x","z") or word[-2:] in ("sh","ch"):
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
            return pronoun + " " + en.loc[en["en_subj"] == pronoun,"be_pres"].values[0] + neg + vocab_sample.loc[item,"en_vn"]
        elif tense == "past":
            if negative == False:
                return pronoun + " " + vocab_sample.loc[item,"en_past"]
            else:
                return pronoun + " did not " + vocab_sample.loc[item,"english"]
        elif tense == "vn_past":
            return pronoun + " " + en.loc[en["en_subj"] == pronoun,"be_past"].values[0] + neg + vocab_sample.loc[item,"en_vn"]
        elif tense == "future":
            return pronoun + " will" + neg + vocab_sample.loc[item,"english"]
        elif tense == "vn_future":
            return pronoun + " will" + neg + "be " + vocab_sample.loc[item,"en_vn"]
    else:
        if negative == True:
            neg = "n't "
        else:
            neg = " "

        if tense == "present":
            if pronoun.lower() == "i" and negative == True:
                return "Aren't " + pronoun + " " +  vocab_sample.loc[item,"en_vn"]
            else:
                return en.loc[en["en_subj"] == pronoun,"be_pres"].values[0] + neg + pronoun + " " +  vocab_sample.loc[item,"en_vn"]
        elif tense == "past":
            return "Did" + neg + pronoun + " " + vocab_sample.loc[item,"english"]
        elif tense == "vn_past":
            return en.loc[en["en_subj"] == pronoun,"be_past"].values[0] + neg + pronoun + " " +  vocab_sample.loc[item,"en_vn"]
        else:
            if negative == True:
                start = "Will "
            else:
                start = "Won't "
            if tense == "future":
                return start + pronoun + " " + vocab_sample.loc[item,"english"]
            elif tense == "vn_future":
                return start + pronoun + " be " + vocab_sample.loc[item,"en_vn"]
