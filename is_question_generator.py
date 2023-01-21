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
numbers = pd.read_csv('Vocabulary/grammar_numbers.csv')
vb = pd.read_csv('Vocabulary/verbs_regular.csv')
professions = pd.read_csv('Vocabulary/people_professions.csv')
adjectives = pd.read_csv('Vocabulary/adjectives_misc.csv')

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

def verbs_reg(tense, verbal_noun, verb_form):
    #Randomiser ---------------------------------------------------------------
    
    ## form: Positive (0), negative (1), questioning positive (2), questioning negative (3)
    if verb_form == "1":
        form = 0
    elif verb_form == "2":
        form = rd.randrange(2)
    else:
        form = rd.randrange(4)
    ## verb
    verb_num = rd.randrange(len(vb))
    ## person
    pers_num = rd.randrange(len(pp))
    
    #Parts of sentence --------------------------------------------------------
    person_gd = pp.loc[pers_num, "pronoun_gd"]
    person_en = pp.loc[pers_num, "en_subj"]
    
    if verbal_noun == "y":
        ## verbal noun
        if vb.loc[verb_num,"verbal_noun"][0] in ("a","e","i","o","u","à","è","ì","ò","ù"):
            vn = "ag " + vb.loc[verb_num,"verbal_noun"]
        else:
            vn = "a' " + vb.loc[verb_num,"verbal_noun"]
            
        #the verb bi
        bi_past = ["bha", "cha robh", "an robh", "nach robh"]
        bi_pres = ["tha", "chan eil", "a bheil", "nach eil"]
        bi_fut = ["bidh", "cha bhi", "am bi", "nach bi"]
    
    #root form of verb
    v_root = vb.loc[verb_num,"root"]
    
    #form type
    form_type = ["positive statement", "negative statement", "positive question", "negative question"]
    
    #Construct sentences ------------------------------------------------------
    
    if verbal_noun == "y":
    
        if tense == "1":
            ## verbal noun present
            verb = bi_pres[form] + " " + person_gd + " " + vn
            
        elif tense == "2":
            ## verbal noun past
            verb = bi_past[form] + " " + person_gd + " " + vn
        
        elif tense == "3":
            ## verbal noun future
            verb = bi_fut[form] + " " + person_gd + " " + vn
    
    else:
        if tense == "2":
            ## past
            verb = is_utility.lenite(v_root)
            
            if verb[0] in ("f","a","e","i","o","u","à","è","ì","ò","ù"):
                verb = "dh'" + verb
            
            if form == 1:
                #negative
                verb = "cha do " + verb
            elif form == 2:
                #positive question
                verb = "an do " + verb
            elif form == 3:
                #negative question
                verb = "nach do " + verb
            
            verb = verb + " " + person_gd
        
        elif tense == "3":
            ## future
            if form == 0: #positive statement
                if is_utility.end_width(v_root) == "broad":
                    verb = v_root + "aidh"
                else:
                    verb = v_root + "idh"
            elif form == 1: #negative statement
                if v_root[0] in {"f","a","e","i","o","u","à","è","ì","ò","ù"}:
                    verb = "chan " + is_utility.lenite_dt(v_root)
                else:
                    verb = "cha " + is_utility.lenite_dt(v_root)
            elif form == 2: #positive question
                verb = is_utility.anm(v_root)
            elif form == 3: #negative question
                verb = "nach " + v_root
            verb = verb + " " + person_gd
    
    #Questions ----------------------------------------------------------------
    if verb_form == "1":
        q = vb.loc[verb_num,"english"].capitalize() + " (" + person_en.capitalize() + ")"
    else:
        q = vb.loc[verb_num,"english"].capitalize() + " (" + person_en.capitalize() + ", " + form_type[form] + ")"
    #Prompts ------------------------------------------------------------------
    prompt1 = ""
    #Solutions ----------------------------------------------------------------
    sol1 = verb.capitalize()
    sol2 = verb.capitalize()
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

