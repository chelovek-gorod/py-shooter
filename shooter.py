# команда для сборки игры в один исходный файл
# pyinstaller --onefile --name MyGame --icon=icon.ico -F --noconsole main5.py

import pygame as PG
import sys # данная библиотека понадобится для корректного выхода из игры
from random import randint
PG.init() # запускаем встроенный функционал PyGame для корректной работы библиотеки

SCREEN_WIDTH = 960 # ширина игрового окна
SCREEN_HEIGHT = 700 # высота игрового окна
SCREEN = PG.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) ) # создаем игровое окно
FPS = 60 # частота обновления экрана (frames per second - количество кадров в секунду)
CLOCK = PG.time.Clock() # создаем счетчик времени между кадрами, для поддержки заданного значения FPS

PG.mixer.init() # запускаем встроенный функционал PyGame для для работы с музыкой и звуками

sound_shoot = PG.mixer.Sound('./src/se_hit.mp3') # создаем звук выстрела и сохраняем в переменную

PG.mixer.music.load('./src/bgm_space_1.mp3') # создаем фоновую музыку для игры
PG.mixer.music.set_volume(0.7) # задаем громкость для фоновой музыки
PG.mixer.music.play() # запускаем фоновую музыку

bg_image = PG.image.load('./src/galaxy.jpg') # загружаем фоновое изображение
bg = PG.transform.scale( bg_image, (960, 701) ) # задаем размер для фонового изображения

player_image = PG.image.load('./src/rocket.png') # загружаем изображение игрока

enemy_image = PG.image.load('./src/ufo.png') # загружаем изображение игрока
enemies_group = PG.sprite.Group() # создаем группу для спрайтов врагов

bullet_image = PG.image.load('./src/bullet.png') # загружаем изображение игрока
bullets_group = PG.sprite.Group() # создаем группу для спрайтов пуль

# класс для создания надписей
class Label(): # text - текст надписи, x и y - координаты, align - направление, font_size - размер, color- цвет
    def __init__(self, text, x, y, align = 'left', font_size = 36, color = (255, 255, 255)):
        self.font = PG.font.Font(None, font_size) # создаем шрифт (None - любой системный, font_size - размер)
        self.align = align # сохраняем направления для перерасчета координат отрисовки
        self.color = color
        self.x = x # сохраняем начальную координату x для перерасчета координат отрисовки
        self.y = y # сохраняем начальную координату y для перерасчета координат отрисовки
        self.render(text) # обновляем текст
    
    def render(self, text): # метод обновления текста
        self.text = self.font.render(text, True, self.color) # переводим текст в набор пикселей (True - сглаживать пиксели)
        self.rect = self.text.get_rect() # определяем прямоугольник по размеру текста
        self.rect.centery = self.y # задаем прямоугольнику для отрисовки текста координаты x и y
        if self.align == 'left': self.rect.left = self.x
        elif self.align == 'right': self.rect.right = self.x
        else : self.rect.centerx = self.x

# создаем надпись 'GAME OVER'
label_game_over = Label('GAME OVER', SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5, 'center', 72, (255, 0, 0))

# класс игрока (наследуемся от PG.sprite.Sprite, для удобной проверки столкновений)
class Player(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self) # вызываем конструктор родительского класса (обязательно)
        self.image = PG.transform.scale( player_image, (62, 80) ) # задаем спрайту изображение нужного размера
        self.rect = self.image.get_rect() # определяем прямоугольник по размеру изображения
        self.rect.centerx = SCREEN_WIDTH * 0.5 # задаем прямоугольнику координаты x и y
        self.rect.centery = SCREEN_HEIGHT - self.rect.height
        self.hp = 5 # жизни игрока
        self.speed = 5 # скорость игрока
        self.score = 0 # очки игрока
        self.shut_speed = 90 # время перезарядки (число кадров между выстрелами)
        self.shut_timeout = self.shut_speed # число кадров до следующего выстрела
        self.hp_label = Label(f'HP: {self.hp}', 15, 30, 'left') # создаем текст с количеством жизней и очками
        self.score_label = Label(f'Score: {self.score}', SCREEN_WIDTH - 15, 30, 'right')

    def update(self): # метод обновления игрока
        # ДВИЖЕНИЕ
        KEY = PG.key.get_pressed() # получаем список всех клавиш, которые были нажаты между обновлениями экрана
        if KEY[PG.K_LEFT]: # если среди них была СТРЕЛКА ВЛЕВО
            self.rect.x -= self.speed # - двигаем игрока влево
            if self.rect.centerx < 0 : self.rect.centerx = 0 # не даем выйти за пределы экрана
        elif KEY[PG.K_RIGHT]: # если среди них была СТРЕЛКА ВПРАВО
            self.rect.x += self.speed # - двигаем игрока вправо
            if self.rect.centerx > SCREEN_WIDTH : self.rect.centerx = SCREEN_WIDTH # не даем выйти за пределы экрана
        elif KEY[PG.K_UP]: # если среди них была СТРЕЛКА ВВЕРХ
            self.rect.y -= self.speed # - двигаем игрока вверх
            if self.rect.centery < 0 : self.rect.centery = 0 # не даем выйти за пределы экрана
        elif KEY[PG.K_DOWN]: # если среди них была СТРЕЛКА ВНИЗ
            self.rect.y += self.speed # - двигаем игрока вниз
            if self.rect.centery > SCREEN_HEIGHT : self.rect.centery = SCREEN_HEIGHT # не даем выйти за пределы экрана

        # СТРЕЛЬБА
        self.shut_timeout -= 1 # уменьшаем число кадров до следующего выстрела
        if self.shut_timeout <= 0: # если дошли до 0 или ниже - стреляем
            self.shut_timeout = self.shut_speed # обновляем число кадров до следующего выстрела
            bullets_group.add( Bullet(self.rect.centerx, self.rect.centery) ) # в группу пуль добавляем пулю
            sound_shoot.play() # проигрываем звук выстрела

        # СТОЛКНОВЕНИЕ С ВРАГАМИ (True - удалить врага, с которым столкнулись)
        if PG.sprite.spritecollide(self, enemies_group, True) : self.getHit()

    def getHit(self): # метод получения урона
        self.hp -= 1 # отнимаем hp и обновляем текст с hp
        self.hp_label.render(f'HP: {self.hp}')

    def getScore(self, score = 1): # метод получения очков
        self.score += score # прибавляем очки и обновляем текст с очками
        self.score_label.render(f'Score: {self.score}')

