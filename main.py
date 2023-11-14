import pygame
import pygame as pg

pygame.init()

W = 1280
H = 720
screen = pygame.display.set_mode((W, H))
screen.fill((99, 156, 247))
pygame.display.set_caption("00 Racing")

clock = pg.time.Clock()

action = True

start_button = pygame.Surface((250, 100), 10)
start_button.fill((250, 60, 85))
start_button_rect = start_button.get_rect(center=(W // 2, H // 2))


title_font = pygame.font.Font("fonts/pixfont.ttf", 100)
other_font = pygame.font.Font("fonts/pixfont.ttf", 80)

title_text = title_font.render("00 RACING", False, (255, 255, 255))
title_text_rect = title_text.get_rect(center=(W // 2, H // 6))

start_text = other_font.render("START", False, (255, 255, 255))
start_text_rect = start_text.get_rect(center=(W // 2, H // 2))

background = pygame.image.load("images/background2.png")
background_x = 0

bg_sound = pygame.mixer.Sound("audio/maintheme.mp3")
bg_sound.set_volume(0.5)
bg_sound.play(10)

motor_sound = pygame.mixer.Sound("audio/motor_sound.mp3")
#skype_sound = pygame.mixer.Sound("audio/skype.mp3")

while action:

    pygame.display.update()

    screen.blit(background, (background_x + 0, 0))
    screen.blit(background, (background_x + 1280, 0))

    #screen.blit(start_button, (95, 95))
    screen.blit(title_text, title_text_rect)
    screen.blit(start_button, start_button_rect)
    screen.blit(start_text, start_text_rect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            action = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                motor_sound.play()
                #skype_sound.play()

    background_x -= 2
    if background_x == - 1280:
        background_x = 0

    clock.tick(30)
