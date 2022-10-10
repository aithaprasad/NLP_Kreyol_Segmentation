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

def create_hmm_dict(tagged_letters):
    tags = {}
    count_dict = {}
    for i in range(len(tagged_letters)):
        for j in range(len(tagged_letters[i])):
            if tagged_letters[i][j][0] in tags.keys():
                if tagged_letters[i][j][1] in tags[tagged_letters[i][j][0]].keys():
                    tags[tagged_letters[i][j][0]][tagged_letters[i][j][1]] += 1
                else:
                    tags[tagged_letters[i][j][0]][tagged_letters[i][j][1]] = 1
            else:
                tags[tagged_letters[i][j][0]] = {}
                tags[tagged_letters[i][j][0]][tagged_letters[i][j][1]] = 1
            if tagged_letters[i][j][1] in count_dict.keys():
                count_dict[tagged_letters[i][j][1]] += 1
            else:
                count_dict[tagged_letters[i][j][1]] = 1

    return tags, count_dict

def create_frequency_dict(tags_dict, count_dict):
    tags_frequency_dict = copy.deepcopy(tags_dict)
    for key in tags_frequency_dict.keys():
        for key2 in tags_frequency_dict[key].keys():
            tags_frequency_dict[key][key2] = tags_frequency_dict[key][key2]/ count_dict[key2]

    return tags_frequency_dict, count_dict

def create_cobigram_dict(labels):
    bigram_dict = {}
    for i in range(len(labels)):
        for j in range(len(labels[i])-1):
            if labels[i][j][1] in bigram_dict.keys():
                if labels[i][j+1][1] in bigram_dict[labels[i][j][1]].keys():
                    bigram_dict[labels[i][j][1]][labels[i][j+1][1]] += 1
                else:
                    bigram_dict[labels[i][j][1]][labels[i][j+1][1]] = 1
            else:
                bigram_dict[labels[i][j][1]] = {}
                bigram_dict[labels[i][j][1]][labels[i][j+1][1]] = 1

    return bigram_dict

def create_bigram_frequency_dict(bigram_dict):
    bigram_frequency_dict = copy.deepcopy(bigram_dict)
    for key in bigram_frequency_dict.keys():
        for key2 in bigram_frequency_dict[key].keys():
            bigram_frequency_dict[key][key2] = bigram_frequency_dict[key][key2]/ count_dict[key]

    return bigram_frequency_dict



if __name__ == "__main__":
    file_name = 'train.tsv'
    
    words, labels = load_dataset(file_name)
    
    training_labels = labels[:650]
    
    tagged_training_letters = tag_words(training_labels)
    
    tags_dict, count_dict = create_hmm_dict(tagged_training_letters)
    
    tags_frequency_dict, count_dict = create_frequency_dict(tags_dict, count_dict)
    
    bigram_dict = create_cobigram_dict(tagged_training_letters)

    bigram_frequency_dict = create_bigram_frequency_dict(bigram_dict)
    
    
    
    
    
    