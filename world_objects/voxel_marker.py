from settings import *
from meshes.cube_mesh import CubeMesh



class VoxelMarker:
    def __init__(self, app):
        self.mesh = CubeMesh(app, app.shader_program.marker)
        self.app = app

    def update(self):
        if self.app.voxel_handler.voxel_world_pos:
            self.mesh.position = self.app.voxel_handler.voxel_world_pos
            self.mesh.active = True
        else:
            self.mesh.active = False
        self.mesh.set_uniform()


    def render(self):
        self.mesh.render()