import pygame
import pygame as pg

pygame.init()

screen = pygame.display.set_mode((1280, 720))
screen.fill((99, 156, 247))
pygame.display.set_caption("00 Racing")

clock = pg.time.Clock()

action = True

start_button = pygame.Surface((200, 100), 10)
start_button.fill((255, 255, 255))

myfont = pygame.font.Font("fonts/itim.ttf", 60)
start_button_text = myfont.render("START", True, (255, 43, 72))

background = pygame.image.load("images/background1.png")

bg_sound = pygame.mixer.Sound("audio/music.mp3")
bg_sound.play()

motor_sound = pygame.mixer.Sound("audio/motor_sound.mp3")

while action:

    pygame.display.update()

    screen.blit(background, (0, 0))
    screen.blit(start_button, (100, 100))
    screen.blit(start_button_text, (110, 110))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            action = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                motor_sound.play()

    clock.tick(30)
