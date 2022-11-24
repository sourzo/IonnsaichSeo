# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 17:55:43 2022

@author: Zoe

To do:
    Numbers and plurals (not started)
    
"""

def numbers(vocab_file):
    """Practice numbers and plurals"""
    import is_utility
    import pandas as pd
    import datetime as dt
    import random as rd

    #Select practice mode
    practice_mode="0"
    while practice_mode not in ("x","1","2","3","4"#,"5"
                                ):
        print("Select practice mode")
        print("1: Numbers only (Digits to Gaelic)")
        print("2: Numbers only (Gaelic to digits)")
        print("3: Plurals only (from Gaelic)")
        print("4: Plurals only (from English)")
        #print("5: Numbers and plurals") - not available yet
        print("X: Exit")
        practice_mode = input("Practice mode: ").lower().strip()
    if practice_mode == "x":
        return

    if practice_mode in ("3","4", "5"):
        #Practicing plurals
        vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
        if ("english" not in vocab_list.columns or "nom_sing" not in vocab_list.columns or "nom_pl" not in vocab_list.columns):
            print("Error: Check format of vocabulary list, must contain columns 'english', 'nom_sing' and 'nom_pl' (lower-case)")
            return
        #Pick vocab list sample size
        sample_size = max(1,min(int(input("Select number of words to practice, must be no more than {}: ".format(len(vocab_list)))),len(vocab_list)))
        print("Selecting {} words for practice".format(sample_size))
        vocab_sample = vocab_list.sample(n=sample_size)
        vocab_sample["score"] = 0

    if practice_mode in ("1","2","4"):
        #Practicing numbers
        numbers = pd.read_csv('Vocabulary/grammar_numbers.csv')
        code_max = 100
        max_num = max(1,min(int(input("Select maximum number to practice, must be less than {}: ".format(code_max))),(code_max-1)))
        print("Practicing numbers 1 to {}".format(max_num))
   

    #numbers only
    if practice_mode in ("1", "2"):
        sample_size_numbers = int(input("Select practice set size: "))
        print("Practicing {} random numbers between 1 and {}".format(sample_size_numbers,max_num))
        score = 0
        q_count = 0
        print("Type \'stop practice\' to stop")
        start_time = dt.datetime.now()
        
        for x in range(sample_size_numbers):
            num = rd.randint(1,max_num)
            #Work out the gaelic for that number
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
            if practice_mode == "1":
                #digits to Gaelic
                print()
                print(num)
                #user input
                answer = input().lower().strip()
                if answer == "stop practice":
                    break
                elif answer == num_gd.lower():
                    is_utility.encourage()
                    score = score + 1
                else:
                    print("No! Correct answer is:", num_gd)
            elif practice_mode == "2":
                #Gaelic to digits
                print()
                print(num_gd)
                answer = input().lower().strip()
                if answer == "stop practice":
                    break
                elif answer == str(num):
                    is_utility.encourage()
                    score = score + 1
                else:
                    print("No! Correct answer is:", num)

            q_count = q_count + 1
        print()
        print("Your score is {} out of {}".format(score,q_count))
                
    #plurals only
    if practice_mode in ("3","4"):
        print("Type \'stop practice\' to stop")
        start_time = dt.datetime.now()
        while len(vocab_sample) > 0:
            vocab_sample = vocab_sample.sample(n=len(vocab_sample)) #shuffle
            for i,r in vocab_sample.iterrows():
                if practice_mode == "3":
                    noun = r["nom_sing"]
                elif practice_mode == "4":
                    noun = r["english"]
                print()
                print("Pluralise: ",noun)
                    
                #user input    
                answer = input().lower().strip()
                
                if answer == "stop practice":
                    break
                elif answer == r["nom_pl"].lower():
                    vocab_sample.loc[i,"score"] = r["score"] + 1
                    is_utility.encourage()
                else :
                    print("Nope, correct answer was: {}".format(r["nom_pl"]))
                    vocab_sample.loc[i,"score"] = 0
                    
                #check scores
                if vocab_sample.loc[i,"score"] == 3:
                    print()
                    print("You have learned the plural of {sing} is {pl}".format(sing=noun, pl=r["nom_pl"]))
                    vocab_sample.drop(i, inplace=True)
                if len(vocab_sample) == 0:
                    break

    #numbers and plurals together
    if practice_mode == "5":
        print("This bit not available at the moment")


    print("End of practice")
    print("Time taken: ",dt.datetime.now() -start_time)

