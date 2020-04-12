# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:58:45 2020

@author: maste
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 22:33:04 2020

@author: maste
"""

'''
Expect High first order only
bee, honey
bicycle, pedal
tv, remote

High second order only
knife, scalpel
glasses, binoculars
door, gate
fence, wall

high both
dog, cat
bee,wasp
book,chapter

doctor, nurse

'''

###################################
# prepare corpus

path = '../apply_to_fluency/tasa_underscored_animals.txt'
save_path = 'wd_files/windowed_10.txt'

words = ['bee','honey']
words = ['bee','honey','bicycle','pedal','tv','remote',
         'knife','scalpel','glasses', 'binoculars','door', 'gate','fence', 'wall',
         'dog', 'cat','wasp','book','chapter','doctor', 'nurse']

def get_expected_vals(first_order,second_order):
    f_ = []
    s_ = []
    for pair in word_comparisons:
#        print(first_order.loc[pair[0]][pair[1]])
#        print(first_order.loc[pair[0]][pair[1]])
        f_.append(first_order[words.index(pair[0]),words.index(pair[1])])
        s_.append(second_order[words.index(pair[0]),words.index(pair[1])])

    
    f_ = np.array(f_)
    s_ = np.array(s_)
    # expect higher first order
    np.mean(f_[:3])
    np.mean(s_[:3])
    
    f_[:3] - s_[:3] # should be positive
    np.mean(f_[:3] - s_[:3])
    
    # expect higher second order
    np.mean(f_[3:7])
    np.mean(s_[3:7])
    
    f_[3:7] - s_[3:7] # should be negative
    np.mean(f_[3:7] - s_[3:7])
    
    # expect close first and second order
    np.mean(f_[7:])
    np.mean(s_[7:])
    
    f_[7:] - s_[7:] # should be near zero
    np.mean(f_[7:] - s_[7:])
    
    return np.mean(f_[:3] - s_[:3]),np.mean(f_[3:7] - s_[3:7]),np.mean(f_[7:] - s_[7:])

def test_measure(function, first, items_s):
    
#    f = jac.get_jaccard_matrix_simp(items_f,function)
    s = jac.get_jaccard_matrix_simp(items_s,function)
    
    return get_expected_vals(first,s)

################################################
# for a windowed corpus, load word by document corpus

import pandas as pd
import numpy as np

from get_wd import loadCorpus
import generalized_jaccard as jac

words = ['bee','honey','bicycle','pedal','tv','remote',
         'knife','scalpel','glasses', 'binoculars','door', 'gate','fence', 'wall',
         'dog', 'cat','wasp','book','chapter','doctor', 'nurse']

word_comparisons = [['bee','honey'],
                    ['bicycle','pedal'],
                    ['tv','remote'],
                    ['knife','scalpel'],
                    ['glasses', 'binoculars'],
                    ['door', 'gate'],
                    ['fence', 'wall'],
                    ['dog', 'cat'],
                    ['bee','wasp'],
                    ['book','chapter'],
                    ['doctor', 'nurse']]


output = pd.DataFrame(columns = ['window_size',
                                 'measure',
                                 'expected_first(pos)',
                                 'expected_second(neg)',
                                 'expected_equal'])
window_size = 1
for window_size in np.arange(1,11):
    print(window_size)
    path = 'wd_files/windowed_'+str(window_size)+'.txt'
    wd,mydict = loadCorpus(path)

    first = jac.get_jaccard_matrix_first(wd,mydict,words)    
#    items_f = jac.get_word_items(wd,[mydict[word] for word in words], second_order = False)
    items_s = jac.get_word_items(wd,[mydict[word] for word in words], second_order = True)
    
    
    print('average')
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_2,first,items_s)
    output = output.append({'window_size': window_size,
           'measure':'average',
           'expected_first(pos)':exp_first,
           'expected_second(neg)':exp_second,
           'expected_equal':exp_equal},ignore_index=True)
    
    print('max')
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_3,first,items_s)
    output = output.append({'window_size': window_size,
           'measure':'max',
           'expected_first(pos)':exp_first,
           'expected_second(neg)':exp_second,
           'expected_equal':exp_equal},ignore_index=True)
    
    print('min')
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_4,first,items_s)
    output = output.append({'window_size': window_size,
           'measure':'min',
           'expected_first(pos)':exp_first,
           'expected_second(neg)':exp_second,
           'expected_equal':exp_equal},ignore_index=True)
    
        
    print('h_eu')
    exp_first,exp_second,exp_equal = test_measure(jac.hausdorff_euclid,first,items_s)
    output = output.append({'window_size': window_size,
           'measure':'h_eu',
           'expected_first(pos)':exp_first,
           'expected_second(neg)':exp_second,
           'expected_equal':exp_equal},ignore_index=True)
    
    print('h_cos')
    exp_first,exp_second,exp_equal = test_measure(jac.hausdorff_cos_dist,first,items_s)
    output = output.append({'window_size': window_size,
           'measure':'h_cos',
           'expected_first(pos)':exp_first,
           'expected_second(neg)':exp_second,
           'expected_equal':exp_equal},ignore_index=True)
    print()









import pickle
import pandas as pd
import numpy as np

# import my function
from get_wd import loadCorpus
import generalized_jaccard as jac

corpus_load_path = '../apply_to_fluency/tasa_underscored_animals.txt'

for i in np.arange(2,11):
    wd,mydict = loadCorpus(corpus_load_path, window_length = i)
    pickle.dump([wd,mydict],open('wd_files/window_'+str(i)+'.p','wb'))
#pickle.dump([wd,mydict],open('window_2.p','wb'))
pickle.dump([wd,mydict],open('window_3.p','wb'))
#pickle.dump([wd,mydict],open('window_4.p','wb'))
#pickle.dump([wd,mydict],open('window_6.p','wb'))



def test_measure(my_func,items_f,items_s):
    print('  Measuring First Order')
    # first order 
    j_f_ave = np.zeros((len(items_f), len(items_f)))
    for i in np.arange(len(items_f)):
#        print(i)
        for j in np.arange(i, len(items_f)):
            j_f_ave[i, j] = my_func(items_f[i], items_f[j])
            j_f_ave[j, i] = j_f_ave[i, j]
            
    j_f_ave = pd.DataFrame(j_f_ave)
    j_f_ave.columns = list(words)
    j_f_ave.index = list(words)
            
    # second order 
    print('  Measuring Second Order')
    j_s_ave = np.zeros((len(items_s), len(items_s)))
    for i in np.arange(len(items_s)):
#        print(i)
        for j in np.arange(i, len(items_s)):
            j_s_ave[i, j] = my_func(items_s[i], items_s[j])
            j_s_ave[j, i] = j_s_ave[i, j]
            
    j_s_ave = pd.DataFrame(j_s_ave)
    j_s_ave.columns = list(words)
    j_s_ave.index = list(words)
    
    return get_expected_vals(j_f_ave,j_s_ave)

# words for testing
words = ['bee','honey','bicycle','pedal','tv','remote',
         'knife','scalpel','glasses', 'binoculars','door', 'gate','fence', 'wall',
         'dog', 'cat','wasp','book','chapter','doctor', 'nurse']
# word comparisons
word_comparisons = [['bee','honey'],
                    ['bicycle','pedal'],
                    ['tv','remote'],
                    ['knife','scalpel'],
                    ['glasses', 'binoculars'],
                    ['door', 'gate'],
                    ['fence', 'wall'],
                    ['dog', 'cat'],
                    ['bee','wasp'],
                    ['book','chapter'],
                    ['doctor', 'nurse']]

output = pd.DataFrame(columns = ['window_size',
                                 'measure',
                                 'expected_first(pos)',
                                 'expected_second(neg)',
                                 'expected_equal'])

#window_size = 3
for window_size in np.arange(2,4):
    wd,mydict = pickle.load(open('wd_files/window_'+str(window_size)+'.p','rb'))
    
    # words for testing
    word_inds = [mydict[word] for word in words]
    
    # get first and second order 
    # get items
    items_f = jac.get_word_items(wd,[mydict[word] for word in words], second_order = False)
    items_s = jac.get_word_items(wd,[mydict[word] for word in words], second_order = True)
    
    
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_1_1,items_f,items_s)
    print('Original')
    output = output.append({'window_size': window_size,
                   'measure':'original',
                   'expected_first(pos)':exp_first,
                   'expected_second(neg)':exp_second,
                   'expected_equal':exp_equal},ignore_index=True)
    print('Mean')
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_2,items_f,items_s)
    output = output.append({'window_size': window_size,
                   'measure':'mean',
                   'expected_first(pos)':exp_first,
                   'expected_second(neg)':exp_second,
                   'expected_equal':exp_equal},ignore_index=True)
    print('Max')
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_3,items_f,items_s)
    output = output.append({'window_size': window_size,
                   'measure':'max',
                   'expected_first(pos)':exp_first,
                   'expected_second(neg)':exp_second,
                   'expected_equal':exp_equal},ignore_index=True)
    print('Min')
    exp_first,exp_second,exp_equal = test_measure(jac.get_jaccard_4,items_f,items_s)
    output = output.append({'window_size': window_size,
                   'measure':'min',
                   'expected_first(pos)':exp_first,
                   'expected_second(neg)':exp_second,
                   'expected_equal':exp_equal},ignore_index=True)





wd2,mydict2 = pickle.load(open('wd_files/window_2.p','rb'))
wd3,mydict3 = pickle.load(open('wd_files/window_3.p','rb'))





