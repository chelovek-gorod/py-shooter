from pygame import *
import sys
from random import randint
init() # запускаем встроенный функционал PyGame для корректной работы библиотеки

SCREEN_WIDTH = 960 # ширина игрового окна
SCREEN_HEIGHT = 700 # высота игрового окна
SCREEN = display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) ) # создаем игровое окно
FPS = 60 # частота обновления экрана (frames per second - количество кадров в секунду)
CLOCK = time.Clock() # создаем счетчик времени между кадрами, для поддержки заданного значения FPS

mixer.init() # запускаем встроенный функционал PyGame для для работы с музыкой и звуками

sound_shoot = mixer.Sound('./src/se_hit.mp3') # создаем звук выстрела и сохраняем в переменную

mixer.music.load('./src/bgm_space_1.mp3') # создаем фоновую музыку для игры
mixer.music.set_volume(0.7) # задаем громкость для фоновой музыки
mixer.music.play() # запускаем фоновую музыку

bg_image = image.load('./src/galaxy.jpg') # загружаем фоновое изображение
bg = transform.scale( bg_image, (960, 701) ) # задаем размер для фонового изображения

player_image = image.load('./src/rocket.png') # загружаем изображение игрока
player_width = 62 # задаем ширину изображения игрока
player_height = 80 # задаем высоту изображения игрока
player_speed = 5 # задаем скорость для игрока
player = transform.scale( player_image, (player_width, player_height) ) # задаем размер для изображения игрока
player_x = SCREEN_WIDTH * 0.5 - player_width * 0.5 # задаем координату X игрока - середина экрана
player_y = SCREEN_HEIGHT - player_height - 20 # задаем координату X игрока - середина экрана
player_max_x = SCREEN_WIDTH - player_width # задаем максимальную координату X игрока - чтобы не вылетал за экран
player_max_y = SCREEN_HEIGHT - player_height # задаем максимальную координату Y игрока - чтобы не вылетал за экран
player_hp = 3 # задаем стартовое число жизней
player_score = 0 # задаем стартовое число очков

# функция для вычитание жизней у игрока
def subtractHp():
    global player_hp, label_hp # получаем доступ для изменения переменных, объявленных вне функции
    player_hp -= 1 # отнимаем 1 очко здоровья и обновляем текст с очками здоровья на экране
    label_hp = label_font.render(f'HP: {player_hp}', True, (255, 255, 255))

# функция для добавления очков игроку (принимает число очков, которое нужно добавить, по умолчанию 1)
def addScore(score = 1):
    global player_score, label_score, label_score_rect  # получаем доступ для изменения переменных, объявленных вне функции
    player_score += score # изменяем число очков и обновляем текст с очками на экране
    label_score = label_font.render(f'Score: {player_score}', True, (255, 255, 255))
    # обновляем положение текста с числом очков на экране (текст должен всегда отступать от правого края экрана)
    label_score_rect = label_score.get_rect(right = SCREEN_WIDTH-20, y = 20)

label_font = font.Font(None, 36) # создаем шрифт для вывода число очков и здоровья игрока
game_over_font = font.Font(None, 72) # создаем шрифт для вывода текста проигрыша

# создаем текст с очками здоровья, и прямоугольник в который будем вписывать данный текст
label_hp = label_font.render(f'HP: {player_hp}', True, (255, 255, 255))
label_hp_rect = label_hp.get_rect(x = 20, y = 20)

# создаем текст с очками игрока и прямоугольник в который будем вписывать данный текст
label_score = label_font.render(f'Score: {player_score}', True, (255, 255, 255))
label_score_rect = label_score.get_rect(right = SCREEN_WIDTH-20, y = 20)

# создаем текст с текстом проигрыша, и прямоугольник в который будем вписывать данный текст
label_game_over = game_over_font.render('GAME OVER', True, (255, 0, 0))
label_game_over_rect = label_game_over.get_rect(center = (SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5))

enemy_image = image.load('./src/ufo.png')  # загружаем изображение врага
enemy_width = 120 # задаем ширину изображения врага
enemy_height = 62 # задаем высоту изображения врага
enemy = transform.scale( enemy_image, (120, 62) )  # задаем размер для изображения врага
enemy_max_x = SCREEN_WIDTH - enemy_width # задаем максимальную координату X врага - чтобы не создавать их за экраном

UFO_LIST = [] # список, в котором будем хранить врагов

# класс для создания врагов
class Enemy():
    def __init__(self):
        self.image = enemy # присваиваем изображение
        self.x = randint(0, enemy_max_x) # присваиваем случайную координату X
        self.y = -enemy_height # присваиваем координату Y выше экрана на высоту изображения врага (для плавного появления сверху)
        self.speed = 1 if randint(0, 3) < 3 else 2 # присваиваем случайную скорость (1 или 2)
        UFO_LIST.append(self) # добавляем в список врагов нового врага

    def remove(self): # метод, для удаления врага из списка врагов
        index = UFO_LIST.index(self)
        del UFO_LIST[index]

    def update(self, screen): # метод, для обновления врагов
        self.y += self.speed # изменяем координату Y на скорость врага
        # проверка - не улетел ли за экран
        if self.y > SCREEN_HEIGHT:
            # если улетел - удаляем из списка, отнимаем игроку здоровье
            self.remove()
            subtractHp()
        else:
            # если не улетел
            # проверяем столкновение с игроком (проверка пересечения прямоугольников)
            if self.x + enemy_width > player_x and self.x < player_x + player_width\
            and self.y + enemy_height > player_y and self.y < player_y + player_height:
                # если пересечение есть - удаляем из списка
                addScore(5)
                self.remove()
            else:
                # если пересечения нет (не сталкиваются) - рисуем врага
                screen.blit(self.image, (self.x, self.y))

tick = 0 # счетчик кадров
game_loop_is = True # переменная, отвечающая за работу главного цикла игры (работает пока True)
while game_loop_is:
    CLOCK.tick(FPS) # ждем, до наступления следующего кадра
    tick += 1 # увеличиваем счетчик кадров
    if tick % FPS == 0 : Enemy() # если номер кадра кратен FPS - создаем нового врага

    # проверяем все события, которые произошли между кадрами
    for e in event.get():
        # если окно было закрыто или игрок нажал на клавишу ESCAPE
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            game_loop_is = False # останавливаем главный игровой цикл

    # получаем список нажатых клавиш
    KEY = key.get_pressed()
    if KEY[K_LEFT]:
        player_x -= player_speed
        if player_x < 0:
            player_x = 0
    elif KEY[K_RIGHT]:
        player_x += player_speed
        if player_x > player_max_x:
            player_x = player_max_x
    elif KEY[K_UP]:
        player_y -= player_speed
        if player_y < 0:
            player_y = 0
    elif KEY[K_DOWN]:
        player_y += player_speed
        if player_y > player_max_y:
            player_y = player_max_y

    SCREEN.blit(bg, (0, 0)) # рисуем фон в верхнем левом углу экрана

    if player_hp > 0: # если у игрока есть жизни - рисуем игрока и обновляем врагов
        SCREEN.blit(player, (player_x, player_y))
        for ufo in UFO_LIST : ufo.update(SCREEN)
    else: # иначе - выводим текст о проигрыше
        SCREEN.blit(label_game_over, label_game_over_rect)

    # выводим на экран надписи, с числом жизней и очков игрока
    SCREEN.blit(label_hp, label_hp_rect)
    SCREEN.blit(label_score, label_score_rect)

    display.flip() # обновляем экран игры

quit() # выходим из Pygame
sys.exit() # закрываем приложение
