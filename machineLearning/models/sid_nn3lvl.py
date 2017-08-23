#!/usr/bin/python3
import sys, csv, gc
import numpy as np

def import_data(fname):
  sequences = []
  fitness = []
  with open(fname,'rt') as f:
    datareader = csv.reader(f,delimiter=',')
    for row in datareader:
      fitness.append(row[0])
      sequences.append(row[1])
    f.close()
  return sequences,fitness

def pad_sequences(sequences):
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
  X = np.array(padded_sequences)
  padded_sequences = None
  return X

def training_output(fitness):
  fitness = [ float(x) for x in fitness ]
  y = np.vstack(np.array(fitness))
  return y

def nonlin(x,deriv=False):
  if(deriv==True):
    return x*(1-x)
  return 1/(1+np.exp(-x))


sequences, fitness = import_data(str(sys.argv[1]))

X = pad_sequences(sequences)
y = training_output(fitness)

print(y)

sequences = None
fitness = None

#X = np.array([[0,0,1],
#              [0,1,1],
#              [1,0,1],
#              [1,1,1]])
                
#y = np.array([[0],
#              [1],
#              [1],
#              [0]])

np.random.seed(1)


syn_per_neuron = len(X[0])
n_neurons = 50


syn0 = 2*np.random.random((syn_per_neuron,n_neurons)) - 1
syn1 = 2*np.random.random((n_neurons,1)) - 1

for j in range(int(sys.argv[2])):
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
