
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
        super().__init__()

        self.image = pygame.image.load("pacman.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.move_x = 0
        self.move_y = 0

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


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color, name):
        super().__init__()
        self.name = name

        self.image = pygame.Surface([25, 25])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.move_x = 0
        self.move_y = 0
        self.walls = None
        self.friends = None

        self.moveUp = True
        self.moveDown = True
        self.moveLeft = True
        self.moveRight = True

    def can_move(self, direction):
        if direction == 0:
            test = self.rect.move((1, 0))
        elif direction == 1:
            test = self.rect.move((-1, 0))
        elif direction == 2:
            test = self.rect.move((0, 1))
        elif direction == 3:
            test = self.rect.move((0, -1))

        for wall in self.walls:
            if wall.rect.colliderect(test):
                return False
        return True

    def change_speed(self):
        priority = ["", "", "", ""]
        x_disp = pacman.rect.x - self.rect.x
        y_disp = pacman.rect.y - self.rect.y

        if abs(x_disp) > abs(y_disp):
            if x_disp >= 0:
                priority[0] = "right"
                priority[2] = "left"
            elif x_disp < 0:
                priority[0] = "left"
                priority[2] = "right"

            if y_disp >= 0:
                priority[1] = "down"
                priority[3] = "up"
            elif y_disp < 0:
                priority[1] = "up"
                priority[3] = "down"
        elif abs(y_disp) > abs(x_disp):
            if y_disp >= 0:
                priority[0] = "down"
                priority[2] = "up"
            elif y_disp < 0:
                priority[0] = "up"
                priority[2] = "down"

            if x_disp >= 0:
                priority[1] = "right"
                priority[3] = "left"
            elif x_disp < 0:
                priority[1] = "left"
                priority[3] = "right"

        """
        if blue:
            priority = priority[::-1]
        """

        for direction in priority:
            if direction == "right":
                if self.can_move(0):
                    self.move_x = 1
                    break
            elif direction == "left":
                if self.can_move(1):
                    self.move_x = -1
                    break
            elif direction == "down":
                if self.can_move(2):
                    self.move_y = 1
                    break
            elif direction == "up":
                if self.can_move(3):
                    self.move_y = -1
                    break

    def update(self):
        """ Update the ghost position. """
        self.rect.x += self.move_x

        if self.rect.x == 0 and self.rect.y == 225 and self.move_x < 0:
            self.rect.x = 500
        if self.rect.x == 500 and self.rect.y == 225 and self.move_x > 0:
            self.rect.x = 0

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.move_x >= 0:
                self.rect.right = block.rect.left
            elif self.move_x < 0:
                self.rect.left = block.rect.right
        ghost_hit_list = pygame.sprite.spritecollide(self, self.friends, False)
        for friend in ghost_hit_list:
            if self.move_x >= 0:
                self.rect.right = friend.rect.left
            elif self.move_x < 0:
                self.rect.left = friend.rect.right
            self.move_x *= -1

        self.rect.y += self.move_y

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            if self.move_y >= 0:
                self.rect.bottom = block.rect.top
            elif self.move_y < 0:
                self.rect.top = block.rect.bottom
        ghost_hit_list = pygame.sprite.spritecollide(self, self.friends, False)
        for friend in ghost_hit_list:
            if self.move_y >= 0:
                self.rect.bottom = friend.rect.top
            elif self.move_y < 0:
                self.rect.top = friend.rect.bottom
            self.move_y *= -1
            
            
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        
class Pellet(pygame.sprite.Sprite):
    def __init__(self, position, radius):
        super().__init__()
        self.image = pygame.Surface([radius, radius])
        self.image.fill(WHITE)
        self.rect = pygame.Rect(position[0]-10, position[1]-10, 5, 5)
        
class Button:
    def __init__(self, text, x, y):
        self.start_game = False
        self.crashed = False
        self.text = text
        my_font = pygame.font.SysFont("broadway", 18)
        my_text = my_font.render(text, True, RED)
        screen.blit(my_text, (x, y))
        text_rect = my_text.get_rect()
        self.rect = pygame.Rect(x-3, y-3, text_rect.width+6, text_rect.height+6)
        pygame.draw.rect(screen, WHITE, self.rect, 0)
        pygame.draw.rect(screen, YELLOW, self.rect, 3)
        screen.blit(my_text, (x, y))

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        global start_game
        global game_over
        global restart

        if self.rect.collidepoint(event.pos):
            if self.text == "START":
                beginning_channel.play(beginning)
                start_game = True
            elif self.text == "RESTART":
                reset()
                restart = True
                start_game = True
                game_over = False
            else:
                quit()
                

