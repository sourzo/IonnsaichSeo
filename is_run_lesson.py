# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 16:48:05 2022

@author: Zoe
"""

async def run_lesson(lesson):
    """Generic code to run any module"""
    import is_utility
    from inspect import signature
    import datetime as dt
    import is_lesson_options as lo
    import re
    
    # User options ------------------------------------------------------------
    
    options = dict()
    
    lesson_parameters = signature(lesson).parameters
    for param in lo.parameter_prompts:
        if param in lesson_parameters:
            await lo.options_menu(options, param, lo.parameter_prompts[param])
            if options[param] == "x":
                return
    
    ##Numbers module - special options
    if "max_num" in lesson_parameters:
        code_max = 100
        user_max=""
        while user_max.isdigit()==False:
            user_max = await is_utility.user_input("Select maximum number to practice, must be less than {}: ".format(code_max))
        options["max_num"] = max(1,min(int(user_max),(code_max-1)))
        print()
        print("Practicing numbers 1 to {}".format(options["max_num"]))
    
    #Select vocab file
    vocab_list = await lo.select_vocab(lesson, options)
    if vocab_list == None:
        pass
    elif vocab_list == "x":
        return
    elif len(vocab_list) == 1:
        options["vocab_sample"] = vocab_list
    elif len(vocab_list) > 1:
        await lo.vocab_sample_select(vocab_list, options)
    
    # Practice ----------------------------------------------------------------
    print()
    print("Type 'X' to finish")
    answer = ""
    q_count = 0
    score = 0
    start_time = dt.datetime.now()
    
    while answer != "x":
        q_count = q_count + 1
        question, prompt, solutions = lesson(**options)
        
        #fix apostrophe issues
        question = question.replace("’","'")
        prompt = prompt.replace("’","'")
        solutions = [x.replace("’","'") for x in solutions]
        #Remove some punctuation from solutions list (and later from user response)
        solutions_comparison = [re.sub("\?|\*|:|!|\.", "", x.lower().strip())
                                for x in solutions]
        #Add extra solutions where user did not include (sg) or (pl)
        extra_solutions = []
        for s in solutions_comparison:
            if any((" (sg)" in s,
                    " (pl)" in s)):
                extra_solutions.append(re.sub(" \(sg\)| \(pl\)", "", s.lower()))
        solutions_comparison += extra_solutions
        
        #Add extra solutions by expanding "aren't" to "are not", "didn't" to "did not" etc
        extra_solutions = []
        for s in solutions_comparison:
            if "n't" in s:
                s_alt = s.replace("n't", " not")
                s_alt = s_alt.replace("wo not", "won't")
                extra_solutions.append(s_alt)
        solutions_comparison += extra_solutions
            
        #Display sentence to translate
        print()
        print(question)
        answer = (await is_utility.user_input(prompt))
        answer = re.sub("\?|\*|:|!|\.", "", answer.lower().strip())
            
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
