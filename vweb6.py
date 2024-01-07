import pyxel



spawner_champ = (2, 8)
sol = (2, 3)
degat = (4,5)
coin_tile_pos = (4,1)
check_point_position = (0,8)
void_tile = (0,6)
finish = (3,8)

class Map:
    def __init__(self,calque,niv,camera):
        self.calque = calque
        self.y = niv*128
        self.niv = niv
        self.les_spawner = []
        self.flags_position = []
        self.coin_position = []
        self.camera = camera
        self.carte = None
        self.cache = None


    def load_element(self):
        self.void = self.get_element(0, 0)
        self.les_spawner.clear()
        self.flags_position.clear()
        self.coin_position.clear()
        for bloc_x in range(256):
            for bloc_y in range(16):
                bloc = self.get_element(bloc_x, bloc_y)
                if bloc == spawner_champ:
                    self.set_element(bloc_x, bloc_y, self.void)
                    self.les_spawner.append((bloc_x,bloc_y))
                elif bloc == check_point_position:
                    self.set_element(bloc_x, bloc_y, self.void)
                    self.flags_position.append((bloc_x, bloc_y))
                elif bloc == coin_tile_pos:
                    self.set_element(bloc_x, bloc_y, self.void)
                    self.coin_position.append((bloc_x,bloc_y))

    def draw(self):
        # Draws the tile map
        pyxel.bltm(0,
                   0,
                   0,
                   self.camera.get_x(),
                   self.y,
                   pyxel.width,
                   pyxel.height)
        pyxel.bltm(0,
                   0,
                   1,
                   self.camera.get_x(),
                   self.y,
                   pyxel.width,
                   pyxel.height,
                   colkey=0)

    def get_element(self,x,y):
        return self.carte.pget(x,self.y//8 + y)

    def set_element(self,x,y,bloc):
        self.cache.pset(x,self.y//8 +y,bloc)


    def set_carte(self,calque):
        self.carte = pyxel.tilemap(calque)
        self.cache = pyxel.tilemap(1)

    def niveau_change(self,n):
        self.niv = n
        self.y = self.niv * 128
        self.set_carte(0)
        self.load_element()

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


camera = Camera()
map = Map(0,0,camera)


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
               (x_tmp + self.camera.get_x() + self.width-1) // 8

    def head(self) -> tuple:
        """Returns the player's head position, especially for the collisions"""
        x_tmp = self.x
        if self.entity_type != "player":
            x_tmp = self.x - self.camera.get_x()
        return int(x_tmp + camera.get_x())//8,int(x_tmp + camera.get_x() + self.width-1)//8,self.y//8,

    def right_side(self) -> tuple:
        """Returns the right side of the sprite in block coordinates"""
        x_tmp = self.x
        if self.entity_type != "player":
            x_tmp = self.x - self.camera.get_x()
        return int(x_tmp + self.width-1 + int(self.camera.get_x())) // 8, self.y // 8, int(self.y + self.height) // 8

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
        self.speed = self.MAX_SPEED
        self.orientation = 1

    def move_left(self):
        # Moves to the left
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



class Player(Sprite):
    # we define a Player class
    def __init__(self,camera):
        super().__init__(0, 64,
                         2,
                         8, 8,
                         1,
                         0.25, 1,
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
        for i in range(self.speed):

            if (self.x < pyxel.width // 2 and self.orientation == 1) or (self.orientation == -1 and self.camera.get_x() <= 0):
                # moves the player IN the screen / camera
                self.x += 1 *self.orientation
                qui = "player"
            else:
                # moves the camera aka the screen
                self.camera.add_x(1 *self.orientation)
                qui = "cam"

            if map.get_element(self.right_side()[0], self.right_side()[1])[1] in sol or \
                    map.get_element(self.right_side()[0], self.right_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                if qui == "cam":
                    self.camera.add_x(-1)
                else:
                    self.x -= 1
                break

            if map.get_element(self.left_side()[0], self.left_side()[1])[1] in sol or \
                    map.get_element(self.left_side()[0], self.left_side()[2])[1] in sol:
                self.speed = 0  # Nullifying the jumping force because of the impact
                if qui == "cam":
                    self.camera.add_x(1)
                else:
                    self.x += 1
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

    def draw(self):
        """Draws the sprite avatar"""
        pyxel.blt(self.x - self.camera.get_x(),
                  self.y,
                  0,
                  self.sprite_x,
                  self.sprite_y,
                  self.width * self.orientation,
                  self.height,
                  colkey=12)  # Won't draw that color (used as transparent color)



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
    def draw(self):
        """Draws the sprite avatar"""
        pyxel.blt(self.x - self.camera.get_x(),
                  self.y,
                  0,
                  self.sprite_x,
                  self.sprite_y,
                  self.width * self.orientation,
                  self.height,
                  colkey=12)  # Won't draw that color (used as transparent color)




class App:
    def __init__(self):
        """Initializes the variables"""
        pyxel.init(128, 128)  # Screen dimensions
        pyxel.load("my_res.pyxres")  # Loads the ressource file
        map.set_carte(0)
        self.menu = True
        self.life = 0
        self.money = 0

        self.player = Player(camera)  # Initialises player Class
        self.mobs = []  # Mob list
        self.flags = []
        self.coins = []


        self.is_player_dead = False
        self.is_playing_dead_music = False


        pyxel.run(self.update, self.draw)  # Main loop
    def reload(self):
        self.mobs.clear()
        self.coins.clear()
        self.flags.clear()
        self.player.star()
        camera.set_x(0)
        camera.respawn = 0
        self.mob_spawner()  # Makes the mobs spawn
        self.flag_spawn()
        self.coin_spawn()
        self.player.star()

    def start(self):
        # place correctement les éléments
        map.niveau_change(0)
        self.reload()

        self.player.star()
        camera.start()


        self.is_player_dead = False
        self.is_playing_dead_music = False


        self.menu = False
        self.life = 3
        self.money = 0
        self.mobs.clear()
        self.coins.clear()
        self.flags.clear()

        self.mob_spawner()  # Makes the mobs spawn
        self.flag_spawn()
        self.coin_spawn()




    def events(self):
        """Handles the players input"""
        if not self.menu:
            if pyxel.btn(pyxel.KEY_Q) and pyxel.btn(pyxel.KEY_D):
                # If both keys are hit, the movement is null
                self.player.move_reset()
            elif pyxel.btn(pyxel.KEY_Q) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.player.move_left()
            elif pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                self.player.move_right()
            elif pyxel.btn(pyxel.KEY_F):
                self.respawn()
            else:
                # Applies inertia
                self.player.speed_friction()
            if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.player.jump()
        else:
            if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.start()

    def mob_spawner(self):  # a mettre dans une classe tile map
        """Makes the mob spawn"""
        self.mobs.clear()
        for spawner in map.les_spawner:
            self.mobs.append(Mob.generate_mob("champ", spawner[0], spawner[1], camera))

    def flag_spawn(self):
        for flag in map.flags_position:
            self.flags.append(Flag(flag[0]*8,flag[1]*8,camera))
    def coin_spawn(self):
        for coin in map.coin_position:
            self.coins.append(Coin(coin[0]*8,coin[1]*8))


    def respawn(self):
        self.life -= 1
        if self.life == 0:
            self.menu = True
        else:
            self.is_player_dead = False
            self.is_playing_dead_music = False

            self.player.respawn()
            self.mob_spawner()
            self.coin_spawn()
    def update(self):
        """Makes the game physics work
        Updates the camera, player and mob status
        """
        self.events()
        if not self.menu:
            if not self.is_player_dead:
                self.player.big_check()
                self.is_player_dead = self.player.dead()

                for mob in self.mobs:
                    mob.big_check()

                if self.money  >= 100:
                    self.life += 1
                    self.money -= 100


                camera.set_bouge(0)
                if map.get_element(self.player.head()[0], self.player.head()[2]) == finish or \
                    map.get_element(self.player.head()[1], self.player.head()[2]) == finish:
                    map.niveau_change(map.niv + 1)
                    camera.set_x(0)
                    self.reload()


                # Mob collisions
                for mob in self.mobs:
                    if mob.life <= 0:
                        self.mobs.remove(mob)
                    # If the player has a collision with another sprite
                    if self.player.sprites_collisions(mob.get_hitbox()):
                        if self.player.y + self.player.height / 2 < mob.y:
                            # If the mob gets jumped on, he dies !
                            mob.life -= 1
                            self.player.jump_force = -self.player.jump_power // 2
                        else:
                            # The player has finally returned to peace...
                            self.player.take_damage(1)
                            self.is_player_dead = True

                for flag in self.flags:
                    if self.player.sprites_collisions(flag.get_hitbox()):
                        if not flag.use:
                            flag.check()
                            pyxel.play(2, 2)
                            self.player.collide_flag(flag.get_position())

                sup_coin = []
                i = 0
                for coin in self.coins:
                    if self.player.sprites_collisions(coin.get_hitbox()):
                        if not coin.taken:
                            sup_coin.append(i)
                            self.money += 1
                            pyxel.play(2, 3)
                    i+=1
                for coin in sup_coin[::-1]:
                    self.coins.pop(coin)


    def draw(self):
        """Displays everything needed"""
        if not self.menu:
            if self.is_player_dead:
                # Death Screen
                pyxel.cls(0)
                pyxel.text(54, 60, "perdu", 7)
                if pyxel.play_pos(0) is None and  not self.is_playing_dead_music:
                    # Toggle the death music
                    pyxel.play(0, 1)
                    self.is_playing_dead_music = True
                elif pyxel.play_pos(0) is None and  self.is_playing_dead_music:
                    self.respawn()


            else:

                map.draw()
                for flag in self.flags:
                    flag.draw()
                # Draws the player
                self.player.draw()
                pyxel.text(4, 4, f"vie: {self.life}", 0)
                pyxel.text(4, 16, f"coins: {self.money}", 0)
                for mob in self.mobs:
                    mob.draw()
                for coin in self.coins:
                    coin.draw()

                """
                # foot
                x_tmp = self.player.x - camera.get_x()
                x1 = x_tmp + camera.get_x()
                y = self.player.y + self.player.height
                x2 = x_tmp + camera.get_x() + self.player.width - 1


                pyxel.rect(x1,y,1,1,5)
                pyxel.rect(x2, y, 1, 1, 5)

                #head
                x_tmp = self.player.x - camera.get_x()
                x1 =int(x_tmp + camera.get_x())
                x2= int(x_tmp + camera.get_x() + self.player.width-1)
                y= self.player.y

                pyxel.rect(x1, y, 1, 1, 5)
                pyxel.rect(x2, y, 1, 1, 5)

                # right
                x_tmp = self.player.x - camera.get_x()
                x1= (int(x_tmp + self.player.width-1 + int(camera.get_x())))
                y=self.player.y
                y2 =int(self.player.y + self.player.height)
                pyxel.line(x1,y,x1,y2,4)
                """


        else:
            pyxel.cls(6)
            pyxel.text(24,pyxel.height/2 - 10,"PRESS SPACE TO START",0)



# Runs the program
App()
