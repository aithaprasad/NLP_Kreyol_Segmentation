# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:16:32 2022

@author: omars
"""

def alpha(words, em, trans, start):
    C_list = []
    H_list = []

    C_list.append(start['C']*em['C'][words[0]])
    H_list.append(start['H']*em['H'][words[0]])

    for i in range(1,len(words)):
        C_list.append(C_list[i-1]*trans['C']['C']*em['C'][words[i]]+H_list[i-1]*trans['C']['H']*em['C'][words[i]])
        H_list.append(H_list[i-1]*trans['H']['H']*em['H'][words[i]]+C_list[i-1]*trans['H']['C']*em['H'][words[i]])


def beta(words, em, trans, start):
    words.reverse()
    C_list = []
    H_list = []

    C_list.append(trans['C']['.'])
    H_list.append(trans['H']['.'])
    for i in range(1,len(words)):
        C_list.append(C_list[i-1]*trans['C']['C']*em['C'][words[i-1]]+H_list[i-1]*trans['C']['H']*em['H'][words[i-1]])
        H_list.append(H_list[i-1]*trans['H']['H']*em['H'][words[i-1]]+C_list[i-1]*trans['H']['C']*em['C'][words[i-1]])

    return




if __name__ == "__main__":
    start = {'C': 0.5, 'H':0.5}
    em = {'C': {1:0.7, 2:0.2, 3: 0.1}, 'H': {1:0.1,2:0.2,3:0.7}}
    trans = {'C': {'C':0.8, 'H':0.1, '.': 0.1}, 'H': {'C':0.1,'H':0.8,'.':0.1}}

    seq = [2,3,3,2,3,2,3,2,2,3,1,3,3,1,1,1,2,1,1,1,3,1,2,1,1,1,2,3,3,2,3,2,2]

    alpha(seq, em, trans, start)
    beta(seq, em, trans, start)