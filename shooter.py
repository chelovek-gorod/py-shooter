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
player = transform.scale( player_image, (62, 80) )
player_x = SCREEN_WIDTH * 0.5 - 31
player_y = SCREEN_HEIGHT - 100
player_max_x = SCREEN_WIDTH - 62

enemy_image = image.load('./src/ufo.png')
enemy = transform.scale( enemy_image, (120, 62) )
enemy_max_x = SCREEN_WIDTH - 120

UFO_LIST = []

class Enemy():
    def __init__(self):
        self.image = enemy
        self.x = randint(0, enemy_max_x)
        self.y = -62
        self.speed = 2
        UFO_LIST.append(self)

    def update(self, screen):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            index = UFO_LIST.index(self)
            del UFO_LIST[index]
        else:
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
        player_x -= 5
        if player_x < 0:
            player_x = 0
    elif KEY[K_RIGHT]:
        player_x += 5
        if player_x > player_max_x:
            player_x = player_max_x

    SCREEN.blit(bg, (0, 0))

    SCREEN.blit(player, (player_x, player_y))

    for ufo in UFO_LIST : ufo.update(SCREEN)

    display.flip()

quit()
sys.exit()
