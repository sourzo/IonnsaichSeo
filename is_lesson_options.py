# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 14:24:28 2023

@author: Zoe
"""
import is_utility
from collections import namedtuple
import pandas as pd

#Part 1: General options menus (ie not including vocabulary)-------------------
menu_option = namedtuple('menu_option', ['key', 'description'])

async def options_menu(options, options_name, message="Select practice option"):
    options_list = eval(options_name)
    user_response = "0"
    while user_response not in ["x"] + [str(n) for n in range(1,len(options_list)+1)]:
        print()
        print(message)
        for index in range(len(options_list)):
            print(str(index+1) + ": " + options_list[index].description)
        print("X: Exit")
        user_response = (await is_utility.user_input("Practice option: ")).lower().strip()
    if user_response != "x":
        options[options_name] = options_list[int(user_response)-1].key
    else:
        options[options_name] = "x"
       
gender_mode = [menu_option("adj", "Adjectives"),
               menu_option("def_nom", "Definite articles (nom.)")#,
               #menu_option("def_prep", "Definite articles (prep.)"),
               #menu_option("def_poss", "Definite articles (poss.)"),
               #menu_option("def_all", "Definite articles (All.)"),
               ]

comp_sup = [menu_option("comp", "Comparatives ('better', 'faster', etc)"),
            menu_option("sup", "Superlatives ('best', 'fastest', etc)"),
            menu_option("both", "Both")]

chosen_tense = [menu_option("present", "Present tense"),
                menu_option("past", "Past tense"),
                menu_option("future", "Future tense"),
                menu_option("any", "All tenses")]

verb_form = [menu_option("p_s", "Positive statements only"),
             menu_option("pn_s", "Positive and negative statements"),
             menu_option("pn_sq", "Positive and negative statements and questions")]

translate_words = [menu_option("en_gd", "English to Gaelic"),
                   menu_option("gd_en", "Gaelic to English")]

translate_numbers = [menu_option("dig_gd", "Digits to Gaelic"),
                     menu_option("gd_dig", "Gaelic to digits")]

translate_generic = [menu_option("from_en", "English prompts"),
                     menu_option("from_gd", "Gaelic prompts")]

sentence = [menu_option("full", "Full sentence"),
            menu_option("blank", "Fill in the blank")]

sentence_qa = [menu_option("full", "Full sentence"),
               menu_option("blank", "Fill in the blank"),
               menu_option("q_and_a", "Question and answer")]

#Part 2: Vocabulary selection functions----------------------------------------
required_columns = {"give_get" : ("english", "nom_sing"),
                    "possession_aig" : ("english", "nom_sing"),
                    "gender" : ("english", "nom_sing", "gender"),
                    "numbers" : (),
                    "plurals" : ("english", "nom_sing", "nom_pl"),
                    "learn_nouns" : ("english", "nom_sing"),
                    "preferences" : ("english", "nom_sing"),
                    "verb_tenses" : ("english", "en_past", "en_vn", "root", "verbal_noun"),
                    "professions_annan" : (),
                    "emphasis_adjectives" : ("english", "adj_gd"),
                    "possession_mo" : ("english", "nom_sing", "nom_pl"),
                    "where_from" : ("english", "nom_sing", "gender"),
                    "where_in" : ("english", "nom_sing", "gender"),
                    "comparisons" : (),
                    "comparatives_superlatives": ("english", "nom_sing", "gender"),
                    "time" : ()}

async def select_vocab(lesson, options):
    """Select vocabulary file to use in lesson"""
    #Cases where vocab file needed for lesson
    if len(required_columns[lesson.__name__]) == 0:
        return pd.DataFrame()
    elif lesson.__name__ == "numbers" and options["num_mode"] in ("1","2"):
            return pd.DataFrame({"a" : [1]})# dummy dataframe
    #Cases where vocab file must be from selected list
    elif lesson.__name__ == "possession_mo":
        vocab_num = ""
        while vocab_num not in ("x","1","2","3"):
            print()
            print("Select topic")
            print("1: Body parts")
            print("2: Clothes")
            print("3: Family")
            print("X: Exit")
            vocab_num = (await is_utility.user_input("Practice mode: ")).lower().strip()
        if vocab_num == "x":
            return "x"
        elif vocab_num == "1":
            return pd.read_csv('Vocabulary/people_body.csv')
        elif vocab_num == "2":
            return pd.read_csv('Vocabulary/people_clothes.csv')
        elif vocab_num == "3":
            return pd.read_csv('Vocabulary/people_family.csv')
    elif lesson.__name__ == "where_from":
        vocab_num = ""
        while vocab_num not in ("x","1","2"):
            print()
            print("Select geography")
            print("1: Countries")
            print("2: Places in Scotland")
            print("X: Exit")
            vocab_num = (await is_utility.user_input("Practice mode: ")).lower().strip()
        if vocab_num == "x":
            return "x"
        elif vocab_num == "1":
            places = pd.read_csv('Vocabulary/places_world.csv')
            places.rename(columns = {"place_en" : "english", "place_gd" : "nom_sing"}, inplace=True)
            return places
        elif vocab_num == "2":
            places = pd.read_csv('Vocabulary/places_scotland.csv')
            places.rename(columns = {"place_en" : "english", "place_gd" : "nom_sing"}, inplace=True)
            return places
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
            vocab_num = (await is_utility.user_input("Practice mode: ")).lower().strip()
        if vocab_num == "x":
            return "x"
        elif vocab_num == "1":
            options["contains_articles"] = True
            places = pd.read_csv('Vocabulary/places_world.csv')
            places.rename(columns = {"place_en" : "english", "place_gd" : "nom_sing"}, inplace=True)
            return places
        elif vocab_num == "2":
            options["contains_articles"] = True
            places = pd.read_csv('Vocabulary/places_scotland.csv')
            places.rename(columns = {"place_en" : "english", "place_gd" : "nom_sing"}, inplace=True)
            return places
        elif vocab_num == "3":
            options["contains_articles"] = False
            return pd.read_csv('Vocabulary/places_town.csv')
        elif vocab_num == "4":
            options["contains_articles"] = False
            return pd.read_csv('Vocabulary/places_home.csv')
    #Case where any compatible vocab file can be used
    else:
        from os.path import exists
        from os import listdir
        #Get list of suitable vocab files, out of list of all files
        allfiles = listdir("Vocabulary/")
        vocab_suggestions = []
        for filename in allfiles:
            checkfile = pd.read_csv("Vocabulary/"+filename)
            if check_vocab(lesson.__name__, checkfile, messages=False) == True:
                vocab_suggestions.append(filename[:-4])
        #Ask for user input
        vocab_file = ""
        print()
        print("Name the vocabulary list to use in practice")
        print("or type 'help' to list all possible vocabulary lists")
        print("or X to exit")
        while vocab_file not in vocab_suggestions + ["x"] + [str(n) for n in range(1,len(vocab_suggestions)+1)]:
            print()
            vocab_file = (await is_utility.user_input("Vocabulary list: ")).lower().strip()
            #user escape
            if vocab_file == "x":
                return "x"
            #user wants list of files
            elif vocab_file == "help":
                for index, file in enumerate(vocab_suggestions):
                    print(str(index+1) + ": " + vocab_suggestions[index])
            elif vocab_file.isnumeric() and int(vocab_file) in range(1,len(vocab_suggestions)+1):
                vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_suggestions[int(vocab_file)]))
            elif exists("Vocabulary/{}.csv".format(vocab_file))==False:
                print()
                print("File not found: Check vocabulary list is a CSV file in the Vocabulary folder")
            elif vocab_file not in vocab_suggestions:
                print()
                check_vocab(lesson.__name__, checkfile, messages=True)
            else:
                vocab_list = pd.read_csv('Vocabulary/{}.csv'.format(vocab_file))
        return vocab_list

def check_vocab(lesson_name, vocab_sample, messages = True):
    """Check that the chosen vocab file has the right columns for the lesson"""

    list_ok = True
    if len(required_columns[lesson_name]) > 0:
        for column in required_columns[lesson_name]:
            if column not in vocab_sample.columns:
                list_ok = False
                if messages == True:
                    print()
                    print("Error: Chosen vocabulary list must contain column {} (lower-case)".format(column))
    if list_ok == False and messages == True:
        print("Try another vocabulary list or add the required columns and try again")
    return list_ok

async def vocab_sample_select(vocab_list, options):
    user_size = ""
    while user_size.isdigit()==False:
        print()
        print("How many words do you want to use from the list?")
        user_size = await is_utility.user_input("(Max " + str(len(vocab_list)) + "): ")
    user_size = max(1,min(int(user_size),len(vocab_list)))
    if user_size == 1:
        print()
        print("Which word do you want to practice?")
        print(vocab_list["english"])
        row_num = ""
        while row_num.isdigit()==False or int(row_num) > len(vocab_list["english"]):
                row_num = await is_utility.user_input("Number: ")
        options["vocab_sample"] = vocab_list.iloc[[int(row_num)]].reset_index(drop=True)
    else:
        options["vocab_sample"] = vocab_list.sample(user_size).reset_index(drop=True)