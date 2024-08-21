from ursina import *
from modules.pc import FirstPersonController
from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader

import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import askyesno, showerror

from sys import exit
from random import randint
import pickle
from perlin_noise import PerlinNoise
from os import listdir
from copy import deepcopy
import shutil
from PIL import Image, ImageTk
import uuid

# from modules.server import Server
# from modules.client import Client, get_ip
# from server.client import send_get_request, send_post_request
# from server.fclient import FlaskClient
# from server.rclient import RedisClient
from server.client import GameClient
from server.sqlite_fclient import SqliteFlaskClient


VERSION = "ver 2.1.1"


class preblocks:
    blocks = [["Cobble", "cobble.png"], ["Gravity Block", "gravity_block.png"], ["Dirt", "dirt.png"], ["Grass", "mgrass.png"],
              ["Planks", "planks.png"], ["Log", "log.png"], ["Leaves", "leaves.png"], ["Flowers", "flowers.png"],
              ["Glass", "glass.png"], ["Bricks", "bricks.png"], ["Stone Bricks", "deepslate_bricks.png"],
              ["Ice", "ice.png"], ["Moss", "moss.png"]]

# World attributes
class w:
    world = []
    sv = []
    s_texs = ["leaves.png", "log.png", "flowers.png"]
    grav_blocks = []
    shaders = True
    old_win = False

# Launcher
class l:
    ws = 10
    flat = False

# Multiplayer
class m:
    is_multiplayer = False
    is_public_server = False

root = tk.Tk()
root.title("mincraft launcher " + VERSION)
root.geometry("400x350")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", lambda: exit(0))

# root.overrideredirect(True)
# root.wm_attributes("-transparent", True)
# root.config(bg='systemTransparent')

# background_image = ImageTk.BitmapImage("assets/dirt.png") # .subsample(50)

# img = Image.open("assets/dirt.png")
# img = img.resize((420, 420)) # Image.ANTIALIAS
# img = ImageTk.PhotoImage(img.convert('RGBA'))
# background_label = tk.Label(root, image=img)
# background_label.pack()
# background_label.place(x=0, y=0, relwidth=1, relheight=1)

def destroy_win():
    try:
        l.ws = int(world_size.get())
    except:
        print("LOG: failed to change wss")
    root.destroy()

def load_world():
    try:
        with open(askopenfilename(filetypes=[("Mincraft World File", "*.mins"), ("All Files", "*.*")]), "rb") as input_file:
            w.world = pickle.load(input_file)
        destroy_win()
    except:
        w.world = []

def flat_load():
    l.flat = True
    destroy_win()

def cust_tex():
    path = askopenfilename()
    shutil.copyfile(path, __file__.replace("mincraft.py", "assets/"))
    preblocks.blocks.append([path.split("/")[-1], path.split("/")[-1] + path.split("/")[-1]])

def deactivate_shaders():
    w.shaders = False

def run_old():
    w.old_win = True


def join_server():
    m.is_multiplayer = True
    destroy_win()

def join_public_server():
    m.is_multiplayer = True
    m.is_public_server = True
    destroy_win()



# rootframe = tk.Frame(root)

tk.Label(root, text="mincraft " + VERSION + "", font=("Impact", 35)).pack()

tk.Label(root, text="World Size:").pack()

world_size = tk.Entry(root)
world_size.pack()
world_size.insert(1, "10")
tk.Button(root, text="turn off shaders", command=deactivate_shaders).pack()
tk.Button(root, text="activate old window type", command=run_old).pack()

# tk.Button(root, text="load custom texture", command=cust_tex).pack()
tk.Label(root, text="Online:").pack()
tk.Button(root, text="join public server", command=join_public_server).pack()
tk.Button(root, text="join LAN", command=join_server).pack()
tk.Label(root, text="Start World:").pack()
tk.Button(root, text="start game", command=destroy_win).pack()
tk.Button(root, text="start flat world game", command=flat_load).pack()
tk.Button(root, text="load world", command=load_world).pack()

root.mainloop()
    

# Game
app = Ursina(development_mode=w.old_win, borderless=w.old_win)

if w.shaders:
    lit_with_shadows_shader.default_input['shadow_color'] = color.hsv(0, 0, 0, 0.2)
    Entity.default_shader = lit_with_shadows_shader

blocks = []

# Define a Voxel class.
# By setting the parent to scene and the model to 'cube' it becomes a 3d button.

