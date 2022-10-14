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
import csv
import copy
import numpy as np

def load_dataset(name):
        with open(name, encoding="utf-8") as file:
          f = csv.reader(file, delimiter="\t")
          word = []
          labels = []
          word_no = []
          for line in f:
            word_no.append(line[0])
            line[0] += ('.')
            word.append(line[0])
            labels.append(line[1])

        return word, word_no, labels


def tag_words(labels):
    # tag letters with either B or I tag
    res = []
    for word_division in labels:
      split_word = word_division.split('-')
      temp = []
      for letter in split_word:
        temp.append((letter[0], 'B'))
        if len(letter) > 1:
          for item in letter[1:]:
            temp.append((item, 'I'))
      res.append(temp)

    return res

def create_beta_dict(tagged_letters, vocab, tags):
    # create the emmission probability dict
    beta_dict = {}
    for tag in tags:
        beta_dict[tag] = {}
        for key in vocab:
            beta_dict[tag][key] = 1 # add smoothing, imagine we saw each word once before
    for i in range(len(tagged_letters)):
        for j in range(len(tagged_letters[i])):
                    beta_dict[tagged_letters[i][j][1]][tagged_letters[i][j][0]] += 1

    return beta_dict

def create_beta_frequency_dict(beta_dict,vocab,tags):
    #get the percentage of the emmission dict
    count = {}
    for tag in tags:
        count[tag] = 0
        for letter in vocab:
            count[tag] += beta_dict[tag][letter]

    beta_frequency_dict = copy.deepcopy(beta_dict)
    for key in beta_frequency_dict.keys():
        for key2 in beta_frequency_dict[key].keys():
            beta_frequency_dict[key][key2] = beta_frequency_dict[key][key2] / count[key]

    return beta_frequency_dict

def create_alpha_dict(labels, tags):
    #create the transition probability dict
    alpha_dict = {}
    for tag in tags:
        alpha_dict[tag] = {}
        for key in tags:
            alpha_dict[tag][key] = 1 # add smoothing, imagine we saw each word once before
            alpha_dict[tag]['.'] = 1

    for i in range(len(labels)):
        for j in range(len(labels[i])):
            if j != len(labels[i]) - 1:
                alpha_dict[labels[i][j][1]][labels[i][j+1][1]] += 1
            else:
                alpha_dict[labels[i][j][1]]['.'] += 1
    return alpha_dict

def create_alpha_frequency_dict(bigram_dict, vocab, tags):
    #create the percentage of the transition probability dict
    bigram_frequency_dict = copy.deepcopy(bigram_dict)
    for key in bigram_frequency_dict.keys():
        for key2 in bigram_frequency_dict[key].keys():
            bigram_frequency_dict[key][key2] = bigram_frequency_dict[key][key2] / sum(bigram_dict[key].values())

    return bigram_frequency_dict

def get_lists(tagged):
    # get list of letters and tags
    vocab = list(set([w for sent in tagged for (w,t) in sent]))
    tags = list(set([t for sent in tagged for (w,t) in sent]))

    return vocab, tags

def get_sets(list1, list2):
    # turn list into set
    sourcevocab = set([w for s in list1 for w in s])
    targetvocab = set([w for s in list2 for w in s])

    return sourcevocab, targetvocab

def create_pi_dict(labels,tags):
    #create start dict
    freq_dict = {}
    words_count = 2
    for tag in tags:
        freq_dict[tag] = 1

    for i in range(len(labels)):
        words_count += 1
        freq_dict[labels[i][0][1]] += 1

    for key in freq_dict.keys():
        freq_dict[key] = freq_dict[key]/ words_count

    return freq_dict

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
    return P_new_BB, P_new_IB, P_new_BI, P_new_II

