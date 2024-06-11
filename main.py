from os import path
import pygame
import random
pygame.init()
joke = pygame.mixer.Sound(path.join( 'game-over-super-mario-made-with-Voicemod (mp3cut.net).mp3'))
joke.set_volume(5)
# Выставляем широту и длину экрана в переменных
W = 800
H = 600
# добавление музыки
pygame.mixer.music.load("super-mario-saundtrek.mp3")
pygame.mixer.music.play(-1)
# создаем сам экран
screen = pygame.display.set_mode((W, H))
# создаем счетчик кадров в секунду
FPS = 60
# объект часов
clock = pygame.time.Clock()

# создание всех необходимых переменных (шрифт, game_over которая будет обозначать проигрыш или нет)
font_path = 'SuperMario256.ttf'
font_xsmall = pygame.font.SysFont('arial_bold', 36)
font_large = pygame.font.Font(font_path, 48)
font_small = pygame.font.Font(font_path, 24)

game_over = False
# поверхности которые будут появляться при проигрыше и расположение их на экране
retry_text = font_small.render('PRESS ANY KEY', True, (255, 255, 255))
retry_rect = retry_text.get_rect()
retry_rect.midtop = (W // 2, H // 2)
# Game over
retry_text1 = font_small.render('GAME OVER', True, (255, 255, 255))
retry_rect1 = retry_text1.get_rect()
retry_rect1.midtop = (400, 220)
# добавление файла кнопки информации об игровых механиках
info_image = pygame.image.load('cnopka3llp.png')
info_image = pygame.transform.scale(info_image, (160, 40))
retry_rect2 = info_image.get_rect()
retry_rect2.midtop = (W // 2, H - 50)

show_info_window = False
# текст для плашки информация
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

# добавления деревьев а также редактирование их в нужные размеры
tree_image = pygame.image.load('images_tree.png')
tree_image = pygame.transform.scale(tree_image, (100, 140))
tree_image1 = pygame.image.load('images_tree.png')
tree_image1 = pygame.transform.scale(tree_image1, (100, 140))

# добавления облаков а также редактирование их в нужные размеры
cloud_image = pygame.image.load('pixel-art-cloud-vector-icon-for-8bit-game-on-white-background_360488-650.jpg.png')
cloud_image = pygame.transform.scale(cloud_image, (100, 100))
cloud_image1 = pygame.image.load('pixel-art-cloud-vector-icon-for-8bit-game-on-white-background_360488-650.jpg.png')
cloud_image1 = pygame.transform.scale(cloud_image1, (100, 100))

# добавление файла земли а также редактирование его в нужные размеры
ground_image = pygame.image.load('Снимок экрана 2024-05-04 в 17.27.10.png')
ground_image = pygame.transform.scale(ground_image, (804, 60))
GROUND_H = ground_image.get_height()

# добавление файла uev,s а также редактирование его в нужные размеры
enemy = pygame.image.load('gimi.png')
enemy = pygame.transform.scale(enemy, (80, 80))

# добавление файла мертвого гумбы а также редактирование его в нужные размеры
enemy_image = pygame.image.load('goomba_mini.png')
enemy_image = pygame.transform.scale(enemy_image, (80, 80))

# добавление файла mario а также редактирование его в нужные размеры
player_image_right = pygame.image.load('images1.png')
player_image_right = pygame.transform.scale(player_image_right, (80, 60))
player_image_left = pygame.transform.flip(player_image_right, True, False)

# ////////////////////////////////////////////////////////////////////////////////////////////////
# класс для объявления сущностей (марио, гумба)
class Entity:
    # создание главной функции конструктора и создания в нем переменных для рисунка марио или гумба, скорости
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        # скорость по x и y
        self.x_speed = 0
        self.y_speed = 0

        self.speed = 5  # основная скорость
        # переменные для проверки упали ли мы в пропасть или живы ли мы или нет
        self.is_out = False
        self.is_dead = False
        # скорость прыжка
        self.jump_speed = -12
        # скорость гравитации
        self.gravity = 0.4
        # переменная для того чтобы мы знали находимся ли мы на земле или нет
        self.is_grounded = False

    # функция для управления пользовательским вводом. Она будет пустая, но я буду предопределять для того кому она нужна, в этом случае для марио
    def handle_input(self):
        pass

    # функция для убивания нашей сущности
    def kill(self, dead_image):
        # замена картинки сущности на сплющенную
        self.image = dead_image
        # будем говорить что наша сущность мертва
        self.is_dead = True
        # эффект отлитания при смерти в сторону и подпрыгивания
        self.x_speed = -self.x_speed
        self.y_speed = self.jump_speed

    # функция перемещения
    def update(self):
        self.rect.x += self.x_speed
        self.y_speed += self.gravity
        self.rect.y += self.y_speed

        # проверка на то, что умерли мы или нет
        if self.is_dead:
            if self.rect.top > GROUND_H:
                self.is_out = True

        else:
            self.handle_input()

            if self.rect.bottom > H - GROUND_H:
                self.is_grounded = True
                self.y_speed = 0
                self.rect.bottom = H - GROUND_H

    # функция для отрисовки сущности
    def draw(self, surface):
        surface.blit(self.image, self.rect)


# ////////////////////////////////////////////////////////////////////////////////////////////////
# класс для марио, унаследованный из класса entity
class Player(Entity):
    def __init__(self):
        super().__init__(player_image_right)  # передаем загруженную картинку игрока
        self.respawn()

    # функция для влияния скорости игрока
    def handle_input(self):
        self.x_speed = 0

        # реализация клавиши для движения влево
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_speed = -self.speed  # двигаем влево
            self.image = player_image_left  # изменяем картинку на левую

        # реализация клавиши для движения вправо
        elif keys[pygame.K_d]:
            self.x_speed = self.speed  # двигаем вправо
            self.image = player_image_right  # изменяем картинку на правую

        # реализация клавиши для прыжка
        if self.is_grounded and keys[pygame.K_SPACE]:
            self.is_grounded = False
            self.jump()

    # функция для рестарта игры
    def respawn(self):
        self.is_out = False
        self.is_dead = False
        show_info_window = False
        self.rect.midbottom = (W // 2, H - GROUND_H)

    # функция прыжка
    def jump(self):
        self.y_speed = self.jump_speed


# /////////////////////////////////////////////////////////
# класс гумба или класса врага
class Goomba(Entity):
    def __init__(self):
        super().__init__(enemy)
        self.spawn()

    # функция для того чтобы гумба появлялся
    def spawn(self):
        direction = random.randint(0, 1)  # выпадение гумба справа (0) или слева (1)

        if direction == 0:
            self.x_speed = self.speed
            self.rect.bottomright = (0, 0)
        if direction == 1:
            self.x_speed = -self.speed
            self.rect.bottomleft = (W, 0)

    # добавление уже существующей функции и доработка её
    def update(self):
        super().update()

        # проверка на то что ушли ли гумбы в правую или левую часть экрана
        if self.x_speed > 0 and self.rect.left > W or self.x_speed < 0 and self.rect.right < 0:
            self.is_out = True


player = Player()  # объект класса

# переменная для подсчитывания наших очков в игре
score = 0

# список который будет хранить всех гумб на экране
goombas = []
# переменная которая будет хранить в себе начальную задержку гумбы
INIT_DELAY = 2000
# переменная которая будет обозначать как часто спавнятся гумбы
spawn_delay = INIT_DELAY
# переменная которая нужна для того чтобы усложнять игру или сокращать время спавна гумб
DECREASE_BASE = 1.01
# переменная для того чтобы знать время последнего спавна
the_last_spawn_time = pygame.time.get_ticks()

# игровой цикл
running = True
while running:
    # перебираю события закрытия окна
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
    # ограничиваю игру по кадрам в секунду
    clock.tick(FPS)

    screen.fill((92, 148, 252))  # залил экран
    # отрисовка облаков
    screen.blit(cloud_image1, (600, 100))

    screen.blit(cloud_image, (100, 100))
    # отрисовка деревьев
    screen.blit(tree_image, (0, 410))
    screen.blit(tree_image1, (700, 410))
    # отрисовка земли
    screen.blit(ground_image, (0, H - GROUND_H))

    # поверхность для отрисовки очков и переменная
    score_text = font_large.render(str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect()

    # проверка на то что вылетел ли марио за границы
    if player.is_out:
        score_rect.midbottom = (W // 2, H // 2)
        screen.blit(retry_text, retry_rect)
        screen.blit(retry_text1, retry_rect1)
        screen.blit(info_image, retry_rect2)
    else:

        # добавление сущности
        player.update()
        player.draw(screen)
        # текущее игровое время
        now_time = pygame.time.get_ticks()
        # время которое прошло с момента предыдущего спавна
        elapsed = now_time - the_last_spawn_time
        # добавление сущности

        # проверка на то что прошло ли время с момента предыдущего спавна
        if elapsed > spawn_delay:
            the_last_spawn_time = now_time
            goombas.append(Goomba())

        # редактирование гумб (удалять тех кто ушел за поле)
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

    # расположение счетчика
    score_rect.midtop = (W // 2, H // 5)
    # выставили счет очков в игре
    screen.blit(score_text, score_rect)
    pygame.display.flip()  # обновил экран для того чтоб все отображалось
quit()
