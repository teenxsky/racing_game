from game import Game
from settings import *


g = Game()

while g.running:
    g.main_menu.display_menu()
    g.game_loop()

pg.quit()
settings.update_all()
