# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:10:24 2023

@author: Zoe
"""
import is_question_generator as qgen
import is_lesson_options as lo
import itertools
import random as rd
from inspect import signature

#This top section of functions are just called inside the actual test function.
#The tester doesn't need to use these functions.
#But you do want to update the all_randomiser_params dictionary 
#when you create a new lesson.

def get_randomiser_params(lesson, vocab):
    """Returns a dictionary of the randomiser parameters with their range of values.
    Update the dictionary in here when a new lesson is created."""
    if vocab == None:
        range_vocab = 0
    else:
        range_vocab = range(len(vocab))
    range_pronouns = range(7)
    range_pronouns_names = range(8)
    range_boolean = [True, False]
    all_randomiser_params =  {"give_get" : {"subject_num" : range_pronouns_names,
                                            "object_num" : range_pronouns_names,
                                            "gift_num" : range_vocab,
                                            "give_get_num" : range(2)},
                              
                              "possession_aig" : {"subject_num" : range_pronouns,
                                                  "object_num" : range_vocab},
                              
                              "gender" : {"vocab_num" : range_vocab},
                              
                              "numbers" : {"num" : range(100)},
                              
                              "plurals" : {"vocab_num" : range_vocab},
                              
                              "learn_nouns" : {"vocab_num" : range_vocab},
                              
                              "preferences" : {"subject_num" : range_pronouns,
                                               "object_num" : range_vocab,
                                               "tense" : range(2),
                                               "pos_neg" : range(2),
                                               "likepref" : range(2)},
                              
                              "verb_tenses" : {"verb_num" : range_vocab,
                                               "pers_num" : range_pronouns},
                              
                              "professions_annan" : {"person_num" : range_pronouns,
                                                     "profession_num" : range(len(qgen.professions))},
                              
                              "emphasis_adjectives" : {"person_num" : range_pronouns,
                                                       "modifier_choice" : range(len(qgen.adj_modifiers)),
                                                       "adj_num" : range_vocab},
                              
                              "possession_mo" : {"whose_num" : range_pronouns,
                                                     "where_num" : range(3),
                                                     "what_num" : range_vocab},
                              
                              "where_from" : {"person_num" : range_pronouns,
                                              "where_num" : range_vocab},
                              
                              "where_in" : {"person_num" : range_pronouns,
                                            "where_num" : range_vocab,
                                            "article_switch" : range(2)},
                              
                              "comparisons" : {"comparison_choice" : range(len(qgen.similes))},
                              
                              "comparatives_superlatives" : {"subject_num" : range_vocab,
                                                             "object_num" : range_vocab,
                                                             "adj_num" : range(len(qgen.adjectives))},
                              
                              "time" : {"hrs_num" : range(0, 24),
                                        "mins_num" : range(0, 60, 5)},
                              
                              "which_season" : {"month_num" : range(12),
                                                "use_prep" : range_boolean},
                              "which_month" : {"holiday_num" : range(len(qgen.list_holidays)),
                                               "month_num" : range(12),
                                               "use_prep" : range_boolean,
                                               "pers_num" : range_pronouns}
                              }
    return all_randomiser_params[lesson.__name__]


def get_user_params(lesson, vocab):
    """Returns a dictionary of user parameters and their possible values"""
    all_lesson_params = [x for x in signature(lesson).parameters]
    user_params = dict()
    for each in all_lesson_params:
        if each in lo.user_menu_options:
            user_params[each] = [option[0] for option in lo.user_menu_options[each]]
    if "max_num" in all_lesson_params:
        user_params["max_num"] = [100]
    return user_params


def generate_params(lesson, param_type, vocab):
    """Creates a generator object of each possible combination of values 
    for the user/randomiser parameters"""
    if param_type == "randomiser":
        params = get_randomiser_params(lesson, vocab)
    else:
        params = get_user_params(lesson, vocab)
    param_names = params.keys()
    ranges = [r for r in params.values()]
    for values in itertools.product(*ranges):
        yield dict(zip(param_names, values))


def list_params(lesson, param_type, vocab):
    """Creates a list of all possible combinations of values
    for the user/randomiser parameters"""
    return [combination for combination in generate_params(lesson, 
                                                           param_type, 
                                                           vocab)]

#-------------- Below is the function you use for testing

def test(lesson, fulltest = False):
    """Generates question, prompt, solution-list
    fulltest == True: all possible combinations of parameters
    fulltest == False: a random combination of parameters, as many times as specified
    'lesson' must be the function, e.g. qgen.give_get;
    vocab_sample must be a vocabulary file (imported with csvr)"""
    
    if "vocab_sample" in signature(lesson).parameters:
        vocab_sample_str = input("Name the vocab list (must be a csvr dict): ")
        vocab = eval(vocab_sample_str)
        if lo.check_vocab(lesson.__name__, vocab) == False:
            return
    else:
        vocab = None
    
    user_params = list_params(lesson, "user", vocab)
    if fulltest == True:
        for user_combination in user_params:
            for randomiser_combination in list_params(lesson, "randomiser", vocab):
                if vocab == None:
                    print(lesson(**user_combination,
                                 testvalues = randomiser_combination))
                else:
                    print(lesson(**user_combination,
                                 vocab_sample = vocab,
                                 testvalues = randomiser_combination))
                    
    else:
        repeat_num = input("Number of tests? ")
        for x in range(int(repeat_num)):
            if vocab == None:
                print(lesson(**rd.choice(user_params), 
                             testvalues = None))
            else:
                print(lesson(**rd.choice(user_params),
                             vocab_sample = vocab,
                             testvalues = None))
                    
        