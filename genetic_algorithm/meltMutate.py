import os
import random
import meltAptamerBreeder as ab
# Formerly named replace.py
'''
This program takes in a aptamer and outputs an a apter with a randomly replaced site
Input: aptamer 
Output: new substituted aptamer 
''' 

#function to replace a random site

#returns sequence with random site substituted 
# input is in the format of ['offspring', 'asdsadsas' 56]
def mutate(aptamer, mdl, mutation_probability = 0.02):
    input_sequence = aptamer[1]
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
        return [aptamer[0], "".join(s), ab.getFitness("".join(s), mdl)] 
    else:
        return aptamer
