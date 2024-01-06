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
        self.les_spawner.clear()
        self.flags_position.clear()
        self.coin_position.clear()
        for bloc_x in range(256):
            for bloc_y in range(16):
                bloc = self.get_element(bloc_x, bloc_y)
                if bloc == spawner_champ:
                    self.set_element(bloc_x, bloc_y, void_tile)
                    self.les_spawner.append((bloc_x,bloc_y))
                elif bloc == check_point_position:
                    self.set_element(bloc_x, bloc_y, void_tile)
                    self.flags_position.append((bloc_x, bloc_y))
                elif bloc == coin_tile_pos:
                    self.set_element(bloc_x, bloc_y, void_tile)
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