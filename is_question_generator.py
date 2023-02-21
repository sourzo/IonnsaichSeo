# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:53:44 2022

@author: Zoe
"""
import is_utility
import pandas as pd
import random as rd

en = pd.read_csv('Vocabulary/grammar_english.csv')
pp = pd.read_csv('Vocabulary/grammar_prepPronouns.csv')
names = pd.read_csv('Vocabulary/people_names.csv')
g_numbers = pd.read_csv('Vocabulary/grammar_numbers.csv')
vb = pd.read_csv('Vocabulary/verbs_regular.csv')
professions = pd.read_csv('Vocabulary/people_professions.csv')
adjectives = pd.read_csv('Vocabulary/adjectives_misc.csv')
def_articles = ("an ", "na ", "a' ", "a’ ", "am ", "an t-")

vowels = ["a","e","i","o","u",
          "à","è","ì","ò","ù",
          "á","é","í","ó","ú"]

def give_get(vocab_file, tense, translate, sentence):
    #Load vocab --------------------------------------------------
        
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
            give_get_en = en["be_pres"][subject_num] + " giving"
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
            give_get_en = en["be_pres"][subject_num] + " getting"
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
        subject_en = pp["en_subj"][subject_num]
        subject_gd = pp["pronoun_gd"][subject_num]
    #subject: names
    elif subject_num == 7:
        name = rd.randrange(names["english"].count())
        subject_en = names["english"][name]
        subject_gd = names["nom_sing"][name]
        
    #object: pronouns / names (object_en, object_gd)
    if object_num < 7:
        object_en = en["en_obj"][object_num]
        #Prep pronouns for do/bho
        if give_get_num==0:
            object_gd = pp["do"][object_num]
        else:
            object_gd = pp["bho"][object_num]
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
    #Load vocab --------------------------------------------------
    
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
    #Load vocab --------------------------------------------------
    
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
    
    #Load vocab --------------------------------------------------
        
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
        num_unit_gd = g_numbers.loc[g_numbers["number"]==int(num_unit)].reset_index(drop=True).at[0,"cardinal"]
        if num < 10: # 0-9
            num_gd = g_numbers.loc[g_numbers["number"]==num].reset_index(drop=True).at[0,"cardinal"]
        elif num == 12:
            num_gd = "dà dheug" #lenition
        elif num < 20: #11-19
            num_gd = num_unit_gd + " deug"
        elif num < 100: #20-99
            num_ten = int(str(num)[-2] + "0")
            num_ten_gd = g_numbers.loc[g_numbers["number"]==int(num_ten)].reset_index(drop=True).at[0,"cardinal"]
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
    #Load vocab --------------------------------------------------
    
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

def preferences(vocab_file, translate, sentence):
    #Load vocab --------------------------------------------------
    
    vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in vocab_sample.columns or "nom_sing" not in vocab_sample.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return

    #Randomiser ---------------------------------------------------------------
    subject_num = rd.randrange(6)
    object_num = rd.randrange(len(vocab_sample))
    obj_indef = is_utility.en_indef_article(vocab_sample.loc[object_num,"english"])
    
    tense = rd.randrange(2) # 0 = present tense, 1 = future conditional
    pos_neg = rd.randrange(2) # 0 = positive, 1 = negative
    likepref = rd.randrange(2) # 0 = like, 1 = prefer

        
    #Parts of sentence --------------------------------------------------------
    
    ##English

    if tense == 0:
        if pos_neg == 0:
            like_prefer_en = ""
        else:
            like_prefer_en = en.loc[subject_num,"do_pres"].lower() + "n't "
    else:
        if pos_neg == 0:
            like_prefer_en = "would "
        else:
            like_prefer_en = "wouldn't "
            
    if likepref == 0:
        like_prefer_en = like_prefer_en + "like"
    else:
        like_prefer_en = like_prefer_en + "prefer"
        
    if tense == 0 and pos_neg == 0:
        if en.loc[subject_num,"en_subj"].lower() in ("he", "she", "name"):
            like_prefer_en = like_prefer_en + "s"
        
    ##Gaelic
    if pos_neg == 0:
        if likepref == 0:
            if tense == 0:
                like_prefer_gd = "is toil"
            else:
                like_prefer_gd = "bu toil"
        else:
            if tense == 0:
                like_prefer_gd = "is fheàrr"
            else:
                like_prefer_gd = "b' fheàrr"
    else:
        if likepref == 0:
            if tense == 0:
                like_prefer_gd = "cha toil"
            else:
                like_prefer_gd = "cha bu toil"
        else:
            if tense == 0:
                like_prefer_gd = "chan fheàrr"
            else:
                like_prefer_gd = "cha b' fheàrr"
        
    
    #Construct sentences ------------------------------------------------------
    sentence_en = en.loc[subject_num,"en_subj"].capitalize() + " " + like_prefer_en.lower() + " " + obj_indef.lower()
    sentence_gd = like_prefer_gd.capitalize() + " " + pp.loc[subject_num,"le"].lower() + " " + vocab_sample.loc[object_num,"nom_sing"].lower()

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
            prompt1 = like_prefer_gd.capitalize() + " ____ " + vocab_sample.loc[object_num,"nom_sing"].lower() + ": "
        elif translate == "2": #gd-en
            prompt1 = "____ " + like_prefer_en.lower() + " " + obj_indef.lower() + ": "
            
    #Solutions ----------------------------------------------------------------
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            sol1 = sentence_gd
            sol2 = sol1
        elif translate == "2": #gd-en
            sol1 = sentence_en
            sol2 = sol1.replace("n't", " not")
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            sol1 = pp.loc[subject_num,"le"].lower()
        elif translate == "2": #gd-en
            sol1 = en.loc[subject_num,"en_subj"].lower()
        sol2 = sol1

    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

def verbs_reg(chosen_tense, verbal_noun, verb_form):
    #Randomiser ---------------------------------------------------------------
    
    ## verb forms: statement/question, positive/negative
    if verb_form == "1":
        p_n = False #positive only
        q_s = False #statements only
    else:
        p_n = bool(rd.getrandbits(1)) #positive or negative
        if verb_form == "2":
            q_s = False #statements only
        else:
            q_s = bool(rd.getrandbits(1)) #statement or question
    
    ##Write the chosen verb form as a string
    if p_n == True:
        vf_str = "Negative "
    else:
        vf_str = "Positive "
    if q_s == True:
        vf_str = vf_str + "question"
    else:
        vf_str = vf_str + "statement"
        
    ## verb
    verb_num = rd.randrange(len(vb))
    
    ## person
    pers_num = rd.randrange(len(pp))
    
    #Parts of sentence --------------------------------------------------------
    person_gd = pp.loc[pers_num, "pronoun_gd"]
    person_en = pp.loc[pers_num, "en_subj"]
    
    if verbal_noun == "y":
        ## verbal noun
        if vb.loc[verb_num,"verbal_noun"][0] in is_utility.vowels:
            vn = "ag " + vb.loc[verb_num,"verbal_noun"]
        else:
            vn = "a' " + vb.loc[verb_num,"verbal_noun"]
            
        #English verb
        verb_en = vb.loc[verb_num,"en_vn"]
    else:
        verb_en = vb.loc[verb_num,"english"]
        
        
    
    #root form of verb
    v_root = vb.loc[verb_num,"root"]
    
    #Construct sentences ------------------------------------------------------
    if verbal_noun == "y":
        sentence = is_utility.transform_verb("bi", tense = chosen_tense, 
                                             negative = p_n, 
                                             question = q_s) + " " + person_gd + " " + vn
    else:
        sentence = is_utility.transform_verb(v_root, tense = chosen_tense, 
                                             negative = p_n, 
                                             question = q_s) + " " + person_gd
    
    #Questions ----------------------------------------------------------------
    if verb_form == "1":
        q = verb_en.capitalize() + " (" + person_en.capitalize() + ")"
    else:
        q = verb_en.capitalize() + " (" + person_en.capitalize() + ", " + vf_str + ")"
    #Prompts ------------------------------------------------------------------
    prompt1 = ""
    #Solutions ----------------------------------------------------------------
    sol1 = sentence.capitalize()
    sol2 = sentence.capitalize()
    #Output -------------------------------------------------------------------
    ## Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

def professions_annan(translate, sentence):
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(6)
    profession_num = rd.randrange(len(professions))
    #Parts of sentence --------------------------------------------------------
    pp_annan = pp.loc[person_num,"ann an"]
    
    if person_num < 4:
        profession_gd = professions.loc[profession_num,"nom_sing"]
    elif person_num in (4,5,6):
        profession_gd = professions.loc[profession_num,"nom_pl"]
    
    pronoun_en = pp.loc[person_num, "en_subj"]
    be_en = en.loc[person_num, "be_pres"]
    
    if person_num < 4:
        profession_en = is_utility.en_indef_article(professions.loc[profession_num,"english"])
    elif person_num in (4,5,6):
        profession_en = is_utility.en_pl(professions.loc[profession_num,"english"])
    
    #Construct sentence -------------------------------------------------------
    sentence_gd = "'S e " + profession_gd.lower() + " a th' " + pp_annan.lower()
    sentence_en = pronoun_en.capitalize() + " " + be_en.lower() + " " + profession_en.lower()
    
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
            prompt1 = "'S e " + profession_gd.lower() + " a th' "
        elif translate == "2": #gd-en
            prompt1 = "____" + profession_en.lower() + ": "
        
    #Solutions ----------------------------------------------------------------
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            sol1 = sentence_gd
        elif translate == "2": #gd-en
            sol1 = sentence_en
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            sol1 = pp_annan
        elif translate == "2": #gd-en
            sol1 = pronoun_en + " " + be_en
    
    sol2 = sol1
    
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

def emphasis_adjectives(translate):
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(6)
    adj_num = rd.randrange(len(adjectives))
    
    #Parts of sentence --------------------------------------------------------
    pers_emph = pp.loc[person_num,"emphatic"]
    adjective_gd = adjectives.loc[adj_num, "gd"]
    adjective_en = adjectives.loc[adj_num, "english"]
    
    pronoun_en = pp.loc[person_num, "en_subj"]
    be_en = en.loc[person_num, "be_pres"]

    #Construct sentence -------------------------------------------------------
    sentence_gd = "Tha " + pers_emph + " " + adjective_gd
    sentence_en = pronoun_en.capitalize() + " " + be_en.lower() + " " + adjective_en
    
    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
    elif translate == "2": #gd-en
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    prompt1 = ""
    
    #Solutions ----------------------------------------------------------------
    if translate == "1": #en-gd
        sol1 = sentence_gd
    elif translate == "2": #gd-en
        sol1 = sentence_en
    sol2 = sol1
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

def possession_mo(vocab_file, translate, sentence):
    #This module is only used with family or body parts vocab files
    #Load vocab --------------------------------------------------
    
    vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in vocab_sample.columns or "nom_sing" not in vocab_sample.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return    
    #Randomiser ---------------------------------------------------------------
    whose_num = rd.randrange(7)
    where_num = rd.randrange(3)
    what_num = rd.randrange(len(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    ## what
    what_en = vocab_sample.loc[what_num,"english"]
    what_gd = vocab_sample.loc[what_num,"nom_sing"]
    ### plurals
    if whose_num in (4,5,6) and vocab_file in ("people_body", "people_clothes"):
        if vocab_sample.loc[what_num,"english"] != "hair":
            what_gd = vocab_sample.loc[what_num,"nom_pl"]
            what_en = is_utility.en_pl(what_en)
    
    ##is/are
    if whose_num in (4,5,6) and vocab_file in ("people_body", "people_clothes"):
        is_are = "are"
    else:
        is_are = "is"
    
    ## where
    if where_num == 0:
        where_gd = "seo"
        where_en = "here"
        where_en_alt = "this"
    elif where_num == 1:
        where_gd = "sin"
        where_en = "there"
        where_en_alt = "that"
    elif where_num == 2:
        where_gd = "siud"
        where_en = "over there"
        where_en_alt = "over there"
    
    ## whose
    ### note - daughter and father take different grammatical structure
    if what_gd in ("nighean","duine"):
        whosewhat_gd = "an " + what_gd + " " + pp.loc[whose_num, "aig"]
        whose_en = pp.loc[whose_num,"en_poss"]
    else:
        ## possessive article
        whose_en = pp.loc[whose_num,"en_poss"]
        if what_gd[0] in vowels:
            whose_gd = ("m'", "d'", "", "a", "àr", "ùr", "an")[whose_num]
        elif whose_num < 6:
            whose_gd = pp.loc[whose_num,"possessive"]
        elif whose_num == 6:
            if what_gd[0] in ("b","m","f","p"):
                whose_gd = "am"
            else:
                whose_gd = "an"
        
        ## my/your/his -> lenition
        if whose_num in (0,1,2) and what_gd[0] not in vowels:
            what_gd = is_utility.lenite(what_gd)
        ## her + vowel -> h-
        elif whose_num ==3 and what_gd[0] in vowels:
            what_gd = "h-" + what_gd
        ## (y)our + vowel -> n-
        elif whose_num in (4, 5) and what_gd[0] in vowels:
            what_gd = "n-" + what_gd
    
    #Construct sentence -------------------------------------------------------
    if what_gd in ("nighean","duine"):
        sentence_gd = where_gd + " " + whosewhat_gd
    else:
        if len(whose_gd) == 0:
            sentence_gd = where_gd + " " + what_gd
        else:
            sentence_gd = where_gd + " " + whose_gd + " " + what_gd
    sentence_en = where_en + " " + is_are + " " + whose_en + " " + what_en
    
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
            prompt1 = where_gd + " "
        elif translate == "2": #gd-en
            prompt1 = where_en + " " + is_are + " ____ " + what_en + ": "
    
    #Solutions ----------------------------------------------------------------
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            sol1 = sentence_gd
            sol2 = sol1
        elif translate == "2": #gd-en
            sol1 = sentence_en
            sol2 = where_en_alt + " " + is_are + " " + whose_en + " " + what_en
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            if what_gd in ("nighean","duine"):
                sol1 = whosewhat_gd
            else:
                if len(whose_gd) == 0:
                    sol1 = what_gd
                else:
                    sol1 = whose_gd + " " + what_gd
            sol2 = sol1
        elif translate == "2": #gd-en
            sol1 = whose_en
            sol2 = sol1
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

def where_from(vocab_file, sentence):
    #Load vocab --------------------------------------------------
    vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if any(("english" not in vocab_sample.columns,
            "nom_sing" not in vocab_sample.columns,
            "gender" not in vocab_sample.columns)):
        print("Error: Check format of vocabulary list, must contain columns 'english', 'gender', and 'nom_sing' (lower-case)")
        return  
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(7)
    where_num = rd.randrange(len(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    
    if vocab_sample.loc[where_num,"nom_sing"].startswith(def_articles):
        from_gd = "às " + is_utility.prep_def(vocab_sample, where_num)
    else:
        from_gd = "à " + vocab_sample.loc[where_num,"nom_sing"]
    
    if sentence == "3":
        who_question = ("thu", "mi", "e", "i", "sibh", "sinn", "iad")
        
    #Construct sentence -------------------------------------------------------
    sentence_en = en.loc[person_num,"en_subj"].capitalize() + " " + en.loc[person_num,"be_pres"] + " from " + vocab_sample.loc[where_num,"english"]
    sentence_gd = "Tha " + pp.loc[person_num, "pronoun_gd"] + " " + from_gd
    
    #Questions ----------------------------------------------------------------
    if sentence in ("1", "2"): #Translate
        q = sentence_en
    else: #Answer question
        q = "Cò às a tha " + who_question[person_num] + "?"
    
    #Prompts ------------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        prompt1 = ""
    elif sentence == "2": #Fill in the blank
        prompt1 = "Tha " + pp.loc[person_num, "pronoun_gd"] + " "
    elif sentence == "3": #Answer the question
        prompt1 = "[" + vocab_sample.loc[where_num,"english"] + "]: "
        
    
    #Solutions ----------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        sol1 = sentence_gd
        sol2 = sol1
    elif sentence == "2": #Fill in the blank
        sol1 = from_gd
        sol2 = sol1
    elif sentence == "3": #Fill in the blank
        sol1 = sentence_gd
        if person_num == 1: #mi -> thu/sibh
            sol2 = "Tha sibh " + from_gd
        elif person_num == 4: #sibh -> sinn/mi
            sol2 = "Tha mi " + from_gd
        else:
            sol2 = sol1
       
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

def where_in(vocab_file, sentence):
    #Load vocab --------------------------------------------------
    vocab_sample = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    #Vocab files which contain the definite article in Gaelic for some words
    contains_articles = ("places_scotland", "places_world")
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(7)
    where_num = rd.randrange(len(vocab_sample))
    if vocab_file not in contains_articles:
        article_switch = rd.randrange(2)
    else:
        if vocab_sample.loc[where_num,"nom_sing"].startswith(def_articles):
            article_switch = 1
        else:
            article_switch = 0
        
    #Parts of sentence --------------------------------------------------------
    
    ##Indefinite article
    if article_switch == 0:
        if vocab_file not in contains_articles:
            where_en = is_utility.en_indef_article(vocab_sample.loc[where_num,"english"])
        else:
            where_en = vocab_sample.loc[where_num,"english"]
        where_gd = "ann " + is_utility.anm(vocab_sample.loc[where_num,"nom_sing"])
    ##Definite article
    else:
        if vocab_file not in contains_articles:
            where_en = "the " + vocab_sample.loc[where_num,"english"]
        else:
            where_en = vocab_sample.loc[where_num,"english"]
        where_gd = "anns " + is_utility.prep_def(vocab_sample, where_num)
    
    if sentence == "3":
        who_question = ("thu", "mi", "e", "i", "sibh", "sinn", "iad")
    
    #Construct sentence -------------------------------------------------------
    sentence_en = en.loc[person_num,"en_subj"].capitalize() + " " + en.loc[person_num, "be_pres"] + " in " + where_en
    sentence_gd = "Tha " + pp.loc[person_num, "pronoun_gd"] + " " + where_gd
    
    #Questions ----------------------------------------------------------------
    if sentence in ("1", "2"): #Translate
        q = sentence_en
    else: #Answer question
        q = "Càite a bheil " + who_question[person_num] + "?"
    
    #Prompts ------------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        prompt1 = ""
    elif sentence == "2": #Fill in the blank
        prompt1 = "Tha " + pp.loc[person_num, "pronoun_gd"] + " "
    elif sentence == "3": #Answer the question
        prompt1 = "[" + where_en + "]: "
        
    #Solutions ----------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        sol1 = sentence_gd
        sol2 = sol1
    elif sentence == "2": #Fill in the blank
        sol1 = where_gd
        sol2 = sol1
    elif sentence == "3": #Fill in the blank
        sol1 = sentence_gd
        if person_num == 1: #mi -> thu/sibh
            sol2 = "Tha sibh " + where_gd
        elif person_num == 4: #sibh -> sinn/mi
            sol2 = "Tha mi " + where_gd
        else:
            sol2 = sol1
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, sol1, sol2, prompt1)

