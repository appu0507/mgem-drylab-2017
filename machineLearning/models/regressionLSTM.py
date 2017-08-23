import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM 
import matplotlib.pylab as plt
# fix random seed for reproducibility
seed = 9
np.random.seed(seed)
# load readscsv data
dataframe = pd.read_csv(str(sys.argv[1]), delimiter=",", header=1)
dataset = dataframe.values
# split into input (X) and output (Y) variables
seqs = dataset[:,0]
reads = dataset[:,1]
#pad seqs to be same len
max_length = 0
for seq in sequences:
    if len(seq) > max_length:
        max_length = len(seq)

for i,seq in enumerate(seqs):
    diff = max_length - len(seq)
    padded_sequence = seq + diff*'0'
    padded_sequence_list = list(padded_sequence)
    padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
    seqs[i,0] = padded_sequence_list_ints

#split into test and trian data
(seqstrain, seqstest, readstrain, readstest) = train_test_split(seqs, reads, test_size=0.33, random_state=seed)
#neruon dimensions

#creating model
model = Sequential()  
model.add(LSTM(max_length, 30, return_sequences=True))  
model.add(LSTM(30, 50, return_sequences=True))  
model.add(LSTM(50, 20, return_sequences=False))  
model.add(Dense(20, 1))  
model.add(Activation("linear"))  
model.compile(loss="mean_squared_error", optimizer="rmsprop")
# fit the model
model.fit(seqstrain, readstrain, batch_size=50, nb_epoch=10, validation_split=0.05)
#prediction 
predicted = model.predict(seqstest)
#error
rmse = np.sqrt(((predicted-readstest)**2).mean(axis=0))
#plotting 
plt.plot(predicted[:,0],'--')
plt.plot(readstest[:,0],'--')
plt.legend(["prediction", "Test"])
