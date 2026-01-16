from settings import *
from typing import Literal
from world_objects.entity import Test

_gch_type = Literal['a', 'e', 'b']
class EntityHandler:
    def __init__(self, app):
        self.app = app
        self.entities = [self.app.player.as_entity(), Test(app, *PLAYER_START_POS, "hello")]
        self.block_entities = []

   
    def update(self):
        for i in self.entities: i.update()

    def render(self):
        for i in self.entities: i.render()
    def add_be(self, e):
        self.block_entities.append(e)
    def add_e(self, e):
        self.entities.append(e)
    
    def get_from_gch(self, gch:_gch_type):
        if gch == "a":
            f = list(map(lambda e: e if e.type == "player" else None, self.entities))
            b = f
            for index, value in enumerate(f):
                if value == None:
                    del b[index]
            return b
        if gch == "e":
            return self.entities
        
        if gch == "b":
            return self.block_entities

    def get_from_gche(self,gche:str):
        try:
            if len(gche) < 2: return None
            if gche[0] != "@": return None

            group = self.get_from_gch(gche[1])

            if len(gche) == 2: return group

            if gche[2] != "[": return None
            if gche[-1] != "]": return None

            
            args = {}
            pending = ""
            arg = ""
        

            for char in gche[3:-1]:
                if char == "=":
                    arg = pending
                    pending = ""

                elif char == ",":
                    args[arg] = pending
                    pending = ""


                else: pending += char


            
            


            for index, e in enumerate(group):
                if e:
                    for key, val in args.items():
                        if val.isnumeric() and val.isdigit(): val = int(val)
                        elif val.isnumeric() : val = float(val)
                        if e[key] != val:
                            del group[index]
            return group

                        

        except:
            return None

    def get_args(self, gche:str):
        try:
            if len(gche) < 2: return None
            if gche[0] != "@": return None


            if len(gche) == 2: return {}

            if gche[2] != "[": return None
            if gche[-1] != "]": return None


            args = {}
            pending = ""
            arg = ""
        

            for char in gche[3:-1]:
                if char == "=":
                    arg = pending
                    pending = ""

                elif char == ",":
                    args[arg] = pending
                    pending = ""


                else: pending += char
            
            return args


        except:
            return None

