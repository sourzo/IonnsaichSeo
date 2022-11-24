# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:49:12 2022

@author: Zoe
"""
while True:
    print("Welcome to Ionnsaich Seo!")
    print()
    
    lesson = "0"
    while lesson not in ("x","1","2","3","4"):
        print("Select lesson:")
        print("1: Basic vocabulary flashcards")
        print("2: Numbers and plurals")
        print("3: Possession using the prepositional pronoun 'aig'")
        print("4: Giving and getting: prepositional pronouns 'bho' and 'do'")
        print("5: Gender of nouns (using adjectives/articles)")
        print("X: Exit")
        print()
        lesson = input("Lesson number: ").lower().strip()
    
    if lesson == "x":
        break
        
    #Select vocab file
    from os.path import exists
    vocab_file = ""
    while exists("Vocabulary/{}.csv".format(vocab_file)) == False :
        print()
        print("Name the vocabulary list to use in practice")
        print("For example: 'animals_pets'")
        vocab_file = input()
        if exists("Vocabulary/{}.csv".format(vocab_file))==False:
            print()
            print("File not found: Check vocabulary list is a CSV file in the Vocabulary folder")
     
    print()
    
    if lesson == "1":
        import is_vocabulary_flashcards
        is_vocabulary_flashcards.vocab_flashcards(vocab_file)
    elif lesson == "2":
        import is_numbers
        is_numbers.numbers(vocab_file)
    elif lesson == "3":
        import is_grammar_aig
        is_grammar_aig.possession(vocab_file)
    elif lesson == "4":
        import is_give_and_get
        is_give_and_get.give_get(vocab_file)
    elif lesson == "5":
        import is_gender
        is_gender.gender(vocab_file)