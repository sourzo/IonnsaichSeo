# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:27:09 2023

@author: Zoe
"""

import is_question_generator as qgen
import is_run_lesson as rl
from is_utility import user_input

async def main():
    while True:
        print("Fàilte gu Ionnsaich Seo!")
        print()
        
        lesson_choice = "0"
        while lesson_choice not in ["x"] + [str(n) for n in range(1,17)]:
            print("Select lesson:")
            print("1: Basic vocabulary flashcards - nouns")
            print("2: Numbers")
            print("3: Plurals")
            print("4: Time")
            print("5: Possession using the prepositional pronoun 'aig'")
            print("6: Possession using the possessive articles 'mo', 'do', etc")
            print("7: Giving and getting: prepositional pronouns 'do' and 'bho'")
            print("8: Gender of nouns (using adjectives/articles)")
            print("9: Preferences (I would like/prefer etc) using the prepositional pronoun 'le'")
            print("10: Verb tenses")
            print("11: Professions: the prepositional pronoun 'ann an'")
            print("12: Emphatic pronouns and adjectives")
            print("13: Comparisons (sayings)")
            print("14: Adjectives: Comparatives and superlatives")
            print("15: Where are they from? [Prepositions]")
            print("16: Where are they (in)? [Prepositions]")
            print("X: Exit")
            print()
            lesson_choice = (await user_input("Lesson number: ")).lower().strip()
        
        if lesson_choice == "x":
            break
        
        if lesson_choice == "1":
            await rl.run_lesson(qgen.learn_nouns)
        elif lesson_choice == "2":
            await rl.run_lesson(qgen.numbers)
        elif lesson_choice == "3":
            await rl.run_lesson(qgen.plurals)
        elif lesson_choice == "4":
            await rl.run_lesson(qgen.time)
        elif lesson_choice == "5":
            await rl.run_lesson(qgen.possession_aig)
        elif lesson_choice == "6":
            await rl.run_lesson(qgen.possession_mo)
        elif lesson_choice == "7":
            await rl.run_lesson(qgen.give_get)
        elif lesson_choice == "8":
            await rl.run_lesson(qgen.gender)
        elif lesson_choice == "9":
            await rl.run_lesson(qgen.preferences)
        elif lesson_choice == "10":
            await rl.run_lesson(qgen.verb_tenses)
        elif lesson_choice == "11":
            await rl.run_lesson(qgen.professions_annan)
        elif lesson_choice == "12":
            await rl.run_lesson(qgen.emphasis_adjectives)
        elif lesson_choice == "13":
            await rl.run_lesson(qgen.comparisons)
        elif lesson_choice == "14":
            await rl.run_lesson(qgen.comparatives_superlatives)
        elif lesson_choice == "15":
            await rl.run_lesson(qgen.where_from)
        elif lesson_choice == "16":
            await rl.run_lesson(qgen.where_in)