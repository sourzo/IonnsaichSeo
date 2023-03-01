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
    ##Adjectives: Comparatives or superlatives
    if lesson.__name__ == "comparatives_superlatives":
        c_s = "0"
        while c_s not in ("x","1","2","3"):
            print("Select practice option")
            print("1: Comparatives ('better', 'faster', etc)")
            print("2: Superlatives ('best', 'fastest', etc)")
            print("3: Both")
            print("X: Exit")
            c_s = input("Practice option: ").lower().strip()
        if c_s == "x":
            return
        elif c_s == "1":
            options["comp_sup"] = "comp"
        elif c_s == "2":
            options["comp_sup"] = "sup"
        elif c_s == "3":
            options["comp_sup"] = "both"
    
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
            user_max=""
            while user_max.isdigit()==False:
                user_max = input("Select maximum number to practice, must be less than {}: ".format(code_max))
            options["max_num"] = max(1,min(int(user_max),(code_max-1)))
            print()
            print("Practicing numbers 1 to {}".format(options["max_num"]))
            
        elif options["num_mode"] in ("3", "4", "5"):
            options["max_num"] = 1
        
    ##Modules involving verbs: select tense
    if lesson.__name__ in ("give_get", "verb_tenses"):
        ct = "0"
        while ct not in ("x","1","2","3","4"):
            print()
            print("Select tense")
            print("1: Present tense")
            print("2: Past tense")
            print("3: Future tense")
            print("4: All tenses")
            print("X: Exit")
            ct = input("Tense: ").lower().strip()
        if ct == "1":
            options["chosen_tense"] = "present"
        elif ct == "2":
            options["chosen_tense"] = "past"
        elif ct == "3":
            options["chosen_tense"] = "future"
        elif ct == "4":
            options["chosen_tense"] = "any"
        elif ct == "x":
            return

    ##Verbs option 2 - Verb form (question/statement, positive/negative)
    if lesson.__name__ in ("verb_tenses"):
        options["verb_form"] = "0"
        while options["verb_form"] not in ("1", "2", "3"):
            print()
            print("Practice which verb forms?")
            print("1: Positive statements only")
            print("2: Positive and negative statements")
            print("3: Positive and negative statements and questions")
            options["verb_form"] = input("Verb forms: ").lower().strip()
    
    ##Translation direction
    if lesson.__name__ in ("give_get", "possession_aig", "learn_nouns", "preferences", "professions_annan", "emphasis_adjectives", "possession_mo", "comparisons", "comparatives_superlatives"):
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
    other_lessons = ("give_get", "preferences", "possession_aig", "professions_annan", "possession_mo", "comparatives_superlatives")
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
    vocab_list = is_utility.select_vocab(lesson, options)
    if type(vocab_list) == str:
        return
    elif len(vocab_list) == 1:
        options["vocab_sample"] = vocab_list
    elif len(vocab_list) > 1:
        user_size = ""
        while user_size.isdigit()==False:
            print()
            print("How many words do you want to use from the list?")
            user_size = input("(Max " + str(len(vocab_list)) + "): ")
        user_size = max(1,min(int(user_size),len(vocab_list)))
        if user_size == 1:
            print()
            print("Which word do you want to practice?")
            print(vocab_list["english"])
            row_num = ""
            while row_num.isdigit()==False or int(row_num) > len(vocab_list["english"]):
                    row_num = input("Number: ")
            options["vocab_sample"] = vocab_list.iloc[[int(row_num)]].reset_index(drop=True)
        else:
            options["vocab_sample"] = vocab_list.sample(user_size).reset_index(drop=True)
    
    # Practice ----------------------------------------------------------------
    print()
    print("Type 'X' to finish")
    answer = ""
    q_count = 0
    score = 0
    start_time = dt.datetime.now()
    
    while answer != "x":
        q_count = q_count + 1
        question, solutions, prompt = lesson(**options)
        
        #fix apostrophe issues
        question = question.replace("’","'")
        prompt = prompt.replace("’","'")
        solutions = [x.replace("’","'") for x in solutions]
        solutions_comparison = [x.lower().strip().replace("?","").replace(".","").replace("!","") for x in solutions]
            
        #Display sentence to translate
        print()
        print(question)
        answer = input(prompt).lower().strip().replace("?","").replace(".","").replace("!","")
            
        #Check answer
        if answer == "x":
            break
        elif answer in solutions_comparison:
                print()
                is_utility.encourage()
                score = score + 1
        else:
            print()
            print("Nope, correct answer is: ", solutions[0])
                
    print()
    print("End of practice!")
    print("Your score is {} out of {}".format(score, q_count-1))
    print("Time taken: ", dt.datetime.now() -start_time)
    print()
    print()
