import pygame as pg
import moderngl as mgl
from settings import print_info

class Textures:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx

        #load textures
        self.u_texture_0 = self.load("frame.png")
        self.u_texture_array_0 = self.load("tex_array_0.png", is_tex_array=True)
        self.u_texture_1 = self.load("sun.png")

        self.torch_side = self.load("torch\\torch_side.png", fx = True, fy = False)
        self.torch_top = self.load("torch\\torch_top.png", fx = False, fy = False)
        
        self.torch_flame_1 = self.load("torch\\flame_1.png", fx = True, fy = False)
        self.torch_flame_2 = self.load("torch\\flame_2.png", fx = True, fy = False)
        self.torch_flame_3 = self.load("torch\\flame_3.png", fx = True, fy = False)
        self.torch_flame_4 = self.load("torch\\flame_4.png", fx = True, fy = False)
        self.torch_flame_5 = self.load("torch\\flame_5.png", fx = True, fy = False)
        self.torch_flame_6 = self.load("torch\\flame_6.png", fx = True, fy = False)
        

        #use the texture
        self.u_texture_0.use(location = 0)
        self.u_texture_array_0.use(location = 1)
        self.u_texture_1.use(location = 2)
        self.torch_side.use(location = 3)
        self.torch_top.use(location = 4)

        

        self.torch_flame_1.use(location = 6)
        self.torch_flame_2.use(location = 7)
        self.torch_flame_3.use(location = 8)
        self.torch_flame_4.use(location = 9)
        self.torch_flame_5.use(location = 10)
        self.torch_flame_6.use(location = 11)
        

        print_info("state: textures_initialized")
    def load(self, name, is_tex_array=False, **args):
        texture = pg.image.load(f"assets\\{name}")
        return self.load_from_texture(texture, is_tex_array, **args)



    def load_from_texture(self, texture, is_tex_array=False, fx=True, fy=False):
        if not is_tex_array:
            texture = pg.transform.flip(texture, flip_y=fy, flip_x=fx)

            texture = self.ctx.texture(
                size = texture.get_size(),
                components = 4,
                data=pg.image.tostring(texture, 'RGBA', False)
            )

            texture.anisotropy = 1.0
            texture.build_mipmaps()
            texture.filter = (mgl.NEAREST, mgl.NEAREST)
            return texture
        else:
            texture = pg.transform.flip(texture, flip_y=fy, flip_x=fx)
            num_layers = 3 * texture.get_height() // texture.get_width()
            texture = self.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(texture, "RGBA")
            )
            texture.anisotropy = 1.0
            texture.build_mipmaps()
            texture.filter = (mgl.NEAREST, mgl.NEAREST)
            return texture