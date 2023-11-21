import pygame as pg
from game import Game

pg.mixer.pre_init(44100, 16, 2, 4096)

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
