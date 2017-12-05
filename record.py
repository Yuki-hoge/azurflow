# coding:utf-8
import pyautogui, subprocess, sys, os, keyboard, time
import azurflow_defs as ad
from PIL import Image


def search_pic(pic_name):
  position = None
  for i in range(0, 10):
    position = pyautogui.locateCenterOnScreen(pic_name)
    if position != None:
      break
  return position

def is_retina():
  return subprocess.call("system_profiler SPDisplaysDataType | grep 'Retina' >> /dev/null", shell= True) == 0

def fix_position4retina(position):
  result = position
  if is_retina():
    result = (position[0]/2, position[1]/2)
  return result

# limit position value to fixed range(0~ad.NUM_OF_MESH)
def calc_fixed_range_pos(position):
  x = position[0]
  y = position[1]

  if x < 0:
    x = 0
  if x > ad.NUM_OF_MESH:
    x = ad.NUM_OF_MESH
  if y < 0:
    y = 0
  if y > ad.NUM_OF_MESH:
    y = ad.NUM_OF_MESH

  return (x, y)


# calc relative position of given position
def calc_relative_fixed_pos(position):
  x = (1.0*(position[0] - TOP_LEFT_POS[0]) / WIDTH) * ad.NUM_OF_MESH
  y = (1.0*(position[1] - TOP_LEFT_POS[1]) / HEIGHT) * ad.NUM_OF_MESH
  return calc_fixed_range_pos((int(round(x)), int(round(y))))

# capture data if space key is pressed
# and click there
cap_ctr = 0
def capture():
  mouse_pos = pyautogui.position()
  relative_mouse_pos = calc_relative_fixed_pos(mouse_pos)
  print relative_mouse_pos
  x = relative_mouse_pos[0]
  y = relative_mouse_pos[1]
  record_cmd = 'echo ' + str(x) + ',' + str(y) + ' >> ' + SAVE_PATH + 'record.csv'
  subprocess.call(record_cmd, shell=True)
  sc = None
  if is_retina():
    sc = pyautogui.screenshot(region=(TOP_LEFT_POS[0]*2, TOP_LEFT_POS[1]*2, WIDTH*2, HEIGHT*2))
  else:
    sc = pyautogui.screenshot(region=(TOP_LEFT_POS[0], TOP_LEFT_POS[1], WIDTH, HEIGHT))

  global cap_ctr
  sc.thumbnail((ad.IMG_X, ad.IMG_Y), Image.ANTIALIAS)
  gray_sc = sc.convert('L')
  gray_sc.save(SAVE_PATH + str(cap_ctr) + '.png')
  cap_ctr += 1
  pyautogui.click()

def move_cursor(position):
  x = position[0]
  y = position[1]
  pyautogui.moveTo(x, y, 1)


########## Main ##########

# check argument
args = sys.argv
if len(args) != 2:
  print "Invalid argument"
  sys.exit()

# init save directory of recorded data
mkdir_cmd = ['mkdir', ad.MEMORIES_DIR + args[1]]
subprocess.call(mkdir_cmd)
SAVE_PATH = os.path.dirname(os.path.abspath(__file__)) \
            + '/' + ad.MEMORIES_DIR + args[1] + '/'

# init action record file
init_cmd = 'echo x,y >> ' + SAVE_PATH + 'record.csv'
subprocess.call(init_cmd, shell=True)

# init screen view
precombat_pos = search_pic('precombat.png')
if precombat_pos == None:
  print "precombat button search error"
  sys.exit()
TOP_LEFT_POS = fix_position4retina(precombat_pos)
move_cursor(TOP_LEFT_POS)

exercise_pos = search_pic('exercise.png')
if exercise_pos == None:
  print "exercise button search error"
  sys.exit()
exercise_pos = fix_position4retina(exercise_pos)
tmp_w = exercise_pos[0] - TOP_LEFT_POS[0]
tmp_h = exercise_pos[1] - TOP_LEFT_POS[1]
tmp_x = int(TOP_LEFT_POS[0] + tmp_w*1.12)
tmp_y = int(TOP_LEFT_POS[1] + tmp_h*1.1)
BOTTOM_RIGHT_POS = (tmp_x, tmp_y)
move_cursor(BOTTOM_RIGHT_POS)
WIDTH = BOTTOM_RIGHT_POS[0] - TOP_LEFT_POS[0]
HEIGHT = BOTTOM_RIGHT_POS[1] - TOP_LEFT_POS[1]


keyboard.hook_key('space', capture)
keyboard.wait()
