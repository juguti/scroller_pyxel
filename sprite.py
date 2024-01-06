from conf import *

def signe(n):
    if n >= 0:
        return 1
    else:
        return -1
class Sprite:
    # we define a Player class
    def __init__(self,
                 x,
                 y,
                 MAX_SPEED,
                 height,
                 width,
                 orientation,
                 GRAVITY,
                 friction,
                 sprite_x,
                 sprite_y,
                 duration,
                 jump_power,
                 ENTITY_TYPE,
                 life,
                 camera):
        self.x = x  # position
        self.y = y
        self.speed = 0
        self.MAX_SPEED = MAX_SPEED
        self.height = height  # sprite dimensions
        self.width = width
        self.orientation = orientation  # where does it point, here it's right
        self.GRAVITY = GRAVITY
        self.jump_force = 0
        self.friction = friction
        self.animation = 0
        self.sprite_x = sprite_x  # aka skin
        self.sprite_y = sprite_y
        self.duration = duration
        self.jump_power = jump_power
        self.entity_type = ENTITY_TYPE
        self.life = life
        self.camera = camera

    def speed_round(self):
        # Rounds the speed to the tenths of a pixel
        if self.speed < 0.1:
            self.speed = 0

    def gravity(self):
        if self.jump_force < 7:
            # Applies the gravity up to 7 (pixels per second)
            self.jump_force += self.GRAVITY

    def collisions(self):
        for i in range(abs(int(self.speed / (self.MAX_SPEED / 4)))):

            self.x += self.MAX_SPEED / 4 * self.orientation

            if map.get_element(self.right_side()[0], self.right_side()[1])[1] in sol or \
                    map.get_element(self.right_side()[0], self.right_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                self.x -= self.MAX_SPEED / 4

                break

            if map.get_element(self.left_side()[0], self.left_side()[1])[1] in sol or \
                    map.get_element(self.left_side()[0], self.left_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
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
    def get_hitbox(self):
        return (self.x - self.camera.get_x(), self.y, self.width, self.height)
    def sprites_collisions(self, hit_box2: tuple) -> bool:
        """
        This function looks for two hit boxes collision
        hit box1 / hit box2 are two hit boxes of two different sprites
        A hit box is defined as (x, y, width, height)
        """
        # Checks the hit boxes as vertical lines
        hit_box1 =  self.get_hitbox()
        if (hit_box2[0] <= hit_box1[0] <= hit_box2[0] + hit_box2[2] or
            hit_box2[0] <= hit_box1[0] + hit_box1[2] < + hit_box2[0] + hit_box2[2]) \
                and \
                (hit_box2[1] <= hit_box1[1] <= hit_box2[1] + hit_box2[3] or
                 hit_box2[1] <= hit_box1[1] + hit_box1[3] < + hit_box2[1] + hit_box2[3]):
            # Checks the hit boxes as horizontal lines
            return True

    def animation_run(self) -> None:  # Mettre des variables pour sprite_x
        """Changes the sprite's sprites when he's running"""
        if self.speed == 0:
            # Idle animation
            self.sprite_x = 8
            self.animation = 0
        else:
            self.animation += 1
            # Changes the avatar sprite according to the animation variable
            if self.animation >= 0:
                self.sprite_x = 8
            if self.animation >= self.duration * 1:
                self.sprite_x = 16
            if self.animation >= self.duration * 2:
                self.sprite_x = 24
            if self.animation > self.duration * 3:
                self.animation = 0

    def draw(self):
        """Draws the sprite avatar"""
        pyxel.blt(self.x - self.camera.get_x(),
                  self.y,
                  0,
                  self.sprite_x,
                  self.sprite_y,
                  self.width * self.orientation,
                  self.height,
                  colkey=0)  # Won't draw that color (used as transparent color)

    def foot(self) -> tuple:
        """Returns the player's feet position, especially for the collisions"""
        x_tmp = self.x
        if self.entity_type != "player":
            x_tmp = self.x - self.camera.get_x()
        return (x_tmp  + self.camera.get_x()) // 8, \
               (self.y + self.height) // 8, \
               (x_tmp + self.camera.get_x() + self.width) // 8

    def head(self) -> tuple:
        """Returns the player's head position, especially for the collisions"""
        x_tmp = self.x
        if self.entity_type != "player":
            x_tmp = self.x - self.camera.get_x()
        return int(x_tmp + 1 + self.camera.get_x()) // 8, int(
            x_tmp + self.camera.get_x() + self.width - 1) // 8, self.y // 8

    def right_side(self) -> tuple:
        """Returns the right side of the sprite in block coordinates"""
        x_tmp = self.x
        if self.entity_type != "player":
            x_tmp = self.x - self.camera.get_x()
        return int(x_tmp + self.width + int(self.camera.get_x())) // 8, self.y // 8, int(self.y + self.height) // 8

    def left_side(self) -> tuple:
        """Returns the left side of the sprite in block coordinates"""
        x_tmp = self.x
        if self.entity_type != "player":
            x_tmp = self.x - self.camera.get_x()
        return int(x_tmp + int(self.camera.get_x())) // 8, self.y // 8, int(self.y + self.height) // 8

    def dead(self):
        """If the player is below the ground, he won't come back with us anymore..."""
        if self.y > 128:
            return True
        if self.life > 0:
            return False
        else:
            return True

    def move_right(self):
        # Moves to the right
        if self.speed < self.MAX_SPEED:
            self.speed += self.MAX_SPEED / 4
        else:
            self.speed = self.MAX_SPEED
        self.orientation = 1

    def move_left(self):
        # Moves to the left
        if self.speed < self.MAX_SPEED:
            self.speed += self.MAX_SPEED / 4
        else:
            self.speed = self.MAX_SPEED
        self.orientation = -1

    def jump(self):
        if self.jump_force == 0:
            # Jumps only if the player is on the ground
            self.jump_force = -self.jump_power
            if self.entity_type == "player":
                # Toggles the jump sound for the player only
                pyxel.play(0, 0)

    def speed_friction(self):
        """Applies the speed friction"""
        # If the player is moving...
        if self.speed > 0:
            # Reduces the player speed
            self.speed -= self.friction

    def big_check(self):
        """Groups all the checks a sprite needs in one function"""
        self.gravity()
        self.collisions()
        self.speed_round()
        self.animation_run()

    def take_damage(self, damage: int) -> None:
        """Applies some damage value"""
        self.life -= damage

    def cure_health(self, health_bonus: int) -> None:
        """Applies some damage value"""
        self.life += health_bonus
