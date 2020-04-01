# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 16:37:42 2020

@author: maste
"""


# load test corpus
from get_wd import loadCorpus
corpus_load_path = '../corpus/test_corpus.txt'
wd,mydict = loadCorpus(corpus_load_path)

# for each word in the dictionary, 
# get the word items
#    -wd matrices describing the contexts in which the word occurs
# second order
import generalized_jaccard as jac
items = jac.get_word_items(wd,list(mydict.values()), second_order = False)
items = jac.get_word_items(wd,list(mydict.values()), second_order = True)

# define jaccard as average cosine matrix
j_ave = np.zeros((len(items), len(items)))
for i in np.arange(len(items)):
    print(i)
    for j in np.arange(i, len(items)):
        j_ave[i, j] = jac.get_jaccard_2(items[i], items[j])
        j_ave[j, i] = j_ave[i, j]
'''
Qualitative notes:
    diagonal isn't 1
    all values above zero
    follows intuition
'''

# define jaccard as ((row.max.sum)+(col.max.sum))/(num_rows+num_cols)
j_max = np.zeros((len(items), len(items)))
for i in np.arange(len(items)):
    print(i)
    for j in np.arange(i, len(items)):
        j_max[i, j] = jac.get_jaccard_3(items[i], items[j])
        j_max[j, i] = j_max[i, j]
'''
Qualitative notes:
    diagonal is one
    doesn't differentiate between mouse and verbs... idk if this matters
    All values above zero
'''

# define jaccard as ((row.min.sum)+(col.min.sum))/(num_rows+num_cols)
j_min = np.zeros((len(items), len(items)))
for i in np.arange(len(items)):
    print(i)
    for j in np.arange(i, len(items)):
        j_min[i, j] = jac.get_jaccard_4(items[i], items[j])
        j_min[j, i] = j_min[i, j]
'''
Qualitative notes:
    this is weird
'''