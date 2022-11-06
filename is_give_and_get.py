# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:57:58 2022

@author: Zoe

To do:
    Imperative?
    add the indefinite article to english sentences
    switch the English "get" sentences to the more natural order
    questions & negatives?
"""


def give_get(vocab_file):
    """practice tense, to/from, prepositional pronouns for to/from"""
    import is_utility
    import pandas as pd
    import random as rd
    import datetime as dt
    
    #Select practice mode
    tense="0"
    while tense not in ("X","1","2","3"#,"4"
                        ):
        print("Select tense")
        print("1: Present tense")
        print("2: Past tense")
        print("3: Future tense")
        #print("4: All tenses")
        print("X: Exit")
        tense = input("Tense: ")
    if tense=="X":
        return
    
    translate="0"
    while translate not in ("X","1","2"):
        print("Select translation direction")
        print("1: English to Gaelic")
        print("2: Gaelic to English")
        print("X: Exit")
        translate = input("Translation direction: ")
    if translate=="X":
        return

    #load vocabulary
    grammar_en = pd.read_csv('Vocabulary/grammar_english.csv')
    pronouns = pd.read_csv('Vocabulary/grammar_prepPronouns.csv')
    names = pd.read_csv('Vocabulary/people_names.csv')
    gifts = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in gifts.columns or "nom_sing" not in gifts.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return
    
    print("Type 'stop practice' to finish")
    answer = ""
    q_count = 0
    score = 0
    start_time = dt.datetime.now()
    
    while answer.lower().strip() != "stop practice":
        q_count = q_count + 1
        #Randomise a sentence
        subject_num = rd.randrange(8)
        object_num = rd.randrange(8)
        gift_num = rd.randrange(gifts["english"].count())
        give_get_num = rd.randrange(2) # 0 = give to, 1 = get from
        
        #the item that's being given
        gift_en = is_utility.indef_article(gifts["english"][gift_num])
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
       
        #Full sentence: English
        if give_get_num == 0:
            sentence_en = subject_en.capitalize() + " " + give_get_en + " " + object_en + " " + gift_en
            sentence_en_alt = subject_en.capitalize() + " " + give_get_en + " " + gift_en + " " + prep_en + " " + object_en
        elif give_get_num == 1:
           sentence_en = subject_en.capitalize() + " " + give_get_en + " " + gift_en + " " + prep_en + " " + object_en
        #Full sentence: Gaelic
        if tense == "1":
            #Gaelic - with verbal noun
            sentence_gd = "Tha " + subject_gd + " " + give_get_gd + " " + gift_gd + " " + object_gd
        #Past / Future tense sentences
        elif tense in ("2", "3"):
            #Gaelic
            sentence_gd = give_get_gd.capitalize() + " " + subject_gd + " " + gift_gd + " " + object_gd
            
        #Display sentence to translate
        if translate == "1": #en to gd
            print()
            print(sentence_en)
            answer = input()
        elif translate == "2": #gd to en
            print()
            print(sentence_gd)
            answer = input()
            
        #Check answer
        if answer.lower().strip() == "stop practice":
            break
        elif translate == "1": #en to gd
            if answer.lower().strip() == sentence_gd.lower():
                print()
                is_utility.encourage()
                score = score + 1
            else:
                print()
                print("Nope, correct answer is: ",sentence_gd)
        elif translate == "2": #gd to en
            if (answer.lower().strip() == sentence_en.lower() or answer.lower().strip() == sentence_en_alt.lower()):
                print()
                is_utility.encourage()
                score = score + 1
            else:
                print()
                print("Nope, correct answer is: ", sentence_en)
                
    print()
    print("End of practice!")
    print("Your score is {} out of {}".format(score, q_count))
    print("Time taken: ",dt.datetime.now() -start_time)
