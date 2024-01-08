from .Settings import settings
import pygame as pg
pg.init()


class SoundFX:
    def __init__(self, sound_path, max_volume=1):
        self.__sound_path = sound_path
        self.__sound = pg.mixer.Sound(sound_path)
        self.max_volume = max_volume
        self.volume = max_volume * settings.sounds_volume

    @property
    def volume(self):
        return self.__dict__["volume"]

    @volume.setter
    def volume(self, value):
        self.__dict__["volume"] = value
        self.__sound.set_volume(self.volume)

    @property
    def length(self):
        return self.__sound.get_length()

    @property
    def num_channels(self):
        return self.__sound.get_num_channels()

    @property
    def file_name(self):
        return self.__sound_path.split("/")[-1].replace(".mp3", "")

    def play(self, loops=0, maxtime=0, fade_ms=0):
        """if 'loops' is set to '-1' the Sound will loop indefinitely. 'maxtime' is for stopping playing after n milliseconds. 'fade_ms' is for fading up to full volume in n milliseconds"""
        self.__sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)

    def stop(self, fadeout=None):
        """'fadeout' will stop the Sound after fading out in n milliseconds"""
        if fadeout:
            self.__sound.fadeout(fadeout)
        else:
            self.__sound.stop()
