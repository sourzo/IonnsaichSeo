# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 18:50:34 2022

@author: Zoe
"""

#to do: add [name] has a [object]

def possession(vocab_file):
    """Practice possession with 'aig' prepositional pronoun"""
    
    #import vocabulary
    import is_utility
    import pandas as pd
    import random as rd
    import datetime as dt
    vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in vocab_list.columns or "nom_sing" not in vocab_list.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return
    pp = pd.read_csv('Vocabulary/grammar_prepPronouns.csv')
    en = pd.read_csv('Vocabulary/grammar_english.csv')
    
    #Select practice mode
    practice_mode="0"
    while practice_mode not in ("X","1","2","3","4"):
        print("Select practice mode")
        print("1: English to Gaelic, full sentence")
        print("2: English to Gaelic, fill in the blank")
        print("3: Gaelic to English, full sentence")
        print("4: Gaelic to English, fill in the blank")
        print("X: Exit")
        practice_mode = input("Practice mode: ")
    if practice_mode == "X":
        return

    #Pick vocab list sample size
    sample_size = max(1,min(int(input("Select number of words to practice, must be no more than {}: ".format(len(vocab_list)))),len(vocab_list)))
    print("Selecting {} words for practice".format(sample_size))
    vocab_sample = vocab_list.sample(n=sample_size).reset_index(drop=True)
    
    #create question order: shuffle or unshuffled!
    questions = [(x,y) for x in range(sample_size) for y in range(6)]
    shuffle = input("Shuffle questions? Y/N: ")
    if shuffle.upper() == "Y":
        rd.shuffle(questions)

    score = 0
    q_count = 0
    start_time = dt.datetime.now()

    #Loop through vocab list:
    for q in questions:
        #Need indefinite article in front of object
        if vocab_sample.loc[q[0],"english"][0] in ("a","e","i","o","u"):
            obj_indef = "an " + vocab_sample.loc[q[0],"english"]
        else:
            obj_indef = "a " + vocab_sample.loc[q[0],"english"]

        #Practice modes 1 & 2: English to Gaelic
        if practice_mode in ("1","2"):

            #Show English sentence
            print()
            print(en.loc[q[1],"en_subj"].capitalize(), en.loc[q[1],"have_pres"], obj_indef)

            if practice_mode == "1":
                #User must write sentence in Gaelic
                phrase = input()
                if phrase.lower() == "stop practice":
                    break
                elif phrase.lower().strip() == "tha " + vocab_sample.loc[q[0],"nom_sing"].lower() + " " + pp.loc[q[1],"aig"].lower():
                    is_utility.encourage()
                    score = score + 1
                else:
                    print("Nope, correct answer was: ", "Tha " + vocab_sample.loc[q[0],"nom_sing"] + " " + pp.loc[q[1],"aig"])
                q_count = q_count + 1

            if practice_mode == "2":
                #User must fill in the missing Gaelic
                phrase = input("Tha " + vocab_sample.loc[q[0],"nom_sing"].lower() + " ")
                if phrase.lower() == "stop practice":
                    break
                elif phrase.lower().strip() == pp.loc[q[1],"aig"].lower():
                    is_utility.encourage()
                    score = score + 1
                else:
                    print("Nope, correct answer was: ", "Tha " + vocab_sample.loc[q[0],"nom_sing"] + " " + pp.loc[q[1],"aig"])
                q_count = q_count + 1  

        #Practice modes 3, 4: Gaelic to English
        elif practice_mode in ("3","4"):

            #Show Gaelic phrase:
            print()
            print("Tha " + vocab_sample.loc[q[0],"nom_sing"].lower() + " " + pp.loc[q[1],"aig"].lower())

            if practice_mode == "3":
                #User must write sentence in English
                phrase = input()
                if phrase.lower() == "stop practice":
                    break
                elif phrase.lower().strip() == en.loc[q[1],"en_subj"].lower() + " " + en.loc[q[1],"have_pres"].lower() + " " + obj_indef.lower():
                    is_utility.encourage()
                    score = score + 1
                else:
                    print("Nope, correct answer was: ", en.loc[q[1],"en_subj"].capitalize() + " " + en.loc[q[1],"have_pres"].lower() + " " + obj_indef.lower())
                q_count = q_count + 1  


            elif practice_mode == "4":
                #User must fill in the missing English 
                phrase = input("____ " + obj_indef.lower() + ": ")
                if phrase.lower() == "stop practice":
                    break
                elif phrase.lower().strip() == en.loc[q[1],"en_subj"].lower() + " " + en.loc[q[1],"have_pres"].lower():
                    is_utility.encourage()
                    score = score + 1
                else:
                    print("Nope, correct answer was: ", en.loc[q[1],"en_subj"].capitalize() + " " + en.loc[q[1],"have_pres"].lower() + " " + obj_indef.lower())
                q_count = q_count + 1
                
    print("End of practice!")
    print("Your score is {} out of {}".format(score, q_count))
    print("Time taken: ",dt.datetime.now() -start_time)
    