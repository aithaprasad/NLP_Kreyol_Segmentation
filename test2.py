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
            beta_dict[tag][key] = 0
    for i in range(len(tagged_letters)):
        for j in range(len(tagged_letters[i])):
                    beta_dict[tagged_letters[i][j][1]][tagged_letters[i][j][0]] += 1

    return beta_dict

def create_beta_frequency_dict(beta_dict):
    beta_frequency_dict = copy.deepcopy(beta_dict)
    for key in beta_frequency_dict.keys():
        count = 0
        for key2 in beta_frequency_dict[key].keys():
            count += beta_frequency_dict[key][key2]
        for key3 in beta_frequency_dict[key].keys():
            beta_frequency_dict[key][key3] = beta_frequency_dict[key][key3] / count

    return beta_frequency_dict

def create_alpha_dict(labels, tags):
    alpha_dict = {}
    for tag in tags:
        alpha_dict[tag] = {}
        for key in tags:
            alpha_dict[tag][key] = 0
            alpha_dict[tag]['.'] = 0

    for i in range(len(labels)):
        for j in range(len(labels[i])-1):
            if j != len(labels[i]) - 2:
                alpha_dict[labels[i][j][1]][labels[i][j+1][1]] += 1
            else:
                alpha_dict[labels[i][j][1]]['.'] += 1

    return alpha_dict

def create_alpha_frequency_dict(bigram_dict):
    bigram_frequency_dict = copy.deepcopy(bigram_dict)
    for key in bigram_frequency_dict.keys():
        count = 0
        for key2 in bigram_frequency_dict[key].keys():
            count += bigram_frequency_dict[key][key2]
        for key3 in bigram_frequency_dict[key].keys():
            bigram_frequency_dict[key][key3] = bigram_frequency_dict[key][key3] / count

    return bigram_frequency_dict

def get_lists(tagged):
    vocab = list(set([w for sent in tagged for (w,t) in sent]))
    tags = list(set([t for sent in tagged for (w,t) in sent]))

    return vocab, tags

def get_sets(list1, list2):
    sourcevocab = set([w for s in vocab for w in s])
    targetvocab = set([w for s in tags for w in s])

    return sourcevocab, targetvocab

def create_pi_dict(labels,tags):
    freq_dict = {}
    words_count = 0
    for tag in tags:
        freq_dict[tag] = 0

    for i in range(len(labels)):
        words_count += 1
        freq_dict[labels[i][0][1]] += 1

    for key in freq_dict.keys():
        freq_dict[key] = freq_dict[key]/ words_count

    return freq_dict

def predict_from_scratch(sentence, labels, frequency_dict, bigram_dict, sentence_dict):
    tags = viterbi(sentence, labels, frequency_dict, bigram_dict, sentence_dict)
    return tags

def viterbi(words, tags, frequency_dict, bigram_dict, sentence_dict):
    V = {}
    B = {}
    tag_list = sentence_dict.keys()
    tag_dict = dict.fromkeys(sentence_freq_dict.keys())
    V[0] = copy.deepcopy(tag_dict)
    for t in tag_list:
        try:
            V[0][t] = sentence_dict[t]*frequency_dict[words[0]].get(t,0)
        except:
            V[0][t] = 0
    for i in range(1,len(words)):
        V[i] = copy.deepcopy(tag_dict)
        B[i] = copy.deepcopy(tag_dict)
        for t in tag_list:
            pair = argmax(V,tag_list,t,i, bigram_dict)
            B[i][t] = pair[0]
            try:
                V[i][t] = pair[1]*frequency_dict[words[i]].get(t,0)
            except:
                V[i][t] = 0
    final_labels = get_best_tag(words, V, B, tag_list)
    return final_labels

def argmax(V,tag_list,t,i, bigram_dict):
    ans=-1
    best=None
    for s in tag_list:
        temp=V[i-1][s]*bigram_dict[t][s]
        if temp > ans:
            ans = temp
            best = s
    return (best,ans)

def get_best_tag(sent, V,B, tags):
    best_ending = None
    best_max = -1

    for tag in tags:
        if V[len(sent) - 1][tag] > best_max:
            best_max = V[len(sent) - 1][tag]
            best_ending = tag
    seq = [best_ending]

    for i in reversed(range(1, len(sent))):
        seq.append(B[i][seq[-1]])
    #print(len(seq), len(sent))
    return seq[::-1]


def evaluate(words, tags, frequency_dict, bigram_dict, sentence_dict):
    sentence = []
    labels = []
    final_tags = []
    correct = 0
    num = 0
    for i in range(len(words)):
      if words[i]=='<S>':
        num+=1
        final_tags.append(predict_from_scratch(sentence, labels, frequency_dict, bigram_dict, sentence_dict))
        final_tags.append('N')
        sentence = []
        labels = []
      else:
        sentence.append(words[i])
        labels.append(tags[i])
    final_tag = [j for i in final_tags for j in i]
    print(final_tag)
    for i in range(len(tags)):
        if final_tag[i] == tags[i]:
            correct += 1
    accuracy = correct / len(tags)
    return accuracy

def fwd_bkw(observations, states, start_prob, trans_prob, emm_prob, end_st):
    """Forward–backward algorithm."""
    # Forward part of the algorithm
    fwd = []
    for i, observation_i in enumerate(observations):
        f_curr = {}
        for st in states:
            if i == 0:
                # base case for the forward part
                prev_f_sum = start_prob[st]
            else:
                prev_f_sum = sum(f_prev[k] * trans_prob[k][st] for k in states)

            f_curr[st] = emm_prob[st][observation_i] * prev_f_sum

        fwd.append(f_curr)
        f_prev = f_curr

    p_fwd = sum(f_curr[k] * trans_prob[k][end_st] for k in states)

    # Backward part of the algorithm
    bkw = []
    for i, observation_i_plus in enumerate(reversed(observations[1:] + (None,))):
        b_curr = {}
        for st in states:
            if i == 0:
                # base case for backward part
                b_curr[st] = trans_prob[st][end_st]
            else:
                b_curr[st] = sum(trans_prob[st][l] * emm_prob[l][observation_i_plus] * b_prev[l] for l in states)

        bkw.insert(0,b_curr)
        b_prev = b_curr

    p_bkw = sum(start_prob[l] * emm_prob[l][observations[0]] * b_curr[l] for l in states)

    # Merging the two parts
    posterior = []
    for i in range(len(observations)):
        posterior.append({st: fwd[i][st] * bkw[i][st] / p_fwd for st in states})

    assert p_fwd == p_bkw
    return fwd, bkw, posterior

def example():
    return fwd_bkw(vocabtuple,
                   tagsset,
                   pi_freq_dict,
                   alpha_frequency_dict,
                   beta_frequency_dict,
                   end_state)

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

    alpha_frequency_dict = create_alpha_frequency_dict(alpha_dict)

    beta_dict = create_beta_dict(tagged_training_letters, vocab, tags)

    beta_frequency_dict = create_beta_frequency_dict(beta_dict)

    pi_freq_dict = create_pi_dict(tagged_training_letters,tags)
    
    end_state = '.'
    
    mm = example()
    
    for line in mm:
        print(*line)
    
    

    # training_accuracy = evaluate(x_train, y_train, tags_frequency_dict, bigram_frequency_dict, sentence_freq_dict)
    # dev_accuracy = evaluate(x_dev, y_dev, tags_frequency_dict, bigram_frequency_dict, sentence_freq_dict)




