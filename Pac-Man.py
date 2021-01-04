
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

                all_sprite_list = None
pacman = None
blinky = None
pinky = None
inky = None
clyde = None
ghost_list = None
wall_list = None
pellet_list = None
power_pellet_list = None



def reset():
    global lives

    global all_sprite_list
    global pacman
    global ghost_list
    global wall_list
    global pellet_list
    global power_pellet_list

    global blinky
    global pinky
    global inky
    global clyde

    lives = 3
    
    all_sprite_list = pygame.sprite.Group()

   
    pacman = PacMan(250, 375)
    all_sprite_list.add(pacman)

    
    pellet_list = pygame.sprite.Group()
    pellets_positions = [[62, 37], [87, 37], [112, 37], [137, 37], [162, 37], [187, 37], [212, 37], [237, 37],
                         [287, 37],
                         [312, 37], [337, 37], [362, 37], [387, 37], [412, 37], [437, 37], [462, 37], [62, 62],
                         [137, 62],
                         [237, 62], [287, 62], [387, 62], [462, 62], [62, 87], [87, 87], [112, 87], [137, 87],
                         [162, 87],
                         [187, 87], [212, 87], [237, 87], [262, 87], [287, 87], [312, 87], [337, 87], [362, 87],
                         [387, 87],
                         [412, 87], [437, 87], [462, 87], [62, 112], [137, 112], [187, 112], [337, 112], [387, 112],
                         [462, 112], [62, 137], [87, 137], [112, 137], [137, 137], [187, 137], [212, 137], [237, 137],
                         [287, 137], [312, 137], [337, 137], [387, 137], [412, 137], [437, 137], [462, 137], [137, 162],
                         [387, 162], [137, 187], [387, 187], [137, 212], [387, 212], [137, 237], [387, 237], [137, 262],
                         [387, 262], [137, 287], [387, 287], [137, 312], [387, 312], [62, 337], [87, 337], [112, 337],
                         [137, 337], [162, 337], [187, 337], [212, 337], [237, 337], [287, 337], [312, 337], [337, 337],
                         [362, 337], [387, 337], [412, 337], [437, 337], [462, 337], [62, 362], [137, 362], [237, 362],
                         [287, 362], [387, 362], [462, 362], [62, 387], [87, 387], [137, 387], [162, 387], [187, 387],
                         [212, 387], [237, 387], [287, 387], [312, 387], [337, 387], [362, 387], [387, 387], [437, 387],
                         [462, 387], [87, 412], [137, 412], [187, 412], [337, 412], [387, 412], [437, 412], [62, 437],
                         [87, 437], [112, 437], [137, 437], [187, 437], [212, 437], [237, 437], [287, 437], [312, 437],
                         [337, 437], [387, 437], [412, 437], [437, 437], [462, 437], [62, 462], [237, 462], [287, 462],
                         [462, 462], [62, 487], [87, 487], [112, 487], [137, 487], [162, 487], [187, 487], [212, 487],
                         [237, 487], [262, 487], [287, 487], [312, 487], [337, 487], [362, 487], [387, 487], [412, 487],
                         [437, 487], [462, 487]]
    
    pellets_positions.remove([62, 37])
    pellets_positions.remove([462, 37])
    pellets_positions.remove([62, 487])
    pellets_positions.remove([462, 487])

    for i in pellets_positions:
        i = [i[0] + 10, i[1] + 10]
        newPellet = Pellet(i, 5)
        all_sprite_list.add(newPellet)
        pellet_list.add(newPellet)
    pacman.pellets = pellet_list

    """"""
    power_pellet_list = pygame.sprite.Group()
    power_pellet_positions = [[60, 35], [458, 35], [60, 483], [458, 483]]
    for i in power_pellet_positions:
        i = [i[0] + 7, i[1] + 7]
        newPellet = Pellet(i, 15)
        all_sprite_list.add(newPellet)
        power_pellet_list.add(newPellet)

    pacman.power_pellets = power_pellet_list
    """"""

    
    ghost_list = pygame.sprite.Group()

    blinky = Ghost(250, 175, RED, "BLINKY")
    ghost_list.add(blinky)
    all_sprite_list.add(blinky)

    pinky = Ghost(225, 225, PINK, "PINKY")
    ghost_list.add(pinky)
    all_sprite_list.add(pinky)

    inky = Ghost(250, 225, AQUA, "INKY")
    ghost_list.add(inky)
    all_sprite_list.add(inky)

    clyde = Ghost(275, 225, ORANGE, "CLYDE")
    ghost_list.add(clyde)
    all_sprite_list.add(clyde)

    
    pacman.ghosts = ghost_list

    blinky.friends = ghost_list.copy()
    blinky.friends.remove(blinky)

    pinky.friends = ghost_list.copy()
    pinky.friends.remove(pinky)

    inky.friends = ghost_list.copy()
    inky.friends.remove(inky)

    clyde.friends = ghost_list.copy()
    clyde.friends.remove(clyde)

    
    wall_list = pygame.sprite.Group()
    walls_dimensions = [[25, 0, 475, 25], [25, 0, 25, 175], [25, 150, 100, 25], [100, 150, 25, 75], [0, 200, 125, 25],
                        [0, 250, 125, 25], [100, 250, 25, 75], [25, 300, 100, 25], [25, 300, 25, 225], [50, 400, 25, 25],
                        [25, 500, 475, 25], [450, 400, 25, 25], [475, 300, 25, 225], [400, 300, 100, 25],
                        [400, 250, 25, 75], [400, 250, 125, 25], [400, 200, 125, 25], [400, 150, 25, 75],
                        [400, 150, 100, 25], [475, 0, 25, 175], [250, 0, 25, 75], [75, 50, 50, 25], [150, 50, 75, 25],
                        [300, 50, 75, 25], [400, 50, 50, 25], [75, 100, 50, 25], [150, 100, 25, 125], [200, 100, 125, 25],
                        [350, 100, 25, 125], [400, 100, 50, 25], [250, 100, 25, 75], [150, 150, 75, 25],
                        [300, 150, 75, 25], [200, 200, 50, 25], [275, 200, 50, 25], [200, 200, 25, 75], [300, 200, 25, 75],
                        [200, 250, 125, 25], [150, 250, 25, 75], [350, 250, 25, 75], [200, 300, 125, 25],
                        [250, 300, 25, 75], [75, 350, 50, 25], [100, 350, 25, 75], [150, 350, 75, 25], [300, 350, 75, 25],
                        [400, 350, 50, 25], [400, 350, 25, 75], [150, 400, 25, 75], [350, 400, 25, 75],
                        [200, 400, 125, 25], [250, 400, 25, 75], [75, 450, 150, 25], [300, 450, 150, 25]]
    for i in walls_dimensions:
        newWall = Wall(i[0], i[1], i[2], i[3], BLUE)
        all_sprite_list.add(newWall)
        wall_list.add(newWall)

    pacman.walls = wall_list.copy()
    blinky.walls = wall_list.copy()
    blinky.walls.add(Wall(250, 200, 25, 25, BLUE))
    pinky.walls = wall_list.copy()
    pinky.walls.add(Wall(275, 225, 25, 25, BLUE))
    inky.walls = wall_list.copy()
    inky.walls.add(Wall(225, 225, 25, 25, BLUE))
    inky.walls.add(Wall(275, 225, 25, 25, BLUE))
    clyde.walls = wall_list.copy()
    clyde.walls.add(Wall(225, 225, 25, 25, BLUE))


