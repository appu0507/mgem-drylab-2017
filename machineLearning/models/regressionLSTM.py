import sys
import numpy as np
import pandas as pd
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
model.fit(seqstrain, readstrain, batch_size=int(sys.argv[2]), epochs=int(sys.argv[3]), validation_split=0.05)

#prediction 
predicted = model.predict(seqstest)
model.save(str(sys.argv[4]))

##error
error = [abs(predicted[i]-readstest[i])*100 for i in range(len(predicted))]
print(error)
#plotting
fig = plt.figure()

ax1 = fig.add_subplot(121)
ax1.plot(predicted,'--')
ax1.plot(readstest,'--')
ax1.legend(["prediction", "Test"])

ax2 = fig.add_subplot(122)
ax2.plot(error, '--')
ax2.legend(["predictions-results"])

plt.show()
plt.savefig(str(sys.argv[5]))
