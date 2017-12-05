# coding:utf-8
import numpy as np
import random
import azurflow_defs as ad
import azurflow_utils as au
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D
from keras import optimizers
from keras import backend as K
from keras.callbacks import EarlyStopping

# global variable
# definition of shape of neural network input/output
# INPUT_SHAPE = (ad.IMG_Y, ad.IMG_X, 3)
INPUT_SHAPE = (ad.IMG_Y, 406, 3)
OUTPUT_SHAPE = 2

def customized_loss(y_true, y_pred, loss='euclidean'):
  # Simply a mean squared error that penalizes large joystick summed values
  val = 0
  if loss == 'L2':
    L2_norm_cost = 0.001
    val = K.mean(K.square((y_pred - y_true)), axis=-1) \
          + K.sum(K.square(y_pred), axis=-1) / 2 * L2_norm_cost
  # euclidean distance loss
  elif loss == 'euclidean':
    val = K.sqrt(K.sum(K.square(y_pred - y_true), axis=-1))
  return val


def create_model(keep_prob=0.8):
  model = Sequential()

  # NVIDIA's model
  model.add(Conv2D(24, kernel_size=(5, 5), strides=(2, 2), activation='relu', input_shape=INPUT_SHAPE))
  model.add(Conv2D(36, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
  model.add(Conv2D(48, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
  model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
  model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
  model.add(Flatten())
  model.add(Dense(1164, activation='relu'))
  drop_out = 1 - keep_prob
  model.add(Dropout(drop_out))
  model.add(Dense(100, activation='relu'))
  model.add(Dropout(drop_out))
  model.add(Dense(50, activation='relu'))
  model.add(Dropout(drop_out))
  model.add(Dense(10, activation='relu'))
  model.add(Dropout(drop_out))
  # model.add(Dense(OUTPUT_SHAPE, activation='linear'))
  model.add(Dense(OUTPUT_SHAPE, activation='softsign'))

  return model


if __name__ == '__main__':
  # initialize training data
  train_x = []
  train_y = np.empty([0, 2])

  # Early-stopping
  early_stopping = EarlyStopping(patience=2)

  # load memories
  for memory in ['memory4', 'memory5', 'memory1', 'memory3', 'memory2', 'memory6']:
    x, y = au.load_memory(memory)
    train_x.extend(x)
    train_y = np.r_[train_y, y]

  # train_x = np.array(train_x)

  # shuffle samples
  z = zip(train_x, train_y)
  random.shuffle(z)
  x, y = zip(*z)
  train_x = np.array(x)
  train_y = np.array(y)

  # Training loop variables
  epochs = 100
  batch_size = 15

  model = create_model()
  model.compile(loss=customized_loss, optimizer=optimizers.adam())
  model.fit(train_x, train_y, batch_size=batch_size, epochs=epochs, shuffle=True, validation_split=0.1, callbacks=[early_stopping])

  model.save_weights('model_weights.h5')
