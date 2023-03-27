# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 13:27:09 2023

@author: Zoe
"""

import is_question_generator as qgen
import is_run_lesson as rl
from is_utility import user_input
from collections import namedtuple

menu_option = namedtuple('menu_option', ['lesson_name', 'description'])

all_lessons = [menu_option("learn_nouns", "Basic vocabulary flashcards - nouns"),
               menu_option("learn_nouns","Numbers"),
               menu_option("plurals","Plurals"),
               menu_option("time","Time"),
               menu_option("which_season","Which season? [Prepositions]"),
               menu_option("which_month","Which month? [Prepositions]"),
               menu_option("possession_aig","Possession using the prepositional pronoun 'aig'"),
               menu_option("possession_mo","Possession using the possessive articles 'mo', 'do', etc"),
               menu_option("give_get","Giving and getting: prepositional pronouns 'do' and 'bho'"),
               menu_option("gender","Gender of nouns (using adjectives/articles)"),
               menu_option("preferences","Preferences (I would like/prefer etc) using the prepositional pronoun 'le'"),
               menu_option("verb_tenses","Verb tenses"),
               menu_option("professions_annan","Professions: the prepositional pronoun 'ann an'"),
               menu_option("emphasis_adjectives","Emphatic pronouns and adjectives"),
               menu_option("comparisons","Comparisons (sayings)"),
               menu_option("comparatives_superlatives","Adjectives: Comparatives and superlatives"),
               menu_option("where_from","Where are they from? [Prepositions]"),
               menu_option("where_in","Where are they (in)? [Prepositions]")
               ]


async def main():
    while True:
        print("Fàilte gu Ionnsaich Seo!")
        print()
        
        lesson_choice = "0"
        while lesson_choice not in ["x"] + [str(n) for n in range(1,len(all_lessons)+1)]:
            print("Select lesson:")
            for index in range(len(all_lessons)):
                print(str(index+1) + ": " + all_lessons[index].description)
            print("X: Exit")
            print()
            lesson_choice = (await user_input("Lesson number: ")).lower().strip()
        
        if lesson_choice == "x":
            break
        else:
            lesson_name = all_lessons[int(lesson_choice)-1][0]
            await rl.run_lesson(eval("qgen." + lesson_name))