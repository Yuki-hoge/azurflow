# coding:utf-8
import pyautogui, subprocess, sys, os, keyboard, time, threading
import azurflow_defs as ad
import redframe
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

# limit position value to fixed range(0~num_of_mesh)
def calc_fixed_range_pos(position, num_of_mesh):
  x = position[0]
  y = position[1]

  if x < 0:
    x = 0
  if x > num_of_mesh:
    x = num_of_mesh
  if y < 0:
    y = 0
  if y > num_of_mesh:
    y = num_of_mesh

  return (x, y)

# calc relative position of given position
def calc_relative_fixed_pos(position, top_left_pos, width, height, num_of_mesh):
  x = (1.0*(position[0] - top_left_pos[0]) / width) * num_of_mesh
  y = (1.0*(position[1] - top_left_pos[1]) / height) * num_of_mesh
  return calc_fixed_range_pos((int(round(x)), int(round(y))), num_of_mesh)

def move_cursor(position):
  x = position[0]
  y = position[1]
  pyautogui.moveTo(x, y, 0.5)


class RecordThread(threading.Thread):
  def __init__(self, top_left_pos, width, height, save_path, num_of_mesh):
    threading.Thread.__init__(self)
    self.top_left_pos = top_left_pos
    self.width = width
    self.height = height
    self.save_path = save_path
    self.num_of_mesh = num_of_mesh
    self.cap_ctr = 0

  # capture data if space key is pressed
  # and click there
  def capture(self):
    mouse_pos = pyautogui.position()
    relative_mouse_pos = calc_relative_fixed_pos(mouse_pos,
                                                 self.top_left_pos,
                                                 self.width,
                                                 self.height,
                                                 self.num_of_mesh)
    print relative_mouse_pos
    x = relative_mouse_pos[0]
    y = relative_mouse_pos[1]
    record_cmd = 'echo ' + str(x) + ',' + str(y) + ' >> ' + self.save_path + 'record.csv'
    subprocess.call(record_cmd, shell=True)
    sc = None
    if is_retina():
      sc = pyautogui.screenshot(region=(self.top_left_pos[0]*2,
                                        self.top_left_pos[1]*2,
                                        self.width*2,
                                        self.height*2))
    else:
      sc = pyautogui.screenshot(region=(self.top_left_pos[0],
                                        self.top_left_pos[1],
                                        self.width,
                                        self.height))

    sc.thumbnail((ad.IMG_X, ad.IMG_Y), Image.ANTIALIAS)
    gray_sc = sc.convert('L')
    gray_sc.save(self.save_path + str(self.cap_ctr) + '.png')
    self.cap_ctr += 1
    pyautogui.click()

  def run(self):
    keyboard.hook_key('space', self.capture)
    keyboard.wait()


########## Main ##########
if __name__ == '__main__':
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

  record_thread = RecordThread(TOP_LEFT_POS, WIDTH, HEIGHT, SAVE_PATH, ad.NUM_OF_MESH)
  record_thread.setDaemon(True)
  record_thread.start()

  redframe.show_redframe(TOP_LEFT_POS[0], TOP_LEFT_POS[1], WIDTH, HEIGHT)

