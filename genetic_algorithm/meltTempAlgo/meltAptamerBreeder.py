from __future__ import division
from random import randint, choice
from numpy import mean
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers.recurrent import LSTM
from sklearn.model_selection import train_test_split



def readMeltCSV(readfile):
    with open(readfile,"r") as input_sequences:
        sequences = input_sequences.readlines()
        aptamers = []
        for i in range(0,len(sequences)-1):
            tmp = sequences[i].split(',')
            aptamers.append(["Sequence"+str(i), str(tmp[0]), float(tmp[1])])
    return aptamers





def getFitness(seqi, mdl):
    tmp = [1 if bp == 'A' else bp for bp in seqi ]
    tmp = [2 if bp == 'C' else bp for bp in tmp ]
    tmp = [3 if bp == 'G' else bp for bp in tmp ]
    tmp = [4 if bp == 'T' else bp for bp in tmp ]
    tmp = ''.join(str(e) for e in tmp)
    df = pd.DataFrame()
    df.set_value(0,0,tmp)
    seqs = df.values
    seqs = [str(int(seq)) for seq in seqs[:,0]]
    max_length = 30#this was the max length from training 30

    for i,seq in enumerate(seqs):
        diff = max_length - len(seq)
        padded_sequence = seq + diff*'0'
        padded_sequence_list = list(padded_sequence)
        padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
        seqs[i] = [padded_sequence_list_ints]
    return float(mdl.predict(np.array(seqs)))






def crossover(parent1, parent2, idnum, gennum, mdl):
    max_pos = min([len(parent1), len(parent2)])   
    crossOverPos = randint(1,max_pos-2) # random nucleotide postion along the max_pos bp aptamer, except not the 
    if crossOverPos%2 == 0:
        # if crossOverpos is even, first half of the child is from parent1, if not first half of child is from parent2
        childseq = parent1[1][:crossOverPos] + parent2[1][crossOverPos:]
        child = ["gen_" + str(gennum) + "_offspring_" + str(idnum), childseq, getFitness(childseq, mdl)]
    else:
        childseq = parent2[1][:crossOverPos] + parent1[1][crossOverPos:]
        child = ["gen_" + str(gennum) + "_offspring_" + str(idnum), childseq, getFitness(childseq, mdl)]
    return child
#   if crossOverPos == 0:
#      # just returns parent 1 since not acutally a crossover
#      child = ["offspring_" + str(i), sortedAptamerList[parent1][1], computeChildFitness(parent1)]
#   elif crossOverPos == max_pos-1:
#      child = ["offspring_" + str(i), sortedAptamerList[parent2][1], computeChildFitness(parent2)]
#   else:



#aptamer list format: [['aptamer_1, 'asdasdasdasd', 45], ['aptamer_2', 'asdasasdasd', 78]]
#the two highest scoring aptamers are randomly crossed over to generate a specified number of offspring
#assumed all aptamers are the same length
def breed(aptamers, gennum, mdl, top_cutoff=0.10):
    # sortedAptamerList should already be sorted but just because im paranoid im going to sort it again
    sortedAptamerList = sorted(aptamers, key=lambda x: x[2], reverse=True) 
    # list initialization
    bred_aptamers = []
    #elites is top 2%
    for elite in range(0, int(len(sortedAptamerList)*0.02)):
        bred_aptamers.append(sortedAptamerList[elite])
    # creates a list of the top 10% of of the sortedAptamerList based on fitness score
    top_parents = sortedAptamerList[:int(len(sortedAptamerList)*0.10)]
    # crossover parents randomly untill you get to population size
    for child in range(len(sortedAptamerList) - int(len(sortedAptamerList)*0.02)):
        bred_aptamers.append(crossover(choice(top_parents), choice(top_parents), child, gennum, mdl))
    return bred_aptamers
