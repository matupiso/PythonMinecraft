import pygame as pg
from typing import Union, Literal


_volume_type = Union[float, Literal['not_assigned',]]



class Sound:
    def __init__(self):
        self.current_sound = None
        self.volume = None
    def    set_volume(self, volume:_volume_type):
        if volume == "not_assigned": self.volume = None
        else:self.volume = volume
    def playsound(self, indicator:str, volume=1.0):
        if self.volume: volume = self.volume
        location1 = f"assets\\sounds\\{indicator.replace(".", "\\")}.wav"
        location2 = f"assets\\sounds\\{indicator.replace(".", "\\")}.mp3"

        try:
            if self.current_sound: self.current_sound.stop()
            self.current_sound  = pg.mixer.Sound(location1)
            self.current_sound.set_volume(volume)
            self.current_sound.play()
            return True
        
        except:
            try:
                if self.current_sound: self.current_sound.stop()
                self.current_sound = pg.mixer.Sound(location2)
                self.current_sound.set_volume(volume)
                self.current_sound.play()
                return True
            
            except: return False



