import pygame as pg
from game import Game

pg.mixer.pre_init(44100, 16, 2, 4096)

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

'''
pg.init()

FPS = 30
FramePerSec = pg.time.Clock()

WIDTH = 1280
HEIGHT = 720

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill((99, 156, 247))
pg.display.set_caption("00 Racing")


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/car_down.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, HEIGHT - 40), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


E1 = Enemy()
action = True

start_button_color = (228, 50, 35)
start_button = pg.Surface((250, 100), 10)

start_button_rect = start_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))

title_font = pg.font.Font("fonts/pixfont.ttf", 100)
other_font = pg.font.Font("fonts/pixfont.ttf", 80)

title_text = title_font.render("00 RACING", False, (255, 255, 255))
title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 6))

start_text_color = (255, 255, 255)
start_text = other_font.render("START", False, start_text_color)
start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

background = pg.image.load("images/background2.png").convert()
background_x = 0

playList = ["audio/Motley Crue - Girls.mp3", "audio/RADIOTAPOK - Monster.mp3"]
current_song = random.choice(playList)

while action:

    SCREEN.blit(background, (background_x + 0, 0))
    SCREEN.blit(background, (background_x + 1280, 0))

    # screen.blit(start_button, (95, 95))
    SCREEN.blit(title_text, title_text_rect)
    SCREEN.blit(start_button, start_button_rect)
    SCREEN.blit(start_text, start_text_rect)

    mouse_x, mouse_y = pg.mouse.get_pos()
    in_button_x = WIDTH // 2 - start_button.get_width() // 2 <= mouse_x <= WIDTH // 2 + start_button.get_width() // 2
    in_button_y = HEIGHT // 2 - start_button.get_height() // 2 <= mouse_y <= WIDTH // 2 + start_button.get_height() // 2

    for event in pg.event.get():
        if event.type == pg.QUIT:
            action = False

        elif event.type == pg.MOUSEBUTTONUP:
            if in_button_x and in_button_y:
                music_change(playList, current_song)

    if in_button_x and in_button_y:
        start_button_color = (100, 100, 100)
        start_button.fill(start_button_color)
    else:
        start_button_color = (228, 50, 35)
        start_button.fill(start_button_color)

    background_x -= 2
    if background_x == - 1280:
        background_x = 0

    E1.move()
    E1.draw(SCREEN)

    pg.display.update()
    FramePerSec.tick(FPS)

pg.quit()
sys.exit()
'''
