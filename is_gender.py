# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 16:48:11 2022

@author: Zoe

To do:
    add practice mode 5: all cases
    add prep and possessive cases: 
        need to first understand the prep and possessive forms of nouns
        then create sentences which make sense for all nouns ("on the"?)
    add more adjectives?
"""

def gender(vocab_file):
    """Practice noun gender"""
    import is_utility
    import pandas as pd
    import random as rd
    import datetime as dt
    
    vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if any(["english" not in vocab_list.columns,
        "nom_sing" not in vocab_list.columns,
        "gender" not in vocab_list.columns]):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' and 'gender' (lower-case))
        return

    #Select practice mode
    practice_mode="0"
    while practice_mode not in ("x","1","2",#"3","4","5"
                                ):
        print("Select practice mode")
        print("1: Adjectives")
        print("2: Definite articles (nom.)")
        #print("3: Definite articles (prep.)")
        #print("4: Definite articles (poss.)")
        #print("5: Definite articles (All)")
        print("X: Exit")
        practice_mode = input("Practice mode: ").lower().strip()
        
    if practice_mode == "x":
        return

    elif practice_mode == "1":
        #basic adjectives? Start "small"
        adjective_en = "small"
        adjective_gd = "beag"
        
        print("Type 'stop practice' to finish")
        answer = ""
        q_count = 0
        score = 0
        start_time = dt.datetime.now()

        while answer != "stop practice":
            q_count = q_count + 1
            #questions
            vocab_num = rd.randrange(len(vocab_list))
          
            #solution
            if vocab_list["gender"][vocab_num] == "masc":
                solution = vocab_list["nom_sing"][vocab_num] + " " + adjective_gd
            elif vocab_list["gender"][vocab_num] == "fem":
                solution = vocab_list["nom_sing"][vocab_num] + " " + is_utility.lenite(adjective_gd)
            
            #User input
            print()
            answer = input("A " + adjective_en + " " + vocab_list["english"][vocab_num] + ": ").lower().strip()

            #Check answer
            if answer == "stop practice":
                break
            elif answer == solution:
                print()
                is_utility.encourage()
                score = score + 1
            else:
                print()
                print("No, the correct answer is:", solution)
    elif practice_mode in ("2","3","4","5"
                               ):
            
        print("Type 'stop practice' to finish")
        answer = ""
        q_count = 0
        score = 0
        start_time = dt.datetime.now()

        while answer != "stop practice":
            q_count = q_count + 1
            #question randomisation
            vocab_num = rd.randrange(len(vocab_list))
            
            #solution
            #nominative
            if practice_mode == "2":
                solution = is_utility.gd_common_article(word = vocab_list["nom_sing"][vocab_num],
                                                        sg_pl = "sg",
                                                        gender = vocab_list["gender"][vocab_num],
                                                        case = "nom")
            #prepositional
            #warning - vocab lists don't have prep_sing at the moment
            elif practice_mode == "3":
                solution = is_utility.gd_common_article(word = vocab_list["prep_sing"][vocab_num],
                                                        sg_pl = "sg",
                                                        gender = vocab_list["gender"][vocab_num],
                                                        case = "prep")
            #possessive
            #warning - vocab lists don't have poss_sing at the moment
            elif practice_mode == "4":
                solution = is_utility.gd_common_article(word = vocab_list["poss_sing"][vocab_num],
                                                        sg_pl = "sg",
                                                        gender = vocab_list["gender"][vocab_num],
                                                        case = "poss")
                
            #User input
            print()
            answer = input("The " + vocab_list["english"][vocab_num] + ": ").lower().strip()
            
            #Check answer
            if answer == "stop practice":
                break
            elif answer == solution.lower():
                print()
                is_utility.encourage()
                score = score + 1
            else:
                print()
                print("No, the correct answer is:", solution)

    print()
    print("End of practice!")
    print("Your score is {} out of {}".format(score, q_count))
    print("Time taken: ",dt.datetime.now() -start_time)