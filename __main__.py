# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:49:12 2022

@author: Zoe
"""
import is_question_generator as qgen
import is_run_lesson as rl

while True:
    print("Welcome to Ionnsaich Seo!")
    print()
    
    lesson_choice = "0"
    while lesson_choice not in ("x","1","2","3","4","5","6", "7", "8"):
        print("Select lesson:")
        print("1: Basic vocabulary flashcards")
        print("2: Numbers and plurals")
        print("3: Possession using the prepositional pronoun 'aig'")
        print("4: Giving and getting: prepositional pronouns 'bho' and 'do'")
        print("5: Gender of nouns (using adjectives/articles)")
        print("6: Preferences (I would like/prefer etc) using the prepositional pronoun 'le'")
        print("7: Regular verb tenses")
        print("8: Professions: the prepositional pronoun 'ann an'")
        print("X: Exit")
        print()
        lesson_choice = input("Lesson number: ").lower().strip()
    
    if lesson_choice == "x":
        break
    
    if lesson_choice == "1":
        rl.run_lesson(qgen.vocab)
    elif lesson_choice == "2":
        rl.run_lesson(qgen.numbers)
    elif lesson_choice == "3":
        rl.run_lesson(qgen.possession_aig)
    elif lesson_choice == "4":
        rl.run_lesson(qgen.give_get)
    elif lesson_choice == "5":
        rl.run_lesson(qgen.gender)
    elif lesson_choice == "6":
        rl.run_lesson(qgen.preferences)
    elif lesson_choice == "7":
        rl.run_lesson(qgen.verbs_reg)
    elif lesson_choice == "8":
        rl.run_lesson(qgen.professions_annan)