def start_again():
    global pacman
    global blinky
    global pinky
    global inky
    global clyde

    pacman.rect.x = 250
    pacman.rect.y = 375

    pacman.moveUp = True
    pacman.moveDown = True
    pacman.moveLeft = True
    pacman.moveRight = True

    blinky.rect.x = 250
    blinky.rect.y = 175
    pinky.rect.x = 225
    pinky.rect.y = 225
    inky.rect.x = 250
    inky.rect.y = 225
    clyde.rect.x = 275
    clyde.rect.y = 225


def title_screen():
    global start_button

    x = 250
    y = 100
    my_font = pygame.font.SysFont("broadway", 36)
    my_text = my_font.render("PAC-MAN", True, GOLD, ORANGE)
    text_rect = my_text.get_rect()
    rect = pygame.Rect(x-6, y-6, text_rect.width+12, text_rect.height+12)
    pygame.draw.rect(screen, RED, rect)
    screen.blit(my_text, (x, y))

    my_font = pygame.font.SysFont("broadway", 18)
    image = pygame.image.load("pacman.png")
    screen.blit(image, [25, 50])
    my_text = my_font.render("- Pac-Man", True, YELLOW, BLACK)
    screen.blit(my_text, (60, 50))
    pygame.draw.rect(screen, WHITE, (25, 110, 5, 5))
    my_text = my_font.render("- 10 points", True, WHITE, BLACK)
    screen.blit(my_text, (40, 100))
    pygame.draw.rect(screen, WHITE, (25, 135, 15, 15))
    my_text = my_font.render("- 50 points", True, WHITE, BLACK)
    screen.blit(my_text, (50, 130))
    pygame.draw.rect(screen, RED, (550, 50, 25, 25))
    my_text = my_font.render("- Blinky", True, RED, BLACK)
    screen.blit(my_text, (585, 50))
    pygame.draw.rect(screen, PINK, (550, 80, 25, 25))
    my_text = my_font.render("- Pinky", True, PINK, BLACK)
    screen.blit(my_text, (585, 80))
    pygame.draw.rect(screen, AQUA, (550, 110, 25, 25))
    my_text = my_font.render("- Inky", True, AQUA, BLACK)
    screen.blit(my_text, (585, 110))
    pygame.draw.rect(screen, ORANGE, (550, 140, 25, 25))
    my_text = my_font.render("- Clyde", True, ORANGE, BLACK)
    screen.blit(my_text, (585, 140))

    my_font = pygame.font.SysFont("broadway", 18)
    my_text = my_font.render("Use the arrow keys to move Pac-Man.", True, (0, 100, 255), BLACK)
    screen.blit(my_text, (150, 200))
    my_text = my_font.render("Eat all pellets to win the game.", True, (0, 100, 255), BLACK)
    screen.blit(my_text, (180, 225))
    my_text = my_font.render("Avoid the ghosts at all costs.", True, (0, 100, 255), BLACK)
    screen.blit(my_text, (190, 250))
    my_text = my_font.render("Have fun, and good luck!", True, (0, 100, 255), BLACK)
    screen.blit(my_text, (210, 275))
    my_text = my_font.render("Press Escape anytime to quit the game", True, (0, 100, 255), BLACK)
    screen.blit(my_text, (140, 300))

    start_button = Button("START", 310, 400)


