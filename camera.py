from conf import *
class Camera:
    def __init__(self):
        self.camera = 0
        self.respawn = 0
        self.x_bouge = 0

    def get_x(self):
        return self.camera

    def add_x(self,x):
        self.camera += x
        self.add_bouge(x)

    def reset(self):
        self.camera = self.respawn

    def set_spawn(self):
        self.respawn = self.get_x()
    def start(self):
        self.camera = 0
    def get_spawn(self):
        return  self.respawn

    def set_x(self,x):
        self.camera = x

    def add_bouge(self,x):
        self.x_bouge += x
    def get_bouge(self):
        return self.x_bouge
    def set_bouge(self,n):
        self.x_bouge = n