from keras.layers import Dense
from keras.models import Sequential
from sklearn import preprocessing
from src.misc.evaluation import mape
import numpy as np
import pandas as pd

x_train = pd.read_csv('train_X.csv', index_col=0).as_matrix()
x_test = pd.read_csv('test_X.csv', index_col=0).as_matrix()
y_train = pd.read_csv('train_Y.csv', index_col=0).as_matrix()
y_test = pd.read_csv('test_Y.csv', index_col=0).as_matrix()

min_max_scaler = preprocessing.MinMaxScaler()
min_max_scaler.fit(np.concatenate((x_train, x_test)))

X_train_scale = min_max_scaler.transform(x_train)
X_test_scale = min_max_scaler.transform(x_test)

model = Sequential()
model.add(Dense(input_dim=154, output_dim=200, activation='relu'))
model.add(Dense(input_dim=200, output_dim=500,activation='relu'))
model.add(Dense(input_dim=500, output_dim=36,activation='relu'))

model.compile(loss='mean_absolute_percentage_error', optimizer='rmsprop')

model.fit(X_train_scale, y_train,
          batch_size=1, epochs=100, verbose=2,
          validation_data=(X_test_scale, y_test), shuffle=False)

y = model.predict(X_test_scale, batch_size=1)
mape = mape(y, y_test)
print(mape)