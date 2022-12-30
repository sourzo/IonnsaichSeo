# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:48:05 2022

@author: Zoe
"""

def run_lesson(lesson, vocab_file):
    """Generic code to run any module"""
    import is_utility
    import datetime as dt
    
    
    # User options ------------------------------------------------------------
    
    options = dict()
    
    ##Gender module - special options
    if lesson.__name__ == "gender":
        options["gender_mode"] = "0"
        while options["gender_mode"] not in ("x","1","2",#"3","4","5"
                                    ):
            print("Select practice option")
            print("1: Adjectives")
            print("2: Definite articles (nom.)")
            #print("3: Definite articles (prep.)")
            #print("4: Definite articles (poss.)")
            #print("5: Definite articles (All)")
            print("X: Exit")
            options["gender_mode"] = input("Practice option: ").lower().strip()
        if options["gender_mode"] == "x":
            return
    
    ##Numbers module - special options
    elif lesson.__name__ == "numbers":
        options["num_mode"] = "0"
        while options["num_mode"] not in ("x","1","2","3","4"#,"5"
                                    ):
            print()
            print("Select practice mode")
            print("1: Numbers only (Digits to Gaelic)")
            print("2: Numbers only (Gaelic to digits)")
            print("3: Plurals only (from Gaelic)")
            print("4: Plurals only (from English)")
            #print("5: Numbers and plurals") - not available yet
            print("X: Exit")
            options["num_mode"] = input("Practice mode: ").lower().strip()
            
        if options["num_mode"] == "x":
            return
        
        elif options["num_mode"] in ("1", "2"):
            code_max = 100
            options["max_num"] = max(1,min(int(input("Select maximum number to practice, must be less than {}: ".format(code_max))),(code_max-1)))
            print()
            print("Practicing numbers 1 to {}".format(options["max_num"]))
            
        elif options["num_mode"] in ("3", "4", "5"):
            options["max_num"] = 1
        
    ##Modules involving verbs: select tense
    if lesson.__name__ in ("give_get"):
        options["tense"] = "0"
        while options["tense"] not in ("x","1","2","3"#,"4"
                            ):
            print()
            print("Select tense")
            print("1: Present tense")
            print("2: Past tense")
            print("3: Future tense")
            #print("4: All tenses")
            print("X: Exit")
            options["tense"] = input("Tense: ").lower().strip()
        if options["tense"] == "x":
            return
    
    ##Translation direction
    if lesson.__name__ in ("give_get", "possession_aig", "vocab"):
        options["translate"] = "0"
        while options["translate"] not in ("x","1","2"):
            print()
            print("Select translation direction")
            print("1: English to Gaelic")
            print("2: Gaelic to English")
            print("X: Exit")
            options["translate"] = input("Translation direction: ").lower().strip()
        if options["translate"] == "x":
            return
    
    ##Full sentence or fill in the blank
    if lesson.__name__ in ("give_get", 
                       "possession_aig"):
        options["sentence"] = "0"
        while options["sentence"] not in ("x","1","2"):
            print()
            print("Select practice mode")
            print("1: Full sentence")
            print("2: Fill in the blank")
            print("X: Exit")
            options["sentence"] = input("Practice mode: ").lower().strip()
        if options["sentence"] == "x":
            return
            
    # Practice ----------------------------------------------------------------
    print()
    print("Type 'stop practice' to finish")
    answer = ""
    q_count = 0
    score = 0
    start_time = dt.datetime.now()
    
    while answer != "stop practice":
        q_count = q_count + 1
        question, solution1, solution2, prompt = lesson(vocab_file, **options)
            
        #Display sentence to translate
        print()
        print(question)
        answer = input(prompt).lower().strip()
            
        #Check answer
        if answer == "stop practice":
            break
        elif answer in (solution1.lower().strip(), solution2.lower().strip()):
                print()
                is_utility.encourage()
                score = score + 1
        else:
            print()
            print("Nope, correct answer is: ", solution1)
                
    print()
    print("End of practice!")
    print("Your score is {} out of {}".format(score, q_count))
    print("Time taken: ", dt.datetime.now() -start_time)
