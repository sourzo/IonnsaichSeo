# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 18:52:47 2022

@author: Zoe
"""

def vocab_flashcards(vocab_file):
    """Practice vocabulary with flashcards"""
    #Basic vocab practice
    import is_utility
    import pandas as pd
    import datetime as dt
    
    vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
    if ("english" not in vocab_list.columns or "nom_sing" not in vocab_list.columns):
        print("Error: Check format of vocabulary list, must contain columns 'english' and 'nom_sing' (lower-case)")
        return

    #Select practice mode
    practice_mode="0"
    while practice_mode not in ("X","1","2"):
        print("Select practice mode")
        print("1: English to Gaelic")
        print("2: Gaelic to English")
        print("X: Exit")
        practice_mode = input("Practice mode: ")
    if practice_mode == "X":
        return

    #Pick vocab list sample size
    sample_size = max(1,min(int(input("Select number of words to practice, must be no more than {}: ".format(len(vocab_list)))),len(vocab_list)))
    print("Selecting {} words for practice".format(sample_size))
    vocab_sample = vocab_list.sample(n=sample_size)
    vocab_sample["score"] = 0

    print("Type \'stop practice\' to stop")
    start_time = dt.datetime.now()
    #Practice vocab! Don't forget accents!
    #must get each word correct 3 times in a row
    while len(vocab_sample) > 0:
        vocab_sample = vocab_sample.sample(n=len(vocab_sample))
        for i,r in vocab_sample.iterrows():
            print()
            if practice_mode == "1":
                print(r["english"])
                word = input()
                if word.lower() == "stop practice":
                    break
                elif word.lower() == r["nom_sing"].lower():
                    vocab_sample.loc[i,"score"] = r["score"] + 1
                    is_utility.encourage()
                else :
                    print("Nope, correct answer was: {}".format(r["nom_sing"]))
                    vocab_sample.loc[i,"score"] = 0
            elif practice_mode == "2":
                print(r["nom_sing"])
                word = input()
                if word.lower() == "stop practice":
                    break
                elif word.lower() == r["english"].lower():
                    vocab_sample.loc[i,"score"] = r["score"] + 1
                    is_utility.encourage()
                else :
                    print("Nope, correct answer was: {}".format(r["english"]))
                    vocab_sample.loc[i,"score"] = 0            
            if vocab_sample.loc[i,"score"] == 3:
                print()
                print("You have learned {en} = {gd}".format(en=r["english"], gd=r["nom_sing"]))
                vocab_sample.drop(i, inplace=True)
            if len(vocab_sample) == 0:
                break
        if word.lower() == "stop practice":
            break
        
    print("End of practice")
    print("Time taken: ",dt.datetime.now() -start_time)
