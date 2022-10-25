# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 17:57:58 2022

@author: Zoe

To do:
    Imperative?
    a/an + gift (English sentence)
    questions & negatives?
"""
def lenite(word):
    if word[0].lower() not in ("l","n","r","a","e","i","o","u","à","è","ì","ò","ù"):
        if word[0:2].lower() not in ("sm","st","sg","sp"):
            word = word[0] + "h" + word[1:]
            
    return word

def give_get(workbook,sheet):
    """practice tense, to/from, prepositional pronouns for to/from"""
    
    #Select practice mode
    tense="0"
    while tense not in ("1","2","3"#,"4"
                        ):
        print("Select tense")
        print("1: Present tense")
        print("2: Past tense")
        print("3: Future tense")
        #print("4: All tenses")
        tense = input("Tense: ")
    translate="0"
    while translate not in ("1","2"):
        print("Select translation direction")
        print("1: English to Gaelic")
        print("2: Gaelic to English")
        translate = input("Translation direction: ")

    #load vocabulary
    import pandas as pd
    grammar_en = pd.read_excel('C:/Users/Zoe/Documents/GitHub/IonnsaichSeo/Vocabulary/grammar.ods',
                               sheet_name="en_grammar",
                               engine='odf')
    pronouns = pd.read_excel('C:/Users/Zoe/Documents/GitHub/IonnsaichSeo/Vocabulary/grammar.ods',
                               sheet_name="prep_pronouns",
                               engine='odf')
    names = pd.read_excel('C:/Users/Zoe/Documents/GitHub/IonnsaichSeo/Vocabulary/people.ods',
                               sheet_name="names",
                               engine='odf')
    gifts = pd.read_excel('C:/Users/Zoe/Documents/GitHub/IonnsaichSeo/Vocabulary/{}.ods'.format(workbook),
                               sheet_name=sheet,
                               engine='odf')
    import random as rd

    subject_num = rd.randrange(8)
    object_num = rd.randrange(8)
    give_get_num = rd.randrange(2)
    gift_num = rd.randrange(gifts["english"].count())
    
    #the item that's being given
    gift_en = gifts["english"][gift_num]
    gift_gd = gifts["nom_sing"][gift_num]
    
    #giving to
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
    #getting from
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
        
    #subject: pronouns
    if subject_num < 7:
        subject_en = pronouns["en_subj"][subject_num]
        subject_gd = pronouns["pronoun_gd"][subject_num]
    #subject: names
    elif subject_num == 7:
        name = rd.randrange(names["english"].count())
        subject_en = names["english"][name]
        subject_gd = names["nom_sing"][name]
        
    #object: pronouns
    if object_num < 7:
        object_en = grammar_en["en_obj"][object_num]
        #Prep pronouns for do/bho
        if give_get_num==0:
            object_gd = pronouns["do"][object_num]
        else:
            object_gd = pronouns["bho"][object_num]
    #object: names
    elif object_num == 7:
        name = rd.randrange(names["english"].count())
        object_en = names["english"][name]
        lenited_name = lenite(names["nom_sing"][name])
        if give_get_num==0:
            if lenited_name[0].lower() in ("a","e","i","o","u","à","è","ì","ò","ù"):
                object_gd = "do dh'" + lenited_name
            elif lenited_name[0:2] == "fh":
                object_gd = "do dh'" + lenited_name
            else:
                object_gd = "do " + lenited_name
        elif give_get_num==1:
            object_gd = "bho " + lenited_name
   
    #Present tense sentences
    #English
    print(subject_en.capitalize(), give_get_en, gift_en, prep_en, object_en)
    if tense == "1":
        #Gaelic - with verbal noun
        print("Tha", subject_gd, give_get_gd, gift_gd, object_gd)
    #Past / Future tense sentences
    elif tense in ("2", "3"):
        #Gaelic
        print(give_get_gd.capitalize(), subject_gd, gift_gd, object_gd)

    
give_get("food_drink","drink")
