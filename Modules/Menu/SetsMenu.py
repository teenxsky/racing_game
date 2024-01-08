from .Menu import *


class SetsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)

        self.sets_bg = Picture("Resources/Images/Backgrounds/window.png", 0.5)
        self.sets_close_button = Button("Resources/Images/Buttons/close_button_off.png",
                                        "Resources/Images/Buttons/close_button_on.png", button_sound, 0.15)
        self.sets_back_button = Button("Resources/Images/Buttons/back_button_off.png",
                                       "Resources/Images/Buttons/back_button_on.png", button_sound, 0.15)

        self.text_settings = Text("SETTNGS", 45, button_sound)
        self.text_volume = Text("VOLUME", 45, button_sound)
        self.text_controls = Text("CONTROLS", 45, button_sound)

        self.sets_volume_button = Button("Resources/Images/Buttons/volume_button_off.png",
                                         "Resources/Images/Buttons/volume_button_on.png", button_sound, 0.15)
        self.sets_controls_button = Button("Resources/Images/Buttons/controls_button_off.png",
                                           "Resources/Images/Buttons/controls_button_on.png", button_sound, 0.15)
        self.sets_text = [Text("VOLUME", 32, color=BLUE),
                          Text("CONTROLS", 32, color=BLUE)
                          ]

        self.volume_text = [Text("GENERAL VOLUME", 28, color=BLUE),
                            Text("MUSIC VOLUME", 28, color=BLUE),
                            Text("SOUNDS VOLUME", 28, color=BLUE)
                            ]

        self.text_keys = []
        for key in settings.KEYS.keys():
            self.text_keys.append(Text(key, 25, button_sound, color=BLUE))

        self.scroll_y = 0
        self.sub_state = "SETS"

    def display_menu(self):
        self.sets_bg.draw(self.game.screen, (640, 360))

        if self.sub_state == "SETS":
            self.display_sets()
        elif self.sub_state == "CONTROLS":
            self.display_controls()
        elif self.sub_state == "VOLUME":
            self.display_volume()

        if self.sets_close_button.draw(self.game.screen, (865, 225)) and self.game.keys["MOUSE DOWN"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"
            self.scroll_y = 0

    def display_sets(self):
        self.text_settings.draw(self.game.screen, (640, 225))

        bar = pg.surface.Surface((510, 170)).convert_alpha()
        bar.fill(BROWN)
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 350)

        distance = 0
        for text in self.sets_text:
            if text.draw_as_button(bar, (5, self.scroll_y + distance), position="topleft",
                                   surface_topleft=bar_rect.topleft):
                if self.game.keys["MOUSE DOWN"]:
                    self.sub_state = text.string
            distance += 40

        if self.sets_text[0].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and self.sets_text[-1].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height:
            self.scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar, bar_rect)

        if self.sets_controls_button.draw(self.game.screen, (475, 460)) and self.game.keys["MOUSE DOWN"]:
            self.sub_state = "CONTROLS"
        if self.sets_volume_button.draw(self.game.screen, (415, 460)) and self.game.keys["MOUSE DOWN"]:
            self.sub_state = "VOLUME"
        if self.game.keys["BACK"]:
            self.game.menu_state = "MENU"
            self.sub_state = "SETS"
            self.scroll_y = 0

    def display_controls(self):
        self.text_controls.draw(self.game.screen, (640, 225))

        bar = pg.surface.Surface((510, 190)).convert_alpha()
        bar.fill(BROWN)
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 360)

        distance = 0
        for key in self.text_keys:
            if key.draw_as_button(bar, (5, self.scroll_y + distance), position="topleft",
                                  surface_topleft=bar_rect.topleft):
                self.key_choosing(key, key.string, bar)
            distance += 30

        if self.text_keys[0].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and self.text_keys[-1].rect.bottomleft[1] + 10 + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height:
            self.scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar, bar_rect)
        if self.game.keys["BACK"] or (
                self.sets_back_button.draw(self.game.screen, (415, 225)) and self.game.keys["MOUSE DOWN"]):
            self.sub_state = "SETS"
            self.scroll_y = 0

    def key_choosing(self, key, key_name, surface):
        chosen = False
        curr_key = Text(pg.key.name(settings.KEYS[key_name]), key.scale)
        curr_key.draw(surface, (key.rect.midright[0] + 15, key.rect.midright[1]), position="midleft")

        if self.game.keys["MOUSE DOWN"]:
            while not chosen:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.game.running, self.game.playing = False, False
                        pg.mixer.fadeout(500)
                        pg.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key not in settings.KEYS.values() \
                                or settings.KEYS[key_name] == event.key:
                            settings.KEYS[key_name] = event.key
                            chosen = True

    def display_volume(self):
        self.text_volume.draw(self.game.screen, (640, 225))

        bar = pg.surface.Surface((510, 170)).convert_alpha()
        bar.fill(BROWN)
        bar_rect = bar.get_rect()
        bar_rect.center = (640, 350)
        level, level_rect = None, None

        pos = pg.mouse.get_pos()[0] - bar_rect.x, pg.mouse.get_pos()[1] - bar_rect.y

        distance = 0
        for text in self.volume_text:
            text.draw(bar, (10, self.scroll_y + distance), position="topleft")
            pg.draw.rect(bar, (255, 255, 255), (10, text.rect.bottomleft[1], 400, 20), 2)
            level = pg.surface.Surface((getattr(settings, '_'.join(text.string.lower().split())) * 400, 20))
            level.fill((255, 255, 255))
            level_rect = level.get_rect()
            level_rect.topleft = (10, text.rect.bottomleft[1])
            if text.string == "MUSIC VOLUME":
                if pg.mouse.get_pressed()[0] and level_rect.collidepoint(pos) and pos[0] <= 400:
                    setattr(settings, '_'.join(text.string.lower().split()), pos[0] / 400)
                    self.game.music_player.set_volume()
            elif text.string == "SOUNDS VOLUME":
                if pg.mouse.get_pressed()[0] and level_rect.collidepoint(pos) and pos[0] <= 400:
                    setattr(settings, '_'.join(text.string.lower().split()), pos[0] / 400)
                    for sound in SOUNDS:
                        sound.volume = (pos[0] / 400) * sound.max_volume

            bar.blit(level, level_rect)
            distance += 70

        if self.volume_text[0].rect.y + (self.game.keys["MOUSEWHEEL"] * 10) <= 0 \
                and level_rect.bottomleft[1] + 10 + (self.game.keys["MOUSEWHEEL"] * 10) >= bar_rect.height:
            self.scroll_y += self.game.keys["MOUSEWHEEL"] * 10

        self.game.screen.blit(bar, bar_rect)
        if self.game.keys["BACK"] or (
                self.sets_back_button.draw(self.game.screen, (415, 225)) and self.game.keys["MOUSE DOWN"]):
            self.sub_state = "SETS"
            self.scroll_y = 0
