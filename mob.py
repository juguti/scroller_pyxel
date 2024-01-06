from conf import *
from sprite import Sprite


class Mob(Sprite):


    def generate_mob(mob_name: str, bloc_x:int, bloc_y:int, camera):
        """Returns a mob class with the mob name, the bloc coordinates and the camera
            mobs names:
                - champ
        """
        if mob_name == "champ":
            return Mob(bloc_x * 8, bloc_y * 8 - 0.1, 1, 8, 8, -1, 0.25, 1, 40, 0, 1, 1, 1, 1, camera)
    # we define a Mob class
    def __init__(self,
                 x, y,
                 MAX_SPEED,
                 height, width,
                 orientation,
                 GRAVITY, mob_friction,
                 sprite_x, sprite_y,
                 duree, jump_power,
                 MOB_ENTITY_TYPE, life,
                 camera
                 ):
        super().__init__(x, y,
                         MAX_SPEED,
                         height, width,
                         orientation,
                         GRAVITY, mob_friction,
                         sprite_x, sprite_y,
                         duree, jump_power,
                         "mob", life,
                         camera)

    def move_reset(self):
        self.mob_speed = 0

    def big_check(self):
        self.gravity()
        self.collisions()
        self.speed_round()
        self.where()

        if self.orientation == 1:
            self.move_right()
        elif self.orientation == -1:
            self.move_left()

    def collisions(self):
        for i in range(abs(int(self.speed / (self.MAX_SPEED / 4)))):

            self.x += self.MAX_SPEED / 4 * self.orientation

            if map.get_element(self.right_side()[0], self.right_side()[1])[1] in sol or \
                    map.get_element(self.right_side()[0], self.right_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                self.x -= self.MAX_SPEED / 4
                self.orientation *= -1

                break

            if map.get_element(self.left_side()[0], self.left_side()[1])[1] in sol or \
                    map.get_element(self.left_side()[0], self.left_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                self.x += self.MAX_SPEED / 4
                self.orientation *= -1
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
                self.orientation *= 1
