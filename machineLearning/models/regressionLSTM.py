from __future__ import division
import sys
import numpy as np
import pandas as pd

seed = 9
np.random.seed(seed)

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Embedding
from keras.layers.recurrent import LSTM
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
#checks cli args
if len(sys.argv) < 6:
    print("how to run this program")
    print("arg1 is the input data file for training")
    print("arg2 is batch size")
    print("arg3 is number of epochs")
    print("arg4 is the filepath where the model willbe saved to (*.h5)")
    print("arg5 is the filepath to the plot of the prediction results (*.png)")
    print("arg6 is the proportion of data to be used for validation, not learning")



# fix random seed for reproducibility
# load tempscsv data
dataframe = pd.read_csv(str(sys.argv[1]), delimiter=",")
dataset = dataframe.values
# split into input (X) and output (Y) variables
seqs = dataset[:,0]
temps = dataset[:,1]
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
(seqstrain, seqstest, tempstrain, tempstest) = train_test_split(seqs, temps, test_size=float(sys.argv[6]), random_state=seed)
#TRAIN IT ON ALL THE DATA VALIDATE WITH OTHER DATA
#creating model
model = Sequential()
model.add(LSTM(80, input_shape=(1, max_length), return_sequences=True))  
model.add(LSTM(40, input_shape=(80,1), return_sequences=True))  
model.add(Dropout(0.2))
model.add(LSTM(20, input_shape=(40,1), return_sequences=True))  
model.add(Dropout(0.2))
model.add(LSTM(10, input_shape=(20,1), return_sequences=False))  
model.add(Dropout(0.2))
model.add(Dense(units=1, input_shape=(10,1))) 
model.add(Activation("sigmoid"))  

model.compile(loss="mean_squared_error", optimizer="adam")

# fit the model
model.fit(seqstrain, tempstrain, batch_size=int(sys.argv[2]), epochs=int(sys.argv[3]), validation_split=0.05)

#prediction 
predicted = model.predict(seqstest)
model.save(str(sys.argv[4]))

numpts = int(len(seqs)*float(sys.argv[6]))
##error
error = [abs(predicted[i]-tempstest[i])*100/tempstest[i] for i in range(numpts)]
print("avg errror per prediction:")
print(sum(error)/numpts)
#plotting
fig = plt.figure()

if numpts > 150: #graphs are unreadable if it is too big
    numpts = 150

ax1 = fig.add_subplot(121)
ax1.plot(predicted[1:numpts],'--')
ax1.plot(tempstest[1:numpts],'--')
ax1.legend(["predictions", "results"])

ax2 = fig.add_subplot(122)
ax2.plot(error[1:numpts],'--')
ax2.legend(["predictions-results"])
plt.savefig(str(sys.argv[5]))
plt.show()
