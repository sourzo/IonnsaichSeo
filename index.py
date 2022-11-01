# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 14:49:12 2022

@author: Zoe
"""
import sys
print("Welcome to Ionnsaich Seo!")
print()

lesson = "0"
while lesson not in ("X","1","2","3","4"):
    print("Select lesson:")
    print("1: Basic vovabulary flashcards")
    print("2: Numbers and plurals")
    print("3: Posession using the prepositional pronoun 'aig'")
    print("4: Giving and getting: prepositional pronouns 'bho' and 'do'")
    print("X: Exit")
    print()
    lesson = input("Lesson number: ")

if lesson == "X":
    sys.exit("Ok bye")
print()
print("Name the vocabulary list to use in practice")
print("For example: animals_pets")
vocab_file = input()
print()

if lesson == "1":
    import is_vocabulary_flashcards
    vocab_flashcards(vocab_file)
elif lesson == "2":
    import is_numbers
    numbers(vocab_file)
elif lesson == "3":
    import is_grammar_aig
    possession(vocab_file)
elif lesson == "4":
    import is_give_and_get
    give_get(vocab_file)