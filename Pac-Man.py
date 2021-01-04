

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


class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set the width and height of Pac-Man
        self.image = pygame.image.load("pacman.png").convert_alpha()

        # Make our top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector.
        self.move_x = 0
        self.move_y = 0

        # Set collision sprites
        self.walls = None
        self.pellets = None
        self.power_pellets = None
        self.ghosts = None

        self.score = 0
        self.win = False

    def change_speed(self, x, y):
        if not hit:
            self.move_x += x
            self.move_y += y
        else:
            self.move_x = 0
            self.move_y = 0

    def update(self):
        global hit
        global blue
        global lives
        global game_over

        # Move left/right
        self.rect.x += self.move_x

        if self.rect.x == 0 and self.rect.y == 225 and self.move_x < 0:
            self.rect.x = 500

        if self.rect.x == 500 and self.rect.y == 225 and self.move_x > 0:
            self.rect.x = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.move_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        self.rect.y += self.move_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            if self.move_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        pellet_hit_list = pygame.sprite.spritecollide(self, self.pellets, False)
        for pellet in pellet_hit_list:
            self.score += 10
            update_score(self.score)
            all_sprite_list.remove(pellet)
            pellet_list.remove(pellet)
            self.pellets.remove(pellet)

        power_pellet_hit_list = pygame.sprite.spritecollide(self, self.power_pellets, False)
        for power_pellet in power_pellet_hit_list:
            self.score += 50
            update_score(self.score)
            all_sprite_list.remove(power_pellet)
            power_pellet_list.remove(power_pellet)
            self.power_pellets.remove(power_pellet)
            blue = True

        ghost_hit_list = pygame.sprite.spritecollide(self, self.ghosts, False)
        if len(ghost_hit_list) != 0:
            hit = True
            lives -= 1
            if lives <= 0:
                all_sprite_list.remove(pacman)
                game_over = True

        if len(pellet_list) == 0:
            self.win = True