# класс игрока (наследуемся от PG.sprite.Sprite, для удобной проверки столкновений)
class Enemy(PG.sprite.Sprite):
    def __init__(self):
        PG.sprite.Sprite.__init__(self) # вызываем конструктор родительского класса (обязательно)
        self.image = PG.transform.scale( enemy_image, (120, 62) ) # задаем спрайту изображение нужного размера
        self.rect = self.image.get_rect() # определяем прямоугольник по размеру изображения
        self.rect.centerx = randint(0, SCREEN_WIDTH) # задаем прямоугольнику координаты
        self.rect.bottom = 0
        self.speed = randint(1, 3) # определяем случайную скорость (от 1 до 3)
        enemies_group.add(self) # в группу врагов добавляем врага

    def update(self): # метод обновления
        self.rect.y += self.speed # двигаем врага вниз
        if self.rect.top > SCREEN_HEIGHT or self.rect.colliderect(player.rect):
            player.getHit() # если улетели за экран или столкнулись с игроком - наносим урон игроку
            return self.kill() # удаляем врага и выходим из метода
        
        SCREEN.blit(self.image, self.rect) # рисуем врага в координатах прямоугольника

# класс пули (наследуемся от PG.sprite.Sprite, для удобной проверки столкновений)
class Bullet(PG.sprite.Sprite):
    def __init__(self, x, y):
        PG.sprite.Sprite.__init__(self) # вызываем конструктор родительского класса (обязательно)
        self.image = PG.transform.scale( bullet_image, (16, 32) ) # задаем спрайту изображение нужного размера
        self.rect = self.image.get_rect() # определяем прямоугольник по размеру изображения
        self.rect.centerx = x # задаем прямоугольнику координаты
        self.rect.centery = y
        self.speed = 10 # скорость пули
        bullets_group.add(self) # в группу пуль добавляем пулю

    def update(self): # метод обновления
        global enemy_add_timeout # получаем доступ к изменению переменной enemy_add_timeout (таймер появления врагов)

        self.rect.y -= self.speed # двигаем пулю вверх
        if self.rect.bottom < 0: # если пуля улетела за экран - удаляем ее и выходим из метода
            return self.kill()
        
        # если пуля столкнулась с врагом (True - удалить врага, с которым столкнулись)
        if PG.sprite.spritecollide(self, enemies_group, True):
            enemy_add_timeout -= 1 # уменьшаем время до появления нового врага
            player.getScore(5) # начисляем игроку очки
            return self.kill() # удаляем пулю и выходим из метода
        
        SCREEN.blit(self.image, self.rect) # рисуем пулю в координатах прямоугольника

player = Player() # создаем игрока

enemy_add_timeout = FPS * 2 # создаем счетчик для ожидания появления новых врагов (считаем в кадрах)

tick = 0 # создаем счетчик кадров
game_loop_is = True # переменная, отвечающая за работу главного цикла игры (работает пока True)

# ГЛАВНыЙ ЦИКЛ ИГРЫ (крутится, пока game_loop_is = True)
while game_loop_is:
    CLOCK.tick(FPS) # ждем, до наступления следующего кадра
    tick += 1 # увеличиваем счетчик кадров

    # если номер кадра кратен счетчику появления врагов - создаем нового врага
    if tick % enemy_add_timeout == 0 : Enemy() 

    # проверяем все события, которые произошли между кадрами
    for event in PG.event.get():
        # если окно было закрыто или игрок нажал на клавишу ESCAPE
        if event.type == PG.QUIT or (event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE):
            game_loop_is = False # останавливаем главный игровой цикл

    SCREEN.blit(bg, (0, 0)) # рисуем фон в верхнем левом углу экрана
    if player.hp > 0: # если у игрока есть жизни
        bullets_group.update() # - обновляем пули
        player.update() # - обновляем игрока
        SCREEN.blit(player.image, player.rect) # - рисуем игрока
        enemies_group.update() # - обновляем врагов
    else: # иначе - выводим текст о проигрыше
        SCREEN.blit(label_game_over.text, label_game_over.rect)

    # выводим на экран надписи, с числом жизней и очков игрока
    SCREEN.blit(player.hp_label.text, player.hp_label.rect)
    SCREEN.blit(player.score_label.text, player.score_label.rect)

    PG.display.flip() # обновляем экран игры

# ПОСЛЕ ОСТАНОВКИ ГЛАВНОГО ИГРОВОГО ЦИКЛА
PG.quit() # выходим из Pygame
sys.exit() # закрываем приложение
