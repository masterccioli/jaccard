# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 19:46:07 2020

@author: maste
"""

# import libraries
from scipy import sparse
import pandas as pd
import numpy as np
from itertools import combinations
from sklearn.metrics.pairwise import euclidean_distances

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

def get_item_ngram_matrix(ngram_matrix, item_ind, second_order = False, ignore_frequency = False):
    
    item = ngram_matrix[sparse.find(ngram_matrix[:,item_ind])[0]] # get instances where item occurs
    
    # if second order, set item ind to zero
    if second_order:
        item[:,item_ind] = 0
        # drop zero rows
        item = item[np.where(item.sum(1) != 0)[0]]
    
    return item


def cosine_table_self(vects): # get cosine table, input one matrix
    return vects.dot(vects.transpose()) / \
            np.outer(np.sqrt(vects.power(2).sum(1)),
                     np.sqrt(vects.power(2).sum(1)))


# simplify first order jaccard - direct co-occurrence
def first_order(item_1,item_2,word_ind_1,word_ind_2):
    #intersection
#    len(sparse.find(item_1[:,word_ind_1].multiply(item_1[:,word_ind_2]))[0])
#    len(sparse.find(item_2[:,word_ind_1].multiply(item_2[:,word_ind_2]))[0])
    intersection = len(sparse.find(item_1[:,word_ind_1].multiply(item_1[:,word_ind_2]))[0])
    
    #union
    union = item_1.shape[0] + item_2.shape[1] - intersection
    
    return intersection/union

# strict jaccard
def get_jaccard_1(item_1, item_2):
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

def get_jaccard_1_1(item_1, item_2):
    '''
    wd: word by document matrix in sparse data structure
    ind_1: index of first word for comparison
    ind_2: index of second word for comparison
    '''
    
#    item_1 = items[i]
#    item_2 = items[j]
    
    set_intersection = np.where(cosine_table(item_1,item_2) > 0.99)
    
    if(len(set_intersection[0]) == 0) or (len(set_intersection[1]) == 0):
        return 0
    
    num = []
#    for i in np.arange(len(set_intersection[0])):
#        num.append(min(item_1[1][set_intersection[0][i]],item_2[1][set_intersection[1][i]]))
    num = len(set_intersection[0])
    denom = item_1.shape[0] + item_2.shape[0]
            # a given context may be repeated in the corpus, treat it
    
    jaccard_second_order = num / denom
    
    return jaccard_second_order

# jaccard as averaged cosine matrix
def get_jaccard_2(item_1, item_2):
    '''
    wd: word by document matrix in sparse data structure
    ind_1: index of first word for comparison
    ind_2: index of second word for comparison
    '''
    
#    item_1 = items[i]
#    item_2 = items[j]
    
    val = np.mean(cosine_table(item_1,item_2))
        
    return val

# define jaccard as ((row.max.sum)+(col.max.sum))/(num_rows+num_cols)
def get_jaccard_3(item_1, item_2):
    '''
    wd: word by document matrix in sparse data structure
    ind_1: index of first word for comparison
    ind_2: index of second word for comparison
    '''
    
#    item_1 = items[i]
#    item_2 = items[j]
    
    vals = cosine_table(item_1,item_2)
    num = vals.max(0).sum() + vals.max(1).sum()
    denom = np.sum(vals.shape)
        
    return num/denom

# define jaccard as ((row.min.sum)+(col.min.sum))/(num_rows+num_cols)
def get_jaccard_4(item_1, item_2):
    '''
    wd: word by document matrix in sparse data structure
    ind_1: index of first word for comparison
    ind_2: index of second word for comparison
    '''
    
#    item_1 = items[i]
#    item_2 = items[j]
    
    vals = cosine_table(item_1,item_2)
    num = vals.min(0).sum() + vals.min(1).sum()
    denom = np.sum(vals.shape)
        
    return num/denom

def hausdorff_euclid(item_1, item_2):
    
    vals = cosine_table(item_1, item_2)
    vals = euclidean_distances(item_1, item_2)
    inf_1 = vals.min(0)
    inf_2 = vals.min(1)
    
    sup_1 = inf_1.max()
    sup_2 = inf_2.max()
    
    return np.max([sup_1,sup_2])

def hausdorff_cos_dist(item_1, item_2):
    
    vals = 1 - cosine_table(item_1, item_2)
#    vals = euclidean_distances(item_1, item_2)
    inf_1 = vals.min(0)
    inf_2 = vals.min(1)
    
    sup_1 = inf_1.max()
    sup_2 = inf_2.max()
    
    return np.max([sup_1,sup_2])

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
            jaccard[i, j] = get_jaccard_1(items[i], items[j])
            jaccard[j, i] = jaccard[i, j]
    return jaccard

def get_jaccard_matrix_simp(items,function):#,words):
    out = np.zeros((len(items), len(items)))
    for i in np.arange(len(items)):
#        print(i)
        for j in np.arange(i, len(items)):
            out[i, j] = function(items[i], items[j])
            out[j, i] = out[i, j]
#    out = pd.DataFrame(out)
#    out.columns = words
#    out.index = words
    return out

def get_jaccard_matrix_first(wd,mydict,words):
    out = np.zeros((len(words), len(words)))
    for i in np.arange(wd.shape[1]):
#        print(i)
        for j in np.arange(i, len(words)):
            out[i, j] = first_order(wd,mydict[words[i]],mydict[words[j]])
            out[j, i] = out[i, j]
    #out = pd.DataFrame(out)
    #out.columns = words
    #out.index = words
    return out
            
def get_word_items_unique(ngram_matrix, word_inds, second_order = False, ignore_frequency = False):
    if word_inds: # word_inds provides list of indices from which to derive jaccard matrix
        items = []
        for ind,i in enumerate(word_inds): # for loop converts wd to set
            print(str(ind + 1) + '/' + str(len(word_inds)))
            items.append(get_unique_item_ngram_matrix(ngram_matrix,i,second_order,ignore_frequency))
        print('finished gathering items')
    return items

def get_word_items(ngram_matrix, word_inds, second_order = False, ignore_frequency = False):
    print('Gathering Word Items')
    if word_inds: # word_inds provides list of indices from which to derive jaccard matrix
        items = []
        for ind,i in enumerate(word_inds): # for loop converts wd to set
#            print(str(ind + 1) + '/' + str(len(word_inds)))
#            items.append(get_item_ngram_matrix(ngram_matrix,i,second_order,ignore_frequency))
            items.append(get_item_ngram_matrix(ngram_matrix,i,second_order,ignore_frequency))
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
