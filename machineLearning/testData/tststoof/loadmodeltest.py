import tensorflow
from keras.models import load_model
import sys
import numpy as np
import pandas as pd


#tmp = [1 if bp == 'A' else bp for bp in seq ]
#tmp = [2 if bp == 'C' else bp for bp in tmp ]
#tmp = [3 if bp == 'G' else bp for bp in tmp ]
#tmp = [4 if bp == 'T' else bp for bp in tmp ]
#tmp = ''.join(str(e) for e in tmp)
#df = pd.DataFrame()
#df.set_value(0,0,tmp)
#seqs = df.values
#seqs = [str(int(seq)) for seq in seqs[:,0]]
#
#max_length = 286 #this was the max length from training 
#
#for i,seq in enumerate(seqs):
#    diff = max_length - len(seq)
#    padded_sequence = seq + diff*'0'
#    padded_sequence_list = list(padded_sequence)
#    padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
#    seqs[i] = [padded_sequence_list_ints]
#
#
#rez = model.predict(np.array(seqs))
#
#print(rez)

model = load_model(str(sys.argv[1]))

seq = 'GGGGGGGTTTCGTAGCGATCGATACTTCGCATTATATAGCTATCCTCGCATAGTCGACGACGATCGACGTACGTACGTACGTACGTCAGATGCTACTACGTACGATCGATCGCTAGCTGCTAGCGCACGATGCTACACATGTCGAATGCCCGATATCGATCATTACGATCG'

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

    max_length = 286 #this was the max length from training 

    for i,seq in enumerate(seqs):
        diff = max_length - len(seq)
        padded_sequence = seq + diff*'0'
        padded_sequence_list = list(padded_sequence)
        padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
        seqs[i] = [padded_sequence_list_ints]

    return float(mdl.predict(np.array(seqs)))

rez = getFitness(seq, model)
print(rez)







