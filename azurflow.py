# coding:utf-8
import train
import numpy as np
import azurflow_utils as au

### main
model = train.create_model(keep_prob=1)
model.load_weights('model_weights.h5')

img_array = au.load_image('memories/memory1/0.png')
x = np.array((img_array, img_array))
# predicted_y = model.predict(x, batch_size=1, verbose=0) * 100
predicted_y = model.predict(x, batch_size=1, verbose=0) * 100

print (predicted_y)
