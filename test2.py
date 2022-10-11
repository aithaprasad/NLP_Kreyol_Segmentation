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

def load_dataset(name):
        with open(name, encoding="utf-8") as file:
          f = csv.reader(file, delimiter="\t")
          word = []
          labels = []
          for line in f:
            line[0] += ('.')
            word.append(line[0])
            labels.append(line[1])

        return word, labels


def tag_words(labels):
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
    beta_dict = {}
    for tag in tags:
        beta_dict[tag] = {}
        for key in vocab:
            beta_dict[tag][key] = 1
    for i in range(len(tagged_letters)):
        for j in range(len(tagged_letters[i])):
                    beta_dict[tagged_letters[i][j][1]][tagged_letters[i][j][0]] += 1

    return beta_dict

def create_beta_frequency_dict(beta_dict,vocab,tags):
    count = {}
    for tag in tags:
        count[tag] = 0
        for letter in vocab:
            count[tag] += beta_dict[tag][letter]
    print(count)

    beta_frequency_dict = copy.deepcopy(beta_dict)
    for key in beta_frequency_dict.keys():
        for key2 in beta_frequency_dict[key].keys():
            beta_frequency_dict[key][key2] = beta_frequency_dict[key][key2] / count[key]

    return beta_frequency_dict

def create_alpha_dict(labels, tags):
    alpha_dict = {}
    for tag in tags:
        alpha_dict[tag] = {}
        for key in tags:
            alpha_dict[tag][key] = 1
            alpha_dict[tag]['.'] = 1

    for i in range(len(labels)):
        for j in range(len(labels[i])-1):
            if j != len(labels[i]) - 2:
                alpha_dict[labels[i][j][1]][labels[i][j+1][1]] += 1
            else:
                alpha_dict[labels[i][j][1]]['.'] += 1

    return alpha_dict

def create_alpha_frequency_dict(bigram_dict, vocab, tags):
    count = {}
    for tag in tags:
        count[tag] = 0
        for tag2 in tags:
            count[tag] += bigram_dict[tag][tag2]

    count['B'] += bigram_dict['B']['.']
    count['I'] += bigram_dict['I']['.']
    print(count)
    bigram_frequency_dict = copy.deepcopy(bigram_dict)
    for key in bigram_frequency_dict.keys():
        for key2 in bigram_frequency_dict[key].keys():
            bigram_frequency_dict[key][key2] = bigram_frequency_dict[key][key2] / count[key]

    return bigram_frequency_dict

def get_lists(tagged):
    vocab = list(set([w for sent in tagged for (w,t) in sent]))
    tags = list(set([t for sent in tagged for (w,t) in sent]))

    return vocab, tags

def get_sets(list1, list2):
    sourcevocab = set([w for s in list1 for w in s])
    targetvocab = set([w for s in list2 for w in s])

    return sourcevocab, targetvocab

def create_pi_dict(labels,tags):
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

def alpha(word, em, trans, start):
    print(word)
    for letter in word:
        print(letter)
    return

if __name__ == "__main__":
    file_name = 'train.tsv'

    words, labels = load_dataset(file_name)

    training_labels = labels[:650]

    tagged_training_letters = tag_words(training_labels)

    tagged_letters = tag_words(labels)

    vocab, tags = get_lists(tagged_letters)

    vocabset, tagsset = get_sets(vocab, tags)

    vocabtuple, tagstuple = tuple(vocab), tuple(tags)

    alpha_dict = create_alpha_dict(tagged_training_letters,tagsset)

    transition_frequency_dict = create_alpha_frequency_dict(alpha_dict,vocab,tags)

    beta_dict = create_beta_dict(tagged_training_letters, vocab, tags)

    emmision_frequency_dict = create_beta_frequency_dict(beta_dict,vocab,tags)

    start_freq_dict = create_pi_dict(tagged_training_letters,tags)

    end_state = '.'

    alpha(words[0], emmision_frequency_dict, transition_frequency_dict, start_freq_dict)




    # training_accuracy = evaluate(x_train, y_train, tags_frequency_dict, bigram_frequency_dict, sentence_freq_dict)
    # dev_accuracy = evaluate(x_dev, y_dev, tags_frequency_dict, bigram_frequency_dict, sentence_freq_dict)




