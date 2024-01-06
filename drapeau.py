from sprite import Sprite
import pyxel
class Flag(Sprite):
    def __init__(self,
                 x, y,
                 camera
                 ):
        super().__init__(x, y,
                         0,
                         8, 8,
                         1,
                         0, 0,
                         0, 64,
                         0, 0,
                         "mob", 0,
                         camera)
        self.use = False

    def check(self):
        self.sprite_x += 8
        self.use = True

    def get_position(self):
        return (self.x-self.camera.get_x(),self.y)
