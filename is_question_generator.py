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
professions = pd.read_csv('Vocabulary/people_professions.csv')

def give_get(chosen_tense, translate, sentence, vocab_sample):
    #Load vocab --------------------------------------------------
    
    gifts = vocab_sample
    
    #Randomiser ---------------------------------------------------------------
    
    subject_num = rd.randrange(8)
    object_num = rd.randrange(8)
    gift_num = rd.randrange(gifts["english"].count())
    give_get_num = rd.randrange(2) # 0 = give to, 1 = get from
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past", "present", "future"))
    
    #Parts of sentence --------------------------------------------------------
    
    #the item that's being given
    gift_en = is_utility.en_indef_article(gifts["english"][gift_num])
    gift_gd = gifts["nom_sing"][gift_num]
    
    #giving to (give_get_en, give_get_gd)
    if give_get_num == 0:
        if chosen_tense == "present":
            give_get_en = en["be_pres"][subject_num] + " giving"
            give_get_gd = "a' toirt"
        elif chosen_tense == "past":
            give_get_en = "gave"
            give_get_gd = "thug"
        elif chosen_tense == "future":
            give_get_en = "will give"
            give_get_gd = "bheir"
        prep_en = "to"
        
    #getting from (give_get_en, give_get_gd)
    elif give_get_num == 1:
        if chosen_tense == "present":
            give_get_en = en["be_pres"][subject_num] + " getting"
            give_get_gd = "a' faighinn"
        elif chosen_tense == "past":
            give_get_en = "got"
            give_get_gd = "fhuair"
        elif chosen_tense == "future":
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
    if chosen_tense == "present": #Gaelic - with verbal noun
        sentence_gd = "Tha " + subject_gd + " " + give_get_gd + " " + gift_gd + " " + object_gd
    
    elif chosen_tense in ("past", "future"):  #Past / Future tense sentences
        #Gaelic
        sentence_gd = give_get_gd.capitalize() + " " + subject_gd + " " + gift_gd + " " + object_gd

    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
    elif translate == "2": #gd-en
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            if chosen_tense == "present": #Present tense with verbal noun
                prompt1 = "Tha " + subject_gd + " " + give_get_gd + " " + gift_gd + " "
            #Past / Future tense sentences
            elif chosen_tense in ("past", "future"):
                prompt1 = give_get_gd.capitalize() + " " + subject_gd + " " + gift_gd + " "
        elif translate == "2": #gd-en
            prompt1 = subject_en.capitalize() + " " + give_get_en + " " + gift_en + " "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            solutions.append(sentence_gd)
        elif translate == "2": #gd-en
            solutions.append(sentence_en, sentence_en_alt)
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            solutions.append(object_gd)
        elif translate == "2": #gd-en
           solutions.append(prep_en + " " + object_en)
            
    #Output -------------------------------------------------------------------
    
    #Return (question, main solution, alternative solution, prompt)
    if translate == "1": #en-gd
        return (q, solutions, prompt1)
    elif translate == "2": #gd-en
        return (q, solutions, prompt1)

def possession_aig(translate, sentence, vocab_sample):
    
    #Load vocab --------------------------------------------------
    
    
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
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            prompt1 = "Tha " + vocab_sample.loc[object_num,"nom_sing"].lower() + " "
        elif translate == "2": #gd-en
            prompt1 = "____ " + obj_indef.lower() + ": "
   

    #Solutions ----------------------------------------------------------------
    solutions = []
    
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            solutions.append(sentence_gd)
        elif translate == "2": #gd-en
            solutions.append(sentence_en)
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            solutions.append(pp.loc[subject_num,"aig"].lower())
        elif translate == "2": #gd-en
            solutions.append(en.loc[subject_num,"en_subj"].lower() + " " + en.loc[subject_num,"have_pres"].lower())
        
    
    #Output -------------------------------------------------------------------
    
    #Return (question, main solution, alternative solution, prompt)
    if translate == "1": #en-gd
        return (q, solutions, prompt1)
    elif translate == "2": #gd-en
        return (q, solutions, prompt1)

