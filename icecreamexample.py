#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:31:18 2022

@author: oalakkad
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 12:43:43 2022

@author: oalakkad
"""
def alpha(words, em, trans, start):
    # get alpha(B) and alpha(I)
    B_list = []
    I_list = []

    B_list.append(start['B']*em['B'][words[0]])
    I_list.append(start['I']*em['I'][words[0]])

    for i in range(1,len(words)):
        B_list.append(B_list[i-1]*trans['B']['B']*em['B'][words[i]]+I_list[i-1]*trans['B']['I']*em['B'][words[i]])
        I_list.append(I_list[i-1]*trans['I']['I']*em['I'][words[i]]+B_list[i-1]*trans['I']['B']*em['I'][words[i]])

    return B_list, I_list


def beta(words, em, trans, start):
    #get beta(B) and beta(I)
    words = words[::-1]#words.reverse()
    B_list = []
    I_list = []

    B_list.append(trans['B']['.'])# + np.finfo(float).eps)
    I_list.append(trans['I']['.'])# + np.finfo(float).eps)
    for i in range(1,len(words)):
        B_list.append(B_list[i-1]*trans['B']['B']*em['B'][words[i-1]]+I_list[i-1]*trans['B']['I']*em['I'][words[i-1]])# + np.finfo(float).eps)
        I_list.append(I_list[i-1]*trans['I']['I']*em['I'][words[i-1]]+B_list[i-1]*trans['I']['B']*em['B'][words[i-1]])# + np.finfo(float).eps)

    B_list = B_list[::-1]
    I_list = I_list[::-1]

    return B_list, I_list

def new_p(letters, em, trans, Alpha_B, Alpha_I, Beta_B, Beta_I, addition):
    #get probabilites of P(B|B) P(B|I) P(I|B) P(I|I)
    P_new_BB, P_new_IB, P_new_BI, P_new_II = [0], [0], [0], [0]
    for i in range(1, len(letters)):
            P_new_BB.append((Alpha_B[i - 1]*trans['B']['B']*Beta_B[i]*em['B'][letters[i]]) / addition[i])
            P_new_IB.append((Alpha_I[i - 1]*trans['I']['B']*Beta_B[i]*em['B'][letters[i]]) / addition[i])
            P_new_BI.append((Alpha_B[i - 1]*trans['B']['I']*Beta_I[i]*em['I'][letters[i]]) / addition[i])
            P_new_II.append((Alpha_I[i - 1]*trans['I']['I']*Beta_I[i]*em['I'][letters[i]]) / addition[i])
    sum_P_new_BB, sum_P_new_IB, sum_P_new_BI, sum_P_new_II = sum(P_new_BB), sum(P_new_IB), sum(P_new_BI), sum(P_new_II)
    return sum_P_new_BB, sum_P_new_IB, sum_P_new_BI, sum_P_new_II

def generate_new_probs(P_B, P_I, sum_B, sum_I, sum_dictB, sum_dictI, P_new_BB, P_new_IB, P_new_BI, P_new_II, vocab):
    #update probabilities
    start = {'B': P_B[0], 'I':P_I[0]}
    trans = {'B': {'B':P_new_BB/sum_B, 'I':P_new_BI/sum_B, '.': P_B[-1]/sum_B}, 'I': {'B':P_new_IB/sum_I,'I':P_new_II/sum_I,'.':P_I[-1]/sum_I}}
    em = {'B': {}, 'I': {}}
    for letter in vocab:
        em['I'][letter] = sum_dictI[letter]/sum_I
        em['B'][letter] = sum_dictB[letter]/sum_B
    return start, em, trans

def fwd_bck(words_list, em, trans, start, vocab):
    sum_dictB = {}
    sum_dictI = {}
    for key in vocab:
        sum_dictB[key] = 0
        sum_dictI[key] = 0

    Alpha_B, Alpha_I = alpha(words_list, em, trans, start)
    Beta_B, Beta_I = beta(words_list, em, trans, start)
    BB = [a*b for a,b in zip(Alpha_B,Beta_B)]
    II = [a*b for a,b in zip(Alpha_I,Beta_I)]
    addition = [sum(x) for x in zip(BB, II)]
    P_B = [a/b for a,b in zip(BB,addition)]
    P_I = [a/b for a,b in zip(II,addition)]
    P_new_BB, P_new_IB, P_new_BI, P_new_II = new_p(words_list, em, trans, Alpha_B, Alpha_I, Beta_B, Beta_I, addition)

    sum_B = sum(P_B)
    sum_I = sum(P_I)

    for i in range(len(words_list)):
        sum_dictB[words_list[i]] += P_B[i]
        sum_dictI[words_list[i]] += P_I[i]

    new_start, new_em, new_trans = generate_new_probs(P_B, P_I, sum_B, sum_I, sum_dictB, sum_dictI, P_new_BB, P_new_IB, P_new_BI, P_new_II,vocab)

    return new_start, new_em, new_trans

if __name__ == "__main__":
    x_train_list = [2,3,3,2,3,2,3,2,2,3,1,3,3,1,1,1,2,1,1,1,3,1,2,1,1,1,2,3,3,2,3,2,2]
    start_freq_dict = {'B': 0.5, 'I':0.5}
    emmision_frequency_dict = {'B': {1:0.7, 2:0.2, 3: 0.1}, 'I': {1:0.1,2:0.2,3:0.7}}
    transition_frequency_dict = {'B': {'B':0.8, 'I':0.1, '.': 0.1}, 'I': {'B':0.1,'I':0.8,'.':0.1}}
    vocab = [1,2,3]

    for i in range(10):
        start_freq_dict, emmision_frequency_dict, transition_frequency_dict = fwd_bck(x_train_list, emmision_frequency_dict, transition_frequency_dict, start_freq_dict, vocab)

