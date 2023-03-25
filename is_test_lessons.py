# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:10:24 2023

@author: Zoe
"""
import is_question_generator as qgen
import is_csvreader as csvr
import is_lesson_options as lo
import itertools
import random as rd
from inspect import signature

#This top section of functions are just called inside the actual test function.
#The tester doesn't need to use these functions.
#But you do want to update the all_randomiser_params dictionary 
#when you create a new lesson.

def get_randomiser_params(lesson, vocab_sample):
    """Returns a dictionary of the randomiser parameters with their range of values.
    Update the dictionary in here when a new lesson is created."""
    range_vocab = range(csvr.length(vocab_sample))
    range_pronouns = range(7)
    range_pronouns_names = range(8)
    all_randomiser_params =  {"give_get" : {"subject_num" : range_pronouns_names,
                                            "object_num" : range_pronouns_names,
                                            "gift_num" : range_vocab,
                                            "give_get_num" : range(2)},
                              
                              "possession_aig" : {"subject_num" : range_pronouns,
                                                  "object_num" : range_vocab},
                              
                              "gender" : {"vocab_num" : range_vocab},
                              
                              "numbers" : {"num" : range(1,100)},
                              
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
                                        "mins_num" : range(0, 60, 5)}
                              }
    return all_randomiser_params[lesson.__name__]


def get_user_params(lesson):
    """Returns a dictionary of user parameters and their possible values"""
    all_lesson_params = [x for x in signature(lesson).parameters]
    user_params = dict()
    for each in all_lesson_params:
        if each in lo.parameter_prompts:
            user_params[each] = [k[0] for k in lo.user_menu_options[each]]
    return user_params


def generate_params(lesson, vocab_sample, param_type):
    """Creates a generator object of each possible combination of values 
    for the user/randomiser parameters"""
    if param_type == "randomiser":
        param_names = get_randomiser_params(vocab_sample, lesson).keys()
        ranges = [r for r in get_randomiser_params(vocab_sample, lesson).values()]
    elif param_type == "user":
        param_names = get_user_params(lesson).keys()
        ranges = [r for r in get_user_params(lesson).values()]
    for values in itertools.product(*ranges):
        yield dict(zip(param_names, values))


def get_params(lesson, vocab_sample, param_type):
    """Creates a list of all possible combinations of values
    for the user/randomiser parameters"""
    return [combination for combination in generate_params(lesson, 
                                                           vocab_sample, 
                                                           param_type)]

#-------------- Below is the function you use for testing

def test(lesson, vocab_sample, fulltest = False):
    """Generates question, prompt, solution-list
    fulltest == True: all possible combinations of parameters
    fulltest == False: a random combination of parameters, as many times as specified
    'lesson' must be the function, e.g. qgen.give_get;
    vocab_sample must be a vocabulary file (imported with csvr)"""
    user_params = get_params(lesson, vocab_sample, "user")
    if fulltest == True:
        for user_combination in user_params:
            for randomiser_combination in get_params(lesson, vocab_sample, "randomiser"):
                print(lesson(**user_combination, 
                             vocab_sample = vocab_sample, 
                             testvalues = randomiser_combination))
    else:
        repeat_num = input("Number of tests? ")
        for x in range(int(repeat_num)):
            print(lesson(**rd.choice(user_params), 
                         vocab_sample = csvr.random_sample(vocab_sample,1), 
                         testvalues = None))
        