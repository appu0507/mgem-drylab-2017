import os
import random
# Formerly named replace.py
'''
This program takes in a aptamer and outputs an a apter with a randomly replaced site
Input: aptamer 
Output: new substituted aptamer 
''' 

#function to replace a random site

#returns sequence with random site substituted (string) 
def mutate(input_sequence, mutation_probability = 0.02):
    if random.random() <= mutation_probability:
        site = random.randint(0, len(input_sequence)-1)
        s = list(input_sequence)
        noA = ['G', 'C', 'T']
        noG = ['A', 'C', 'T']
        noC = ['A', 'T', 'G']
        noT = ['A', 'G', 'C']
        if s[site] == 'A':
            s[site] = random.choice(noA)
        elif s[site] == 'G':
            s[site] = random.choice(noG)
        elif s[site] == 'C':
            s[site] = random.choice(noC)
        elif s[site] == 'T':
            s[site] = random.choice(noT)
        else:
            raise ValueError('Not a valid base')
        return "".join(s) 
    else:
        return input_sequence
#
#      choose = random.randint(1,3)
#      if s[site]== 'A': 
#         if choose == 1:
#            s[site]='T'
#         elif choose == 2:
#            s[site]='G'
#         elif choose == 3: 
#            s[site]='C'
#      elif s[site]== 'T': 
#         if choose == 1:
#            s[site]='A'
#         elif choose == 2:
#            s[site]='G'
#         elif choose == 3: 
#            s[site]='C'
#      elif s[site]== 'C': 
#         if choose == 1:
#            s[site]='A'
#         elif choose == 2:
#            s[site]='G'
#         elif choose == 3: 
#            s[site]='T'
#      elif s[site]== 'G': 
#         if choose == 1:
#            s[site]='A'
#         elif choose == 2:
#            s[site]='T'
#         elif choose == 3: 
#            s[site]='C'
