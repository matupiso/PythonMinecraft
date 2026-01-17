from settings import *
from meshes.cube_mesh import CubeMesh

function = type(vars)

class entity:
    def __init__(self, app, type, x, y, z, name):
        self._app = app
        self.type = type
        if name != None:
            self.name = name
        else: 
            self.name = type(self).__name__

        self.x = x
        self.y = y
        self.z = z

 
        
    def __setitem__(self, key, value):
    
        for k, v in vars(self).items():
            if not k.startswith("_") and not isinstance(v, function):
                if k == key:
                    setattr(self, k, value)

    

    def __getitem__(self, key):
        for k, v in vars(self).items():
            if not k.startswith("_") and not isinstance(v, function):
                if k == key:
                    return v
                
        return None
    
    def render(self):
        pass

    def update(self):
        pass

    def kill(self):
        self._app.sound.playsound("util.die_sound")


class player_entity(entity):
    def __init__(self, app, name, player):

        self._player = player
        self._app = app
        assert hasattr(player, "position"), "player object needs position attribute"
        assert hasattr(player, "yaw"), "player object needs yaw attribute"
        assert hasattr(player, "pitch"), "player object needs pitch attribute"

        super().__init__(app, "player ",*player.position , name)

        self.x,  self.y, self.z = tuple(self._player.position)
        self.yaw, self.pitch = self._player.yaw, self._player.pitch
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._player.position = glm.vec3(self.x, self.y, self.z)
        self._player.yaw = self.yaw
        self._player.pitch = self.pitch

        
class block_entity:
    def __init__(self, voxel_handler, position, type):
        self.voxel_hander = voxel_handler
        self.position = position
        self.type = type

        self.data = {
            "position": glm.vec3(position),
            "x":glm.ivec3(position).x,
            "y":glm.ivec3(position).y,
            "z":glm.ivec3(position).z,
            

        }
    def as_dict(self):
        return entity(self)
    def get(self, key):
        return self.data.get(key, None)
    def set(self, key, value):
        self.data[key] = value
    def has(self, key):
        return True if key in self.data.keys() else False
    

    def destroy(self):
        self.voxel_hander.set_block(*self.position, 0)
        del self

    def change(self, block):
        self.voxel_hander.set_block(*self.position, block)
        del self  
    def update(self): pass

class Torch(block_entity):
    TO_UP = 1
    TO_LEFT = 2
    TO_RIGHT = 3
    TO_FRONT = 4
    TO_BACK = 5
    def __init__(self, voxel_handler, position, data:dict):
        super().__init__(voxel_handler, position, "torch")

        for i in data.items():
            key, item = i
            if not self.has(key): self.set(key, item)

        if not self.has("angled"): self.set("angled", self.TO_UP)
    def kill(self):
        self.voxel_hander.app.sound.playsound("minecraft.torch.fizz")
        self.destroy()



class Test(entity):
    def __init__(self, app, x, y, z, name="test"):
        super().__init__(app, "test", x, y, z, name)
        self._app = app
        self.mesh = CubeMesh(self._app, self._app.shader_program.marker)


    def render(self):
        print("dffffff")
    def update(self):
        dir = glm.vec3(0, 0.001, 0)

        self.x = dir.x
        self.y = dir.y
        self.z = dir.z
    

def get_from_type(type):
    if type == "Test":
        return Test
    
    else:
        return None