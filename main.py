import pygame
import pygame as pg

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pg.time.Clock()

action = True

bg_sound = pygame.mixer.Sound("audio/music1.mp3")
bg_sound.play()

while action:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            action = False
            pygame.quit()

    clock.tick(30)
