from os import path
import pygame
import random
pygame.init()
joke = pygame.mixer.Sound(path.join( 'game-over-super-mario-made-with-Voicemod (mp3cut.net).mp3'))
joke.set_volume(5)
# Setting the width and length of the screen in variables
W = 800
H = 600
# adding music
pygame.mixer.music.load("super-mario-saundtrek.mp3")
pygame.mixer.music.play(-1)
# create the screen itself
screen = pygame.display.set_mode((W, H))
# create a frames per second counter
FPS = 60
# clock object
clock = pygame.time.Clock()

# creating all the necessary variables (font, game_over which will indicate loss or not)
font_path = 'SuperMario256.ttf'
font_xsmall = pygame.font.SysFont('arial_bold', 36)
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)

game_over = False
# surfaces that will appear when losing and their location on the screen
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W // 2, H // 2)
# Game over
retry_text1 = font_small.render('GAME OVER', True, (255, 255, 255))
retry_rect1 = retry_text1.get_rect()
retry_rect1.midtop = (400, 220)
# adding a button file about game mechanics information
info_image = pygame.image.load('cnopka3llp.png')
info_image = pygame.transform.scale(info_image, (160, 40))
retry_rect2 = info_image.get_rect()
retry_rect2.midtop = (W // 2, H - 50)

show_info_window = False
# text for information dies
info_text = font_small.render('Information', True, (255, 255, 255))
info_rect = info_text.get_rect()
info_rect.midtop = (W // 2, 200)
info_text1 = font_xsmall.render('Робота студента', True, (255, 255, 255))
info_rect1 = info_text1.get_rect()
info_rect1.midtop = (W // 2 - 90, 220)
info_text2 = font_xsmall.render('групи ІПЗ-21/9д', True, (255, 255, 255))
info_rect2 = info_text2.get_rect()
info_rect2.midtop = (W // 2 - 95, 250)
info_text3 = font_xsmall.render('Задої Володимира', True, (255, 255, 255))
info_rect3 = info_text3.get_rect()
info_rect3.midtop = (W // 2 - 75, 280)
info_text4 = font_xsmall.render('Управління', True, (255, 255, 255))
info_rect4 = info_text4.get_rect()
info_rect4.midtop = (W // 2, 320)
info_text5 = font_xsmall.render('A,D - Відвертання від Гумби', True, (255, 255, 255))
info_rect5 = info_text5.get_rect()
info_rect5.midtop = (W // 2 - 20, 350)
info_text6 = font_xsmall.render('SPACE - Прижок', True, (255, 255, 255))
info_rect6 = info_text6.get_rect()
info_rect6.midtop = (W // 2 - 90, 380)
info_window_rect = pygame.Rect(W // 2 - 200, H // 2 - 115, 400, 230)

# adding trees and editing them to the desired size
tree_image = pygame.image.load('images_tree.png')
tree_image = pygame.transform.scale(tree_image, (100, 140))
tree_image1 = pygame.image.load('images_tree.png')
tree_image1 = pygame.transform.scale(tree_image1, (100, 140))

# adding clouds and editing them to the desired size
cloud_image = pygame.image.load('pixel-art-cloud-vector-icon-for-8bit-game-on-white-background_360488-650.jpg.png')
cloud_image = pygame.transform.scale(cloud_image, (100, 100))
cloud_image1 = pygame.image.load('pixel-art-cloud-vector-icon-for-8bit-game-on-white-background_360488-650.jpg.png')
cloud_image1 = pygame.transform.scale(cloud_image1, (100, 100))

# adding a land file and editing it to the required dimensions
ground_image = pygame.image.load('Снимок экрана 2024-05-04 в 17.27.10.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

# adding the uev,s file and editing it to the desired size
enemy = pygame.image.load('gimi.png')
enemy = pygame.transform.scale(enemy, (80, 80))

# adding a dead goomba file and editing it to the desired size
enemy_image = pygame.image.load('goomba_mini.png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))

# adding a mario file and editing it to the desired size
player_image_right = pygame.image.load('images1.png')
player_image_right = pygame.transform.scale(player_image_right, (80, 60))
player_image_left = pygame.transform.flip(player_image_right, True, False)

# ////////////////////////////////////////////////////////////////////////////////////////////////
# class for declaring entities (Mario, Goomba)
class Entity:
    # creating the main constructor function and creating variables in it for the Mario or Goomba drawing, speed
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        # speed in x and y
        self.x_speed = 0
        self.y_speed = 0

        self.speed = 5  # main speed
        # variables to check whether we fell into the abyss or whether we are alive or not
        self.is_out = False
        self.is_dead = False
        # jump speed
        self.jump_speed = -12
        # speed of gravity
        self.gravity = 0.4
        # variable so that we know whether we are on the ground or not
        self.is_grounded = False

    # function to manage user input. It will be empty, but I will predetermine it for the one who needs it, in this case for Mario
    def handle_input(self):
        pass

    # function to kill our entity
    def kill(self, dead_image):
        # replacing the entity image with a flattened one
        self.image = dead_image
        # let's say that our essence is dead
        self.is_dead = True
        # the effect of casting to the side when dying and bouncing
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed

    # move function
    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        # checking whether we died or not
        if self.is_dead:
            if self.rect.top > GROUND_H:
                self.is_out = True

        else:
            self.handle_input()

            if self.rect.bottom > H - GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = H - GROUND_H

    # function to render an entity
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ////////////////////////////////////////////////////////////////////////////////////////////////
# class for Mario, inherited from entity class
class Player(Entity):
    def __init__(self):
        super().__init__(player_image_right)  # передаем загруженную картинку игрока
        self.respawn()

    # function to influence player speed
    def handle_input(self):
        self.x_speed = 0

        # implementation of a key to move left
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed  # move left
            self.image = player_image_left  # change the image to the left

        # implementation of a key to move right
        elif keys[pygame.K_d]:
            self.x_speed = self.speed  # move to the right
            self.image = player_image_right  # change the image to the right one

        # implementation of the jump key
        if self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded = False
            self.jump()

    # function to restart the game
    def respawn(self):
        self.is_out = False
        self.is_dead = False
        show_info_window = False
        self.rect.midbottom = (W // 2, H - GROUND_H)

    # jump function
    def jump(self):
        self.y_speed = self.jump_speed


# /////////////////////////////////////////////////////////
# goomba class or enemy class
class Goomba(Entity):
    def __init__(self):
        super().__init__(enemy)
        self.spawn()

    # function for making a goomba appear
    def spawn(self):
        direction = random.randint(0, 1)  # Goomba falling out on the right (0) or left (1)
        if direction == 0:
            self.x_speed = self.speed
            self.rect.bottomright = (0, 0)
        if direction == 1:
            self.x_speed = -self.speed
            self.rect.bottomleft = (W, 0)

    # adding an existing function and improving it
    def update(self):
        super().update()

        # checking whether goombas have gone to the right or left side of the screen
        if self.x_speed > 0 and self.rect.left > W or self.x_speed < 0 and self.rect.right < 0:
            self.is_out = True


player = Player()  # class object

# variable for counting our points in the game
score = 0

# a list that will store all goombas on the screen
goombas = []
# a variable that will store the initial delay of the goomba
INIT_DELAY = 2000
# a variable that will indicate how often goombas spawn
spawn_delay = INIT_DELAY
# a variable that is needed to complicate the game or reduce the spawn time of goombas
DECREASE_BASE = 1.01
# variable to know the last spawn time
the_last_spawn_time = pygame.time.get_ticks()

# game loop
running = True
while running:
    # going through the window closing events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if retry_rect2.collidepoint(e.pos):
                show_info_window = True

        elif e.type == pygame.KEYDOWN:
            pygame.mixer.music.unpause()
            show_info_window = False

            if player.is_out:
                score = 0
                spawn_delay = INIT_DELAY
                the_last_spawn_time = pygame.time.get_ticks()
                player.respawn()
                goombas.clear()
    # I'm limiting the game to frames per second
    clock.tick(FPS)

    screen.fill((92, 148, 252))  # flooded the screen
    # cloud rendering
    screen.blit(cloud_image1, (600, 100))

    screen.blit(cloud_image, (100, 100))
    # tree drawing
    screen.blit(tree_image, (0, 410))
    screen.blit(tree_image1, (700, 410))
    # land rendering
    screen.blit(ground_image, (0, H - GROUND_H))

    # surface for drawing glasses and variable
    score_text = font_large.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()

    # checking to see if mario's out of bounds
    if player.is_out:
        score_rect.midbottom = (W // 2, H // 2)
        screen.blit(retry_text, retry_rect)
        screen.blit(retry_text1, retry_rect1)
        screen.blit(info_image, retry_rect2)
    else:

        # entity addition
        player.update()
        player.draw(screen)
        # current playing time
        now_time = pygame.time.get_ticks()
        # time elapsed since the previous spavin
        elapsed = now_time - the_last_spawn_time
        # entity addition

        # check to see if time has elapsed since the previous spawning
        if elapsed > spawn_delay:
            the_last_spawn_time = now_time
            goombas.append(Goomba())

        # editing the goombas (remove those who have left the field)
        for goomba in list(goombas):
            if goomba.is_out:
                goombas.remove(goomba)
            else:
                goomba.update()
                goomba.draw(screen)
            if not player.is_dead and not goomba.is_dead and player.rect.colliderect(goomba.rect):
                if player.rect.bottom - player.y_speed < goomba.rect.top:
                    goomba.kill(enemy_image)
                    player.jump()
                    score += 1
                    spawn_delay = INIT_DELAY / (DECREASE_BASE ** score)
                else:
                    joke.play()
                    pygame.mixer.music.pause()

                    player.kill(player_image_right)

    if show_info_window:
        pygame.draw.rect(screen, (70, 130, 180), info_window_rect)
        screen.blit(info_text, info_rect)
        screen.blit(info_text1, info_rect1)
        screen.blit(info_text2, info_rect2)
        screen.blit(info_text3, info_rect3)
        screen.blit(info_text4, info_rect4)
        screen.blit(info_text5, info_rect5)
        screen.blit(info_text6, info_rect6)

    # meter location
    score_rect.midtop = (W // 2, H // 5)
    # put up a score in the game
    screen.blit(score_text, score_rect)
    pygame.display.flip()  # I refreshed the screen so that everything would show up.
quit()
