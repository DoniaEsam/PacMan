

import pygame
import time


pygame.init()
size = (725, 525)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
start_time = time.time()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (238, 118, 0)
GOLD = (218, 165, 32)
PINK = (255, 192, 203)
AQUA = (0, 255, 255)
GRAY = (100, 100, 100)




crashed = False
start_game = False
ready = False
hit = False
lives = 3
blue = False
blue_time = 10
game_over = False
win = False
on = False
restart = False


start_button = None
exit_button = None
restart_button = None



def update_score(score):
    my_font = pygame.font.SysFont("broadway", 18)
    my_text = my_font.render("HIGH SCORE", True, WHITE, BLACK)
    screen.blit(my_text, (550, 50))
    my_text = my_font.render(str(score), True, WHITE, BLACK)
    screen.blit(my_text, (550, 75))


def update_clock(seconds):
    hours = str(int(seconds / 3600)).zfill(2)
    seconds %= 3600
    minutes = str(int(seconds / 60)).zfill(2)
    seconds %= 60
    seconds = str(seconds).zfill(2)

    my_font = pygame.font.SysFont("broadway", 18)
    my_text = my_font.render("TIME ELAPSED", True, WHITE, BLACK)
    screen.blit(my_text, (550, 150))
    my_text = my_font.render("{}:{}:{}".format(hours, minutes, seconds), True, WHITE, BLACK)
    screen.blit(my_text, (550, 175))


def update_lives():
    my_font = pygame.font.SysFont("broadway", 18)
    my_text = my_font.render("LIVES", True, WHITE, BLACK)
    screen.blit(my_text, (550, 250))

    image = pygame.image.load("pacman.png")
    x = 550
    for i in range(lives):
        screen.blit(image, [x, 275])
        x += 30


