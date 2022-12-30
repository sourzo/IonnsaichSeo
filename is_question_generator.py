# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:53:44 2022

@author: Zoe
"""

def give_get(vocab_file, tense, translate, sentence):
    #Load packages and vocab --------------------------------------------------
    import is_utility
    import pandas as pd
    import random as rd

    grammar_en = pd.read_csv('Vocabulary/grammar_english.csv')
    pronouns = pd.read_csv('Vocabulary/grammar_prepPronouns.csv')
    names = pd.read_csv('Vocabulary/people_names.csv')
    
    gifts = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in gifts.columns or "nom_sing" not in gifts.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return
    
    #Randomiser ---------------------------------------------------------------
    
    subject_num = rd.randrange(8)
    object_num = rd.randrange(8)
    gift_num = rd.randrange(gifts["english"].count())
    give_get_num = rd.randrange(2) # 0 = give to, 1 = get from
    
    #Parts of sentence --------------------------------------------------------
    
    #the item that's being given
    gift_en = is_utility.en_indef_article(gifts["english"][gift_num])
    gift_gd = gifts["nom_sing"][gift_num]
    
    #giving to (give_get_en, give_get_gd)
    if give_get_num == 0:
        if tense == "1":
            give_get_en = grammar_en["be_pres"][subject_num] + " giving"
            give_get_gd = "a' toirt"
        elif tense == "2":
            give_get_en = "gave"
            give_get_gd = "thug"
        elif tense == "3":
            give_get_en = "will give"
            give_get_gd = "bheir"
        prep_en = "to"
        
    #getting from (give_get_en, give_get_gd)
    elif give_get_num == 1:
        if tense == "1":
            give_get_en = grammar_en["be_pres"][subject_num] + " getting"
            give_get_gd = "a' faighinn"
        elif tense == "2":
            give_get_en = "got"
            give_get_gd = "fhuair"
        elif tense == "3":
            give_get_en = "will get"
            give_get_gd = "gheibh"
        prep_en = "from"
        
    #subject: pronouns (subject_en, subject_gd)
    if subject_num < 7:
        subject_en = pronouns["en_subj"][subject_num]
        subject_gd = pronouns["pronoun_gd"][subject_num]
    #subject: names
    elif subject_num == 7:
        name = rd.randrange(names["english"].count())
        subject_en = names["english"][name]
        subject_gd = names["nom_sing"][name]
        
    #object: pronouns / names (object_en, object_gd)
    if object_num < 7:
        object_en = grammar_en["en_obj"][object_num]
        #Prep pronouns for do/bho
        if give_get_num==0:
            object_gd = pronouns["do"][object_num]
        else:
            object_gd = pronouns["bho"][object_num]
    #names
    elif object_num == 7:
        name = rd.randrange(names["english"].count())
        object_en = names["english"][name]
        lenited_name = is_utility.lenite(names["nom_sing"][name])
        if give_get_num==0:
            if lenited_name[0].lower() in ("a","e","i","o","u","à","è","ì","ò","ù"):
                object_gd = "do dh'" + lenited_name
            elif lenited_name[0:2] == "fh":
                object_gd = "do dh'" + lenited_name
            else:
                object_gd = "do " + lenited_name
        elif give_get_num==1:
            object_gd = "bho " + lenited_name
       
    #Construct sentences ------------------------------------------------------
    
    #English
    if give_get_num == 0:
        sentence_en = subject_en.capitalize() + " " + give_get_en + " " + object_en + " " + gift_en
        sentence_en_alt = subject_en.capitalize() + " " + give_get_en + " " + gift_en + " " + prep_en + " " + object_en
    elif give_get_num == 1:
       sentence_en = subject_en.capitalize() + " " + give_get_en + " " + gift_en + " " + prep_en + " " + object_en
    #Gaelic
    if tense == "1": #Gaelic - with verbal noun
        sentence_gd = "Tha " + subject_gd + " " + give_get_gd + " " + gift_gd + " " + object_gd
    
    elif tense in ("2", "3"):  #Past / Future tense sentences
        #Gaelic
        sentence_gd = give_get_gd.capitalize() + " " + subject_gd + " " + gift_gd + " " + object_gd

    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
    elif translate == "2": #gd-en
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        prompt1 = ""
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            if tense == "1": #Present tense with verbal noun
                prompt1 = "Tha " + subject_gd + " " + give_get_gd + " " + gift_gd + " "
            #Past / Future tense sentences
            elif tense in ("2", "3"):
                prompt1 = give_get_gd.capitalize() + " " + subject_gd + " " + gift_gd + " "
        elif translate == "2": #gd-en
            prompt1 = subject_en.capitalize() + " " + give_get_en + " " + gift_en + " "
            
    #Solutions ----------------------------------------------------------------
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            sol1 = sentence_gd
        elif translate == "2": #gd-en
            sol1 = sentence_en
            sol2 = sentence_en_alt
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            sol1 = object_gd
        elif translate == "2": #gd-en
            sol1 = prep_en + " " + object_en
            sol2 = sol1
            
    #Output -------------------------------------------------------------------
    
    #Return (question, main solution, alternative solution, prompt)
    if translate == "1": #en-gd
        return (q, sol1, sol1, prompt1)
    elif translate == "2": #gd-en
        return (q, sol1, sol2, prompt1)

def possession_aig(vocab_file, translate, sentence):
    #Load packages and vocab --------------------------------------------------
    import is_utility
    import random as rd
    import pandas as pd
    
    pp = pd.read_csv('Vocabulary/grammar_prepPronouns.csv')
    en = pd.read_csv('Vocabulary/grammar_english.csv')

    vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in vocab_sample.columns or "nom_sing" not in vocab_sample.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return

    #Randomiser ---------------------------------------------------------------
    
    subject_num = rd.randrange(6)
    object_num = rd.randrange(len(vocab_sample))
    obj_indef = is_utility.en_indef_article(vocab_sample.loc[object_num,"english"])


    #Construct sentences ------------------------------------------------------
    
    sentence_en = en.loc[subject_num,"en_subj"].capitalize() + " " + en.loc[subject_num,"have_pres"].lower() + " " + obj_indef.lower()
    sentence_gd = "Tha " + vocab_sample.loc[object_num,"nom_sing"].lower() + " " + pp.loc[subject_num,"aig"].lower()

    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
    elif translate == "2": #gd-en
        q = sentence_gd

    #Prompts ------------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        prompt1 = ""
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            prompt1 = "Tha " + vocab_sample.loc[object_num,"nom_sing"].lower() + " "
        elif translate == "2": #gd-en
            prompt1 = "____ " + obj_indef.lower() + ": "
   

    #Solutions ----------------------------------------------------------------
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            sol1 = sentence_gd
        elif translate == "2": #gd-en
            sol1 = sentence_en
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            sol1 = pp.loc[subject_num,"aig"].lower()
        elif translate == "2": #gd-en
            sol1 = en.loc[subject_num,"en_subj"].lower() + " " + en.loc[subject_num,"have_pres"].lower()
        
    
    #Output -------------------------------------------------------------------
    
    #Return (question, main solution, alternative solution, prompt)
    if translate == "1": #en-gd
        return (q, sol1, sol1, prompt1)
    elif translate == "2": #gd-en
        return (q, sol1, sol1, prompt1)

def gender(vocab_file, gender_mode):
    #Load packages and vocab --------------------------------------------------
    import is_utility
    import pandas as pd
    import random as rd
    
    vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if any(["english" not in vocab_list.columns,
        "nom_sing" not in vocab_list.columns,
        "gender" not in vocab_list.columns]):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' and 'gender' (lower-case)")
        return
    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(len(vocab_list))
    
    #Parts of sentence --------------------------------------------------------
    adjective_en = "small"
    adjective_gd = "beag"
            
    #Construct sentence -------------------------------------------------------
    
    if gender_mode == "1": #Adjectives
    
        sentence_en = "A " + adjective_en + " " + vocab_list["english"][vocab_num]
            
        if vocab_list["gender"][vocab_num] == "masc":
            sentence_gd = vocab_list["nom_sing"][vocab_num] + " " + adjective_gd
        elif vocab_list["gender"][vocab_num] == "fem":
            sentence_gd = vocab_list["nom_sing"][vocab_num] + " " + is_utility.lenite(adjective_gd)
            
    elif gender_mode == "2": #Definite articles (nom.)
    
        sentence_en = "The " + vocab_list["english"][vocab_num] + " (nominative)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_list["nom_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_list["gender"][vocab_num],
                                                case = "nom")
    
    #warning - vocab lists don't have prep_sing at the moment
    elif gender_mode == "3": #Definite articles (prep.)
    
        sentence_en = "The " + vocab_list["english"][vocab_num] + " (prepositional)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_list["prep_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_list["gender"][vocab_num],
                                                case = "prep")
    
    #warning - vocab lists don't have poss_sing at the moment
    elif gender_mode == "4": #Definite articles (poss.)
    
        sentence_en = "The " + vocab_list["english"][vocab_num] + " (possessive)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_list["poss_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_list["gender"][vocab_num],
                                                case = "poss")
    
    #Questions ----------------------------------------------------------------
    
    q = sentence_en
    
    #Prompts ------------------------------------------------------------------
    
    prompt1 = ""
    
    #Solutions ----------------------------------------------------------------
    
    sol1 = sentence_gd
    
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol1, prompt1)

def numbers(vocab_file, num_mode, max_num):
    
    #Load packages and vocab --------------------------------------------------
    import pandas as pd
    import random as rd
    
    if num_mode in ("1", "2"): #translating numbers
        numbers = pd.read_csv('Vocabulary/grammar_numbers.csv')

    if num_mode in ("3", "4", "5"): #plurals of nouns
        #Practicing plurals
        vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
        if ("english" not in vocab_sample.columns or "nom_sing" not in vocab_sample.columns or "nom_pl" not in vocab_sample.columns):
            print("Error: Check format of vocabulary list, must contain columns 'english', 'nom_sing' and 'nom_pl' (lower-case)")
            return
        
    #Randomiser ---------------------------------------------------------------
    if num_mode in ("1", "2"):
        num = rd.randint(1,max_num)
    
    elif num_mode in ("3", "4", "5"):
        vocab_num = rd.randrange(len(vocab_sample))

    
    #Work out the Gaelic for given number ----------------------------------
    if num_mode in ("1", "2"):
        num_unit = str(num)[-1]
        num_unit_gd = numbers.loc[numbers["number"]==int(num_unit)].reset_index(drop=True).at[0,"cardinal"]
        if num < 10: # 0-9
            num_gd = numbers.loc[numbers["number"]==num].reset_index(drop=True).at[0,"cardinal"]
        elif num == 12:
            num_gd = "dà dheug" #lenition
        elif num < 20: #11-19
            num_gd = num_unit_gd + " deug"
        elif num < 100: #20-99
            num_ten = int(str(num)[-2] + "0")
            num_ten_gd = numbers.loc[numbers["number"]==int(num_ten)].reset_index(drop=True).at[0,"cardinal"]
            if num_unit == "0":
                num_gd = num_ten_gd
            else:
                if num_unit in ("1","8"):
                    num_gd = num_ten_gd + " 's a h-" + num_unit_gd
                else:
                    num_gd = num_ten_gd + " 's a " + num_unit_gd
            
    #Questions ----------------------------------------------------------------
    
    if num_mode == "1": #digits to Gaelic
        q = num
        
    elif num_mode == "2": #Gaelic to digits
        q = num_gd
        
    elif num_mode == "3": #Plural from Gaelic
        q = "Pluralise: " + vocab_sample["nom_sing"][vocab_num]
        
    elif num_mode == "4": #Plural from English
        q = "Pluralise the Gaelic for: " + vocab_sample["english"][vocab_num]
    
        
    #Prompts ------------------------------------------------------------------
    
    prompt1 = ""
        
    #Solutions ----------------------------------------------------------------
    
    if num_mode == "1": #digits to Gaelic
        sol1 = num_gd
        
    elif num_mode == "2": #Gaelic to digits
        sol1 = str(num)
        
    elif num_mode in ("3", "4"): #Plural of noun
        sol1 = vocab_sample["nom_pl"][vocab_num]
            
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol1, prompt1)

def vocab(vocab_file, translate):
    #Load packages and vocab --------------------------------------------------
    import pandas as pd
    import random as rd
    
    vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in vocab_sample.columns or "nom_sing" not in vocab_sample.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(len(vocab_sample))
        
    #Questions ----------------------------------------------------------------
    
    if translate == "1": #en-gd
        q = vocab_sample["english"][vocab_num]
    if translate == "2": #gd-en
        q = vocab_sample["nom_sing"][vocab_num]
        
    #Prompts ------------------------------------------------------------------
        
    prompt1 = ""
    
    #Solutions ----------------------------------------------------------------
    if translate == "1": #en-gd
        sol1 = vocab_sample["nom_sing"][vocab_num]
    if translate == "2": #gd-en
        sol1 = vocab_sample["english"][vocab_num]
    
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol1, prompt1)    