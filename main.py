import pygame
import pygame as pg

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pg.time.Clock()

action = True

while action:

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            action = False
            pygame.quit()

    clock.tick(30)
