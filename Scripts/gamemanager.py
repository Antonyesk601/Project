import pygame
import definitions
from pygame import mixer
import worldGridDraw as screeninfo
tile_size = 50
score = 0
clock=pygame.time.Clock()
fps = 60
game_over = 0
pygame.display.set_caption("Hi fucker")
bg= pygame.Surface((screeninfo.screenWidth,screeninfo.screenHeight))
bg.set_alpha(255)
bg.fill((255,255,255))
startPosX = screeninfo.screenWidth/2
startPosY = screeninfo.screenHeight/2
screen = pygame.display.set_mode([screeninfo.screenWidth, screeninfo.screenHeight])
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()
#
screen_width = 1300
screen_height = 750
#
slime_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
# #define font

font = pygame.font.SysFont("Bauhaus 93", 70)
font_score = pygame.font.SysFont("Bauhaus 93", 30)
font_intro = pygame.font.SysFont("Matura MT Script Capitals", 60)
font_intro2 = pygame.font.SysFont("Snap ITC", 55)
#
# #define colours
# white = (255,255,255)
# blue = (100,0,255)
# red = (255,0,0)
# moon_glow = ((235,245,255))
#
# # Screen
# screen = pygame.display.set_mode((screen_width,screen_height))
# pygame.display.set_caption("A wizard`s tale")
#
# # load images

#
# #load sounds
pygame.mixer.music.load("level 4 sounds/level 4 original.mp3")
pygame.mixer.music.play(-1, 0.0, 3000)
pygame.mixer.music.set_volume(0.2)
coin_fx = pygame.mixer.Sound("level 4 sounds/coin.mp3")
jump_fx = pygame.mixer.Sound("level 4 sounds/jump.mp3")
jump_fx.set_volume(0.5) #halves the original volume
game_over_fx = pygame.mixer.Sound("level 4 sounds/game_over.mp3")
slime_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

