#!/bin/python
import sys
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
# load readscsv data
dataframe = pd.read_csv(str(sys.argv[1]), delimiter=",", header=1)
dataset = dataframe.values
# split into input (X) and output (Y) variables
seqs = dataset[:,0]
reads = dataset[:,1]
print seqs 
print reads
