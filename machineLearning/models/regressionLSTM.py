import sys
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers.recurrent import LSTM
import matplotlib.pylab as plt
# fix random seed for reproducibility
seed = 9
np.random.seed(seed)
# load readscsv data
dataframe = pd.read_csv(str(sys.argv[1]), delimiter=",")
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
#
for i,seq in enumerate(seqs):
    diff = max_length - len(seq)
    padded_sequence = seq + diff*'0'
    padded_sequence_list = list(padded_sequence)
    padded_sequence_list_ints = [ int(x) for x in padded_sequence_list ]
    seqs[i] = [padded_sequence_list_ints]

#split into test and trian data
(seqstrain, seqstest, readstrain, readstest) = train_test_split(seqs, reads, test_size=0.33, random_state=seed)

#creating model
model = Sequential()
model.add(LSTM(30, input_shape=(1, max_length), return_sequences=True))  
model.add(LSTM(50, input_shape=(30,1), return_sequences=True))  
model.add(Dropout(0.2))
model.add(LSTM(20, input_shape=(50,1), return_sequences=False))  
model.add(Dropout(0.2))
model.add(Dense(output_dim=1, input_shape=(20,1))) 
model.add(Activation("relu"))  
model.compile(loss="mean_squared_error", optimizer="rmsprop")
# fit the model
model.fit(seqstrain, readstrain, batch_size=30, epochs=int(sys.argv[2]), validation_split=0.05)
#prediction 
predicted = model.predict(seqstest)
#error
rmse = [np.sqrt(x) for x in ((predicted[:]-readstest[:])**2).mean(axis=0)]
print('rmse error is:')
print(rmse)
#plotting
plt.plot(predicted,'--')
plt.plot(readstest,'--')
plt.legend(["prediction", "Test"])
