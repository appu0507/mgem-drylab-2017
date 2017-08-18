#!/usr/bin/python3

import numpy as np
import csv
import gc

def import_data(fname):

  sequences = []
  sizes = []

  with open(fname,'rt') as f:
    datareader = csv.reader(f,delimiter=',')
 
    for row in datareader:
      sizes.append(row[0])
      sequences.append(row[1])
    
    f.close()
  
  return sequences,sizes

def pad_sequences(sequences):
  print('Starting to pad!')
  max_length = 0
  for seq in sequences:
    if len(seq) > max_length:
      max_length = len(seq)

  padded_sequences = []
  for i,seq in enumerate(sequences):
    diff = max_length - len(seq)

    padded_sequence = seq + diff*'0'
    padded_sequence_list = list(padded_sequence)
    padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]

    padded_sequences.append(list(padded_sequence_list_ints))

  sequences = None
  print('Threw out raw sequences')

  X = np.memmap('X.txt'padded_sequences)

  return X

def training_output(sizes):
  sizes = [ int(x) for x in sizes ]
  y = []
  max_size = float(max(sizes))
  for i,size in enumerate(sizes):
    if size != sizes[i - 1]:
      y.append(float(size)/max_size)
    else:
      y.append(y[-1])

  y = np.vstack(np.array(y))

  return y

def nonlin(x,deriv=False):
  if(deriv==True):
    return x*(1-x)
  return 1/(1+np.exp(-x))


sequences, sizes = import_data('ALS_round_12_dereplicated_Binary.csv')

X = pad_sequences(sequences)
y = training_output(sizes)

#X = np.array([[0,0,1],
#              [0,1,1],
#              [1,0,1],
#              [1,1,1]])
                
#y = np.array([[0],
#              [1],
#              [1],
#              [0]])

np.random.seed(1)

syn0 = 2*np.random.random((len(X[0]),len(X))) - 1
syn1 = 2*np.random.random((len(y),1)) - 1

for j in range(60000):
  print(j)
  l0 = X
  l1 = nonlin(np.dot(l0,syn0))
  l2 = nonlin(np.dot(l1,syn1))

  l2_error = y - l2
    
  if (j% 10000) == 0:
      print("Error:" + str(np.mean(np.abs(l2_error))))
        
  l2_delta = l2_error*nonlin(l2,deriv=True)

  l1_error = l2_delta.dot(syn1.T)
    
  l1_delta = l1_error * nonlin(l1,deriv=True)

  syn1 += l1.T.dot(l2_delta)
  syn0 += l0.T.dot(l1_delta)

print(l2)
