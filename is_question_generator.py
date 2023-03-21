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

def give_get(chosen_tense, translate_words, sentence, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    
    subject_num = rd.randrange(8)
    object_num = rd.randrange(8)
    gift_num = rd.randrange(csvr.length(vocab_sample))
    give_get_num = rd.randrange(2) # 0 = give to, 1 = get from
    if chosen_tense == "any":
        chosen_tense = rd.choice(("past", "present", "future"))
    
    #Parts of sentence --------------------------------------------------------
    
    #subject: pronouns (subject_en, subject_gd)
    if subject_num < 7:
        subject_en = pp["en_subj"][subject_num]
        subject_gd = pp["pronoun_gd"][subject_num]
    #subject: names
    elif subject_num == 7:
        name = rd.randrange(csvr.length(names))
        subject_en = names["english"][name]
        subject_gd = names["nom_sing"][name]
        
    
    #Subject and verb: giving to
    if give_get_num == 0:
        if chosen_tense == "present":
            verb_subj_gd = is_utility.verbal_noun("toirt", subject_gd, chosen_tense, negative=False, question=False).capitalize()
            verb_subj_en = subject_en.capitalize() + " " + en["be_pres"][subject_num] + " giving"
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
            verb_subj_en = subject_en.capitalize() + " " + en["be_pres"][subject_num] + " getting"
        elif chosen_tense == "past":
            verb_subj_gd = is_utility.transform_verb("faigh", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
            verb_subj_en = subject_en.capitalize() + " got"
        elif chosen_tense == "future":
            verb_subj_gd = is_utility.transform_verb("faigh", chosen_tense, negative=False, question=False).capitalize() + " " + subject_gd
            verb_subj_en = subject_en.capitalize() + " will get"
        prep_en = "from"
        
        
    #the item that's being given
    gift_en = is_utility.en_indef_article(vocab_sample["english"][gift_num])
    gift_gd = vocab_sample["nom_sing"][gift_num]
        
        
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
        name = rd.randrange(csvr.length(names))
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
        prompt1 = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt1 = verb_subj_gd + " " + gift_gd + " "
        elif translate_words == "gd_en":
            prompt1 = verb_subj_en + " " + gift_en + " "
            
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
    
    #Return (question, solutions, prompt)
    if translate_words == "en_gd":
        return (q, solutions, prompt1)
    elif translate_words == "gd_en":
        return (q, solutions, prompt1)

def possession_aig(translate_words, sentence, vocab_sample):
    
    #Load vocab --------------------------------------------------
    
    
    #Randomiser ---------------------------------------------------------------
    
    subject_num = rd.randrange(6)
    object_num = rd.randrange(csvr.length(vocab_sample))
    obj_indef = is_utility.en_indef_article(vocab_sample["english"][object_num])


    #Construct sentences ------------------------------------------------------
    
    sentence_en = en["en_subj"][subject_num].capitalize() + " " + en["have_pres"][subject_num].lower() + " " + obj_indef.lower()
    sentence_gd = "Tha " + vocab_sample["nom_sing"][object_num].lower() + " " + pp["aig"][subject_num].lower()

    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd

    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt1 = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt1 = "Tha " + vocab_sample["nom_sing"][object_num].lower() + " "
        elif translate_words == "gd_en":
            prompt1 = "____ " + obj_indef.lower() + ": "
   

    #Solutions ----------------------------------------------------------------
    solutions = []
    
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(pp["aig"][subject_num].lower())
        elif translate_words == "gd_en":
            solutions.append(en["en_subj"][subject_num].lower().capitalize() + " " + en["have_pres"][subject_num].lower())
        
    
    #Output -------------------------------------------------------------------
    
    #Return (question, solutions, prompt)
    if translate_words == "en_gd":
        return (q, solutions, prompt1)
    elif translate_words == "gd_en":
        return (q, solutions, prompt1)

def gender(gender_mode, vocab_sample):
    #Load vocab --------------------------------------------------
    
    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(csvr.length(vocab_sample))
    if gender_mode == "def_all":
        gender_mode = rd.choice(("def_nom"#, "def_prep", "def_poss"
                                 ))
    #Parts of sentence --------------------------------------------------------
    adjective_en = "small"
    adjective_gd = "beag"
            
    #Construct sentence -------------------------------------------------------
    
    if gender_mode == "adj":
    
        sentence_en = "A " + adjective_en + " " + vocab_sample["english"][vocab_num]
            
        if vocab_sample["gender"][vocab_num] == "masc":
            sentence_gd = vocab_sample["nom_sing"][vocab_num] + " " + adjective_gd
        elif vocab_sample["gender"][vocab_num] == "fem":
            sentence_gd = vocab_sample["nom_sing"][vocab_num] + " " + is_utility.lenite(adjective_gd)
            
    elif gender_mode == "def_nom":
    
        sentence_en = "The " + vocab_sample["english"][vocab_num] + " (nominative)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample["nom_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_sample["gender"][vocab_num],
                                                case = "nom")
    
    #warning - vocab lists don't have prep_sing at the moment
    elif gender_mode == "def_prep":
    
        sentence_en = "The " + vocab_sample["english"][vocab_num] + " (prepositional)"
        
        sentence_gd = is_utility.gd_common_article(word = vocab_sample["prep_sing"][vocab_num],
                                                sg_pl = "sg",
                                                gender = vocab_sample["gender"][vocab_num],
                                                case = "prep")
    
    #warning - vocab lists don't have poss_sing at the moment
    elif gender_mode == "def_poss":
    
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

    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def numbers(translate_numbers, max_num):
    
    #Randomiser ---------------------------------------------------------------
    num = rd.randint(1,max_num)
       
    #Work out the Gaelic for given number ----------------------------------
    num_gd = is_utility.digits_to_gd(num)
            
    #Questions ----------------------------------------------------------------
    
    if translate_numbers == "dig_gd":
        q = str(num)
        
    elif translate_numbers == "gd_dig":
        q = num_gd
    
    #Prompts ------------------------------------------------------------------
    
    if translate_numbers == "dig_gd":
        prompt1 = "Àireamh: "
        
    elif translate_numbers == "gd_dig":
        prompt1 = "Number (in digits): "
    
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    if translate_numbers == "dig_gd":
        solutions.append(num_gd)
        
    elif translate_numbers == "gd_dig":
        solutions.append(str(num))
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def plurals(translate_generic, vocab_sample):
    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(csvr.length(vocab_sample))
    
    #Work out the Gaelic for given number ----------------------------------
            
    #Questions ----------------------------------------------------------------
    
    if translate_generic == "from_en": #Plural from English
        q = "Pluralise the Gaelic for: " + vocab_sample["english"][vocab_num]
    
    elif translate_generic == "from_gd": #Plural from Gaelic
        q = "Pluralise: " + vocab_sample["nom_sing"][vocab_num]
        
    #Prompts ------------------------------------------------------------------
    
    prompt1 = "Plural: "
        
    #Solutions ----------------------------------------------------------------
    
    solutions = []
    
    solutions.append(vocab_sample["nom_pl"][vocab_num])
            
    #Output -------------------------------------------------------------------
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def learn_nouns(translate_words, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    vocab_num = rd.randrange(csvr.length(vocab_sample))
        
    #Questions ----------------------------------------------------------------
    
    if translate_words == "en_gd":
        q = vocab_sample["english"][vocab_num]
    if translate_words == "gd_en":
        q = vocab_sample["nom_sing"][vocab_num]
        
    #Prompts ------------------------------------------------------------------
        
    prompt1 = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(vocab_sample["nom_sing"][vocab_num])
    if translate_words == "gd_en":
        solutions.append(vocab_sample["english"][vocab_num])
    
    #Output -------------------------------------------------------------------

    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def preferences(translate_words, sentence, vocab_sample):
    #Load vocab --------------------------------------------------
    

    #Randomiser ---------------------------------------------------------------
    subject_num = rd.randrange(6)
    object_num = rd.randrange(csvr.length(vocab_sample))
    
    tense = rd.randrange(2) # 0 = present tense, 1 = future conditional
    pos_neg = rd.randrange(2) # 0 = positive, 1 = negative
    likepref = rd.randrange(2) # 0 = like, 1 = prefer

        
    #Parts of sentence --------------------------------------------------------
    obj_indef = is_utility.en_indef_article(vocab_sample["english"][object_num])
    
    ##English

    if tense == 0:
        if pos_neg == 0:
            like_prefer_en = ""
        else:
            like_prefer_en = en["do_pres"][subject_num].lower() + "n't "
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
        if en["en_subj"][subject_num].lower() in ("he", "she", "name"):
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
    sentence_en = en["en_subj"][subject_num].capitalize() + " " + like_prefer_en.lower() + " " + obj_indef.lower()
    sentence_gd = like_prefer_gd.capitalize() + " " + pp["le"][subject_num].lower() + " " + vocab_sample["nom_sing"][object_num].lower()

    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    if sentence == "full":
        prompt1 = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt1 = like_prefer_gd.capitalize() + " ____ " + vocab_sample["nom_sing"][object_num].lower() + ": "
        elif translate_words == "gd_en":
            prompt1 = "____ " + like_prefer_en.lower() + " " + obj_indef.lower() + ": "
            
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence == "full":
        if translate_words == "en_gd":
            solutions.append(sentence_gd)
        elif translate_words == "gd_en":
            solutions.append(sentence_en)
            
    elif sentence == "blank":
        if translate_words == "en_gd":
            solutions.append(pp["le"][subject_num].lower())
        elif translate_words == "gd_en":
            solutions.append(en["en_subj"][subject_num].lower().capitalize())
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def verb_tenses(chosen_tense, verb_form, vocab_sample):
    #Randomiser ---------------------------------------------------------------
    
    ## verb forms: statement/question, positive/negative
    if verb_form == "p_s":
        n_p = False #positive only
        q_s = False #statements only
    else:
        n_p = bool(rd.getrandbits(1)) #negative (T) or positive (F)
        if verb_form == "pn_s":
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
    verb_num = rd.randrange(csvr.length(vocab_sample))
    
    ## person
    pers_num = rd.randrange(csvr.length(pp))
    
    #Parts of sentence --------------------------------------------------------
    person_gd = pp["pronoun_gd"][pers_num]
    person_en = pp["en_subj"][pers_num]
    
    if chosen_tense in ("past", "future"):
        v_root = vocab_sample["root"][verb_num]
        print(v_root)
    else:
        v_noun = vocab_sample["verbal_noun"][verb_num]
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
    
    ## Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def professions_annan(translate_words, sentence):
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(6)
    profession_num = rd.randrange(csvr.length(professions))
    #Parts of sentence --------------------------------------------------------
    pp_annan = pp["ann an"][person_num]
    
    if person_num < 4:
        profession_gd = professions["nom_sing"][profession_num]
    elif person_num in (4,5,6):
        profession_gd = professions["nom_pl"][profession_num]
    
    pronoun_en = pp["en_subj"][person_num]
    be_en = en["be_pres"][person_num]
    
    if person_num < 4:
        profession_en = is_utility.en_indef_article(professions["english"][profession_num])
    elif person_num in (4,5,6):
        profession_en = is_utility.en_pl(professions["english"][profession_num])
    
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
        prompt1 = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt1 = "'S e " + profession_gd.lower() + " a th' "
        elif translate_words == "gd_en":
            prompt1 = "____" + profession_en.lower() + ": "
        
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

    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def emphasis_adjectives(translate_words, vocab_sample):
    
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
    adj_num = rd.randrange(csvr.length(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    pers_emph = pp["emphatic"][person_num]
    pronoun_en = pp["en_subj"][person_num]
        
    adjective_gd = vocab_sample["adj_gd"][adj_num]
    adjective_en = modifier_choice[0] + vocab_sample["english"][adj_num]
    
    if modifier_choice[1] in ("ro ", "glè "):
        adjective_gd = modifier_choice[1] + is_utility.lenite(adjective_gd)
    else:
        adjective_gd = modifier_choice[1] + adjective_gd
    
    be_en = en["be_pres"][person_num]
    
    #Construct sentence -------------------------------------------------------
    sentence_gd = "Tha " + pers_emph + " " + adjective_gd
    sentence_en = "*" + pronoun_en.capitalize() + "* " + be_en.lower() + " " + adjective_en
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd
    
    #Prompts ------------------------------------------------------------------
    prompt1 = "Translation: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(sentence_gd)
    elif translate_words == "gd_en":
        solutions.append(sentence_en)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def possession_mo(translate_words, sentence, vocab_sample):
    #This module is only used with family or body parts vocab files
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    whose_num = rd.randrange(7)
    where_num = rd.randrange(3)
    what_num = rd.randrange(csvr.length(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    ## what
    what_en = vocab_sample["english"][what_num]
    what_gd = vocab_sample["nom_sing"][what_num]
    
    ### plurals
    if whose_num in (4,5,6) and vocab_sample["english"][what_num] != "hair":
        what_gd = vocab_sample["nom_pl"][what_num]
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
        whosewhat_gd = "an " + what_gd + " " + pp["aig"][whose_num]
        whose_en = pp["en_poss"][whose_num]
    elif what_gd in ("nigheanan","daoine"):
        whosewhat_gd = "na " + what_gd + " " + pp["aig"][whose_num]
        whose_en = pp["en_poss"][whose_num]
    else:
        ## possessive article
        whose_en = pp["en_poss"][whose_num]
        if what_gd[0] in is_utility.vowels:
            whose_gd = ("m'", "d'", "", "a", "àr", "ùr", "an")[whose_num]
        elif whose_num < 6:
            whose_gd = pp["possessive"][whose_num]
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
        prompt1 = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            prompt1 = where_gd + " "
        elif translate_words == "gd_en":
            prompt1 = where_en + " " + is_are + " ____ " + what_en + ": "
    
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
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def where_from(sentence_qa, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(7)
    where_num = rd.randrange(csvr.length(vocab_sample))
    
    #Parts of sentence --------------------------------------------------------
    
    if vocab_sample["nom_sing"][where_num].lower().startswith(is_utility.def_articles):
        from_gd = "às " + is_utility.prep_def(vocab_sample, where_num)
    else:
        from_gd = "à " + vocab_sample["nom_sing"][where_num]
    
    if sentence_qa == "q_and_a":
        who_question = ("thu", "mi", "e", "i", "sibh", "sinn", "iad")
        
    #Construct sentence -------------------------------------------------------
    sentence_en = en["en_subj"][person_num].capitalize() + " " + en["be_pres"][person_num] + " from " + vocab_sample["english"][where_num]
    sentence_gd = "Tha " + pp["pronoun_gd"][person_num] + " " + from_gd
    
    #Questions ----------------------------------------------------------------
    if sentence_qa in ("full", "blank"): #Translate
        q = sentence_en
    else: #Answer question
        q = "Cò às a tha " + who_question[person_num] + "?"
    
    #Prompts ------------------------------------------------------------------
    if sentence_qa == "full":
        prompt1 = "Translation: "
    elif sentence_qa == "blank":
        prompt1 = "Tha " + pp["pronoun_gd"][person_num] + " "
    elif sentence_qa == "q_and_a":
        prompt1 = "[" + vocab_sample["english"][where_num] + "]: "
    
    #Solutions ----------------------------------------------------------------
    solutions = []
    if sentence_qa == "full":
        solutions.append(sentence_gd)
    elif sentence_qa == "blank":
        solutions.append(from_gd)
    elif sentence_qa == "q_and_a":
        solutions.append(sentence_gd)
        if person_num == 1: #mi -> thu/sibh
            solutions.append("Tha sibh " + from_gd)
        elif person_num == 4: #sibh -> sinn/mi
            solutions.append("Tha mi " + from_gd)
    
    #Output -------------------------------------------------------------------
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def where_in(sentence_qa, contains_articles, vocab_sample):
    #Load vocab --------------------------------------------------
    
    #Randomiser ---------------------------------------------------------------
    person_num = rd.randrange(7)
    where_num = rd.randrange(csvr.length(vocab_sample))
    if contains_articles == True:
        if vocab_sample["nom_sing"][where_num].lower().startswith(is_utility.def_articles):
            article_switch = 1
        else:
            article_switch = 0
    else:
        article_switch = rd.randrange(2)
        
    #Parts of sentence --------------------------------------------------------
    
    ##Indefinite article
    if article_switch == 0:
        if contains_articles == False:
            where_en = is_utility.en_indef_article(vocab_sample["english"][where_num])
        else:
            where_en = vocab_sample["english"][where_num]
        where_gd = "ann " + is_utility.anm(vocab_sample["nom_sing"][where_num])
    ##Definite article
    else:
        if contains_articles == False:
            where_en = "the " + vocab_sample["english"][where_num]
        else:
            where_en = vocab_sample["english"][where_num]
        where_gd = "anns " + is_utility.prep_def(vocab_sample, where_num)
    
    if sentence_qa == "q_and_a":
        who_question = ("thu", "mi", "e", "i", "sibh", "sinn", "iad")
    
    #Construct sentence -------------------------------------------------------
    sentence_en = en["en_subj"][person_num].capitalize() + " " + en["be_pres"][person_num] + " in " + where_en
    sentence_gd = "Tha " + pp["pronoun_gd"][person_num] + " " + where_gd
    
    #Questions ----------------------------------------------------------------
    if sentence_qa in ("full", "blank"): #Translate
        q = sentence_en
    else: #Answer question
        q = "Càite a bheil " + who_question[person_num] + "?"
    
    #Prompts ------------------------------------------------------------------
    if sentence_qa == "full":
        prompt1 = "Translation: "
    elif sentence_qa == "blank":
        prompt1 = "Tha " + pp["pronoun_gd"][person_num] + " "
    elif sentence_qa == "q_and_a":
        prompt1 = "[" + where_en + "]: "
        
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
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def comparisons(translate_words):
    #Load vocab --------------------------------------------------
    similes = csvr.read_csv("adjectives_comparisons")
    
    #Randomiser ---------------------------------------------------------------
    comparison_choice = rd.randrange(csvr.length(similes))
   
    #Construct sentence -------------------------------------------------------
    sentence_en = "As " + similes["english"][comparison_choice] + " as " + similes["simile_en"][comparison_choice]
    sentence_gd = "Cho " + similes["adj_gd"][comparison_choice] + " ri " + similes["simile_gd"][comparison_choice]
    
    #Questions ----------------------------------------------------------------
    if translate_words == "en_gd":
        q = sentence_en
    elif translate_words == "gd_en":
        q = sentence_gd

    #Prompts ------------------------------------------------------------------
    prompt1 = "Translation: "

    #Solutions ----------------------------------------------------------------
    solutions = []
    if translate_words == "en_gd":
        solutions.append(sentence_gd)
    elif translate_words == "gd_en":
        solutions.append(sentence_en)

    #Output -------------------------------------------------------------------
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def comparatives_superlatives(vocab_sample, comp_sup, sentence, translate_words):
    #Load vocab --------------------------------------------------
    nouns = vocab_sample
    adjectives = csvr.read_csv("adjectives_misc").sample(10).reset_index(drop=True)
    #Randomiser ---------------------------------------------------------------
    subject_num = rd.randrange(csvr.length(nouns))
    object_num = rd.randrange(csvr.length(nouns))
    adj_num = rd.randrange(csvr.length(adjectives))
    
    if comp_sup not in ("comp", "sup"):
        comp_sup = rd.choice(("comp","sup"))
    
    #Parts of sentence --------------------------------------------------------
    subject_en = nouns["english"][subject_num]
    subject_gd = nouns["nom_sing"][subject_num]
        
    if comp_sup == "comp":
        
        object_en = nouns["english"][object_num]
        object_gd = nouns["nom_sing"][object_num]
        
        comparative_gd = "nas " + adjectives["comp_sup"][adj_num]
        
        comparative_en = adjectives["comp_en"][adj_num]
        comparative_en_alt = "more " + adjectives["english"][adj_num]
    
    elif comp_sup == "sup":
        subject_en = nouns["english"][subject_num]
        subject_gd = is_utility.gd_common_article(nouns["nom_sing"][subject_num],
                                                  "sg", 
                                                  nouns["gender"][subject_num],
                                                  "nom")
        
        superlative_gd = "as " + adjectives["comp_sup"][adj_num]
    
        superlative_en = adjectives["sup_en"][adj_num]
        superlative_en_alt = "most " + adjectives["english"][adj_num]
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
        prompt1 = "Translation: "
    elif sentence == "blank":
        if translate_words == "en_gd":
            if comp_sup == "comp":
                prompt1 = "A bheil " + subject_gd + " _____ na " + object_gd + "? : "
            elif comp_sup == "sup":
                prompt1 = subject_gd.capitalize() + " "
        elif translate_words == "gd_en":
            if comp_sup == "comp":
                prompt1 = "Is " + is_utility.en_indef_article(subject_en) + " ____ than " + is_utility.en_indef_article(object_en) + "? : "
            elif comp_sup == "sup":
                prompt1 = "The ____ " + subject_en + ": "
    
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
    
    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)

def time(translate_numbers):
    
    #Randomiser ---------------------------------------------------------------
    hrs_num = rd.randrange(24)
    mins_num = rd.randrange(0, 60, 5)
    
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
            return csvr.filter_matches(is_utility.numlist, "number", hrs12)["cardinal"][0]
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
        prompt1 = "Tha e "
    elif translate_numbers == "gd_dig": #Gaelic to digits
        prompt1 = "Time (digital): "
        
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

    ##Return (question, solutions, prompt)
    return (q, solutions, prompt1)
