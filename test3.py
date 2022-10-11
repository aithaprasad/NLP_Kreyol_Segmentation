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

    return C_list, H_list


def beta(words, em, trans, start):
    words.reverse()
    C_list = []
    H_list = []

    C_list.append(trans['C']['.'])
    H_list.append(trans['H']['.'])
    for i in range(1,len(words)):
        C_list.append(C_list[i-1]*trans['C']['C']*em['C'][words[i-1]]+H_list[i-1]*trans['C']['H']*em['H'][words[i-1]])
        H_list.append(H_list[i-1]*trans['H']['H']*em['H'][words[i-1]]+C_list[i-1]*trans['H']['C']*em['C'][words[i-1]])

    C_list.reverse()
    H_list.reverse()

    return C_list, H_list

if __name__ == "__main__":
    start = {'C': 0.5, 'H':0.5}
    em = {'C': {1:0.7, 2:0.2, 3: 0.1}, 'H': {1:0.1,2:0.2,3:0.7}}
    trans = {'C': {'C':0.8, 'H':0.1, '.': 0.1}, 'H': {'C':0.1,'H':0.8,'.':0.1}}

    seq = [2,3,3,2,3,2,3,2,2,3,1,3,3,1,1,1,2,1,1,1,3,1,2,1,1,1,2,3,3,2,3,2,2]

    Alpha_C, Alpha_H = alpha(seq, em, trans, start)
    Beta_C, Beta_H = beta(seq, em, trans, start)
    CC = [a*b for a,b in zip(Alpha_C,Beta_C)]
    HH = [a*b for a,b in zip(Alpha_H,Beta_H)]
    addition = [sum(x) for x in zip(CC, HH)]
    P_C = [a/b for a,b in zip(CC,addition)]
    P_H = [a/b for a,b in zip(HH,addition)]

    seq.reverse()

    P_C1 = []
    P_C2 = []
    P_C3 = []
    P_H1 = []
    P_H2 = []
    P_H3 = []
    print(seq)
    for i in range(len(seq)):
        if seq[i] == 1:
            P_C1.append(P_C[i])
            P_C2.append(0)
            P_C3.append(0)
            P_H1.append(P_H[i])
            P_H2.append(0)
            P_H3.append(0)
        elif seq[i] == 2:
            P_C1.append(0)
            P_C2.append(P_C[i])
            P_C3.append(0)
            P_H1.append(0)
            P_H2.append(P_H[i])
            P_H3.append(0)
        elif seq[i] == 3:
            P_C1.append(0)
            P_C2.append(0)
            P_C3.append(P_C[i])
            P_H1.append(0)
            P_H2.append(0)
            P_H3.append(P_H[i])

    sum_C = sum(P_C)
    sum_H = sum(P_H)
    sum_C1 = sum(P_C1)
    sum_C2 = sum(P_C2)
    sum_C3 = sum(P_C3)
    sum_H1 = sum(P_H1)
    sum_H2 = sum(P_H2)
    sum_H3 = sum(P_H3)






