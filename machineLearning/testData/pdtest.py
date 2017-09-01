#!/bin/python
import sys
import numpy as np
import pandas as pd
# load readscsv data
dataframe = pd.read_csv(str(sys.argv[1]), delimiter=",")
dataset = dataframe.values
# split into input (X) and output (Y) variables
seqs = dataset[:,0]
reads = dataset[:,1]
seqs = [str(int(s)) for s in seqs]

print(seqs)
print("seqs len:" + str(len(seqs)))
print("reads len:" + str(len(reads)))

#pad seqs to be same len
max_length = 0
for seq in seqs:
    if len(seq) > max_length:
        max_length = len(seq)

#max_length = max_length + (3-(max_length%3))
print("maxlen is:" + str(max_length))

for i,seq in enumerate(seqs):
    diff = max_length - len(seq)
    padded_sequence = seq + diff*'0'
    padded_sequence_list = list(padded_sequence)
    padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
    seqs[i] = [padded_sequence_list_ints]

print(seqs[1:10])
