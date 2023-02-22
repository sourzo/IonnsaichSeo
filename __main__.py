# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:49:12 2022

@author: Zoe
"""
import is_question_generator as qgen
import is_run_lesson as rl

while True:
    print("Fàilte gu Ionnsaich Seo!")
    print()
    
    lesson_choice = "0"
    while lesson_choice not in ("x","1","2","3","4","5","6", "7", "8", "9", "10", "11", "12"):
        print("Select lesson:")
        print("1: Basic vocabulary flashcards - nouns")
        print("2: Numbers and plurals")
        print("3: Possession using the prepositional pronoun 'aig'")
        print("4: Possession using the possessive articles 'mo', 'do', etc")
        print("5: Giving and getting: prepositional pronouns 'do' and 'bho'")
        print("6: Gender of nouns (using adjectives/articles)")
        print("7: Preferences (I would like/prefer etc) using the prepositional pronoun 'le'")
        print("8: Verb tenses")
        print("9: Professions: the prepositional pronoun 'ann an'")
        print("10: Emphatic pronouns and adjectives")
        print("11: Where are they from? [Prepositions]")
        print("12: Where are they (in)? [Prepositions]")
        print("X: Exit")
        print()
        lesson_choice = input("Lesson number: ").lower().strip()
    
    if lesson_choice == "x":
        break
    
    if lesson_choice == "1":
        rl.run_lesson(qgen.learn_nouns)
    elif lesson_choice == "2":
        rl.run_lesson(qgen.numbers)
    elif lesson_choice == "3":
        rl.run_lesson(qgen.possession_aig)
    elif lesson_choice == "4":
        rl.run_lesson(qgen.possession_mo)
    elif lesson_choice == "5":
        rl.run_lesson(qgen.give_get)
    elif lesson_choice == "6":
        rl.run_lesson(qgen.gender)
    elif lesson_choice == "7":
        rl.run_lesson(qgen.preferences)
    elif lesson_choice == "8":
        rl.run_lesson(qgen.verb_tenses)
    elif lesson_choice == "9":
        rl.run_lesson(qgen.professions_annan)
    elif lesson_choice == "10":
        rl.run_lesson(qgen.emphasis_adjectives)
    elif lesson_choice == "11":
        rl.run_lesson(qgen.where_from)
    elif lesson_choice == "12":
        rl.run_lesson(qgen.where_in)