class Voxel(Button):
    def __init__(self, position=(0,0,0), tex='cobble.png', dest=True):
        super().__init__(parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture=tex,
            color=color.hsv(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.gray,
        )
        self.destructible = dest

if not m.is_multiplayer:
    if w.world == []:
        def make_voxel(position, tex, dest=True):
            # w.world.append([position[0], position[1], position[2], tex])
            blocks.append(Voxel(position=position, tex=tex, dest=dest))
        def make_structure_voxel(position, tex, dest=True):
            for ptex in w.s_texs:
                if [position[0], position[1], position[2], ptex] in w.sv:
                    return
            w.sv.append([position[0], position[1], position[2], tex])
            blocks.append(Voxel(position=position, tex=tex, dest=dest))
        def make_stone_block(x, y, z):
            if randint(1, 4) == 1:
                    make_voxel(position=(x,y,z), tex="iron_ore.png")
            else:
                if randint(1, 10) == 1:
                    make_voxel(position=(x,y,z), tex="gold_ore.png")
                else:
                    make_voxel(position=(x,y,z), tex="stone.png")
        def make_leaf_voxel(position):
            if randint(1, 4) == 1:
                make_structure_voxel(position=position, tex="flowers.png")
            else:
                make_structure_voxel(position=position, tex="leaves.png")
        def load_structure(path, position):
            with open(path, "r") as file:
                lines = str(file.read()).split("\n")
                for i in lines:
                    j = i.split(",")
                    make_structure_voxel(position=(position[0] + int(j[0]), position[1] + int(j[1]),
                                                position[2] + int(j[2])), tex=j[3])
        def get_structure_path(sname: str):
            return __file__.replace("mincraft.py", "models/") + sname
        def make_tree(x, y, z):
            treetype = randint(1, 2)
            if treetype == 1:
                make_structure_voxel(position=(x,y,z), tex="log.png")
                make_structure_voxel(position=(x,y + 1,z), tex="log.png")
                make_structure_voxel(position=(x,y + 2,z), tex="log.png")
                make_structure_voxel(position=(x,y + 3,z), tex="log.png")
                make_leaf_voxel(position=(x,y + 4,z))
                make_leaf_voxel(position=(x-1,y+3,z-1))
                make_leaf_voxel(position=(x-1,y+3,z))
                make_leaf_voxel(position=(x-1,y+3,z+1))
                make_leaf_voxel(position=(x,y+3,z-1))
                make_leaf_voxel(position=(x,y+3,z+1))
                make_leaf_voxel(position=(x+1,y+3,z-1))
                make_leaf_voxel(position=(x+1,y+3,z))
                make_leaf_voxel(position=(x+1,y+3,z+1))
            elif treetype == 2:
                load_structure(get_structure_path("tree1.txt"), position=(x, y, z))
            

        if l.flat:
            for z in range(l.ws):
                for x in range(l.ws):
                    make_voxel(position=(x,0,z), tex="stone.png")
        else:
            for z in range(l.ws):
                for x in range(l.ws):
                    make_voxel(position=(x,-1,z), tex="bedrock.png", dest=False)
            for z in range(l.ws):
                for x in range(l.ws):
                    make_stone_block(x, 0, z)

            # for z in range(l.ws):
            #     for x in range(l.ws):
            #         blocks.append(Voxel(position=(x,1,z), tex="grass.png"))
            noise = PerlinNoise(octaves=3, seed=randint(1,1000000))

            for z in range(l.ws):
                for x in range(l.ws):
                    y = noise([x * .02,z * .02])
                    y = math.floor(y * 7.5)
                    w.world.append([x, y + 6, z, "mgrass.png"])
            
            for i in w.world:
                blocks.append(Voxel(position=(i[0], i[1], i[2]), tex=i[3]))
            
            for i in w.world: # 7 is the highest it goes (2-7)
                if i[1] == 2:
                    make_stone_block(i[0], 1, i[2])
                if i[1] == 3:
                    make_stone_block(i[0], 1, i[2])
                    make_stone_block(i[0], 2, i[2])
                    if randint(1, 36) == 1:
                        make_tree(i[0], 4, i[2])
                if i[1] == 4:
                    make_stone_block(i[0], 1, i[2])
                    make_stone_block(i[0], 2, i[2])
                    make_stone_block(i[0], 3, i[2])
                    if randint(1, 30) == 1:
                        make_tree(i[0], 5, i[2])
                if i[1] == 5:
                    make_stone_block(i[0], 1, i[2])
                    make_stone_block(i[0], 2, i[2])
                    make_stone_block(i[0], 3, i[2])
                    make_stone_block(i[0], 4, i[2])
                    if randint(1, 30) == 1:
                        make_tree(i[0], 6, i[2])
                if i[1] == 6:
                    make_stone_block(i[0], 1, i[2])
                    make_stone_block(i[0], 2, i[2])
                    make_stone_block(i[0], 3, i[2])
                    make_stone_block(i[0], 4, i[2])
                    make_stone_block(i[0], 5, i[2])
                    if randint(1, 30) == 1:
                        make_tree(i[0], 7, i[2])
                if i[1] == 7:
                    make_stone_block(i[0], 1, i[2])
                    make_stone_block(i[0], 2, i[2])
                    make_stone_block(i[0], 3, i[2])
                    make_stone_block(i[0], 4, i[2])
                    make_stone_block(i[0], 5, i[2])
                    make_stone_block(i[0], 6, i[2])
                    if randint(1, 30) == 1:
                        make_tree(i[0], 8, i[2])
    else:
        for i in w.world:
            blocks.append(Voxel(position=(i[0], i[1], i[2]), tex=i[3]))

    class b:
        blocks = deepcopy(preblocks.blocks)
        curblock = 0

        blocktext = Text(font="assets/font.ttf", position=Vec2(0.01, 0.01))

    def fill(sx, sy, sz, ex, ey, ez, block):
        nx = ex - sx
        ny = ey - sy
        nz = ez - sz
        for x in range(nx):
            for y in range(ny):
                for z in range(nz):
                    blocks.append(Voxel(position=(x + sx, y + sy, z + sz), tex=block, dest=True))

    def input(key):
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                if b.curblock == 1:
                    blocks.append(Voxel(position=hit_info.entity.position + hit_info.normal, tex=b.blocks[b.curblock][1]))
                    w.grav_blocks.append(blocks[-1])
                else:
                    blocks.append(Voxel(position=hit_info.entity.position + hit_info.normal, tex=b.blocks[b.curblock][1]))
        if key == 'left mouse down' and mouse.hovered_entity:
            if blocks[blocks.index(mouse.hovered_entity)].destructible:
                blocks.remove(mouse.hovered_entity)
                try:
                    w.grav_blocks.remove(mouse.hovered_entity)
                except:pass
                destroy(mouse.hovered_entity)
        if key == 'escape':
            if player.enabled:
                player.disable()
            else:
                player.enable()
            # destroy(app)
        if key == 'q':
            b.curblock -= 1
            if b.curblock == -1:
                b.curblock = 0
        if key == 'e':
            b.curblock += 1
            if b.curblock >= len(b.blocks):
                b.curblock = len(b.blocks) - 1
        if key == 'enter':
            root = tk.Tk()
            root.withdraw()
            pic_list = []
            for i in blocks:
                pic_list.append([i.position[0], i.position[1], i.position[2], i.texture])
            with open(asksaveasfilename(defaultextension=".mins"), "wb") as output_file:
                pickle.dump(pic_list, output_file)
            root.destroy()
        if key == 't':
            root = tk.Tk()
            root.withdraw()
            command = str(askstring("mincraft", "Command:", initialvalue="/"))
            if command.startswith("/fill "):
                commandsplit = command.replace("/fill ", "").split(" ")
                coords1 = commandsplit[1].split(",")
                coords2 = commandsplit[2].split(",")
                fill(int(coords1[0]), int(coords1[1]), int(coords1[2]), 
                    int(coords2[0]), int(coords2[1]), int(coords2[2]), commandsplit[0] + ".png")
            root.destroy()
        for i in range(9):
            if key == str(i + 1):
                b.curblock = i
        if key == 't':
            print("heheheheheheheh")
    def update():
        b.blocktext.text = b.blocks[b.curblock][0]
        if player.y < -8:
            # player.position = Vec3(0, 3, 0)
            player.gravity = -1
        if player.y > 50:
            player.gravity = 1
        for i in w.grav_blocks:
            print(i)
            if distance(player, i) < i.scale_x / 2:
                player.gravity = -1
                # if player.gravity == 1:
                #     player.gravity = -1
                # else:
                #     player.gravity = 1


    player = FirstPersonController(position=(0, 15, 0))

    if w.shaders:
        light = DirectionalLight(shadows=True)
        light.look_at(Vec3(1, -1, 1))
    Sky().texture = "sky_sunset"

    app.run()





else:
    throwaway = tk.Tk()
    throwaway.withdraw()
    client: GameClient
    if m.is_public_server:
        client = SqliteFlaskClient("18.220.151.198", "8574", 
                                askstring("mincraft online", "Name:"),  uuid.uuid4(), "brick") # 192.168.68.124
        try:
            client.get_player()
        except RuntimeError:
            showerror("mincraft online", "Player Name Already Exists")
    else:
        pass
        # if askyesno("mincraft online", "Join Redis server?"):
        #     client: GameClient = RedisClient(askstring("mincraft online", "IP:", initialvalue="127.0.0.1"), 
        #                                      int(askstring("mincraft online", "Port:", initialvalue="6379")), l.ws)
        # else:
        #     client: GameClient = FlaskClient(askstring("mincraft online", "IP:", initialvalue="127.0.0.1"),
        #                                      askstring("mincraft online", "Port:", initialvalue="9000"))
    throwaway.destroy()

    class b:
        blocks = deepcopy(preblocks.blocks)
        curblock = 0
        blocktext = Text(font="assets/font.ttf", position=Vec2(0.01, 0.01))
        
        last_edit_id = 0
        voxworld = {}
    
    class s:
        updateiter = 0
        past_position = (0, 0, 0)

    class Enemy(Entity):
        def __init__(self, name: str, hp, position, texture, **kwargs):
            super().__init__(model='cube', scale_y=2, origin_y=-.5, color=color.blue, # parent=shootables_parent, 
                             collider='box', position=position, texture=texture, **kwargs)
            self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
            self.name_text = Text(name, parent=self, y=1.5, color=color.green, world_scale=20)
            self.max_hp = 100
            self.hp = hp
            self.name = name
        
        def update(self):
            self.health_bar.look_at_2d(player.position, 'y')
            self.name_text.look_at_2d(player.position, 'y')
            self.name_text.rotation_y += 180
        
        @property
        def hp(self):
            return self._hp

        @hp.setter
        def hp(self, value):
            self._hp = value
            if value <= 0:
                destroy(self)
                return

            self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
    
    enemies = {}
    
    def input(key):
        if key == 'right mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                client.send_block(position=hit_info.entity.position + hit_info.normal, tex=b.blocks[b.curblock][1])
                # b.world.append([pos[0], pos[1], pos[2], b.blocks[b.curblock][1]])
        if key == 'left mouse down' and mouse.hovered_entity:
            epos = mouse.hovered_entity.position
            etex = mouse.hovered_entity.texture
            client.send_destroy(position=epos, tex=etex)
        if key == 'escape':
            if player.enabled:
                player.disable()
            else:
                player.enable()
            # destroy(app)
        if key == 'q':
            b.curblock -= 1
            if b.curblock == -1:
                b.curblock = 0
        if key == 'e':
            b.curblock += 1
            if b.curblock >= len(b.blocks):
                b.curblock = len(b.blocks) - 1
        if key == 'enter':
            root = tk.Tk()
            root.withdraw()
            with open(asksaveasfilename(defaultextension=".mins"), "wb") as output_file:
                pickle.dump(client.get_world(), output_file)
            root.destroy()

    def update():
        b.blocktext.text = b.blocks[b.curblock][0]

        s.updateiter += 1
        if s.updateiter == 4:
            edits = client.get_world_edits(b.last_edit_id + 1)
            for edit in edits:
                pos = (int(edit[0]), int(edit[1]), int(edit[2]))
                if edit[3] is None and pos in b.voxworld:
                    destroy(b.voxworld[pos])
                    del b.voxworld[pos]
                else:
                    if pos in b.voxworld:
                        destroy(b.voxworld[pos])
                    b.voxworld[pos] = Voxel(position=pos, tex=edit[3])
                b.last_edit_id = int(edit[4])
            s.updateiter = 0

            for i in client.get_players():
                if i[5] != client.name:
                    if i[5] in enemies:
                        destroy(enemies[i[5]])

                    enemies[i[5]] = Enemy(i[5], 100, (i[0], i[1], i[2]), i[3])
        
        if player.position[1] < -8:
            player.position = Vec3(0, 0, 0)
        
        if s.past_position != player.position:
            client.send_player(player.position)
        
        s.past_position = player.position

    player = FirstPersonController()

    def end_client():
        client.end_player(player.position)
        app.quit()

    window.exit_button.on_click = end_client

    if w.shaders:
        light = DirectionalLight(shadows=True)
        light.look_at(Vec3(1, -1, 1))
    Sky().texture = "sky_sunset"

    app.run()