from game import Game
from settings import *

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

settings.update_all()
