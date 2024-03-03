from pygame import *
import sys
init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
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

tick = 0
game_loop_is = True
while game_loop_is:
    CLOCK.tick(FPS)
    tick += 1

    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            game_loop_is = False

    if (tick % FPS == 0):
        sound_shoot.play()

    SCREEN.blit(bg, (0, 0))
    display.flip()

quit()
sys.exit()
