# coding:utf-8
# some definitions used in azurflow

# the number of mesh
# 画面を何*何分割するか
# 100だと画面を100*100で分割する
# 学習するクリック座標はこの値に依存するので，学習時とプレイ時でこの値は同じにする
NUM_OF_MESH = 100

# the size of image
IMG_X = 412
#IMG_X = 406
IMG_Y = 244

# a memory will be saved under here
MEMORIES_DIR = 'memories/'