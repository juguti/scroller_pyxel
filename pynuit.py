from player import Player
from mob import Mob
from conf import *
from drapeau import Flag
from coin import Coin

class App:
    def __init__(self):
        """Initializes the variables"""
        pyxel.init(128, 128)  # Screen dimensions
        pyxel.load("res.pyxres")  # Loads the ressource file
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
            if pyxel.btn(pyxel.KEY_SPACE):
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
        else:
            pyxel.cls(6)
            pyxel.text(24,pyxel.height/2 - 10,"PRESS SPACE TO START",0)



# Runs the program
App()
