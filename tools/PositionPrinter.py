import time
import mouse
from PIL import ImageGrab
import pyautogui

pyautogui.FAILSAFE = True
time.sleep(3)

while 1:
    print("Pos: " + str(mouse.get_position()) + " Color: " + str(ImageGrab.grab().load()[mouse.get_position()[0], mouse.get_position()[1]]))
    time.sleep(3)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)

class Region:
    def __init__(self, topLeft, bottomRight):
        self.region = (*topLeft.pos, *bottomRight.pos)