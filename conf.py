import pyxel
from camera import Camera
from map import *

camera = Camera()
map = Map(0,0,camera)

def signe(n):
    if n >= 0:
        return 1
    else:
        return -1




