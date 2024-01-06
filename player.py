from conf import *
from sprite import Sprite

class Player(Sprite):
    # we define a Player class
    def __init__(self,camera):
        super().__init__(0, 64,
                         2,
                         8, 8,
                         1,
                         0.25, 0.25,
                         8, 0,
                         5,
                         5,
                         "player",
                         1,
                         camera)

        self.start_co = (0,64)
        self.checkpoint = self.start_co
        self.camera = camera
    def respawn(self):
        """Resets the player position and camera"""
        self.x = self.checkpoint[0]
        self.y = self.checkpoint[1]
        self.x = self.x//8 * 8
        self.y = self.y // 8 * 8
        self.camera.reset()
        self.speed = 0
        self.life = 1

    def star(self):
        self.start_co = (0, 64)
        self.checkpoint = self.start_co
        self.x = self.start_co[0]
        self.y = self.start_co[1]
        self.speed = 0
        self.jump_force = 0
    def move_reset(self):
        self.speed = 0

    def big_check(self):
        if self.dead():
            self.respawn()
        self.gravity()
        self.collisions()
        self.speed_round()
        self.where()
        self.animation_run()

    def collisions(self):
        for i in range(abs(int(self.speed / (self.MAX_SPEED / 4)))):

            if (self.x < pyxel.width // 2 and self.orientation == 1) or (self.orientation == -1 and self.camera.get_x() <= 0):
                # moves the player IN the screen / camera
                self.x += self.MAX_SPEED / 4 * self.orientation
                qui = "player"
            else:
                # moves the camera aka the screen
                self.camera.add_x( self.MAX_SPEED / 4 * self.orientation)
                qui = "cam"

            if map.get_element(self.right_side()[0], self.right_side()[1])[1] in sol or \
                    map.get_element(self.right_side()[0], self.right_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                if qui == "cam":
                    self.camera.add_x(-self.MAX_SPEED / 4)
                else:
                    self.x -= self.MAX_SPEED / 4
                break

            if map.get_element(self.left_side()[0], self.left_side()[1])[1] in sol or \
                    map.get_element(self.left_side()[0], self.left_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                if qui == "cam":
                    self.camera.add_x( self.MAX_SPEED / 4)
                else:
                    self.x += self.MAX_SPEED / 4
                break

        for i in range(abs(int(self.jump_force // self.GRAVITY))):
            self.y += (self.GRAVITY * signe(self.jump_force))  # Applies the jump physics
            if map.get_element(self.foot()[0], self.foot()[1])[1] in sol or \
                    map.get_element(self.foot()[2], self.foot()[1])[1] in sol:
                self.jump_force = 0
                self.y -= self.GRAVITY
                break

            elif map.get_element(self.head()[0], self.head()[2])[1] in sol or \
                    map.get_element(self.head()[1], self.head()[2])[1] in sol:
                self.y += self.GRAVITY
                self.jump_force = 0  # Nullifying the jumping force because of the impact
                break

    def where(self):
        bloc_touche = [
            map.get_element(self.right_side()[0], self.right_side()[1]),
            map.get_element(self.right_side()[0], self.right_side()[2]),
            map.get_element(self.left_side()[0], self.left_side()[1]),
            map.get_element(self.left_side()[0], self.left_side()[2])
        ]
        for bloc in bloc_touche:
            if bloc[1] in degat:
                self.take_damage(1)

    def get_hitbox(self):
        return (self.x, self.y, self.width, self.height)

    def collide_flag(self,pos):
        self.checkpoint = (pos[0], pos[1]-1)
        self.camera.set_spawn()
    def speed_round(self):
        if self.speed < 0.1:
            self.speed = 0

        if self.x < 0:
            # Collision of the left side of the screen
            self.x = 0
            self.speed = 0

        elif self.x + self.width > 128:
            # Collision of the right side of the screen
            self.x = 128 - self.width
            self.speed = 0
        if self.camera.get_x() < 0:
            self.camera.set_x(0)

    def draw(self):
        """Draws the sprite avatar"""
        pyxel.blt(self.x,
                  self.y,
                  0,
                  self.sprite_x,
                  self.sprite_y,
                  self.width * self.orientation,
                  self.height,
                  colkey=0)  # Won't draw that color (used as transparent color)