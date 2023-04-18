# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:53:44 2022

@author: Zoe
"""
import is_utility
import random as rd
import is_csvreader as csvr

en = csvr.read_csv('grammar_english')
pp = csvr.read_csv('grammar_prepPronouns')
names = csvr.read_csv('people_names')
g_numbers = csvr.read_csv('grammar_numbers')
professions = csvr.read_csv('people_professions')
similes = csvr.read_csv("adjectives_comparisons")
adjectives = rd.sample(csvr.read_csv("adjectives_misc"), 10)
list_months = csvr.read_csv("datetime_months")
list_holidays = csvr.read_csv("datetime_holidays")
list_seasons = csvr.read_csv("datetime_seasons")

adj_modifiers = [("", ""),
                 ("so ", "cho "), 
                 ("too ", "ro "), 
                 ("very ", "glè "),
                 ("terribly ", "uabhasach "),
                 ("really ", "gu math "),
                 ("a bit ", "beagan ")]

def give_get(chosen_tense, translate_words, sentence, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        subject_num = rd.randrange(8)
        object_num = rd.randrange(8)
        gift_num = rd.randrange(len(vocab_sample))
        give_get_num = rd.randrange(2) # 0 = give to, 1 = get from
    else:
        subject_num = testvalues["subject_num"]
        object_num = testvalues["object_num"]
        gift_num = testvalues["gift_num"]
        give_get_num = testvalues["give_get_num"]
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past", "present", "future"))
    
    #Parts of sentence --------------------------------------------------------
    
    #subject: pronouns (subject_en, subject_gd)
    if subject_num < 7:
        subject_en = pp[subject_num]["en_subj"]
        subject_gd = pp[subject_num]["pronoun_gd"]
    #subject: names
    elif subject_num == 7:
        name = rd.randrange(len(names))
        subject_en = names[name]["english"]
        subject_gd = names[name]["nom_sing"]
        
    
    #Subject and verb: giving to
    if give_get_num == 0:
        if chosen_tense == "present":
            verb_subj_gd = is_utility.verbal_noun("toirt", subject_gd, chosen_tense, negative=False, question=False).capitalize()
            verb_subj_en = subject_en.capitalize() + " " + en[subject_num]["be_pres"] + " giving"
        elif chosen_tense == "past":
            verb_subj_gd = is_utility.transform_verb("thig", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
            verb_subj_en = subject_en.capitalize() + " gave"
        elif chosen_tense == "future":
            verb_subj_gd = is_utility.transform_verb("thig", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
            verb_subj_en = subject_en.capitalize() + " will give"
        prep_en = "to"
        
    #Subject and verb: getting from
    elif give_get_num == 1:
        if chosen_tense == "present":
            verb_subj_gd = is_utility.verbal_noun("faighinn", subject_gd, chosen_tense, negative=False, question=False).capitalize()
            verb_subj_en = subject_en.capitalize() + " " + en[subject_num]["be_pres"] + " getting"
        elif chosen_tense == "past":
            verb_subj_gd = is_utility.transform_verb("faigh", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
            verb_subj_en = subject_en.capitalize() + " got"
        elif chosen_tense == "future":
            verb_subj_gd = is_utility.transform_verb("faigh", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
            verb_subj_en = subject_en.capitalize() + " will get"
        prep_en = "from"
        
        
    #the item that's being given
    gift_en = is_utility.en_indef_article(vocab_sample[gift_num]["english"])
    gift_gd = vocab_sample[gift_num]["nom_sing"]
        
        
    #object: pronouns / names (object_en, object_gd)
    if object_num < 7:
        object_en = en[object_num]["en_obj"]
        #Prep pronouns for do/bho
        if give_get_num==0:
            object_gd = pp[object_num]["do"]
        else:
            object_gd = pp[object_num]["bho"]
            
    #names
    elif object_num == 7:
        name = rd.randrange(len(names))
        object_en = names[name]["english"]
        lenited_name = is_utility.lenite(names[name]["nom_sing"])
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
        sentence_en = verb_subj_en + " " + object_en + " " + gift_en
        sentence_en_alt = verb_subj_en + " " + gift_en + " " + prep_en + " " + object_en
    elif give_get_num == 1:
       sentence_en = verb_subj_en + " " + gift_en + " " + prep_en + " " + object_en
    #Gaelic
    sentence_gd = verb_subj_gd + " " + gift_gd + " " + object_gd
    
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd": #en-gd
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = verb_subj_gd + " " + gift_gd + " "
        elif translate_words == "gd_en":
            prompt = verb_subj_en + " " + gift_en + " "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            if give_get_num == 0:
                solutions.append(sentence_en_alt)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(object_gd)
        elif translate_words == "gd_en":
           solutions.append(prep_en + " " + object_en)
            
    #Output -------------------------------------------------------------------
    
    #Return (question, prompt, solutions)
    return (q, prompt, solutions)

def possession_aig(translate_words, sentence, vocab_sample, testvalues = None):
    
    #Load vocab --------------------------------------------------
    
    
    #Randomiser ---------------------------------------------------------------
    
    if testvalues == None:
        subject_num = rd.randrange(7)
        object_num = rd.randrange(len(vocab_sample))
    else:
        subject_num = testvalues["subject_num"]
        object_num = testvalues["object_num"]
        
    #Construct sentences ------------------------------------------------------
    obj_indef = is_utility.en_indef_article(vocab_sample[object_num]["english"])
   
    sentence_en = en[subject_num]["en_subj"].capitalize() + " " + en[subject_num]["have_pres"].lower() + " " + obj_indef.lower()
    sentence_gd = "Tha " + vocab_sample[object_num]["nom_sing"].lower() + " " + pp[subject_num]["aig"].lower()
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = "Tha " + vocab_sample[object_num]["nom_sing"].lower() + " "
        elif translate_words == "gd_en":
            prompt = "____ " + obj_indef.lower() + ": "
   
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(pp[subject_num]["aig"].lower())
        elif translate_words == "gd_en":
            solutions.append(en[subject_num]["en_subj"].lower().capitalize() + " " + en[subject_num]["have_pres"].lower())
        
    
    #Output -------------------------------------------------------------------
    
    #Return (question, prompt, solutions)
    return (q, prompt, solutions)

def gender(gender_mode, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        vocab_num = rd.randrange(len(vocab_sample))
    else:
        vocab_num = testvalues["vocab_num"]
    
    if gender_mode == "def_all":
        gender_mode = rd.choice(("def_nom"#, "def_prep", "def_poss"
                                 ))
    #Parts of sentence --------------------------------------------------------
    adjective_en = "small"
    adjective_gd = "beag"
            
    #Construct sentence -------------------------------------------------------
    
    if gender_mode == "adj":
    
        sentence_en = "A " + adjective_en + " " + vocab_sample[vocab_num]["english"]
            
        if vocab_sample[vocab_num]["gender"] == "masc":
            sentence_gd = vocab_sample[vocab_num]["nom_sing"] + " " + adjective_gd
        elif vocab_sample[vocab_num]["gender"] == "fem":
            sentence_gd = vocab_sample[vocab_num]["nom_sing"] + " " + is_utility.lenite(adjective_gd)
            
    elif gender_mode == "def_nom":
    
        sentence_en = "The " + vocab_sample[vocab_num]["english"] + " (nominative)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample[vocab_num]["nom_sing"],
                                                sg_pl = "sg",
                                                gender = vocab_sample[vocab_num]["gender"],
                                                case = "nom")
    
    #warning - vocab lists don't have prep_sing at the moment
    elif gender_mode == "def_prep":
    
        sentence_en = "The " + vocab_sample[vocab_num]["english"] + " (prepositional)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample[vocab_num]["prep_sing"],
                                                sg_pl = "sg",
                                                gender = vocab_sample[vocab_num]["gender"],
                                                case = "prep")
    
    #warning - vocab lists don't have poss_sing at the moment
    elif gender_mode == "def_poss":
    
        sentence_en = "The " + vocab_sample[vocab_num]["english"] + " (possessive)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample[vocab_num]["poss_sing"],
                                                sg_pl = "sg",
                                                gender = vocab_sample[vocab_num]["gender"],
                                                case = "poss")
    
    #Questions ----------------------------------------------------------------
    
    q = sentence_en
    
    #Prompts ------------------------------------------------------------------
    
    prompt = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    solutions.append(sentence_gd)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def numbers(translate_numbers, max_num, testvalues = None):
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        num = rd.randint(1,max_num)
    else:
        num = testvalues["num"]
       
    #Work out the Gaelic for given number ----------------------------------
    num_gd = is_utility.digits_to_gd(num)
            
    #Questions ----------------------------------------------------------------
    
    if translate_numbers == "dig_gd":
        q = str(num)
        
    elif translate_numbers == "gd_dig":
        q = num_gd
    
    #Prompts ------------------------------------------------------------------
    
    if translate_numbers == "dig_gd":
        prompt = "Àireamh: "
        
    elif translate_numbers == "gd_dig":
        prompt = "Number (in digits): "
    
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    if translate_numbers == "dig_gd":
        solutions.append(num_gd)
        
    elif translate_numbers == "gd_dig":
        solutions.append(str(num))
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def plurals(translate_generic, vocab_sample, testvalues = None):
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        vocab_num = rd.randrange(len(vocab_sample))
    else:
        vocab_num = testvalues["vocab_num"]
    
    #Work out the Gaelic for given number ----------------------------------
            
    #Questions ----------------------------------------------------------------
    
    if translate_generic == "from_en": #Plural from English
        q = "Pluralise the Gaelic for: " + vocab_sample[vocab_num]["english"]
    
    elif translate_generic == "from_gd": #Plural from Gaelic
        q = "Pluralise: " + vocab_sample[vocab_num]["nom_sing"]
        
    #Prompts ------------------------------------------------------------------
    
    prompt = "Plural: "
        
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    solutions.append(vocab_sample[vocab_num]["nom_pl"])
            
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def learn_nouns(translate_words, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        vocab_num = rd.randrange(len(vocab_sample))
    else:
        vocab_num = testvalues["vocab_num"]
        
    #Questions ----------------------------------------------------------------
    
    if translate_words == "en_gd":
        q = vocab_sample[vocab_num]["english"]
    if translate_words == "gd_en":
        q = vocab_sample[vocab_num]["nom_sing"]
        
    #Prompts ------------------------------------------------------------------
        
    prompt = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(vocab_sample[vocab_num]["nom_sing"])
    if translate_words == "gd_en":
        solutions.append(vocab_sample[vocab_num]["english"])
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def preferences(translate_words, sentence, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        subject_num = rd.randrange(7)
        object_num = rd.randrange(len(vocab_sample))
        tense = rd.randrange(2) # 0 = present tense, 1 = future conditional
        pos_neg = rd.randrange(2) # 0 = positive, 1 = negative
        likepref = rd.randrange(2) # 0 = like, 1 = prefer
    else:
        subject_num = testvalues["subject_num"]
        object_num = testvalues["object_num"]
        tense = testvalues["tense"]
        pos_neg = testvalues["pos_neg"]
        likepref = testvalues["likepref"]
        
    #Parts of sentence --------------------------------------------------------
    obj_indef = is_utility.en_indef_article(vocab_sample[object_num]["english"])
    
    ##English
    
    if tense == 0:
        if pos_neg == 0:
            like_prefer_en = ""
        else:
            like_prefer_en = en[subject_num]["do_pres"].lower() + "n't "
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
        if en[subject_num]["en_subj"].lower() in ("he", "she", "name"):
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
    sentence_en = en[subject_num]["en_subj"].capitalize() + " " + like_prefer_en.lower() + " " + obj_indef.lower()
    sentence_gd = like_prefer_gd.capitalize() + " " + pp[subject_num]["le"].lower() + " " + vocab_sample[object_num]["nom_sing"].lower()
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = like_prefer_gd.capitalize() + " ____ " + vocab_sample[object_num]["nom_sing"].lower() + ": "
        elif translate_words == "gd_en":
            prompt = "____ " + like_prefer_en.lower() + " " + obj_indef.lower() + ": "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(pp[subject_num]["le"].lower())
        elif translate_words == "gd_en":
            solutions.append(en[subject_num]["en_subj"].lower().capitalize())
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def verb_tenses(chosen_tense, verb_form, vocab_sample, testvalues = None):
    #Randomiser ---------------------------------------------------------------
    
    if testvalues == None:
        verb_num = rd.randrange(len(vocab_sample))
        pers_num = rd.randrange(len(pp))
    else:
        verb_num = testvalues["verb_num"]
        pers_num = testvalues["pers_num"]
    
    ## verb forms: statement/question, positive/negative
    if verb_form == "p_s":
        n_p = False #positive only
        q_s = False #statements only
    else:
        n_p = bool(rd.randrange(2)) #negative (T) or positive (F)
        if verb_form == "pn_s":
            q_s = False #statements only
        else:
            q_s = bool(rd.randrange(2)) #question (T) or statement (F)
    
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past","present","future"))
    
    #Verbal noun switch
    if chosen_tense == "past":
        chosen_tense = rd.choice(("past", "vn_past"))
    elif chosen_tense == "future":
        chosen_tense = rd.choice(("future", "vn_future"))
    
    
    #Parts of sentence --------------------------------------------------------
    person_gd = pp[pers_num]["pronoun_gd"]
    person_en = pp[pers_num]["en_subj"]
    
    if chosen_tense in ("past", "future"):
        v_root = vocab_sample[verb_num]["root"]
    else:
        v_noun = vocab_sample[verb_num]["verbal_noun"]
    
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
    
    prompt = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    solutions.append(sentence_gd.capitalize())
    
    #Output -------------------------------------------------------------------
    
    ## Return (question, prompt, solutions)
    return (q, prompt, solutions)

def professions_annan(translate_words, sentence, testvalues = None):
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        person_num = rd.randrange(7)
        profession_num = rd.randrange(len(professions))
    else:
        person_num = testvalues["person_num"]
        profession_num = testvalues["profession_num"]
        
    #Parts of sentence --------------------------------------------------------
    pp_annan = pp[person_num]["ann an"]
    
    if person_num < 4:
        profession_gd = professions[profession_num]["nom_sing"]
    elif person_num in (4,5,6):
        profession_gd = professions[profession_num]["nom_pl"]
    
    pronoun_en = pp[person_num]["en_subj"]
    be_en = en[person_num]["be_pres"]
    
    if person_num < 4:
        profession_en = is_utility.en_indef_article(professions[profession_num]["english"])
    elif person_num in (4,5,6):
        profession_en = is_utility.en_pl(professions[profession_num]["english"])
    
    #Construct sentence -------------------------------------------------------
    sentence_gd = "'S e " + profession_gd.lower() + " a th' " + pp_annan.lower()
    sentence_en = pronoun_en.capitalize() + " " + be_en.lower() + " " + profession_en.lower()
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = "'S e " + profession_gd.lower() + " a th' "
        elif translate_words == "gd_en":
            prompt = "____" + profession_en.lower() + ": "
        
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(pp_annan)
        elif translate_words == "gd_en":
            solutions.append(pronoun_en + " " + be_en)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def emphasis_adjectives(translate_words, vocab_sample, testvalues = None):
    
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        person_num = rd.randrange(7)
        modifier_choice = adj_modifiers[rd.randrange(len(adj_modifiers))]
        adj_num = rd.randrange(len(vocab_sample))
    else:
        person_num = testvalues["person_num"]
        modifier_choice = adj_modifiers[testvalues["modifier_choice"]]
        adj_num = testvalues["adj_num"]
    
    #Parts of sentence --------------------------------------------------------
    pers_emph = pp[person_num]["emphatic"]
    pronoun_en = pp[person_num]["en_subj"]
        
    adjective_gd = vocab_sample[adj_num]["adj_gd"]
    adjective_en = modifier_choice[0] + vocab_sample[adj_num]["english"]
    
    if modifier_choice[1] in ("ro ", "glè "):
        adjective_gd = modifier_choice[1] + is_utility.lenite(adjective_gd)
    else:
        adjective_gd = modifier_choice[1] + adjective_gd
    
    be_en = en[person_num]["be_pres"]
    
    #Construct sentence -------------------------------------------------------
    sentence_gd = "Tha " + pers_emph + " " + adjective_gd
    sentence_en = "*" + pronoun_en.capitalize() + "* " + be_en.lower() + " " + adjective_en
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    prompt = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(sentence_gd)
    elif translate_words == "gd_en":
        solutions.append(sentence_en)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def possession_mo(translate_words, sentence, vocab_sample, testvalues = None):
    #This module is only used with family or body parts vocab files
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        whose_num = rd.randrange(7)
        where_num = rd.randrange(3)
        what_num = rd.randrange(len(vocab_sample))
    else:
        whose_num = testvalues["whose_num"]
        where_num = testvalues["where_num"]
        what_num = testvalues["what_num"]
    
    #Parts of sentence --------------------------------------------------------
    ## what
    what_en = vocab_sample[what_num]["english"]
    what_gd = vocab_sample[what_num]["nom_sing"]
    
    ### plurals
    if whose_num in (4,5,6) and vocab_sample[what_num]["english"] != "hair":
        what_gd = vocab_sample[what_num]["nom_pl"]
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
        whosewhat_gd = "an " + what_gd + " " + pp[whose_num]["aig"]
        whose_en = pp[whose_num]["en_poss"]
    elif what_gd in ("nigheanan","daoine"):
        whosewhat_gd = "na " + what_gd + " " + pp[whose_num]["aig"]
        whose_en = pp[whose_num]["en_poss"]
    else:
        ## possessive article
        whose_en = pp[whose_num]["en_poss"]
        if what_gd[0] in is_utility.vowels:
            whose_gd = ("m'", "d'", "", "a", "àr", "ùr", "an")[whose_num]
        elif whose_num < 6:
            whose_gd = pp[whose_num]["possessive"]
        elif whose_num == 6:
            if what_gd[0] in ("b","m","f","p"):
                whose_gd = "am"
            else:
                whose_gd = "an"
        
        ## my/your/his -> lenition
        if whose_num in (0,1,2) and what_gd[0] not in is_utility.vowels:
            what_gd = is_utility.lenite(what_gd)
        ## her + vowel -> h-
        elif whose_num == 3 and what_gd[0] in is_utility.vowels:
            what_gd = "h-" + what_gd
        ## (y)our + vowel -> n-
        elif whose_num in (4, 5) and what_gd[0] in is_utility.vowels:
            what_gd = "n-" + what_gd
    
    #Construct sentence -------------------------------------------------------
    if what_gd in ("nighean","duine","nigheanan","daoine"):
        sentence_gd = where_gd + " " + whosewhat_gd
    else:
        if len(whose_gd) == 0:
            sentence_gd = where_gd + " " + what_gd
        else:
            sentence_gd = where_gd + " " + whose_gd + " " + what_gd
    sentence_en = where_en + " " + is_are + " " + whose_en + " " + what_en
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = where_gd + " "
        elif translate_words == "gd_en":
            prompt = where_en + " " + is_are + " ____ " + what_en + ": "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.extend([sentence_en,
                              where_en_alt + " " + is_are + " " + whose_en + " " + what_en])
    
    elif sentence == "blank":
        if translate_words == "en_gd":
            if what_gd in ("nighean","duine","nigheanan","daoine"):
                solutions.append(whosewhat_gd)
            else:
                if len(whose_gd) == 0:
                    solutions.append(what_gd)
                else:
                    solutions.append(whose_gd + " " + what_gd)
        elif translate_words == "gd_en":
            solutions.append(whose_en)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def where_from(sentence_qa, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        person_num = rd.randrange(7)
        where_num = rd.randrange(len(vocab_sample))
    else:
        person_num = testvalues["person_num"]
        where_num = testvalues["where_num"]
    
    #Parts of sentence --------------------------------------------------------
    
    if vocab_sample[where_num]["place_gd"].lower().startswith(is_utility.def_articles):
        from_gd = "às " + is_utility.prep_def(vocab_sample, where_num)
    else:
        from_gd = "à " + vocab_sample[where_num]["place_gd"]
    
    if sentence_qa == "q_and_a":
        who_question = ("thu", "mi", "e", "i", "sibh", "sinn", "iad")
        
    #Construct sentence -------------------------------------------------------
    sentence_en = en[person_num]["en_subj"].capitalize() + " " + en[person_num]["be_pres"] + " from " + vocab_sample[where_num]["english"]
    sentence_gd = "Tha " + pp[person_num]["pronoun_gd"] + " " + from_gd
    sentence_gd_alt = "'S ann " + from_gd + " a tha " + pp[person_num]["pronoun_gd"]
    
    #Questions ----------------------------------------------------------------
    if sentence_qa in ("full", "blank"): #Translate
        q = sentence_en
    else: #Answer question
        q = "Cò às a tha " + who_question[person_num] + "?"
    
    #Prompts ------------------------------------------------------------------
    if sentence_qa == "full":
        prompt = "Translation: "
    elif sentence_qa == "blank":
        prompt = "Tha " + pp[person_num]["pronoun_gd"] + " "
    elif sentence_qa == "q_and_a":
        prompt = "[" + vocab_sample[where_num]["english"] + "]: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence_qa == "full":
        solutions.extend((sentence_gd, sentence_gd_alt))
    elif sentence_qa == "blank":
        solutions.append(from_gd)
    elif sentence_qa == "q_and_a":
        solutions.extend((sentence_gd, sentence_gd_alt))
        if person_num == 1: #mi -> thu/sibh
            solutions.append("Tha sibh " + from_gd)
        elif person_num == 4: #sibh -> sinn/mi
            solutions.append("Tha mi " + from_gd)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def where_in(sentence_qa, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    contains_articles = is_utility.contains_articles(vocab_sample)
    if testvalues == None:
        person_num = rd.randrange(7)
        where_num = rd.randrange(len(vocab_sample))
    else:
        person_num = testvalues["person_num"]
        where_num = testvalues["where_num"]
    if contains_articles == True:
        if vocab_sample[where_num]["nom_sing"].lower().startswith(is_utility.def_articles):
            article_switch = 1
        else:
            article_switch = 0
    else:
        if testvalues == None:
            article_switch = rd.randrange(2)
        else:
            article_switch = testvalues["article_switch"]
        
    #Parts of sentence --------------------------------------------------------
    
    ##Indefinite article
    if article_switch == 0:
        if contains_articles == False:
            where_en = is_utility.en_indef_article(vocab_sample[where_num]["english"])
        else:
            where_en = vocab_sample[where_num]["english"]
        where_gd = "ann " + is_utility.anm(vocab_sample[where_num]["nom_sing"])
    ##Definite article
    else:
        if contains_articles == False:
            where_en = "the " + vocab_sample[where_num]["english"]
        else:
            where_en = vocab_sample[where_num]["english"]
        where_gd = "anns " + is_utility.prep_def(vocab_sample, where_num)
    
    if sentence_qa == "q_and_a":
        who_question = ("thu", "mi", "e", "i", "sibh", "sinn", "iad")
    
    #Construct sentence -------------------------------------------------------
    sentence_en = en[person_num]["en_subj"].capitalize() + " " + en[person_num]["be_pres"] + " in " + where_en
    sentence_gd = "Tha " + pp[person_num]["pronoun_gd"] + " " + where_gd
    
    #Questions ----------------------------------------------------------------
    if sentence_qa in ("full", "blank"): #Translate
        q = sentence_en
    else: #Answer question
        q = "Càite a bheil " + who_question[person_num] + "?"
    
    #Prompts ------------------------------------------------------------------
    if sentence_qa == "full":
        prompt = "Translation: "
    elif sentence_qa == "blank":
        prompt = "Tha " + pp[person_num]["pronoun_gd"] + " "
    elif sentence_qa == "q_and_a":
        prompt = "[" + where_en + "]: "
        
    solutions = []
    if sentence_qa == "full":
        solutions.append(sentence_gd)
    elif sentence_qa == "blank":
        solutions.append(where_gd)
    elif sentence_qa == "q_and_a":
        solutions.append(sentence_gd)
        if person_num == 1: #mi -> thu/sibh
            solutions.append("Tha sibh " + where_gd)
        elif person_num == 4: #sibh -> sinn/mi
            solutions.append("Tha mi " + where_gd)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def comparisons(translate_words, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        comparison_choice = rd.randrange(len(similes))
    else:
        comparison_choice = testvalues["comparison_choice"]
   
    #Construct sentence -------------------------------------------------------
    sentence_en = "As " + similes[comparison_choice]["english"] + " as " + similes[comparison_choice]["simile_en"]
    sentence_gd = "Cho " + similes[comparison_choice]["adj_gd"] + " ri " + similes[comparison_choice]["simile_gd"]
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    prompt = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(sentence_gd)
    elif translate_words == "gd_en":
        solutions.append(sentence_en)
        
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def comparatives_superlatives(vocab_sample, comp_sup, sentence, translate_words, testvalues = None):
    #Load vocab --------------------------------------------------
    nouns = vocab_sample
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        subject_num = rd.randrange(len(nouns))
        object_num = rd.randrange(len(nouns))
        adj_num = rd.randrange(len(adjectives))
    else:
        subject_num = testvalues["subject_num"]
        object_num = testvalues["object_num"]
        adj_num = testvalues["adj_num"]
    
    if comp_sup not in ("comp", "sup"):
        comp_sup = rd.choice(("comp","sup"))
    
    #Parts of sentence --------------------------------------------------------
    subject_en = nouns[subject_num]["english"]
    subject_gd = nouns[subject_num]["nom_sing"]
        
    if comp_sup == "comp":
        
        object_en = nouns[object_num]["english"]
        object_gd = nouns[object_num]["nom_sing"]
        
        comparative_gd = "nas " + adjectives[adj_num]["comp_sup"]
        
        comparative_en = adjectives[adj_num]["comp_en"]
        comparative_en_alt = "more " + adjectives[adj_num]["english"]
    
    elif comp_sup == "sup":
        subject_en = nouns[subject_num]["english"]
        subject_gd = is_utility.gd_common_article(nouns[subject_num]["nom_sing"],
                                                  "sg", 
                                                  nouns[subject_num]["gender"],
                                                  "nom")
        
        superlative_gd = "as " + adjectives[adj_num]["comp_sup"]
    
        superlative_en = adjectives[adj_num]["sup_en"]
        superlative_en_alt = "most " + adjectives[adj_num]["english"]
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
    if translate_words == "en_gd":
        q = sentence_en
        if comp_sup == "comp":
            q = q + "?"
    elif translate_words == "gd_en":
        q = sentence_gd
        if comp_sup == "comp":
            q = q + "?"
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            if comp_sup == "comp":
                prompt = "A bheil " + subject_gd + " _____ na " + object_gd + "? : "
            elif comp_sup == "sup":
                prompt = subject_gd.capitalize() + " "
        elif translate_words == "gd_en":
            if comp_sup == "comp":
                prompt = "Is " + is_utility.en_indef_article(subject_en) + " ____ than " + is_utility.en_indef_article(object_en) + "? : "
            elif comp_sup == "sup":
                prompt = "The ____ " + subject_en + ": "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.extend([sentence_en, sentence_en_alt])
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            if comp_sup == "comp":
                solutions.append(comparative_gd)
            elif comp_sup == "sup":
                solutions.append(superlative_gd)
        elif translate_words == "gd_en":
            if comp_sup == "comp":
                solutions.extend([comparative_en, comparative_en_alt])
            elif comp_sup == "sup":
                solutions.extend([superlative_en, superlative_en_alt])
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def time(translate_numbers, testvalues = None):
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        hrs_num = rd.randrange(24)
        mins_num = rd.randrange(0, 60, 5)
    else:
        hrs_num = testvalues["hrs_num"]
        mins_num = testvalues["mins_num"]
    
    #Helper functions ---------------------------------------------------------
    def get_12h(h24):
        """convert 24h time to 12h time"""
        if h24 > 12:
            return h24 - 12
        elif h24 == 0:
            return 12
        else: 
            return h24
    
    def get_hrs_am(h24):
        """Get hrs < 12"""
        if h24 >= 12:
            return h24 - 12
        else:
            return h24
    
    def get_hrs_pm(h24):
        """get hrs >= 12"""
        if h24 < 12:
            return h24 + 12
        else:
            return h24
    
    def get_hrs_gd(h24):
        hrs12 = get_12h(h24)
        if hrs12 == 1:
            return "uair"
        elif hrs12 == 2:
            return "dhà"
        elif hrs12 <= 10:
            return csvr.filter_matches(is_utility.numlist, "number", str(hrs12))[0]["cardinal"]
        elif hrs12 == 11:
            return "aon uair deug"
        elif hrs12 == 12:
            return "dà uair dheug"
    
    def get_time(hrs, mins):
        ## hrs o'clock
        if mins == 0:
            hrs12 = get_12h(hrs)
            if hrs12 == 2:
                return "dà uair"
            elif hrs12 in range(3,10):
                return get_hrs_gd(hrs) + " uairean"
            else:
                return get_hrs_gd(hrs)
    
        ## quarter past
        elif mins == 15:
            return "cairteal an dèidh " + get_hrs_gd(hrs)
    
        ## quarter to
        elif mins == 45:
            return "cairteal gu " + get_hrs_gd(hrs + 1)
    
        ## half past
        elif mins == 30:
            return "leth-uair an dèidh " + get_hrs_gd(hrs)
    
        ## other times
        else:
            mins_tofrom = min(mins, 60-mins)
            mins_gd = is_utility.digits_to_gd(mins_tofrom)
            if mins_tofrom == 20:
                mins_gd = mins_gd + " mionaid"
            elif mins_tofrom == 25:
                mins_gd = "còig mionaidean fichead"
            else:
                mins_gd = mins_gd + " mionaidean"
            if mins_tofrom == mins:
                return mins_gd + " an dèidh " + get_hrs_gd(hrs)
            else: 
                return mins_gd + " gu " + get_hrs_gd(hrs + 1)
    
    #Questions ----------------------------------------------------------------
    if translate_numbers == "dig_gd": #Digits to Gaelic
        q = f"Dè an uair a tha e? ({hrs_num:02}:{mins_num:02})"
    elif translate_numbers == "gd_dig": #Gaelic to digits
        q = f"Tha e {get_time(hrs_num, mins_num)}"
    
    
    #Prompts ------------------------------------------------------------------
    
    if translate_numbers == "dig_gd": #Digits to Gaelic
        prompt = "Tha e "
    elif translate_numbers == "gd_dig": #Gaelic to digits
        prompt = "Time (digital): "
        
    #Solutions ----------------------------------------------------------------
    
    if translate_numbers == "dig_gd": #Digits to Gaelic
        solutions = [get_time(hrs_num, mins_num)]
        if mins_num == 0:
            if hrs_num == 0:
                solutions.append("meadhan oidhche")
            elif hrs_num == 12:
                solutions.append("meadhan latha")
        
        ## in the morning
        if hrs_num < 12:
            solutions.append(get_time(hrs_num, mins_num) + " anns a' mhadainn")
        ## in the afternoon/evening
        elif hrs_num > 12 or (hrs_num == 12 and mins_num != 0):
            if hrs_num < 19:
                solutions.append(get_time(hrs_num, mins_num) + " feasgar")
            if hrs_num > 15:
                solutions.append(get_time(hrs_num, mins_num) + " as t-oidhche")
                
    elif translate_numbers == "gd_dig":
        #include a.m. and p.m. times
        hrs_am = get_hrs_am(hrs_num)
        hrs_pm = get_hrs_pm(hrs_num)
        solutions = [f"{hrs_am:02}:{mins_num:02} or {hrs_pm:02}:{mins_num:02}"]
        solutions.append(f"{hrs_pm:02}:{mins_num:02} or {hrs_am:02}:{mins_num:02}")
        solutions.extend([f"{hrs_am:02}:{mins_num:02}", f"{hrs_pm:02}:{mins_num:02}"])
        #include dropped leading zero for hours
        solutions.append(f"{hrs_am:01}:{mins_num:02}")
            
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def which_season(sentence, testvalues = None):
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        month_num = rd.randrange(12)
        use_prep = bool(rd.randrange(2)) #True = sentence with prepositional
    else:
        month_num = testvalues["month_num"]
        use_prep = testvalues["use_prep"]
        
    #Parts of sentence --------------------------------------------------------
    month_en = list_months[month_num]["english"]
    month_gd = list_months[month_num]["nom_sing"]
    
    season = csvr.filter_matches(list_seasons, "english", list_months[month_num]["season_en"])
    
    season_en = season[0]["english"]
    season_gd = season[0]["nom_sing"]
    
    #There are two ways to say the prepositional for seasons
    season_in1 = season[0]["in_gd"]
    season_in2 = "anns " + is_utility.gd_common_article(season_gd, "sg", "masc", "prep")
    
    #Construct sentence -------------------------------------------------------
    if use_prep == True:
        sentence_en = f"{month_en} is in {season_en}"
        sentence_gd = f"Tha {month_gd} {season_in1}"
    elif use_prep == False:
        sentence_en = f"It is {season_en}"
        sentence_gd = f"'S e {season_gd} a th' ann"
    
    #Questions ----------------------------------------------------------------
    q = sentence_en
    
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if use_prep == True:
            prompt = f"Tha {month_gd} "
        elif use_prep == False:
            prompt = "'S e ____ a th' ann: "
    
    #Solutions ----------------------------------------------------------------
    if sentence == "full":
        solutions = [sentence_gd]
        if use_prep == True:
            solutions.append(f"Tha {month_gd} {season_in2}")
    elif sentence == "blank":
        if use_prep == True:
            solutions = [season_in1, season_in2]
        elif use_prep == False:
            solutions = [season_gd]
    #Output -------------------------------------------------------------------
    
    ##Return (question, main solution, alternative solution, prompt)
    return (q, prompt, solutions)

def which_month(sentence, testvalues=None):
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        holiday_num = rd.randrange(len(list_holidays) + 1)
        month_num = rd.randrange(12)
        use_prep = bool(rd.randrange(2))
        pers_num = rd.randrange(7)
    else:
        holiday_num = testvalues["holiday_num"]
        month_num = testvalues["month_num"]
        use_prep = testvalues["use_prep"]
        pers_num = testvalues["pers_num"]
    
    #Parts of sentence --------------------------------------------------------
    
    if holiday_num < len(list_holidays):
        holiday_en = list_holidays[holiday_num]["english"]
        holiday_gd = list_holidays[holiday_num]["nom_sing"]
        month_en = list_holidays[holiday_num]["month_en"]
        month_gd = csvr.filter_matches(list_months, "english", month_en)[0]["nom_sing"]
        month_gender = csvr.filter_matches(list_months, "english", month_en)[0]["gender"]
    else:
        whose_en = pp[pers_num]["en_poss"].capitalize()
        whose_gd = pp[pers_num]["aig"]
        holiday_en = f"{whose_en} birthday"
        holiday_gd = f"an co-là breith {whose_gd}"
        month_en = list_months[month_num]["english"]
        month_gd = list_months[month_num]["nom_sing"]
        month_gender = list_months[month_num]["gender"]
    
    if use_prep == True:
        month_prep = is_utility.gd_common_article(month_gd, "sg", month_gender, "prep")
    
    #Construct sentence -------------------------------------------------------
    if use_prep == True:
        sentence_en = f"{holiday_en} is in {month_en}"
        sentence_gd = f"Tha {holiday_gd} anns {month_prep}"
    elif use_prep == False:
        sentence_en = f"It is {month_en}"
        sentence_gd = f"'S e {month_gd} a th' ann"
    
    #Questions ----------------------------------------------------------------
    q = sentence_en
    
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if use_prep == True:
            prompt = f"Tha {holiday_gd} anns "
        elif use_prep == False:
            prompt = "'S e ____ a th' ann: "
            
    #Solutions ----------------------------------------------------------------
    if sentence == "full":
        solutions = [sentence_gd]
    elif sentence == "blank":
        if use_prep == True:
            solutions = [month_prep]
        elif use_prep == False:
            solutions = [month_gd]
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def going_to(chosen_tense, translate_words, vocab_sample, testvalues = None):
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        person_num = rd.randrange(7)
        where_num = rd.randrange(len(vocab_sample))
    else:
        person_num = testvalues["person_num"]
        where_num = testvalues["where_num"]
        
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past","present","future"))
    
    #Verbal noun switch
    if chosen_tense == "past":
        chosen_tense = rd.choice(("past", "vn_past"))
    elif chosen_tense == "future":
        chosen_tense = rd.choice(("future", "vn_future"))
    
    #Parts of sentence --------------------------------------------------------
    person_gd = pp[person_num]["pronoun_gd"]
    person_en = pp[person_num]["en_subj"]
    
    ## "Going" in Gaelic
    if chosen_tense in ("past", "future"):
        pers_going_gd = is_utility.transform_verb("rach",
                                                  tense = chosen_tense, 
                                                  negative = False, 
                                                  question = False) + " " + person_gd
    else:
        pers_going_gd = is_utility.verbal_noun(vn = "dòl",
                                               person = person_gd,
                                               tense = chosen_tense, 
                                               negative = False, 
                                               question = False)
    ## "Going" in English
    if chosen_tense == "past":
        going_en = "went"
    elif chosen_tense == "future":
        going_en = "will go"
    elif chosen_tense == "vn_future":
        going_en = "will be going"
    elif chosen_tense == "vn_past":
        going_en = csvr.filter_matches(en, "en_subj", person_en)[0]["be_past"] + " going"
    elif chosen_tense == "present":
        going_en = csvr.filter_matches(en, "en_subj", person_en)[0]["be_pres"] + " going"
    
    ## Place
    place_en = vocab_sample[where_num]["english"]
    place_gd = vocab_sample[where_num]["place_gd"]
    
    ##lenite and add "do" form
    if place_gd.lower().startswith(is_utility.def_articles) == False:
        place_gd = is_utility.lenite(place_gd)
        if place_gd[0].lower() in is_utility.vowels or place_gd[:2].lower() == "fh":
            to_place_gd = "a dh'" + place_gd
        else:
            to_place_gd = "a " + place_gd
    else:
        art, sep, place = is_utility.extract_firstword(place_gd)
        if art == "na":
            to_place_gd = "dha na " + is_utility.lenite(place)
        elif place[:2] == "t-":
            to_place_gd = "dhan t-" + is_utility.lenite(place[2:])
        else:
            to_place_gd = "dhan " + is_utility.lenite(place)
            
    
    #Construct sentence -------------------------------------------------------
    sentence_en = person_en.capitalize() + " " + going_en + " to " + place_en
    sentence_gd = pers_going_gd.capitalize() + " " + to_place_gd
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd

    #Prompts ------------------------------------------------------------------
    prompt = "Translation: "

    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(sentence_gd)
    elif translate_words == "gd_en":
        solutions.append(sentence_en)

    #Output -------------------------------------------------------------------
    
    ##Return (question, prompt, solutions)
    return (q, prompt, solutions)

def give_to(chosen_tense, prep_object, translate_words, sentence, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        subject_num = rd.randrange(7)
        object_num = rd.randrange(7)
        gift_num = rd.randrange(len(vocab_sample))
        article_switch = bool(rd.randrange(2))
    else:
        subject_num = testvalues["subject_num"]
        object_num = testvalues["object_num"]
        gift_num = testvalues["gift_num"]
        article_switch = testvalues["article_switch"]
        
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past", "present", "future"))
    
    if prep_object == "nouns":
        names_sample = rd.sample(names, 7)
        professions_sample = rd.sample(professions, 7)
    
    #Parts of sentence --------------------------------------------------------
    
    #subject: pronouns (subject_en, subject_gd)
    if prep_object == "pronouns":
        subject_en = pp[subject_num]["en_subj"]
        subject_gd = pp[subject_num]["pronoun_gd"]
    #subject: names
    elif prep_object == "nouns":
        if article_switch == True:
            subject_en = "The " + professions_sample[subject_num]["english"]
            subject_gd = is_utility.gd_common_article(professions_sample[subject_num]["nom_sing"], 
                                                      "sg", "masc", "nom")
        else:
            subject_en = names_sample[subject_num]["english"]
            subject_gd = names_sample[subject_num]["nom_sing"]
        
    #Subject and verb: giving to
    if chosen_tense == "present":
        verb_subj_gd = is_utility.verbal_noun("toirt", subject_gd, chosen_tense, negative=False, question=False).capitalize()
        if prep_object == "pronouns":
            verb_subj_en = subject_en.capitalize() + " " + en[subject_num]["be_pres"] + " giving"
        elif prep_object == "nouns":
            verb_subj_en = subject_en.capitalize() + " is giving"
    elif chosen_tense == "past":
        verb_subj_gd = is_utility.transform_verb("thig", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
        verb_subj_en = subject_en.capitalize() + " gave"
    elif chosen_tense == "future":
        verb_subj_gd = is_utility.transform_verb("thig", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
        verb_subj_en = subject_en.capitalize() + " will give"
        
        
    #the item that's being given
    gift_en = is_utility.en_indef_article(vocab_sample[gift_num]["english"])
    gift_gd = vocab_sample[gift_num]["nom_sing"]
        
        
    #object: pronouns (subject_en, subject_gd)
    if prep_object == "pronouns":
        object_en = pp[object_num]["en_obj"]
        object_gd = pp[object_num]["do"]
    #object: names
    elif prep_object == "nouns":
        if article_switch == True:
            object_en = "the " + professions_sample[object_num]["english"]
            object_gd = professions_sample[object_num]["nom_sing"]
            if object_gd[0] == "s" and object_gd[1] in is_utility.vowels.union(set("lrn")):
                object_gd = "dhan t-" + object_gd
            else:
                object_gd = "dhan " + is_utility.lenite(object_gd, extras = ("d","t"))
                #note the final n of dhan prevents lenition of d, t
        else:
            object_en = names_sample[object_num]["english"]
            object_gd = is_utility.lenite(names_sample[object_num]["nom_sing"])
            if object_gd[0] in is_utility.vowels or object_gd[:2] == "fh":
                object_gd = "do dh'" + object_gd
            else:
                object_gd = "do " + object_gd

       
    #Construct sentences ------------------------------------------------------
    
    #English
    sentence_en = verb_subj_en + " " + object_en + " " + gift_en
    sentence_en_alt = verb_subj_en + " " + gift_en + " to " + object_en
    #Gaelic
    sentence_gd = verb_subj_gd + " " + gift_gd + " " + object_gd
    
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd": #en-gd
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = verb_subj_gd + " " + gift_gd + " "
        elif translate_words == "gd_en":
            prompt = verb_subj_en + " " + gift_en + " "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            solutions.append(sentence_en_alt)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(object_gd)
        elif translate_words == "gd_en":
           solutions.append("to " + object_en)
            
    #Output -------------------------------------------------------------------
    
    #Return (question, prompt, solutions)
    return (q, prompt, solutions)

def get_from(chosen_tense, prep_object, translate_words, sentence, vocab_sample, testvalues = None):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    if testvalues == None:
        subject_num = rd.randrange(7)
        object_num = rd.randrange(7)
        gift_num = rd.randrange(len(vocab_sample))
        article_switch = bool(rd.randrange(2))
    else:
        subject_num = testvalues["subject_num"]
        object_num = testvalues["object_num"]
        gift_num = testvalues["gift_num"]
        article_switch = testvalues["article_switch"]
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past", "present", "future"))
       
    if prep_object == "nouns":
        names_sample = rd.sample(names, 7)
        professions_sample = rd.sample(professions, 7)
 
    #Parts of sentence --------------------------------------------------------
    
    #subject: pronouns (subject_en, subject_gd)
    if prep_object == "pronouns":
        subject_en = pp[subject_num]["en_subj"]
        subject_gd = pp[subject_num]["pronoun_gd"]
    #subject: names
    elif prep_object == "nouns":
        if article_switch == True:
            subject_en = "The " + professions_sample[subject_num]["english"]
            subject_gd = is_utility.gd_common_article(professions_sample[subject_num]["nom_sing"], 
                                                      "sg", "masc", "nom")
        else:
            subject_en = names_sample[subject_num]["english"]
            subject_gd = names_sample[subject_num]["nom_sing"]
        
    #Subject and verb: getting from
    if chosen_tense == "present":
        verb_subj_gd = is_utility.verbal_noun("faighinn", subject_gd, chosen_tense, negative=False, question=False).capitalize()
        if prep_object == "pronouns":
            verb_subj_en = subject_en.capitalize() + " " + en[subject_num]["be_pres"] + " getting"
        elif prep_object == "nouns":
            verb_subj_en = subject_en.capitalize() + " is getting"
    elif chosen_tense == "past":
        verb_subj_gd = is_utility.transform_verb("faigh", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
        verb_subj_en = subject_en.capitalize() + " got"
    elif chosen_tense == "future":
        verb_subj_gd = is_utility.transform_verb("faigh", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
        verb_subj_en = subject_en.capitalize() + " will get"
        
        
    #the item that's being received
    gift_en = is_utility.en_indef_article(vocab_sample[gift_num]["english"])
    gift_gd = vocab_sample[gift_num]["nom_sing"]
        
        
    #object: pronouns (subject_en, subject_gd)
    if prep_object == "pronouns":
        object_en = pp[object_num]["en_obj"]
        object_gd = pp[object_num]["bho"]
    #object: names
    elif prep_object == "nouns":
        if article_switch == True:
            object_en = "the " + professions_sample[object_num]["english"]
            object_gd = professions_sample[object_num]["nom_sing"]
            if object_gd[0] == "s" and object_gd[1] in is_utility.vowels.union(set("lrn")):
                object_gd = "bhon t-" + object_gd
            else:
                object_gd = "bhon " + is_utility.lenite(object_gd, extras = ("d","t"))
                #note the final n of bhon prevents lenition of d, t
        else:
            object_en = names_sample[object_num]["english"]
            object_gd = "bho " + is_utility.lenite(names_sample[object_num]["nom_sing"])
       
    #Construct sentences ------------------------------------------------------
    
    #English
    sentence_en = verb_subj_en + " " + gift_en + " from " + object_en
    #Gaelic
    sentence_gd = verb_subj_gd + " " + gift_gd + " " + object_gd
    
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd": #en-gd
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
        
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt = verb_subj_gd + " " + gift_gd + " "
        elif translate_words == "gd_en":
            prompt = verb_subj_en + " " + gift_en + " "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(object_gd)
        elif translate_words == "gd_en":
           solutions.append("from " + object_en)
            
    #Output -------------------------------------------------------------------
    
    #Return (question, prompt, solutions)
    return (q, prompt, solutions)