def generate_new_probs(P_B, P_I, sum_B, sum_I, sum_dictB, sum_dictI, P_new_BB, P_new_IB, P_new_BI, P_new_II,P_start_B_sum, P_start_I_sum, P_end_B_sum,P_end_I_sum,number_of_words, vocab):
    #update probabilities
    start = {'B': P_start_B_sum/number_of_words, 'I': P_start_I_sum/number_of_words}
    trans = {'B': {'B':P_new_BB/sum_B, 'I':P_new_BI/sum_B, '.': P_end_B_sum/sum_B}, 'I': {'B':P_new_IB/sum_I,'I':P_new_II/sum_I,'.':P_end_I_sum/sum_I}}
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

    P_B = []
    P_I = []
    P_new_BB = []
    P_new_IB = []
    P_new_BI = []
    P_new_II = []
    P_start_B = []
    P_start_I = []
    P_end_B = []
    P_end_I = []

    number_of_words = len(words_list)
    for word in words_list:
        Alpha_B, Alpha_I = alpha(word, em, trans, start)
        Beta_B, Beta_I = beta(word, em, trans, start)
        BB = [a*b for a,b in zip(Alpha_B,Beta_B)]
        II = [a*b for a,b in zip(Alpha_I,Beta_I)]
        addition = [sum(x) for x in zip(BB, II)]
        current_PB = [a/b for a,b in zip(BB,addition)]
        current_PI = [a/b for a,b in zip(II,addition)]
        P_BB, P_IB, P_BI, P_II = new_p(word, em, trans, Alpha_B, Alpha_I, Beta_B, Beta_I, addition)
        P_new_BB.append(P_BB)
        P_new_IB.append(P_IB)
        P_new_BI.append(P_BI)
        P_new_II.append(P_II)
        P_B.append(current_PB)
        P_I.append(current_PI)
        P_start_B.append(current_PB[0])
        P_start_I.append(current_PI[0])
        P_end_B.append(current_PB[-1])
        P_end_I.append(current_PI[-1])

        for i in range(len(word)):
            sum_dictB[word[i]] += current_PB[i]
            sum_dictI[word[i]] += current_PI[i]
    sum_B = sum([sum(x) for x in P_B])
    sum_I = sum([sum(x) for x in P_I])
    P_new_BB_sum = sum([sum(x) for x in P_new_BB])
    P_new_IB_sum = sum([sum(x) for x in P_new_IB])
    P_new_BI_sum = sum([sum(x) for x in P_new_BI])
    P_new_II_sum = sum([sum(x) for x in P_new_II])
    P_start_B_sum = sum(P_start_B)
    P_start_I_sum = sum(P_start_I)
    P_end_B_sum = sum(P_end_B)
    P_end_I_sum = sum(P_end_I)

    new_start, new_em, new_trans = generate_new_probs(P_B, P_I, sum_B, sum_I,
                                                      sum_dictB, sum_dictI, P_new_BB_sum,
                                                      P_new_IB_sum, P_new_BI_sum, P_new_II_sum,
                                                      P_start_B_sum, P_start_I_sum, P_end_B_sum,P_end_I_sum,
                                                      number_of_words,vocab)

    return new_start, new_em, new_trans

if __name__ == "__main__":
    file_name = 'train.tsv'

    words, words_no, labels = load_dataset(file_name)

    training_labels = labels[:10000]

    tagged_training_letters = tag_words(training_labels)

    tagged_letters = tag_words(labels)

    vocab, tags = get_lists(tagged_letters)

    vocabset, tagsset = get_sets(vocab, tags)

    alpha_dict = create_alpha_dict(tagged_training_letters,tagsset)

    transition_frequency_dict = create_alpha_frequency_dict(alpha_dict,vocab,tags)

    beta_dict = create_beta_dict(tagged_training_letters, vocab, tags)

    emmision_frequency_dict = create_beta_frequency_dict(beta_dict,vocab,tags)

    start_freq_dict = create_pi_dict(tagged_training_letters,tags)

    x_train, x_dev = words_no[:11000], words[11000:]

    x_train_list = []
    for word in x_train:
        x_train_list.append(list(word))

    # x_train_list = [[2,3,3,2,3,2,3,2,2,3,1,3,3,1,1,1,2,1,1,1,3,1,2,1,1,1,2,3,3,2,3,2,2]]
    # x_train_list = [[2,3,3,2,3,2,3,2,2,3,2,3,3,2,2],[1,2,1,1,1,3,1,2,1,1,1,2,3,3,2,3,2,2], [2,3,3,2,3,2,3,2,2,3,2,3,3,2,2]]
    # start_freq_dict = {'B': 0.5, 'I':0.5}
    # emmision_frequency_dict = {'B': {1:0.7, 2:0.2, 3: 0.1}, 'I': {1:0.1,2:0.2,3:0.7}}
    # transition_frequency_dict = {'B': {'B':0.8, 'I':0.1, '.': 0.1}, 'I': {'B':0.1,'I':0.8,'.':0.1}}
    # vocab = [1,2,3]

    for i in range(1):
        start_freq_dict, emmision_frequency_dict, transition_frequency_dict = fwd_bck(x_train_list, emmision_frequency_dict, transition_frequency_dict, start_freq_dict, vocab)


    # training_accuracy = evaluate(x_train, y_train, tags_frequency_dict, bigram_frequency_dict, sentence_freq_dict)
    # dev_accuracy = evaluate(x_dev, y_dev, tags_frequency_dict, bigram_frequency_dict, sentence_freq_dict)




