# coding:utf-8
import numpy as np
import azurflow_defs as ad
from keras.preprocessing.image import load_img, img_to_array

# some functions used in azurflow

# load image and return fixed image array
def load_image(image_path):
  img_array = img_to_array(load_img(image_path))
  img_array /= 255 # 画像配列は255で割って使うのがしきたりらしい
  return img_array

# load memory and return train data
# (in) memory_name: name of memory
# (out) ret_x: list of numpy array (one array element represents one image)
# (out) csv: array of numpy array (one array element represents one click point)
def load_memory(memory_name):
  ret_x = []
  memory_dir = ad.MEMORIES_DIR + memory_name + '/'

  csv = np.loadtxt(memory_dir + 'record.csv', delimiter=',', skiprows=1)
  num_of_rows = csv.shape[0]
  csv /= 100

  for i in range(0, num_of_rows):
    img_array = load_image(memory_dir + str(i) + '.png')
    ret_x.append(img_array)

  return ret_x, csv