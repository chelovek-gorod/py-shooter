from pygame import *
import sys
from random import randint
init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 700
SCREEN = display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
CLOCK = time.Clock()
FPS = 60

mixer.init()

sound_shoot = mixer.Sound('./src/se_hit.mp3')

mixer.music.load('./src/bgm_space_1.mp3')
mixer.music.set_volume(0.7)
mixer.music.play()

bg_image = image.load('./src/galaxy.jpg')
bg = transform.scale( bg_image, (960, 701) )

player_image = image.load('./src/rocket.png')
player_width = 62
player_height = 80
player_speed = 5
player = transform.scale( player_image, (player_width, player_height) )
player_x = SCREEN_WIDTH * 0.5 - player_width * 0.5
player_y = SCREEN_HEIGHT - player_height - 20
player_max_x = SCREEN_WIDTH - player_width
player_hp = 3

def subtractHp():
    global player_hp, label_hp
    player_hp -= 1
    label_hp = label_font.render(f'HP: {player_hp}', True, (255, 255, 255))

label_font = font.Font(None, 36)
game_over_font = font.Font(None, 72)

label_hp = label_font.render(f'HP: {player_hp}', True, (255, 255, 255))
label_hp_rect = label_hp.get_rect(x=20, y = 20) # get_rect(center = (130, 30))

label_game_over = game_over_font.render('GAME OVER', True, (255, 0, 0))
label_game_over_rect = label_game_over.get_rect(center = (SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.5))

enemy_image = image.load('./src/ufo.png')
enemy_width = 120
enemy_height = 62
enemy = transform.scale( enemy_image, (120, 62) )
enemy_max_x = SCREEN_WIDTH - enemy_width

UFO_LIST = []

class Enemy():
    def __init__(self):
        self.image = enemy
        self.x = randint(0, enemy_max_x)
        self.y = -enemy_height
        self.speed = 2
        UFO_LIST.append(self)

    def update(self, screen):
        self.y += self.speed
        # проверка - не улетел ли за экран
        if self.y > SCREEN_HEIGHT:
            # если улетел - удаляем из списка
            index = UFO_LIST.index(self)
            del UFO_LIST[index]
            subtractHp()
        else:
            # если не улетел
            # проверяем столкновение с игроком
            screen.blit(self.image, (self.x, self.y))

tick = 0
game_loop_is = True
while game_loop_is:
    CLOCK.tick(FPS)
    tick += 1
    if tick % FPS == 0 : Enemy()

    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            game_loop_is = False

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

    SCREEN.blit(bg, (0, 0))

    if player_hp > 0:
        SCREEN.blit(player, (player_x, player_y))
        for ufo in UFO_LIST : ufo.update(SCREEN)
        SCREEN.blit(label_hp, label_hp_rect)
    else:
        SCREEN.blit(label_game_over, label_game_over_rect)

    display.flip()

quit()
sys.exit()
