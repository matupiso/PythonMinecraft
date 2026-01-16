from settings import *
from world_objects.world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.sun import Sun
from world_objects.clouds import Clouds
from font import get_font_default

class Scene:
    def __init__(self, app):
        #create application instance
        self.app = app

        

        #rendering objects
        self.world = World(app)
        self.marker = VoxelMarker(app)
        self.sun = Sun(app)
        self.clouds = Clouds(app)
        

        print_info("state: scene_initialized")

    def render(self):
        #render all rendering objects
        self.world.render()
        self.marker.render()
        self.sun.render()
        self.app.entity_handler.render()

    
        

    def update(self):
        self.world.update()
        self.marker.update()
        self.sun.update()

        
