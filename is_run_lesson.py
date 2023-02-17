# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:48:05 2022

@author: Zoe
"""

def run_lesson(lesson):
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
    if lesson.__name__ in ("give_get", "verbs_reg"):
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

    ##Verbs option 2 - verbal noun (past and present)
    if lesson.__name__ in ("verbs_reg"):
        if options["tense"] in ("2","3"):
            options["verbal_noun"] = "0"
            while options["verbal_noun"] not in ("y","n"):
                print()
                print("Practice verbal nouns ('-ing' words)?")
                print("Y: Yes")
                print("N: No")
                options["verbal_noun"] = input("Verbal nouns: ").lower().strip()
        elif options["tense"] == "1":
            options["verbal_noun"] = "y"
            
    ##Verbs option 3 - Verb form (question/statement, positive/negative)
    if lesson.__name__ in ("verbs_reg"):
        options["verb_form"] = "0"
        while options["verb_form"] not in ("1", "2", "3"):
            print()
            print("Practice which verb forms?")
            print("1: Positive statements only")
            print("2: Positive and negative statements")
            print("3: Positive and negative statements and questions")
            options["verb_form"] = input("Verb forms: ").lower().strip()
    
    ##Translation direction
    if lesson.__name__ in ("give_get", "possession_aig", "vocab", "preferences", "professions_annan", "emphasis_adjectives", "possession_mo"):
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
    QandA_lessons = ("where_from", "where_in")
    other_lessons = ("give_get", "preferences", "possession_aig", "professions_annan", "possession_mo")
    if lesson.__name__ in QandA_lessons + other_lessons:
        if lesson.__name__ in QandA_lessons:
            sentence_tuple = ("x","1","2","3")
        else:
            sentence_tuple = ("x","1","2","3")    
        options["sentence"] = "0"
        while options["sentence"] not in sentence_tuple:
            print()
            print("Select practice mode")
            print("1: Full sentence")
            print("2: Fill in the blank")
            if lesson.__name__ in QandA_lessons:
                print("3: Question and answer")
            print("X: Exit")
            options["sentence"] = input("Practice mode: ").lower().strip()
        if options["sentence"] == "x":
            return
        
    #Select vocab file
    if lesson.__name__ not in ("verbs_reg", "professions_annan", "emphasis_adjectives"):
        if lesson.__name__ == "numbers" and options["num_mode"] in ("1","2"):
            options["vocab_file"] = "xxx" #no vocab file needed
        elif lesson.__name__ == "possession_mo":
            vocab_num = ""
            while vocab_num not in ("x","1","2","3"):
                print()
                print("Select topic")
                print("1: Body parts")
                print("2: Clothes")
                print("3: Family")
                print("X: Exit")
                vocab_num = input("Practice mode: ").lower().strip()
            if vocab_num == "x":
                return        
            elif vocab_num == "1":
                options["vocab_file"] = "people_body"        
            elif vocab_num == "2":
                options["vocab_file"] = "people_clothes"        
            elif vocab_num == "3":
                options["vocab_file"] = "people_family"        
        elif lesson.__name__ == "where_from":
            vocab_num = ""
            while vocab_num not in ("x","1","2"):
                print()
                print("Select geography")
                print("1: Countries")
                print("2: Places in Scotland")
                print("X: Exit")
                vocab_num = input("Practice mode: ").lower().strip()
            if vocab_num == "x":
                return        
            elif vocab_num == "1":
                options["vocab_file"] = "places_world"        
            elif vocab_num == "2":
                options["vocab_file"] = "places_scotland"        
        elif lesson.__name__ == "where_in":
            vocab_num = ""
            while vocab_num not in ("x","1","2","3","4"):
                print()
                print("Select places")
                print("1: Countries")
                print("2: Places in Scotland")
                print("3: Around town")
                print("4: In the house")
                print("X: Exit")
                vocab_num = input("Practice mode: ").lower().strip()
            if vocab_num == "x":
                return        
            elif vocab_num == "1":
                options["vocab_file"] = "places_world"        
            elif vocab_num == "2":
                options["vocab_file"] = "places_scotland"        
            elif vocab_num == "3":
                options["vocab_file"] = "places_town"        
            elif vocab_num == "4":
                options["vocab_file"] = "places_home"        
        else:
            from os.path import exists
            options["vocab_file"] = "xxx"
            while exists("Vocabulary/{}.csv".format(options["vocab_file"])) == False :
                print()
                print("Name the vocabulary list to use in practice")
                print("For example: 'animals_pets'")
                options["vocab_file"] = input()
                if exists("Vocabulary/{}.csv".format(options["vocab_file"]))==False:
                    print()
                    print("File not found: Check vocabulary list is a CSV file in the Vocabulary folder")
            
    # Practice ----------------------------------------------------------------
    print()
    print("Type 'X' to finish")
    answer = ""
    q_count = 0
    score = 0
    start_time = dt.datetime.now()
    
    while answer != "x":
        q_count = q_count + 1
        question, solution1, solution2, prompt = lesson(**options)
        
        #fix apostrophe issues
        question = question.replace("’","'")
        solution1 = solution1.replace("’","'")
        solution2 = solution2.replace("’","'")
        prompt = prompt.replace("’","'")
            
        #Display sentence to translate
        print()
        print(question)
        answer = input(prompt).lower().strip()
            
        #Check answer
        if answer == "x":
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
    print()
    print()
