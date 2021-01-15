import pygame
from pygame import mixer
import worldGridDraw as screeninfo
score = 0
clock=pygame.time.Clock()

game_over = 0
startPosX = screeninfo.screenWidth/2
startPosY = screeninfo.screenHeight/2
screen = pygame.display.set_mode([screeninfo.screenWidth, screeninfo.screenHeight])
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
#

slime_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
# #define font

levelsfinished=0
#
currentlevel=0
# #load sounds
pygame.mixer.music.load("level 4 sounds/level 4 original.mp3")
pygame.mixer.music.play(-1, 0.0, 3000)
pygame.mixer.music.set_volume(0.2)
coin_fx = pygame.mixer.Sound("level 4 sounds/coin.mp3")
jump_fx = pygame.mixer.Sound("level 4 sounds/jump.mp3")
jump_fx.set_volume(0.5) #halves the original volume
game_over_fx = pygame.mixer.Sound("level 4 sounds/game_over.mp3")
slime_group = pygame.sprite.Group()
small_slime_group=pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
water_group= pygame.sprite.Group()
base_enemyGroup = pygame.sprite.Group()
