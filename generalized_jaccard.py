# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 19:46:07 2020

@author: maste
"""

# import libraries
from scipy import sparse
import numpy as np
from itertools import combinations

# because we're dealing with sets, should each duplicate instance be removed?
# we want frequency independent of first order independent of second order

# convert wd matrix into sparse ngram matrix
def get_ngram_matrix(wd,ngram):
    row_ind = 0
    cols = []
    rows = []
    for i in sorted(set(sparse.find(wd)[0])):
        inds = sparse.find(wd[i])[1]
        col = list(combinations(inds,ngram)) # all ngrams
        row = np.repeat(np.arange(row_ind,row_ind+len(col)),ngram)
        row_ind += len(col)
        col = [item for val in col for item in val]
        
        cols.extend(col)
        rows.extend(row)
    data = np.ones(len(cols))
    ngram_matrix = sparse.csr_matrix((data,(rows,cols)), shape = (row_ind, wd.shape[1]))
    return ngram_matrix

def get_unique_item_ngram_matrix(ngram_matrix, item_ind, second_order = False, ignore_frequency = False):
    
    item = ngram_matrix[sparse.find(ngram_matrix[:,item_ind])[0]] # get instances where item occurs
    
    # if second order, set item ind to zero
    if second_order:
        item[:,item_ind] = 0
        # drop zero rows
        item = item[np.where(item.sum(1) != 0)[0]]
    
    ngram_sims = cosine_table_self(item) # find matching instances
    ngram_inds = list(np.arange(item.shape[0])) # list to track instances visited
    
    new_ngram_list = [] # output list of unique instances
    ngram_counts = [] # counts per instance

    # visit each instance, add unique to output list, track counts
    while len(ngram_inds) > 0:
        new_ngram_list.append(item[ngram_inds[0]])
        inds,vals = sparse.find(ngram_sims[ngram_inds[0]])[1:]
        this_inds = inds[np.where(vals > .99)[0]]
        ngram_counts.append(len(this_inds))
        for i in this_inds:
            ngram_inds.remove(i)
            
    # if ignore frequency == True, set ngram counts to list of ones
    if ignore_frequency:
        ngram_counts = [1] * len(ngram_counts)
        
    new_ngram_list = sparse.vstack(new_ngram_list) # change output list format
    return new_ngram_list,ngram_counts

#ngram_sims = cosine_table_self(ngram_matrix)
#ngram_inds = list(np.arange(ngram_matrix.shape[0]))
#
#new_ngram_list = []
#ngram_counts = []
#count = 0
#while len(ngram_inds) > 0:
#    new_ngram_list.append(ngram_matrix[ngram_inds[0]])
#    inds,vals = sparse.find(ngram_sims[ngram_inds[0]])[1:]
#    this_inds = inds[np.where(vals > .9999)[0]]
#    ngram_counts.append(len(this_inds))
#    for i in this_inds:
#        ngram_inds.remove(i)
#    count += 1
#ngram_matrix[sparse.find(ngram_matrix[:,ind_1])[0]]
    
def cosine_table_self(vects): # get cosine table, input one matrix
    return vects.dot(vects.transpose()) / \
            np.outer(np.sqrt(vects.power(2).sum(1)),
                     np.sqrt(vects.power(2).sum(1)))


# code jaccard similarity - first order similarity
#def get_jaccard_first_order_1(wd, ngram_matrix, ind_1, ind_2):
#    '''
#    wd: word by document matrix in sparse data structure
#    ind_1: index of first word for comparison
#    ind_2: index of second word for comparison
#    '''
#    
#    item_1 = set(sparse.find(ngram_matrix[:,ind_1])[0]) # get all the unique instances where item_1 occurs
#    item_2 = set(sparse.find(ngram_matrix[:,ind_2])[0]) # get all the unique instances where item_2 occurs
#    jaccard = len(item_1.intersection(item_2)) / len(item_1.union(item_2))
#    
#    return jaccard
    
def get_jaccard(item_1, item_2):
    '''
    wd: word by document matrix in sparse data structure
    ind_1: index of first word for comparison
    ind_2: index of second word for comparison
    '''
    
#    item_1 = items[i]
#    item_2 = items[j]
    
    set_intersection = np.where(cosine_table(item_1[0],item_2[0]) > 0.99)
    
    if(len(set_intersection[0]) == 0) or (len(set_intersection[1]) == 0):
        return 0
    
    num = []
    for i in np.arange(len(set_intersection[0])):
        num.append(min(item_1[1][set_intersection[0][i]],item_2[1][set_intersection[1][i]]))
    num = sum(num)
    denom = sum(item_1[1]) + \
            sum(item_2[1]) - num
            # a given context may be repeated in the corpus, treat it
    
    jaccard_second_order = num / denom
    
    return jaccard_second_order

# code variant of jaccard - second order similarity
        
def cosine_table(vects_a,vects_b): # get cosine sims between two matrices
    return vects_a.dot(vects_b.transpose()) / \
            np.outer(np.sqrt(vects_a.power(2).sum(1)),
                     np.sqrt(vects_b.power(2).sum(1)))

#def get_jaccard_second_order(wd,ngram_matrix,ind_1,ind_2):
#    '''
#    wd: word by document matrix in sparse data structure
#    ind_1: index of first word for comparison
#    ind_2: index of second word for comparison
#    '''
#        
#    item_1 = ngram_matrix[sparse.find(ngram_matrix[:,ind_1])[0]] # get all the unique instances where item_1 occurs
#    item_1[:,ind_1] = 0 # modify instances into the context only of item_1
#    item_2 = ngram_matrix[sparse.find(ngram_matrix[:,ind_2 ])[0]] # get all the unique instances where item_1 occurs
#    item_2[:,ind_2] = 0 # modify instances into the context only of item_1
#    
#    set_intersection_length = len(np.where(np.round(cosine_table(item_1,item_2),5) == 1)[0])
##    denominator_1 = item_1.shape[0] - set_intersection_length
##    denominator_2 = item_2.shape[0] - set_intersection_length
##    denominator = set_intersection_length + denominator_1 + denominator_2 + 1
#    # short term solution
#    denominator = np.max([item_1.shape[0], item_2.shape[0],set_intersection_length])
#    
#    jaccard_second_order = set_intersection_length / denominator
#    return jaccard_second_order

def get_jaccard_matrix(wd, ngram, second_order = False, ignore_frequency = False, word_inds = False):
    
#    ngram = 3
    if ngram:
        ngram_matrix = get_ngram_matrix(wd, ngram)
    else:
        ngram_matrix = wd

    if word_inds: # word_inds provides list of indices from which to derive jaccard matrix
        items = []
        for ind,i in enumerate(word_inds): # for loop converts wd to set
            print(str(ind) + '/' + str(len(word_inds)))
            items.append(get_unique_item_ngram_matrix(ngram_matrix,i,second_order,ignore_frequency))
        print('finished gathering items')
    else: # if word_inds not provided, make jaccard for entire corpus dictionary
        word_inds = list(np.arange(wd.shape[1]))
        items = []
        for i in np.arange(wd.shape[1]): # for loop converts wd to set
            items.append(get_unique_item_ngram_matrix(ngram_matrix,i,second_order,ignore_frequency))
       
    jaccard = np.zeros((len(word_inds), len(word_inds)))
    for i in np.arange(len(word_inds)):
        print(i)
        for j in np.arange(i, len(word_inds)):
            jaccard[i, j] = get_jaccard(items[i], items[j])
            jaccard[j, i] = jaccard[i, j]
    return jaccard
            
def get_word_items(ngram_matrix, word_inds, second_order = False, ignore_frequency = False):
    if word_inds: # word_inds provides list of indices from which to derive jaccard matrix
        items = []
        for ind,i in enumerate(word_inds): # for loop converts wd to set
            print(str(ind + 1) + '/' + str(len(word_inds)))
            items.append(get_unique_item_ngram_matrix(ngram_matrix,i,second_order,ignore_frequency))
        print('finished gathering items')
    return items
    

    
#    ngram_matrix = get_ngram_matrix(wd, ngram)
#    
#    items = []
#    for i in np.arange(wd.shape[1]):
#        items.append(get_unique_item_ngram_matrix(ngram_matrix,i))
#   
#    jaccard = np.zeros((wd.shape[1], wd.shape[1]))
#    for i in np.arange(wd.shape[1]):
#        for j in np.arange(i, wd.shape[1]):
#            jaccard[i, j] = order_function(wd, ngram_matrix, i, j)
#            jaccard[j, i] = jaccard[i, j]