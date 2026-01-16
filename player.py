from settings import *
from camera import Camera
import pygame as pg
from utils import is_breakable, is_climbable, to_surival_mined
from world_objects.entity import player_entity
from world_objects.item import InventoryItem as Item


class Inventory:
    def __init__(self, app):
        self.app = app
        self.slots = [0 for i in range(40)]
        
        self.inventory_image = pg.image.load("C:\\Users\\stano\\vs_code\\assets\\inventory.png")
        self.inventory_image = pg.transform.rotate(self.inventory_image, -90.0)

        grass_item = pg.image.load("C:\\Users\\stano\\vs_code\\Matusko\\Minecraft\\assets\\items\\grass.png")
        grass_item = pg.transform.scale(grass_item, (50, 53))

        dirt_item = pg.image.load("C:\\Users\\stano\\vs_code\\Matusko\\Minecraft\\assets\\items\\dirt.png")
        dirt_item = pg.transform.scale(dirt_item, (50, 53))

        stone_item = pg.image.load("C:\\Users\\stano\\vs_code\\Matusko\\Minecraft\\assets\\items\\stone.png")
        stone_item = pg.transform.scale(stone_item, (50, 53))

        sand_item = pg.image.load("C:\\Users\\stano\\vs_code\\Matusko\\Minecraft\\assets\\items\\sand.png")
        sand_item = pg.transform.scale(sand_item, (50, 53))

        

        self.item_name_font = pg.font.Font("freesansbold.ttf", 24)

        self.items = [grass_item, dirt_item, stone_item, sand_item]
        self.item_names = ["grass block", "dirt", "stone", "sand"]

        self.enabled = False
    def update(self):
        for index, value in enumerate(self.slots):
            if value != 0 and value.count == 0:
                self.slots[index] = 0
    def render(self):
        if not self.enabled:
            return
        screen = pg.surface.Surface(tuple(WIN_RES))
        screen.fill((0, 0, 0, 0))
        width, height = 950,700
        screen.blit(self.inventory_image, ((width - self.inventory_image.get_width()) // 2, (height - self.inventory_image.get_height()) // 2))

        slot_idf = [f"a{i + 1}" for i in range(8)] + [f"b{i + 1}" for i in range(8)] + [f"c{i + 1}" for i in range(8)] + [f"d{i + 1}" for i in range(8)] + [f"e{i + 1}" for i in range(4)] + [f"f{i + 1}" for i in range(4)]
        for idf in slot_idf:
            x, y = 0,0    
            item_id = self[idf].item_id if isinstance(self[idf], Item) else self[idf]
    

            if item_id == 0 or item_id > len(self.items):
                continue

            row, column = idf[0], idf[1]

            if row in "abcd":
                if row == "a":
                    y = 569
                if row == "b":
                    y = 497
                if row == "c":
                    y = 435
                if row == "d":
                    y = 377

                if column == "1":
                    x = 178

                if column == "2":
                    x = 239

                if column == "3":
                    x = 299
                
                if column == "4":
                    x = 357
                
                if column == "5":
                    x = 417
                
                if column == "6":
                    x == 478
                
                if column == "7":
                    x = 535

                if column == "8":
                    x = 593

                    
            if x == 0: x = 478
            screen.blit(self.items[item_id - 1], (x + 2, y + 2))

        try:
            if self[mpos_to_idf(*pg.mouse.get_pos())] != 0:
                text = self.item_name_font.render(self.item_names[self[mpos_to_idf(*pg.mouse.get_pos())] - 1], True, "white", (0, 0, 255))
                pg.draw.rect(text, (0, 0, 50), ((0, 0), text.get_size()), width=2)
                
                mx, my = pg.mouse.get_pos()
                screen.blit(text, (mx + 12, my + 12))
        except:
            pass




        texture = self.app.textures.load_from_texture(screen, is_tex_array=False, fx=False, fy=False)
        texture.use(location = 12)

        x = (WIN_RES.x - width) // 2
        x /= WIN_RES.x
        x += -1.0

        y = (WIN_RES.y - width) // 2
        y /= WIN_RES.y
        y += -1.0

        vbo = np.array([
            x, y, 0.0,                                            0.0, 1.0,
            x + width / WIN_RES.x, y, 0.0,                        1.0, 0.0,
            x, y + height / WIN_RES.y, 0.0,                       0.0, 0.0,

            x, y, 0.0,                                            0.0, 1.0,
            x + width / WIN_RES.x, y, 0.0,                        1.0, 0.0,
            x + width / WIN_RES.x, y + height / WIN_RES.y, 0.0,   1.0, 1.0,
            

            
        ])

        vbo = self.app.ctx.buffer(vbo)

        vao = self.app.ctx.vertex_array(
            self.app.shader_program.gui_shader,
            [(vbo, "3f 2f", "in_position", "in_uv")], skip_errors = True
        )
        vao.render()







                    






    def __setitem__(self, key, value):
        index = self._idf_to_index(key)
        self.slots[index] = value
    def __getitem__(self, key):
        index = self._idf_to_index(key)
        return self.slots[index]
    def __delitem__(self, key):
        index = self._idf_to_index(key)
        self.slots[index] = 0   
    def _get_group(self, group_id):
        group_start, group_end = tuple(group_id.split("-"))
        index1 = self._idf_to_index(group_start)
        index2 = self._idf_to_index(group_end) + 1

        return self.slots[index1:index2]
    
    def get_hand_group(self):
        return self._get_group("a1-a8")
    
    def get_craft_group(self):
        return self._get_group("e1-e4")
    
    def get_armor_group(self):
        return self._get_group("f1-f4")
    def get_inventory_group(self):
        return self._get_group("b1-d8")
        
    @staticmethod
    def _idf_to_index(idf):
        if type(idf) != str:
            raise TypeError(f"argument 1(idf) must be a string got '{type(idf)}.__name__'")
        if len(idf) != 2:
            raise TypeError(f"argument 1(idf) needs to have lentgh '2' got '{len(idf)}'")
        
        row_id, colum = tuple(idf)


        if not colum.isdigit() or not row_id.isalpha() or colum == "0":
            raise TypeError(f"argument 1(idf) has invalid format ('{idf}') should be like a1")


        rows = {"a":0, "b":8, "c":16, "d":24, "e":32, "f":36} # a = hand, b = inventory 1, c = inventory 2, d = inventory 3, e = craftingtable, f = armor
        colum = int(colum) - 1

        index = rows[row_id] + colum
        if index < 40 and index > -1: return index


        raise ValueError(f"bad index '{index}'")




def mpos_to_idf(x, y):
    width, height = 950,700

    x -= (WIN_RES.x - width) // 2
    y -= (WIN_RES.y - height) // 2

    row = ""
    column = ""
    if y > 569 and y <= 624:
        row = "a"
    if y > 497 and y <= 552:
        row = "b"
    if y > 435 and y <= 492:
        row = "c"
    if y > 377 and y <= 435:
        row = "d"
    if y > 130 and y <= 245 and x > 535 and x <= 650:
        row = "e"
    if y > 70 and y <= 303 and x > 178 and x <= 237:
        row = "f"


    if row == "":
        return "?"
    
    if row in "abcd":
        if x > 178 and x <= 237:
            column = "1"

        if x > 239 and x <= 294:
            column = "2"

        if x > 299 and x <= 354:
            column = "3"
        
        if x > 357 and x <= 413:
            column = "4"
        
        if x > 417 and x <= 471:
            column = "5"
        
        if x > 476 and x <= 531:
            column = "6"
        
        if x > 535 and x <= 590:
            column = "7"

        if x > 593 and x <= 649:
            column = "8"
    if row == "f":
        if y > 70 and y <= 124:
            column = "1"
        if y > 128 and y <= 181:
            column = "2"
        if y > 188 and y <= 242:
            column = "3"
        if y > 246 and y <= 302:
            column = "4"
        

    return row + column




class Player(Camera):
    def __init__(self, app, position=PLAYER_START_POS, yaw=-90, pitch=0, gravity=0.1, velocity_at_jump=0.5, velocity_at_fall=-0.2):
        #initialize Camera and create an instance of main application
        
        self.app = app
        self.removed_block = False
        self.placed_block = False

        self.vaj = velocity_at_jump
        self.vaf = velocity_at_fall
        self.gravity = gravity
        self.velocity = 0 
        self.last_vel = 0
        self.not_jumping = True
        self.type = "player"
        self.name = "Steve"



        #inventory
        self.inventory = Inventory(app)
        if GAMEMODE == CREATIVE:
            self.inventory['a1'] = Item(1, 64)
            self.inventory['a2'] = Item(2, 64)
            self.inventory['a3'] = Item(3, 64)
            self.inventory['a4'] = Item(4, 64)
            self.inventory['a5'] = Item(5, 64)
            self.inventory['a6'] = Item(6, 64)
            self.inventory['a7'] = Item(7, 64)
            self.inventory['a8'] = Item(255, 64)
            
            
            
        self.hand_index = 0

        self.movable = True
        super().__init__(position, yaw, pitch)

        self.inventory_on()
     

        print_info("state: player_initialized")

    def can_ud(self):
        can_climb = False
        b1 = self.app.collisions.get_vid(self.position + glm.vec3(1, 0, 0))
        b2 = self.app.collisions.get_vid(self.position + glm.vec3(-1, 0, 0))
        b3 = self.app.collisions.get_vid(self.position + glm.vec3(0, 0, 1))
        b4 = self.app.collisions.get_vid(self.position + glm.vec3(0, 0, -1))

        b = [b1, b2, b3, b4]

        for i in b:
            if is_climbable(i):
                can_climb = True
                break


        can_swim = False

        return can_climb or can_swim
        


    def update(self):
        self.update_inventory()
        self.keyboard_controll()
        self.mouse_controll()
        if not self.can_ud(): self.handle_gravity()
        if self.movable:super().update()

    def inventory_on(self):
        self.inventory.enabled = True
        self.on = False

    def inventory_off(self):
        self.inventory.enabled = False
        self.on = True

    
        
    def update_inventory(self):
        self.app.voxel_handler.new_voxel_id = self.inventory.get_hand_group()[self.hand_index]
        if self.app.voxel_handler.new_voxel_id != 0:
            self.app.voxel_handler.new_voxel_id = self.app.voxel_handler.new_voxel_id.item_id
        self.inventory.update()

   
    def mouse_controll(self):
        
        mouse_dx, mouse_dy = pg.mouse.get_rel()

        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITVITY)

        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITVITY)


        l, m, r = pg.mouse.get_pressed()

        if GAMEMODE == CREATIVE:
            #creative           
            voxel_handler = self.app.voxel_handler 
            if r and not self.removed_block and voxel_handler.voxel_world_pos and is_breakable(voxel_handler.getblock(voxel_handler.voxel_world_pos.x, voxel_handler.voxel_world_pos.y, voxel_handler.voxel_world_pos.z)):
                b = voxel_handler.getblock(voxel_handler.voxel_world_pos.x, voxel_handler.voxel_world_pos.y, voxel_handler.voxel_world_pos.z)
                succes = voxel_handler.setblock(voxel_handler.voxel_world_pos.x, voxel_handler.voxel_world_pos.y, voxel_handler.voxel_world_pos.z, 0)
                voxel_handler.update()
                if succes:
                    name = BLOCK_NAMES[BLOCKS.index(b)].lower()
                    self.app.sound.playsound(f"minecraft.blocks.{name}.destroy")
                    
                    
                self.removed_block = True

            if l and not self.placed_block and voxel_handler.voxel_world_pos and voxel_handler.voxel_normal and voxel_handler.new_voxel_id:
                succes = voxel_handler.setblock(voxel_handler.voxel_world_pos.x + voxel_handler.voxel_normal.x, voxel_handler.voxel_world_pos.y + voxel_handler.voxel_normal.y, voxel_handler.voxel_world_pos.z + voxel_handler.voxel_normal.z, voxel_handler.new_voxel_id)
                voxel_handler.update()
                if succes:
                    name = BLOCK_NAMES[BLOCKS.index(voxel_handler.new_voxel_id)].lower()
                    self.app.sound.playsound(f"minecraft.blocks.{name}.place")
                    
                self.placed_block = True
        else:
            #surival       
            voxel_handler = self.app.voxel_handler 
            if r and not self.removed_block and voxel_handler.voxel_world_pos and is_breakable(voxel_handler.getblock(voxel_handler.voxel_world_pos.x, voxel_handler.voxel_world_pos.y, voxel_handler.voxel_world_pos.z)):
                b = voxel_handler.getblock(voxel_handler.voxel_world_pos.x, voxel_handler.voxel_world_pos.y, voxel_handler.voxel_world_pos.z)
                succes = voxel_handler.setblock(voxel_handler.voxel_world_pos.x, voxel_handler.voxel_world_pos.y, voxel_handler.voxel_world_pos.z, 0)
                voxel_handler.update()
                if succes:
                    name = BLOCK_NAMES[BLOCKS.index(b)].lower()
                    self.app.sound.playsound(f"minecraft.blocks.{name}.destroy")

                    #update inventory
                    for index, value in enumerate(self.inventory.get_hand_group(), 1):
                        if value == 0:
                            self.inventory[f'a{index}'] = Item(to_surival_mined(b), 1)
                            break

                        elif value.item_id == to_surival_mined(b):
                            value.count += 1
                            break


                    
                    
                self.removed_block = True

            if l and not self.placed_block and voxel_handler.voxel_world_pos and voxel_handler.voxel_normal and voxel_handler.new_voxel_id:
                succes = voxel_handler.setblock(voxel_handler.voxel_world_pos.x + voxel_handler.voxel_normal.x, voxel_handler.voxel_world_pos.y + voxel_handler.voxel_normal.y, voxel_handler.voxel_world_pos.z + voxel_handler.voxel_normal.z, voxel_handler.new_voxel_id)
                voxel_handler.update()
                if succes:
                    name = BLOCK_NAMES[BLOCKS.index(voxel_handler.new_voxel_id)].lower()
                    self.app.sound.playsound(f"minecraft.blocks.{name}.place")



                    #update inventory
                    if self.inventory[f'a{self.hand_index + 1}']: self.inventory[f'a{self.hand_index + 1}'].count -= 1
                    self.update_inventory()

                    
                self.placed_block = True

        if not r: self.removed_block = False
        if not l: self.placed_block = False
    def handle_gravity(self):
        if self.app.collisions.player_collided_top(self.position) and self.velocity > 0:
            self.velocity = 0
        elif self.app.collisions.player_collided_bottom(self.position) and self.velocity < 0:
            self.velocity = 0





        elif not self.app.collisions.player_collided_bottom(self.position) and self.velocity == 0:
            self.velocity = self.vaf


        if self.velocity != 0:
            self.position += glm.vec3(0, self.velocity, 0) 
            self.velocity -= self.gravity


        self.last_vel = self.velocity

        

    def keyboard_controll(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.app.delta_time

        if self.movable:


            if key_state[pg.K_w]:
                self.move_forward(vel)

            if key_state[pg.K_s]:
                self.move_back(vel)

            if key_state[pg.K_a]:
                self.move_left(vel)

            if key_state[pg.K_d]:
                self.move_right(vel)
            if self.can_ud():

                if key_state[pg.K_q]:
                    self.move_up(vel)
                if key_state[pg.K_e]:
                    self.move_down(vel)

            if key_state[pg.K_SPACE] and self.not_jumping and self.app.collisions.player_collided_bottom(self.position):
                self.velocity = self.vaj
                self.not_jumping = False

            elif not key_state[pg.K_SPACE]:
                self.not_jumping = True

            if key_state[pg.K_SLASH]:
                print(self.app.commands.call(input("command here>"), self.as_entity(),  3 * GAMEMODE))
            

        for i in range(1, 9):
            if key_state[eval(f"pg.K_{i}")]:
                self.hand_index = i - 1
                break
        if key_state[pg.K_LEFT] and GAMEMODE == CREATIVE:
            self.app.voxel_handler.new_voxel_id -= 1 if self.app.voxel_handler.new_voxel_id != 1 else 0
        if key_state[pg.K_RIGHT] and GAMEMODE == CREATIVE:
            self.app.voxel_handler.new_voxel_id += 1 if self.app.voxel_handler.new_voxel_id != BLOCKS[-1] else 0
     
    def as_entity(self):
        return player_entity(self.app, self.name, self)
    
    def get(self, key):
        if key == "position":
            return self.position
        
        elif key == "x":
            return int(self.position.x)
        elif key == "y":
            return int(self.position.x)
        elif key == "z":
            return int(self.position.x)
        elif key == "inventory":
            return self.inventory
        
        
        else:
            return None

    def set(self, key, value):
        if key == "position":
            self.position = value
        elif key == "x":
            self.position.x = value

        elif key == "y":
            self.position.y = value

        elif key == "z":
            self.position.z = value

        elif key == "inventory":
            if isinstance(value, Inventory):
                self.inventory = value
        
    def has(self, key):
        if key in ["position", "x", "y", "z", "inventory"]:
            return True
        
        else:
            return False