def game_over_screen():
    global restart_button

    my_font = pygame.font.SysFont("broadway", 36)
    my_text = my_font.render("GAME OVER", True, RED, BLACK)
    screen.blit(my_text, [250, 150])

    image = pygame.image.load("pacman.png")
    screen.blit(image, [350, 250])
    pygame.draw.rect(screen, RED, (350, 225, 25, 25))
    pygame.draw.rect(screen, PINK, (325, 250, 25, 25))
    pygame.draw.rect(screen, AQUA, (375, 250, 25, 25))
    pygame.draw.rect(screen, ORANGE, (350, 275, 25, 25))

    my_font = pygame.font.SysFont("broadway", 18)
    my_text = my_font.render("Better luck next time...", True, (0, 100, 255), BLACK)
    screen.blit(my_text, [250, 325])

    restart_button = Button("RESTART", 320, 425)


reset()
title_screen()
while not crashed:
    for event in pygame.event.get():
        start_button.get_event(event)

        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("LEFT")
                pacman.change_speed(-1, 0)
            elif event.key == pygame.K_RIGHT:
                print("RIGHT")
                pacman.change_speed(1, 0)
            elif event.key == pygame.K_UP:
                print("UP")
                pacman.change_speed(0, -1)
            elif event.key == pygame.K_DOWN:
                print("DOWN")
                pacman.change_speed(0, 1)
            elif event.key == pygame.K_ESCAPE:
                crashed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                print("LEFT")
                pacman.change_speed(1, 0)
            elif event.key == pygame.K_RIGHT:
                print("RIGHT")
                pacman.change_speed(-1, 0)
            elif event.key == pygame.K_UP:
                print("UP")
                pacman.change_speed(0, 1)
            elif event.key == pygame.K_DOWN:
                print("DOWN")
                pacman.change_speed(0, -1)

    
    if start_game:
        for ghost in ghost_list:
            ghost.change_speed()
        all_sprite_list.update()
        screen.fill(BLACK)
        all_sprite_list.draw(screen)

        if beginning_channel.get_busy():
            my_font = pygame.font.SysFont("broadway", 18)
            my_text = my_font.render("READY!", True, YELLOW, BLACK)
            screen.blit(my_text, (230, 275))

        update_score(pacman.score)
        update_clock(int(time.time() - start_time))
        update_lives()
    else:
        start_time = time.time()

    if hit:
        hit = False
        while death_channel.get_busy():
            time.sleep(1)
        start_again()

        all_sprite_list.update()
        screen.fill(BLACK)
        all_sprite_list.draw(screen)
        update_score(pacman.score)
        update_clock(int(time.time() - start_time))

   
    if game_over:
        start_game = False
        screen.fill(BLACK)
        while death_channel.get_busy():
            time.sleep(1)
        game_over_screen()
        for event in pygame.event.get():
            restart_button.get_event(event)

    
    if pacman.win:
        start_game = False
        for ghost in ghost_list:
            all_sprite_list.remove(ghost)
        all_sprite_list.remove(pacman)

        my_font = pygame.font.SysFont("broadway", 18)
        if not on:
            my_text = my_font.render("YOU WIN!", True, GREEN, BLACK)
            on = True
            clock.tick(3)
        else:
            my_text = my_font.render("                        ", True, GREEN, BLACK)
            on = False
            clock.tick(3)
        screen.blit(my_text, (575, 300))

    if restart:
        restart = False
        pygame.display.flip()
        

    pygame.display.flip()

    while title_channel.get_busy():
        time.sleep(1)
        start_time = time.time()
    while beginning_channel.get_busy():
        time.sleep(1)
        start_time = time.time()

    clock.tick(60)
                

