from Modules.Objects.GUIObjects import *
from Modules.Objects.APIObjects import *

SCREEN_WIDTH, SCREEN_HEIGHT = config.SCREEN_SIZE
BLUE = (147, 179, 242)
YELLOW = (255, 255, 200)
BROWN = (162, 48, 42)
BLACK = (0, 0, 0)

SOUNDS = set()

button_sound = SoundFX("Resources/Audio/button_sound.mp3")
SOUNDS.add(button_sound)

car_sound = SoundFX("Resources/Audio/Car/car_sound.mp3", 0.85)
SOUNDS.add(button_sound)


class Menu:
    def __init__(self, game):
        self.game = game

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.running, self.game.playing = False, False
                self.game.garage_menu.player_stats.update_time_in_game()
                self.game.music_player.clean_covers()
                pg.mixer.fadeout(500)
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.game.keys["MOUSE DOWN"] = True
            if event.type == pg.KEYDOWN:
                if event.key == settings.KEYS["BACK"]:
                    self.game.keys["BACK"] = True
                if event.key == settings.KEYS["ENTER"]:
                    self.game.keys["ENTER"] = True
                if event.key == settings.KEYS["MOVE LEFT"]:
                    self.game.keys["MOVE LEFT"] = True
                if event.key == settings.KEYS["MOVE RIGHT"]:
                    self.game.keys["MOVE RIGHT"] = True
                if event.key == settings.KEYS["PLAY MUSIC"]:
                    self.game.music_player.play()
                if event.key == settings.KEYS["CHANGE MUSIC"]:
                    self.game.music_player.next()
            if event.type == pg.MOUSEWHEEL:
                self.game.keys["MOUSEWHEEL"] = event.y
                self.game.keys["MOUSEWHEEL_X"] = event.x
            if event.type == self.game.music_player.MUSIC_END:
                self.game.music_player.playing = False
                if self.game.music_player.loop:
                    self.game.music_player.play()
                else:
                    self.game.music_player.next()


def load_bg(place):
    bg_path = f'Resources/Images/Backgrounds/bgs/{settings.current_bg[place]}/'
    try:
        bg = GIF(bg_path, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except FileNotFoundError:
        raise FileNotFoundError(f'There is no directory with name "{settings.current_bg[place]}" in Backgrounds!')

    bg_speed = config.BGS_SPEED[settings.current_bg[place]]
    return bg, bg_speed


def load_bg_sound(place):
    sound_path = f'Resources/Audio/LevelsSoundFX/{settings.current_bg[place]}.mp3'
    try:
        sound = SoundFX(sound_path, max_volume=config.BGS_SOUNDS_MAX_VOLUME[settings.current_bg[place]])
    except FileNotFoundError:
        raise FileNotFoundError(f'Add sound to "settings.current_bg[place]" in LevelsSoundFX directory!')

    SOUNDS.add(sound)
    return sound


def delay(start_time, milliseconds=250):
    current_time = pg.time.get_ticks()
    return current_time - start_time >= milliseconds
