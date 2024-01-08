import pygame as pg
from Modules.Objects.APIObjects.Settings import settings, config

SCREEN_WIDTH, SCREEN_HEIGHT = config.SCREEN_SIZE


class Text:
    def __init__(self, text='', scale=20, sound=None, color=(255, 255, 255), font="Resources/Fonts/pxl_tactical.ttf"):
        self.scale = scale
        self.sound = sound
        self.color = color
        self.string = text
        self.font_path = font

        self.font = pg.font.Font(self.font_path, self.scale)
        self.text = self.font.render(self.string, False, self.color).convert_alpha()
        self.rect = self.text.get_rect()

        self.on_button = False

        self.temporary_string = None

        # FOR TEXT BAR

        self.last_update = pg.time.get_ticks()
        self.current_text = ""

    def draw(self, surface, coordinates, mp3_cut=False, color=None, position="center"):
        setattr(self.rect, position, coordinates)
        if color:
            if mp3_cut:
                text = self.font.render(self.string[:-4], False, color).convert_alpha()
            else:
                text = self.font.render(self.string, False, color).convert_alpha()
            surface.blit(text, self.rect)
        else:
            if mp3_cut:
                text = self.font.render(self.string[:-4], False, self.color).convert_alpha()
                surface.blit(text, self.rect)
            else:
                surface.blit(self.text, self.rect)

    def draw_as_button(self, surface, coordinates, block=False, surface_topleft=(0, 0), press_color=(255, 255, 200), position="center"):
        setattr(self.rect, position, coordinates)
        action = False
        x, y = surface_topleft
        if not block:
            pos = pg.mouse.get_pos()
            x_b = (pos[0] >= x) and (pos[0] <= x + surface.get_width())
            y_b = (pos[1] >= y) and (pos[1] <= y + surface.get_height())
            if self.rect.collidepoint((pos[0] - x, pos[1] - y)) and x_b and y_b:
                action = True
                if not self.on_button:
                    self.on_button = True
                    if self.sound:
                        self.sound.play()
                press_text = self.font.render(self.string, False, press_color).convert_alpha()
                surface.blit(press_text, self.rect)
            else:
                self.on_button = False
                surface.blit(self.text, self.rect)
        else:
            surface.blit(self.text, self.rect)

        return action

    def typing(self, surface, game, max_symbols=15, set_left=False, set_right=False):
        self.temporary_string = ""
        screen = pg.Surface((SCREEN_HEIGHT, SCREEN_HEIGHT)).convert_alpha()
        typing = True
        while typing:
            screen.blit(surface, (0, 0))

            text = self.font.render(self.temporary_string, False, self.color).convert_alpha()
            text_rect = text.get_rect()

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE and len(self.temporary_string) > 0:
                        self.temporary_string = self.temporary_string[:-1]
                    elif event.key == settings.KEYS["BACK"]:
                        typing = False
                    elif event.key == settings.KEYS["ENTER"]:
                        if self.temporary_string:
                            self.string = self.temporary_string
                            self.text = self.font.render(self.string, False, self.color).convert_alpha()
                            self.rect = text_rect
                        typing = False
                    else:
                        if len(self.temporary_string) + 1 < max_symbols:
                            if event.key == pg.K_SPACE:
                                self.temporary_string += " "
                            elif event.key not in [pg.K_TAB, pg.K_LSHIFT, pg.K_CAPSLOCK, pg.K_RSHIFT]:
                                self.temporary_string += pg.key.name(event.key)

            if set_left:
                text_rect.midleft = self.rect.midleft
            elif set_right:
                text_rect.topright[0] = self.rect.topright[0]
            else:
                text_rect.center = self.rect.center

            if typing:
                screen.blit(text, text_rect)
                game.screen.blit(screen, (0, 0))
                game.blit_screen()

    def get_text_bar(self, surface, bar_color=(0, 0, 0, 230), block=False, surface_topleft=(0, 0), time=80, max_len=30):
        x, y = surface_topleft
        if not block:
            pos = pg.mouse.get_pos()
            if surface.collidepoint((pos[0] - x, pos[1] - y)) and self.string:
                current_time = pg.time.get_ticks()
                if current_time - self.last_update >= time:
                    if self.current_text != self.string:
                        self.current_text += self.string.replace(self.current_text, "", 1)[0]
                    self.last_update = pg.time.get_ticks()

                text = []
                bar_width = bar_height = 0
                for i in range(len(self.current_text) // max_len + 1):
                    string = self.current_text[i * max_len:(i+1) * max_len]
                    if string.startswith(" "):
                        string = string[1:]
                    text_string = Text(string, self.scale)

                    bar_width = max(bar_width, text_string.rect.width)
                    bar_height += (text_string.rect.height + 4)
                    text.append(text_string)

                bar = pg.Surface((bar_width + 4, bar_height), pg.SRCALPHA).convert_alpha()
                bar.fill((0, 0, 0, 0))

                for string in text:
                    string_bar = pg.Surface((string.rect.width + 4, string.rect.height + 4), pg.SRCALPHA).convert_alpha()
                    string_bar.fill(bar_color)
                    string.draw(string_bar, (2, string_bar.get_height() // 2), position="midleft")
                    bar.blit(string_bar, (0, text.index(string) * string_bar.get_height()))

                return bar, (pos[0] + 10, pos[1] + 10)
        self.current_text = ""
        return None
