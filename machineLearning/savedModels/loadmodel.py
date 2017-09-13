from __future__ import division
import sys
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

mdl = load_model(str(sys.argv[1]))

seed = 9
np.random.seed(seed)
# load readscsv data
dataframe = pd.read_csv(str(sys.argv[2]), delimiter=",")
dataset = dataframe.values
# split into input (X) and output (Y) variables
seqs = dataset[:,0]
reads = dataset[:,1]
seqs = [str(int(seq)) for seq in seqs]
#pad seqs to be same len
max_length = 0
for seq in seqs:
    if len(seq) > max_length:
        max_length = len(seq)

#max_length = max_length + (3-(max_length%3))

for i,seq in enumerate(seqs):
    diff = max_length - len(seq)
    padded_sequence = seq + diff*'0'
    padded_sequence_list = list(padded_sequence)
    padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
    seqs[i] = [padded_sequence_list_ints]


#split into test and trian data
(seqstrain, seqstest, readstrain, readstest) = train_test_split(seqs, reads, test_size=0.20, random_state=seed)

predicted = mdl.predict(seqstest)

error = [abs(predicted[i]-readstest[i])*100 for i in range(int(sys.argv[3]))]
print("average error per prediction")
print(sum(error)/int(sys.argv[3]))
#plotting
fig = plt.figure()

ax1 = fig.add_subplot(121)
ax1.plot(predicted[1:int(sys.argv[3])],'--')
ax1.plot(readstest[1:int(sys.argv[3])],'--')
ax1.legend(["prediction", "Test"])

ax2 = fig.add_subplot(122)
ax2.plot(error, '--')
ax2.legend(["predictions-results"])

plt.show()
#plt.savefig(str(sys.argv[3]))
