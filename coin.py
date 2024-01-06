from sprite import Sprite
from conf import *

class Coin(Sprite):
    def __init__(self,x,y):
        super().__init__(x, y,
                         0,
                         8, 8,
                         1,
                         0, 0,
                         32, 8,
                         0, 0,
                         "coin", 0,
                         camera)

        self.taken = False

