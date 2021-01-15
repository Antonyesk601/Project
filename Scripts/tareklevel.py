import pickle
from os import path  # to check whether the file exsists in the first place to avoid error
import pygame
from pygame import mixer
from pygame.locals import *
import definitions
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

main_menu = True
level = 4
score = definitions.score

#define colours
white = (255,255,255)
blue = (100,0,255)
red = (255,0,0)
moon_glow = ((235,245,255))

# Screen
screen = definitions.screen

# load images

#load sounds
pygame.mixer.music.load("level 4 sounds/level 4 original.mp3")
pygame.mixer.music.play(-1, 0.0, 3000)
pygame.mixer.music.set_volume(0.2)
coin_fx = pygame.mixer.Sound("level 4 sounds/coin.mp3")
jump_fx = pygame.mixer.Sound("level 4 sounds/jump.mp3")
jump_fx.set_volume(0.5) #halves the original volume
game_over_fx = pygame.mixer.Sound("level 4 sounds/game_over.mp3")


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x ,y))

slime_group = definitions.slime_group
platform_group =definitions.platform_group
lava_group = definitions.lava_group
coin_group = definitions.coin_group
exit_group = definitions.exit_group

#create dummy coin for showing the score


#load in level data and create world
if path.exists(f"level{level}_data"):
    pickle_in = open(f"level{level}_data", "rb") #open file and read binary to process whatever info is in this file
    world_data = pickle.load(pickle_in)
world =definitions.World(world_data) #(runs once outside game loop)

#call player class with starting coordinates
resetpositions=[definitions.screen_width - 50, definitions.screen_height - 170]
player = definitions.Player(resetpositions[0],resetpositions[1])
score_coin= definitions.Coin(definitions.tile_size // 2, definitions.tile_size // 2)
#create buttons
restart_button = definitions.TuTButton(definitions.screen_width // 2 - 50,definitions. screen_height // 2 + 100, definitions.tkrestart_img)
start_button = definitions.TuTButton(definitions.screen_width // 2 - 350,definitions. screen_height // 2, definitions.tkstart_img)
exit_button = definitions.TuTButton(definitions.screen_width // 2 + 150,definitions. screen_height // 2, definitions.tkexitbtn_img)
def run(main_menu,game_over,world,score,level,world_data,resetpositions):
    # game loop
    run = True
    scorepenalty = 0
    definitions.currentlevel=level
    coin_group.add(score_coin)
    score=  definitions.score
    while run:
            clock.tick(fps) #adjust framerate
            # Drawing
            screen.blit(definitions.tkbkg,(0,0)) # Background

            screen.blit(definitions.tkbg, (0, 0))
            world.draw()
            if definitions.exit_button.draw():
                run = False
            if game_over == 0:
                slime_group.update()
                platform_group.update()
                #update score
                #check if a coin has been collected
                coin_collision = pygame.sprite.spritecollide(player, coin_group, True)#gives a list of the coins the player has collided with
                if coin_collision:
                    coin_fx.play()
                    score += 1
                draw_text("X " + str(score),definitions. font_score, white,definitions. tile_size - 10, 10)
                slime_group.draw(screen)
                platform_group.draw(screen)
                lava_group.draw(screen)
                coin_group.draw(screen)
                exit_group.draw(screen)
            elif game_over ==1:
                score = definitions.score
                definitions.levelsfinished += 1
                run =False
            game_over = player.update(game_over,world)
            #if player has died
            if game_over == -1:
                coin_collision = []
                if restart_button.draw(): #used in if as it draws and returns true/false
                    #recreate the level to reload collected coins before death
                    world = definitions.reset_level(4,player,world_data,resetpositions)
                    game_over = 0
                    scorepenalty-=1
                    score =definitions.score+ scorepenalty
                    coin_group.add(score_coin)
                    pygame.mixer.music.play(-1, 0.0, 3000)
                    run=False


        #close event handler
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                    pygame.quit()
            pygame.display.update()