def gender(gender_mode, vocab_sample):
    #Load vocab --------------------------------------------------
    
    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(len(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    adjective_en = "small"
    adjective_gd = "beag"
            
    #Construct sentence -------------------------------------------------------
    
    if gender_mode == "1": #Adjectives
    
        sentence_en = "A " + adjective_en + " " + vocab_sample["english"][vocab_num]
            
        if vocab_sample["gender"][vocab_num] == "masc":
            sentence_gd = vocab_sample["nom_sing"][vocab_num] + " " + adjective_gd
        elif vocab_sample["gender"][vocab_num] == "fem":
            sentence_gd = vocab_sample["nom_sing"][vocab_num] + " " + is_utility.lenite(adjective_gd)
            
    elif gender_mode == "2": #Definite articles (nom.)
    
        sentence_en = "The " + vocab_sample["english"][vocab_num] + " (nominative)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample["nom_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_sample["gender"][vocab_num],
                                                case = "nom")
    
    #warning - vocab lists don't have prep_sing at the moment
    elif gender_mode == "3": #Definite articles (prep.)
    
        sentence_en = "The " + vocab_sample["english"][vocab_num] + " (prepositional)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample["prep_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_sample["gender"][vocab_num],
                                                case = "prep")
    
    #warning - vocab lists don't have poss_sing at the moment
    elif gender_mode == "4": #Definite articles (poss.)
    
        sentence_en = "The " + vocab_sample["english"][vocab_num] + " (possessive)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample["poss_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_sample["gender"][vocab_num],
                                                case = "poss")
    
    #Questions ----------------------------------------------------------------
    
    q = sentence_en
    
    #Prompts ------------------------------------------------------------------
    
    prompt1 = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    solutions.append(sentence_gd)
    
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def numbers(num_mode, max_num, vocab_sample):
    
    #Load vocab --------------------------------------------------
    
        
        
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
        q = str(num)
        
    elif num_mode == "2": #Gaelic to digits
        q = num_gd
        
    elif num_mode == "3": #Plural from Gaelic
        q = "Pluralise: " + vocab_sample["nom_sing"][vocab_num]
        
    elif num_mode == "4": #Plural from English
        q = "Pluralise the Gaelic for: " + vocab_sample["english"][vocab_num]
    
        
    #Prompts ------------------------------------------------------------------
    
    if num_mode == "1": #digits to Gaelic
        prompt1 = "Àireamh: "
        
    elif num_mode == "2": #Gaelic to digits
        prompt1 = "Number (in digits): "
        
    elif num_mode in ("3", "4"): #Plurals
        prompt1 = "Plural: "
        
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    if num_mode == "1": #digits to Gaelic
        solutions.append(num_gd)
        
    elif num_mode == "2": #Gaelic to digits
        solutions.append(str(num))
        
    elif num_mode in ("3", "4"): #Plural of noun
        solutions.append(vocab_sample["nom_pl"][vocab_num])
            
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def learn_nouns(translate, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(len(vocab_sample))
        
    #Questions ----------------------------------------------------------------
    
    if translate == "1": #en-gd
        q = vocab_sample["english"][vocab_num]
    if translate == "2": #gd-en
        q = vocab_sample["nom_sing"][vocab_num]
        
    #Prompts ------------------------------------------------------------------
        
    prompt1 = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate == "1": #en-gd
        solutions.append(vocab_sample["nom_sing"][vocab_num])
    if translate == "2": #gd-en
        solutions.append(vocab_sample["english"][vocab_num])
    
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def preferences(translate, sentence, vocab_sample):
    #Load vocab --------------------------------------------------
    

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
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            prompt1 = like_prefer_gd.capitalize() + " ____ " + vocab_sample.loc[object_num,"nom_sing"].lower() + ": "
        elif translate == "2": #gd-en
            prompt1 = "____ " + like_prefer_en.lower() + " " + obj_indef.lower() + ": "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            solutions.append(sentence_gd)
        elif translate == "2": #gd-en
            solutions.append(sentence_en)
            solutions.append(sentence_en.replace("n't", " not"))
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            solutions.append(pp.loc[subject_num,"le"].lower())
        elif translate == "2": #gd-en
            solutions.append(en.loc[subject_num,"en_subj"].lower())
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def verb_tenses(chosen_tense, verb_form, vocab_sample):
    #Randomiser ---------------------------------------------------------------
    
    ## verb forms: statement/question, positive/negative
    if verb_form == "1":
        n_p = False #positive only
        q_s = False #statements only
    else:
        n_p = bool(rd.getrandbits(1)) #negative (T) or positive (F)
        if verb_form == "2":
            q_s = False #statements only
        else:
            q_s = bool(rd.getrandbits(1)) #question (T) or statement (F)
    
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past","present","future"))
    
    #Verbal noun switch
    if chosen_tense == "past":
        chosen_tense = rd.choice(("past", "vn_past"))
    elif chosen_tense == "future":
        chosen_tense = rd.choice(("future", "vn_future"))
    
    ## verb
    verb_num = rd.randrange(len(vocab_sample))
    
    ## person
    pers_num = rd.randrange(len(pp))
    
    #Parts of sentence --------------------------------------------------------
    person_gd = pp.loc[pers_num, "pronoun_gd"]
    person_en = pp.loc[pers_num, "en_subj"]
    
    if chosen_tense in ("past", "future"):
        v_root = vocab_sample.loc[verb_num,"root"]
        print(v_root)
    else:
        v_noun = vocab_sample.loc[verb_num,"verbal_noun"]
        print(v_noun)
    
    #Construct sentences ------------------------------------------------------
    if chosen_tense in ("past", "future"):
        sentence_gd = is_utility.transform_verb(v_root,
                                                tense = chosen_tense, 
                                                negative = n_p, 
                                                question = q_s) + " " + person_gd
    else:
        sentence_gd = is_utility.verbal_noun(vn = v_noun,
                                             person = person_gd,
                                             tense = chosen_tense, 
                                             negative = n_p, 
                                             question = q_s)
    
    sentence_gd = sentence_gd.capitalize()
        
    sentence_en = is_utility.en_verb(vocab_sample, verb_num, 
                                     pronoun = person_en, 
                                     tense = chosen_tense, 
                                     negative = n_p, 
                                     question = q_s)
    sentence_en = sentence_en.capitalize().replace(" i ", " I ")
    
    #Questions ----------------------------------------------------------------
    q = sentence_en
    if q_s == True:
        q = q + "?"
    
    #Prompts ------------------------------------------------------------------
    
    prompt1 = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    solutions.append(sentence_gd.capitalize())
    
    #Output -------------------------------------------------------------------
    
    ## Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

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
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            prompt1 = "'S e " + profession_gd.lower() + " a th' "
        elif translate == "2": #gd-en
            prompt1 = "____" + profession_en.lower() + ": "
        
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            solutions.append(sentence_gd)
        elif translate == "2": #gd-en
            solutions.append(sentence_en)
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            solutions.append(pp_annan)
        elif translate == "2": #gd-en
            solutions.append(pronoun_en + " " + be_en)
    
    #Output -------------------------------------------------------------------

    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def emphasis_adjectives(translate, vocab_sample):
    
    modifiers = [("", ""),
                 ("so ", "cho "), 
                 ("too ", "ro "), 
                 ("very ", "glè "),
                 ("terribly ", "uabhasach "),
                 ("really ", "gu math "),
                 ("a bit ", "beagan ")]
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(6)
    modifier_choice = modifiers[rd.randrange(len(modifiers))]
    adj_num = rd.randrange(len(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    pers_emph = pp.loc[person_num,"emphatic"]
    pronoun_en = pp.loc[person_num, "en_subj"]
        
    adjective_gd = vocab_sample.loc[adj_num, "adj_gd"]
    adjective_en = modifier_choice[0] + vocab_sample.loc[adj_num, "english"]
    
    if modifier_choice[1] in ("ro ", "glè "):
        adjective_gd = modifier_choice[1] + is_utility.lenite(adjective_gd)
    else:
        adjective_gd = modifier_choice[1] + adjective_gd
    
    be_en = en.loc[person_num, "be_pres"]
    
    #Construct sentence -------------------------------------------------------
    sentence_gd = "Tha " + pers_emph + " " + adjective_gd
    sentence_en = "*" + pronoun_en.capitalize() + "* " + be_en.lower() + " " + adjective_en
    
    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
    elif translate == "2": #gd-en
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    prompt1 = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate == "1": #en-gd
        solutions.append(sentence_gd)
    elif translate == "2": #gd-en
        solutions.append(sentence_en)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def possession_mo(translate, sentence, vocab_sample):
    #This module is only used with family or body parts vocab files
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    whose_num = rd.randrange(7)
    where_num = rd.randrange(3)
    what_num = rd.randrange(len(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    ## what
    what_en = vocab_sample.loc[what_num,"english"]
    what_gd = vocab_sample.loc[what_num,"nom_sing"]
    
    ### plurals
    if whose_num in (4,5,6):
        if vocab_sample.loc[what_num,"english"] != "hair":
            what_gd = vocab_sample.loc[what_num,"nom_pl"]
            what_en = is_utility.en_pl(what_en)
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
    elif what_gd in ("nigheanan","daoine"):
        whosewhat_gd = "na " + what_gd + " " + pp.loc[whose_num, "aig"]
        whose_en = pp.loc[whose_num,"en_poss"]
    else:
        ## possessive article
        whose_en = pp.loc[whose_num,"en_poss"]
        if what_gd[0] in is_utility.vowels:
            whose_gd = ("m'", "d'", "", "a", "àr", "ùr", "an")[whose_num]
        elif whose_num < 6:
            whose_gd = pp.loc[whose_num,"possessive"]
        elif whose_num == 6:
            if what_gd[0] in ("b","m","f","p"):
                whose_gd = "am"
            else:
                whose_gd = "an"
        
        ## my/your/his -> lenition
        if whose_num in (0,1,2) and what_gd[0] not in is_utility.vowels:
            what_gd = is_utility.lenite(what_gd)
        ## her + vowel -> h-
        elif whose_num ==3 and what_gd[0] in is_utility.vowels:
            what_gd = "h-" + what_gd
        ## (y)our + vowel -> n-
        elif whose_num in (4, 5) and what_gd[0] in is_utility.vowels:
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
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            prompt1 = where_gd + " "
        elif translate == "2": #gd-en
            prompt1 = where_en + " " + is_are + " ____ " + what_en + ": "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            solutions.append(sentence_gd)
        elif translate == "2": #gd-en
            solutions.append(sentence_en,
                              where_en_alt + " " + is_are + " " + whose_en + " " + what_en)
    
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            if what_gd in ("nighean","duine"):
                solutions.append(whosewhat_gd)
            else:
                if len(whose_gd) == 0:
                    solutions.append(what_gd)
                else:
                    solutions.append(whose_gd + " " + what_gd)
        elif translate == "2": #gd-en
            solutions.append(whose_en)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def where_from(sentence, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(7)
    where_num = rd.randrange(len(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    
    if vocab_sample.loc[where_num,"nom_sing"].startswith(is_utility.def_articles):
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
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        prompt1 = "Tha " + pp.loc[person_num, "pronoun_gd"] + " "
    elif sentence == "3": #Answer the question
        prompt1 = "[" + vocab_sample.loc[where_num,"english"] + "]: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "1": # Full sentence, no prompt
        solutions.append(sentence_gd)
    elif sentence == "2": #Fill in the blank
        solutions.append(from_gd)
    elif sentence == "3": #Answer the question
        solutions.append(sentence_gd)
        if person_num == 1: #mi -> thu/sibh
            solutions.append("Tha sibh " + from_gd)
        elif person_num == 4: #sibh -> sinn/mi
            solutions.append("Tha mi " + from_gd)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def where_in(sentence, contains_articles, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(7)
    where_num = rd.randrange(len(vocab_sample))
    if contains_articles == True:
        if vocab_sample.loc[where_num,"nom_sing"].startswith(is_utility.def_articles):
            article_switch = 1
        else:
            article_switch = 0
    else:
        article_switch = rd.randrange(2)
        
    #Parts of sentence --------------------------------------------------------
    
    ##Indefinite article
    if article_switch == 0:
        if contains_articles == False:
            where_en = is_utility.en_indef_article(vocab_sample.loc[where_num,"english"])
        else:
            where_en = vocab_sample.loc[where_num,"english"]
        where_gd = "ann " + is_utility.anm(vocab_sample.loc[where_num,"nom_sing"])
    ##Definite article
    else:
        if contains_articles == False:
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
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        prompt1 = "Tha " + pp.loc[person_num, "pronoun_gd"] + " "
    elif sentence == "3": #Answer the question
        prompt1 = "[" + where_en + "]: "
        
    solutions = []
    if sentence == "1": # Full sentence, no prompt
        solutions.append(sentence_gd)
    elif sentence == "2": #Fill in the blank
        solutions.append(where_gd)
    elif sentence == "3": #Fill in the blank
        solutions.append(sentence_gd)
        if person_num == 1: #mi -> thu/sibh
            solutions.append("Tha sibh " + where_gd)
        elif person_num == 4: #sibh -> sinn/mi
            solutions.append("Tha mi " + where_gd)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def comparisons(translate):
    #Load vocab --------------------------------------------------
    similes = pd.read_csv("Vocabulary/adjectives_comparisons.csv")
    
    #Randomiser ---------------------------------------------------------------
    comparison_choice = rd.randrange(len(similes))
   
    #Construct sentence -------------------------------------------------------
    sentence_en = "As " + similes.loc[comparison_choice,"english"] + " as " + similes.loc[comparison_choice,"simile_en"]
    sentence_gd = "Cho " + similes.loc[comparison_choice,"adj_gd"] + " ri " + similes.loc[comparison_choice,"simile_gd"]
    
    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
    elif translate == "2": #gd-en
        q = sentence_gd

    #Prompts ------------------------------------------------------------------
    prompt1 = "Translation: "

    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate == "1": #en-gd
        solutions.append(sentence_gd)
    elif translate == "2": #gd-en
        solutions.append(sentence_en)

    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

def comparatives_superlatives(vocab_sample, comp_sup, sentence, translate):
    #Load vocab --------------------------------------------------
    nouns = vocab_sample
    adjectives = pd.read_csv("Vocabulary/adjectives_misc.csv").sample(10).reset_index(drop=True)
    #Randomiser ---------------------------------------------------------------
    subject_num = rd.randrange(len(nouns))
    object_num = rd.randrange(len(nouns))
    adj_num = rd.randrange(len(adjectives))
    
    if comp_sup not in ("comp", "sup"):
        comp_sup = rd.choice(("comp","sup"))
    
    #Parts of sentence --------------------------------------------------------
    subject_en = nouns.loc[subject_num,"english"]
    subject_gd = nouns.loc[subject_num,"nom_sing"]
        
    if comp_sup == "comp":
        
        object_en = nouns.loc[object_num,"english"]
        object_gd = nouns.loc[object_num,"nom_sing"]
        
        comparative_gd = "nas " + adjectives.loc[adj_num, "comp_sup"]
        
        comparative_en = adjectives.loc[adj_num, "comp_en"]
        comparative_en_alt = "more " + adjectives.loc[adj_num, "english"]
    
    elif comp_sup == "sup":
        subject_en = nouns.loc[subject_num, "english"]
        subject_gd = is_utility.gd_common_article(nouns.loc[subject_num, "nom_sing"],
                                                  "sg", 
                                                  nouns.loc[subject_num, "gender"],
                                                  "nom")
        
        superlative_gd = "as " + adjectives.loc[adj_num, "comp_sup"]
    
        superlative_en = adjectives.loc[adj_num, "sup_en"]
        superlative_en_alt = "most " + adjectives.loc[adj_num, "english"]
    #Construct sentence -------------------------------------------------------
    if comp_sup == "comp":
        sentence_gd = "A bheil " + subject_gd + " " + comparative_gd + " na " + object_gd
        sentence_en = "Is " + is_utility.en_indef_article(subject_en) + " " + comparative_en + " than " + is_utility.en_indef_article(object_en)
        sentence_en_alt = "Is " + is_utility.en_indef_article(subject_en) + " " + comparative_en_alt + " than " + is_utility.en_indef_article(object_en)
    elif comp_sup == "sup":
        sentence_gd = subject_gd.capitalize() + " " + superlative_gd
        sentence_en = "The " + superlative_en + " " + subject_en
        sentence_en_alt = "The " + superlative_en_alt + " " + subject_en
    #Questions ----------------------------------------------------------------
    if translate == "1": #en-gd
        q = sentence_en
        if comp_sup == "comp":
            q = q + "?"
    elif translate == "2": #gd-en
        q = sentence_gd
        if comp_sup == "comp":
            q = q + "?"
    #Prompts ------------------------------------------------------------------
    if sentence == "1": # Full sentence, no prompt
        prompt1 = "Translation: "
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            if comp_sup == "comp":
                prompt1 = "A bheil " + subject_gd + " _____ na " + object_gd + "? : "
            elif comp_sup == "sup":
                prompt1 = subject_gd.captialize() + " "
        elif translate == "2": #gd-en
            if comp_sup == "comp":
                prompt1 = "Is " + is_utility.en_indef_article(subject_en) + " ____ than " + is_utility.en_indef_article(object_en) + "? : "
            elif comp_sup == "sup":
                prompt1 = "The ____ " + subject_en + ": "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "1": #Full sentence
        if translate == "1": #en-gd
            solutions.append(sentence_gd)
        elif translate == "2": #gd-en
            solutions.append(sentence_en, sentence_en_alt)
            
    elif sentence == "2": #Fill in the blank
        if translate == "1": #en-gd
            if comp_sup == "comp":
                solutions.append(comparative_gd)
            elif comp_sup == "sup":
                solutions.append(superlative_gd)
        elif translate == "2": #gd-en
            if comp_sup == "comp":
                solutions.append(comparative_en, comparative_en_alt)
            elif comp_sup == "sup":
                solutions.append(superlative_en, superlative_en_alt)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, solutions, prompt1)

