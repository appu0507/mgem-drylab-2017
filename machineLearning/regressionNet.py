import sys
import numpy as np
import pandas as pd
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
# fix random seed for reproducibility
seed = 9
np.random.seed(seed)
# load readscsv data
dataframe = pd.read_csv(str(sys.argv[1]), delimiter=",", header=1)
dataset = dataframe.values
# split into input (X) and output (Y) variables
seqs = dataset[:,1]
reads = dataset[:,0]
#split into test and trian data
(seqstrain, seqstest, readstrain, readstest) = train_test_split(seqs, reads, test_size=0.33, random_state=seed)
# create model
def base_model():
    model = Sequential()
    model.add(Dense(152, input_dim=1, kernel_initializer='normal', activation='relu'))
    model.add(Dense(76, kernel_initializer='normal', activation='relu'))
    model.add(Dense(38, kernel_initializer='normal', activation='relu'))
    model.add(Dense(19, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

predictor = KerasRegressor(build_fn=base_model, nb_epoch=int(sys.argv[2]), batch_size=5, verbose=0)

predictor.fit(seqstrain, readstrain)
result = predictor.predict(seqstest)
print("predictions are" + str(result))
result = mean_squared_error(readstest, predictor.predict(seqstest))




