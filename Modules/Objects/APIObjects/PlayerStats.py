from Modules.Objects.GUIObjects.Sheet import get_sheet
from Modules.Objects.GUIObjects.Picture import Picture
from Modules.Objects.GUIObjects.Text import Text
from .Settings import settings
import pygame as pg
import os


class PlayerStats:
    def __init__(self, coins_scale=4):

        self.coins_scale = coins_scale
        self.coins_image = pg.image.load("Resources/Images/Hud/coins/MonedaD.png").convert_alpha()
        self.coins_sheets = get_sheet(self.coins_image, 5, self.coins_scale)
        self.frame = 0

        self.level_bar = []
        for file in sorted(os.listdir("Resources/Images/Hud/LevelBar/")):
            if file[-4:] == ".png":
                self.level_bar.append(Picture("Resources/Images/Hud/LevelBar/" + file, scale=2))

        self.start_level = 1000
        self.delta_level = 100

        self.last_update_time_in_game = 0

        self.last_update = pg.time.get_ticks()

        self.coins_sheets_mini = get_sheet(self.coins_image, 5, 1)
        self.last_update_mini = pg.time.get_ticks()
        self.frame_mini = 0

    def draw_coins(self, surface, coordinates, time=250, position="center"):
        current_time = pg.time.get_ticks()
        if current_time - self.last_update >= time:
            self.frame += 1
            self.last_update = current_time
            if self.frame == len(self.coins_sheets):
                self.frame = 0

        coin_rect = self.coins_sheets[self.frame].get_rect()
        coin_val = Text(str(settings.player_stats["coins"]), self.coins_scale * 10)

        setattr(coin_rect, position, coordinates)
        surface.blit(self.coins_sheets[self.frame], coin_rect)
        coin_val.draw(surface, (coin_rect.midright[0] + 5, coin_rect.midright[1]), position="midleft")

    def draw_level(self, surface, coordinates, position="center"):
        start_level = self.start_level
        delta_level = self.delta_level

        max_score = start_level + delta_level * settings.player_stats["level"]

        curr_score = settings.player_stats["score"] - (
                (start_level + (start_level + delta_level * (settings.player_stats["level"] - 1))) *
                settings.player_stats["level"]) // 2

        score = Text("LVL: " + str(settings.player_stats["level"]) + " - " + str(curr_score) + "/" + str(max_score), 20)

        curr_level = 0
        while curr_level * (max_score / len(self.level_bar)) < curr_score:
            if curr_level + 1 < len(self.level_bar):
                curr_level += 1
            else:
                break

        self.level_bar[curr_level].draw(surface, coordinates, position=position)
        score.draw(surface, (self.level_bar[curr_level].rect.bottomright[0], self.level_bar[curr_level].rect.bottomright[1] + 10), position="topleft")

    def increase_score(self, value):
        start_level = self.start_level
        delta_level = self.delta_level
        max_score = ((start_level + (start_level + delta_level * settings.player_stats["level"])) *
                     (settings.player_stats["level"] + 1)) // 2
        settings.player_stats["score"] += value
        curr_score = settings.player_stats["score"]
        if curr_score >= max_score:
            settings.player_stats["level"] += 1
            return self.increase_score(0)
        return 0

    @property
    def coins(self):
        return settings.player_stats["coins"]

    @coins.setter
    def coins(self, value):
        settings.player_stats["coins"] = value

    def update_time_in_game(self):
        settings.player_stats["time_in_game"] += pg.time.get_ticks() - self.last_update_time_in_game
        self.last_update_time_in_game = pg.time.get_ticks()

    @property
    def time_in_game(self):
        self.update_time_in_game()
        time = settings.player_stats["time_in_game"]
        return f'{(time // 86400000):03}' + ":" + f'{((time % 86400000) // 3600000):02}' + ":" + f'{((time % 3600000) // 60000):02}'

    def show_cost(self, surface, cost, surface_topleft=(0, 0), position="midleft"):
        bar = pg.Surface((80, 30), pg.SRCALPHA).convert_alpha()

        cost_text = Text(str(cost), 20)

        if cost <= settings.player_stats["coins"]:
            bar.fill((76, 175, 80, 235))
            afford = True
        else:
            bar.fill((213, 0, 0, 235))
            afford = False

        current_time = pg.time.get_ticks()
        if current_time - self.last_update_mini >= 250:
            self.frame_mini += 1
            self.last_update_mini = current_time
            if self.frame_mini == len(self.coins_sheets_mini):
                self.frame_mini = 0

        coin_rect = self.coins_sheets_mini[self.frame_mini].get_rect()
        setattr(coin_rect, position, (7, bar.get_height() // 2))

        x, y = surface_topleft
        pos = list(pg.mouse.get_pos())
        pos[0], pos[1] = pos[0] - x, pos[1] - y

        bar.blit(self.coins_sheets_mini[self.frame_mini], coin_rect)
        cost_text.draw(bar, (bar.get_width() - 7, bar.get_height() // 2), position="midright")
        surface.blit(bar, pos)

        return afford
