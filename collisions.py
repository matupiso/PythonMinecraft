from settings import *
from utils import is_solid, get_floatpart_fromfloat

class Collisions:
    def __init__(self, app):
        self.app = app
    def get_edge(self, position):
        pos = glm.vec3(position)
        on_block_pos = pos - glm.vec3(glm.ivec3(position))

        info = {
            "-x":on_block_pos.x < 0.19,
            "+x":on_block_pos.x > 0.81,
            "-z":on_block_pos.z < 0.19,
            "+z":on_block_pos.z > 0.81
        }


        edge_blocks = {
            1:info["-x"] and info["-z"],
            2:info['-z'],
            3:info['+x'] and info['-z'],
            4:info['+x'],
            5:info['+x'] and info['+z'],
            6:info['+z'],
            7:info['-x'] and info['+z'],
            8:info['-x']

        }

        return info, edge_blocks



    def get_vid(self, wposition) -> int:
        return self.app.voxel_handler.get_block(*glm.ivec3(wposition))[0]
    
    def player_in_block(self, position):
        if is_solid(self.get_vid(position)) or is_solid(self.get_vid(position - glm.vec3(0, 1, 0))):
            return True
        
        return False

    def player_collided_bottom(self, position):
        ipos = glm.ivec3(position) - glm.ivec3(0, PLAYER_HEIGHT, 0)
        if not is_solid(self.get_vid(position - glm.vec3(0, PLAYER_HEIGHT, 0))) :
            info, edge_blocks = self.get_edge(position)

            block_1 = is_solid(self.get_vid(ipos + glm.ivec3(-1, 0, -1))) if edge_blocks[1] else 0
            block_2 = is_solid(self.get_vid(ipos + glm.ivec3(0, 0, -1))) if edge_blocks[2] else 0
            block_3 = is_solid(self.get_vid(ipos + glm.ivec3(1, 0, -1))) if edge_blocks[3] else 0
            block_4 = is_solid(self.get_vid(ipos + glm.ivec3(1, 0, 0))) if edge_blocks[4] else 0
            block_5 = is_solid(self.get_vid(ipos + glm.ivec3(1, 0, 1))) if edge_blocks[5] else 0
            block_6 = is_solid(self.get_vid(ipos + glm.ivec3(0, 0, 1))) if edge_blocks[6] else 0
            block_7 = is_solid(self.get_vid(ipos + glm.ivec3(-1, 0, 1))) if edge_blocks[7] else 0
            block_8 = is_solid(self.get_vid(ipos + glm.ivec3(-1, 0, 0))) if edge_blocks[8] else 0
            blocks = [block_1, block_2, block_3, block_4, block_5, block_6, block_7, block_8]
            if blocks.count(0) != 8:
                return True
            
            return False

        
        return True
    def player_collided_top(self, position):
        if not is_solid(self.get_vid(position + glm.vec3(0, 1, 0))):
            return False
        
        return True
    def _player_can_move_forward_x(self, position):
        if is_solid(self.get_vid(position + glm.vec3(1, 0, 0))) or is_solid(self.get_vid(position + glm.vec3(1, -1, 0))):
            x = get_floatpart_fromfloat(position.x)
            if x > 0.6: return True
            return False
        else:
            return False
        


    def _player_can_move_backward_x(self, position):
        if is_solid(self.get_vid(position + glm.vec3(-1, 0, 0))) or is_solid(self.get_vid(position + glm.vec3(-1, -1, 0))):
            x = get_floatpart_fromfloat(position.x)
            if x < 0.4: return True
            return False
        else:
            return False
    def _player_can_move_forward_z(self, position):
        if is_solid(self.get_vid(position + glm.vec3(0, 0, 1))) or is_solid(self.get_vid(position + glm.vec3(0, -1, 1))):
            z = get_floatpart_fromfloat(position.z)
            if z > 0.6: return True
            return False
        
        return False
    def _player_can_move_backward_z(self, position):
        if is_solid(self.get_vid(position + glm.vec3(0, 0, -1))) or is_solid(self.get_vid(position + glm.vec3(0, -1, -1))):
            z = get_floatpart_fromfloat(position.z)
            if z < 0.4: return True
            return False
        
        return False




    def player_can_move_forward_x(self, position): return not self._player_can_move_forward_x(position)
    def player_can_move_backward_x(self, position): return not self._player_can_move_backward_x(position)
    def player_can_move_forward_z(self, position): return not self._player_can_move_forward_z(position)
    def player_can_move_backward_z(self, position): return not self._player_can_move_backward_z(position)
 
    
    

