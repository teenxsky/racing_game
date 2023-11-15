import pygame
import pygame as pg

pygame.init()


def music_change(playList, number_of_song):
    i = number_of_song
    if i == len(playList):
        i = 0
    current_song = playList[i]
    current_song.play(-1)
    current_song.set_volume(0.5)


W = 1280
H = 720
screen = pygame.display.set_mode((W, H))
screen.fill((99, 156, 247))
pygame.display.set_caption("00 Racing")

clock = pg.time.Clock()

action = True

start_button_color = (228, 50, 35)
start_button = pygame.Surface((250, 100), 10)

start_button_rect = start_button.get_rect(center=(W // 2, H // 2))

title_font = pygame.font.Font("fonts/pixfont.ttf", 100)
other_font = pygame.font.Font("fonts/pixfont.ttf", 80)

title_text = title_font.render("00 RACING", False, (255, 255, 255))
title_text_rect = title_text.get_rect(center=(W // 2, H // 6))

start_text_color = (255, 255, 255)
start_text = other_font.render("START", False, start_text_color)
start_text_rect = start_text.get_rect(center=(W // 2, H // 2))

background = pygame.image.load("images/background2.png")
background_x = 0

playList = [pygame.mixer.Sound("audio/maintheme.mp3"), pygame.mixer.Sound("audio/music.mp3")]
number_of_song = 0

motor_sound = pygame.mixer.Sound("audio/motor_sound.mp3")
# skype_sound = pygame.mixer.Sound("audio/skype.mp3")

while action:

    pygame.display.update()

    screen.blit(background, (background_x + 0, 0))
    screen.blit(background, (background_x + 1280, 0))

    # screen.blit(start_button, (95, 95))
    screen.blit(title_text, title_text_rect)
    screen.blit(start_button, start_button_rect)
    screen.blit(start_text, start_text_rect)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    in_button_x = W // 2 - start_button.get_width() // 2 <= mouse_x <= W // 2 + start_button.get_width() // 2
    in_button_y = H // 2 - start_button.get_height() // 2 <= mouse_y <= W // 2 + start_button.get_height() // 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            action = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                motor_sound.play()
                # skype_sound.play()
        elif event.type == pygame.MOUSEBUTTONUP:
            if in_button_x and in_button_y:
                music_change(playList, number_of_song)
                number_of_song += 1

    if in_button_x and in_button_y:
        start_button_color = (100, 100, 100)
        start_button.fill(start_button_color)
    else:
        start_button_color = (228, 50, 35)
        start_button.fill(start_button_color)

    background_x -= 2
    if background_x == - 1280:
        background_x = 0

    clock.tick(30)
