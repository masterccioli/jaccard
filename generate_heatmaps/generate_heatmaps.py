# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 19:02:36 2020

@author: maste
"""

import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
import os

# import my function
from get_wd import loadCorpus
#import jaccard_implementation as ji
import generalized_jaccard as jac
import annotated_heat_maps as ahm

corpus_load_path = '../corpus/shape_6_nsew_sampledas_shape.txt'
corpus_load_path = '../corpus/shape_nf.txt'
corpus_load_path = '../corpus/test_corpus.txt'
corpus_load_path = '../corpus/shape_nsew_sampledAs_shape.txt'
jaccard_function = jac.get_jaccard_first_order
ngram = 2
csv_save_path = '../csv_output/shape_nsew_sampledAs_shape.csv'
heatmap_save_path = '../heatmaps/shape_nsew_sampledAs_shape.png'
heatmap_header = 'First_2 Order Jaccard Index'
inds = 20
img_size = 12
font_size = 15


def output_csv_heatmap(corpus_load_path, ngram, second_order, ignore_frequency,
                       csv_save_path, 
                       heatmap_save_path, inds, img_size=10,
                       font_size = 20,annotate = False):
    # load test corpus
    wd,mydict = loadCorpus(corpus_load_path)
    
    # get first order matrix
    f = jac.get_jaccard_matrix(wd,ngram,second_order,ignore_frequency)
    np.fill_diagonal(f,0)
    
    out = pd.DataFrame(f)
    out.columns = list(mydict.keys())
    out.index = list(mydict.keys())
    out.to_csv(csv_save_path, index = False)
    
    # plot first order
    fig, ax = plt.subplots()
    
    im, cbar = ahm.heatmap(f[:inds, :inds], list(mydict.keys())[:inds], list(mydict.keys())[:inds], ax=ax,
                       cmap="gist_heat", cbarlabel='Jaccard Index')
    if annotate:
        ahm.annotate_heatmap(im, valfmt="{x:.2f}", fontsize = font_size)
    
    fig.tight_layout()
    
    fig = plt.gcf()
    fig.set_size_inches(img_size, img_size)
    #plt.show()
    fig.savefig(heatmap_save_path, dpi=100, transparent = True)

def set_of_outputs(corpus_load_path, inds, img_size = 10, annotate = False):
    
    #make folder for jaccard output
    if not os.path.exists('../output/'+corpus_load_path):
        os.mkdir('../output/'+corpus_load_path)
    
    #bigram
     # first order
      # frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',2,False,False,
                       '../output/'+corpus_load_path+'/2_first_frequency.csv',
                       '../output/'+corpus_load_path+'/2_first_frequency.png',inds,img_size,annotate=annotate)
      # ignore frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',2,False,True,
                       '../output/'+corpus_load_path+'/2_first_ignoreFrequency.csv',
                       '../output/'+corpus_load_path+'/2_first_ignoreFrequency.png',inds,img_size,annotate=annotate)

     # second order
      # frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',2,True,False,
                       '../output/'+corpus_load_path+'/2_second_frequency.csv',
                       '../output/'+corpus_load_path+'/2_second_frequency.png',inds,img_size,annotate=annotate)
      # ignore frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',2,True,True,
                       '../output/'+corpus_load_path+'/2_second_ignoreFrequency.csv',
                       '../output/'+corpus_load_path+'/2_second_ignoreFrequency.png',inds,img_size,annotate=annotate)
    # trigram
     # first order
      # frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',3,False,False,
                       '../output/'+corpus_load_path+'/3_first_frequency.csv',
                       '../output/'+corpus_load_path+'/3_first_frequency.png',inds,img_size,annotate=annotate)
      # ignore frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',3,False,True,
                       '../output/'+corpus_load_path+'/3_first_ignoreFrequency.csv',
                       '../output/'+corpus_load_path+'/3_first_ignoreFrequency.png',inds,img_size,annotate=annotate)

     # second order
      # frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',3,True,False,
                       '../output/'+corpus_load_path+'/3_second_frequency.csv',
                       '../output/'+corpus_load_path+'/3_second_frequency.png',inds,img_size,annotate=annotate)
      # ignore frequency
    output_csv_heatmap('../corpus/'+corpus_load_path+'.txt',3,True,True,
                       '../output/'+corpus_load_path+'/3_second_ignoreFrequency.csv',
                       '../output/'+corpus_load_path+'/3_second_ignoreFrequency.png',inds,img_size,annotate=annotate)


output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',2,True,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',2,True,True,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)

output_csv_heatmap('../corpus/shape_nsew_sampledas_cluster2.txt',3,False,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/f_2_shape_nsew_sampledAs_cluster2.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',3,True,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/s_2_shape_nsew_sampledAs_cluster2.png',
                   'Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_nsew_sampledas_cluster2.txt',3,True,True,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
                

output_csv_heatmap('../corpus/test_corpus.txt',3,False,False,
                   '../csv_output/testcorpus_f_2.csv',
                   '../heatmaps/testcorpus_f_2.png',
                   'First_2 Order Jaccard Index', 5)


set_of_outputs('test_corpus',5,annotate=True)
output_csv_heatmap('../corpus/test_corpus.txt', jac.get_jaccard_first_order,2,
                   '../csv_output/testcorpus_f_2.csv',
                   '../heatmaps/testcorpus_f_2.png',
                   'First_2 Order Jaccard Index', 5)
output_csv_heatmap('../corpus/test_corpus.txt', jac.get_jaccard_first_order,3,
                   '../csv_output/testcorpus_f_3.csv',
                   '../heatmaps/testcorpus_f_3.png',
                   'First_3 Order Jaccard Index', 5)

output_csv_heatmap('../corpus/test_corpus.txt', jac.get_jaccard_second_order,2,
                   '../csv_output/testcorpus_s_2.csv',
                   '../heatmaps/testcorpus_s_2.png',
                   'Second_1 Order Jaccard Index', 5)
output_csv_heatmap('../corpus/test_corpus.txt', jac.get_jaccard_second_order,3,
                   '../csv_output/testcorpus_s_3.csv',
                   '../heatmaps/testcorpus_s_3.png',
                   'Second_2 Order Jaccard Index', 5)


########################################
# generate matrix for artificial grammar
########################################

# load corpus - near/far
set_of_outputs('shape_20_nf',20)
#
#output_csv_heatmap('../corpus/shape_nf.txt', 2, False, False,
#                   '../csv_output/shape_nf_f_2.csv',
#                   '../heatmaps/shape_nf_f_2.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#
#
#output_csv_heatmap('../corpus/shape_nf.txt', jac.get_jaccard_first_order,2,
#                   '../csv_output/shape_nf_f_2.csv',
#                   '../heatmaps/shape_nf_f_2.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nf.txt', jac.get_jaccard_first_order,3,
#                   '../csv_output/shape_nf_f_3.csv',
#                   '../heatmaps/shape_nf_f_3.png',
#                   'First_3 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/shape_nf.txt', jac.get_jaccard_second_order,2,
#                   '../csv_output/shape_nf_s_2.csv',
#                   '../heatmaps/shape_nf_s_2.png',
#                   'Second_1 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nf.txt', jac.get_jaccard_second_order,3,
#                   '../csv_output/shape_nf_s_3.csv',
#                   '../heatmaps/shape_nf_s_3.png',
#                   'Second_2 Order Jaccard Index',20,12, 15)

# load corpus - nsew
set_of_outputs('shape_20_nsew',20)
#output_csv_heatmap('../corpus/shape_nsew.txt', jac.get_jaccard_first_order,2,
#                   '../csv_output/shape_nsew_f_2.csv',
#                   '../heatmaps/shape_nsew_f_2.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nsew.txt', jac.get_jaccard_first_order,3,
#                   '../csv_output/shape_nsew_f_3.csv',
#                   '../heatmaps/shape_nsew_f_3.png',
#                   'First_3 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/shape_nsew.txt', jac.get_jaccard_second_order,2,
#                   '../csv_output/shape_nsew_s_2.csv',
#                   '../heatmaps/shape_nsew_s_2.png',
#                   'Second_1 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nsew.txt', jac.get_jaccard_second_order,3,
#                   '../csv_output/shape_nsew_s_3.csv',
#                   '../heatmaps/shape_nsew_s_3.png',
#                   'Second_2 Order Jaccard Index',20,12, 15)

# load corpus - artificialGrammar
set_of_outputs('artificialGrammar',20)
#output_csv_heatmap('../corpus/artificialGrammar.txt', jac.get_jaccard_first_order,2,
#                   '../csv_output/artificialGrammar_f_2.csv',
#                   '../heatmaps/artificialGrammar_f_2.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/artificialGrammar.txt', jac.get_jaccard_first_order,3,
#                   '../csv_output/artificialGrammar_f_3.csv',
#                   '../heatmaps/artificialGrammar_f_3.png',
#                   'First_3 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/artificialGrammar.txt', jac.get_jaccard_second_order,2,
#                   '../csv_output/artificialGrammar_s_2.csv',
#                   '../heatmaps/artificialGrammar_s_2.png',
#                   'Second_1 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/artificialGrammar.txt', jac.get_jaccard_second_order,3,
#                   '../csv_output/artificialGrammar_s_3.csv',
#                   '../heatmaps/artificialGrammar_s_3.png',
#                   'Second_2 Order Jaccard Index',20,12, 15)


# load corpus - nsew, shape, confused by sampling
set_of_outputs('shape_20_nsew_sampledas_cluster2',20)
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_cluster2.txt', jac.get_jaccard_first_order,2,
#                   '../csv_output/shape_nsew_sampledAs_cluster2.csv',
#                   '../heatmaps/shape_nsew_sampledAs_cluster2.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_cluster2.txt', 2,False,False,
#                   '../csv_output/shape_nsew_sampledAs_cluster2.csv',
#                   '../heatmaps/shape_nsew_sampledAs_cluster2.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_cluster2.txt', jac.get_jaccard_first_order,3,
#                   '../csv_output/shape_nsew_sampledAs_cluster2.csv',
#                   '../heatmaps/shape_nsew_sampledAs_cluster2.png',
#                   'First_3 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_cluster2.txt', jac.get_jaccard_second_order,2,
#                   '../csv_output/shape_nsew_sampledAs_cluster2.csv',
#                   '../heatmaps/shape_nsew_sampledAs_cluster2.png',
#                   'Second_1 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_cluster2.txt', jac.get_jaccard_second_order,3,
#                   '../csv_output/shape_nsew_sampledAs_cluster2.csv',
#                   '../heatmaps/shape_nsew_sampledAs_cluster2.png',
#                   'Second_2 Order Jaccard Index',20,12, 15)

# load corpus - nsew, shape, w/sampling
set_of_outputs('shape_20_nsew_sampledas_shape',20)
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_shape.txt', jac.get_jaccard_first_order,2,
#                   '../csv_output/shape_nsew_sampledAs_shape.csv',
#                   '../heatmaps/shape_nsew_sampledAs_shape.png',
#                   'First_2 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_shape.txt', jac.get_jaccard_first_order,3,
#                   '../csv_output/shape_nsew_sampledAs_shape.csv',
#                   '../heatmaps/shape_nsew_sampledAs_shape.png',
#                   'First_3 Order Jaccard Index',20,12, 15)
#
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_shape.txt', jac.get_jaccard_second_order,2,
#                   '../csv_output/shape_nsew_sampledAs_shape.csv',
#                   '../heatmaps/shape_nsew_sampledAs_shape.png',
#                   'Second_1 Order Jaccard Index',20,12, 15)
#output_csv_heatmap('../corpus/shape_nsew_sampledAs_shape.txt', jac.get_jaccard_second_order,3,
#                   '../csv_output/shape_nsew_sampledAs_shape.csv',
#                   '../heatmaps/shape_nsew_sampledAs_shape.png',
#                   'Second_2 Order Jaccard Index',20,12, 15)


# load corpus - nsew, shape, w/sampling
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_shape.txt',2,False,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_shape.txt',2,True,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_shape.txt',2,True,True,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)

output_csv_heatmap('../corpus/shape_6_nsew_sampledas_shape.txt',3,False,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_shape.txt',3,True,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_shape.txt',3,True,True,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)

output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',2,False,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',2,True,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',2,True,True,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)

output_csv_heatmap('../corpus/shape_nsew_sampledas_cluster2.txt',3,False,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/f_2_shape_nsew_sampledAs_cluster2.png',
                   'First_2 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_6_nsew_sampledas_cluster2.txt',3,True,False,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/s_2_shape_nsew_sampledAs_cluster2.png',
                   'Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_nsew_sampledas_cluster2.txt',3,True,True,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_2 Order Jaccard Index',20,12, 15)

output_csv_heatmap('../corpus/shape_6_nsew_sampledAs_shape.txt', jac.get_jaccard_first_order,3,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'First_3 Order Jaccard Index',20,12, 15)

output_csv_heatmap('../corpus/shape_nsew_sampledAs_shape.txt', jac.get_jaccard_second_order,2,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'Second_1 Order Jaccard Index',20,12, 15)
output_csv_heatmap('../corpus/shape_nsew_sampledAs_shape.txt', jac.get_jaccard_second_order,3,
                   '../csv_output/shape_nsew_sampledAs_shape.csv',
                   '../heatmaps/shape_nsew_sampledAs_shape.png',
                   'Second_2 Order Jaccard Index',20,12, 15)


