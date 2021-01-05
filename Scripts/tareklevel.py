import pygame, sys, random, time
from pygame.locals import *
from pygame import mixer
import pickle #module for importing level files
from os import path #to check whether the file exsists in the first place to avoid error
import definitions
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1300
screen_height = 750

#define font
font = pygame.font.SysFont("Bauhaus 93", 70)
font_score = pygame.font.SysFont("Bauhaus 93", 30)
font_intro = pygame.font.SysFont("Matura MT Script Capitals", 60)
font_intro2 = pygame.font.SysFont("Snap ITC", 55)

#define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 4
max_levels = 4
score = 0

#define colours
white = (255,255,255)
blue = (100,0,255)
red = (255,0,0)
moon_glow = ((235,245,255))

# Screen
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("A wizard`s tale")

# load images
bkg_img = pygame.image.load("level 4 images/level 4 intro.jpg")
bkg = pygame.transform.scale(bkg_img, (screen_width,screen_height))
bg_img = pygame.image.load("level 4 images/NightForest/Forestgrey.png") # Background
bg = pygame.transform.scale(bg_img,(screen_width,screen_height)) #fix background scale
restart_img = pygame.image.load("level 4 images/restart_btn.png")
start_img = pygame.image.load("level 4 images/start_btn.png")
exitbtn_img = pygame.image.load("level 4 images/exit_btn.png")

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

#reset level funciton
def reset_level(level):
    #reset player position and destroy all entities
    player.reset(screen_width - 50, screen_height - 170)
    slime_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()

    #load in level data and create world
    if path.exists(f"level{level}_data"):
        pickle_in = open(f"level{level}_data",
                         "rb")  # open file and read binary to process whatever info is in this file
        world_data = pickle.load(pickle_in)
    world = definitions.World(world_data)  # (runs once outside game loop)

    return world #take a receipt for game loop


# Buttons

slime_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin =  definitions.Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)



#load in level data and create world
if path.exists(f"level{level}_data"):
    pickle_in = open(f"level{level}_data", "rb") #open file and read binary to process whatever info is in this file
    world_data = pickle.load(pickle_in)
world =definitions.World(world_data) #(runs once outside game loop)

#call player class with starting coordinates
player = definitions.Player(screen_width - 50, screen_height - 170)

#create buttons
restart_button = definitions.TuTButton(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = definitions.TuTButton(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = definitions.TuTButton(screen_width // 2 + 150, screen_height // 2, exitbtn_img)
def run():
    # game loop
    run = True
    while run:
        clock.tick(fps) #adjust framerate

        # Drawing
        screen.blit(bkg,(0,0)) # Background
        draw_text("Level 4", font_intro2, blue, (screen_width // 2) - 80, 30)
        draw_text("BOSS BATTLE", font_intro2, moon_glow, (screen_width // 2) - 200, screen_height - 200)

        if main_menu == True:
            if exit_button.draw():
                run = False
            if start_button.draw():
                main_menu = False
        else:
            screen.blit(bg, (0, 0))
            world.draw()

            if game_over == 0:
                slime_group.update()
                platform_group.update()
                #update score
                #check if a coin has been collected
                coin_collision = pygame.sprite.spritecollide(player, coin_group, True)#gives a list of the coins the player has collided with
                if coin_collision:
                    coin_fx.play()
                    score += 1
                draw_text("X " + str(score), font_score, white, tile_size - 10, 10)

            game_over = player.update(game_over)

            slime_group.draw(screen)
            platform_group.draw(screen)
            lava_group.draw(screen)
            coin_group.draw(screen)
            exit_group.draw(screen)

            #if player has died
            if game_over == -1:
                coin_collision = []
                if restart_button.draw(): #used in if as it draws and returns true/false
                    #recreate the level to reload collected coins before death
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0
                    pygame.mixer.music.play(-1, 0.0, 3000)


            #if player has completed the level
            if game_over == 1:
                #reset game and go to next level
                level += 1
                if level <= max_levels:
                    #reset level to get new level data
                    world_data = []
                    world = reset_level(level) # loads the next level data
                    game_over = 0 #reset game over variable
                else:
                    draw_text("YOU WIN!", font, blue, (screen_width // 2) - 140, screen_height // 2)
                    if restart_button.draw():
                        level = 1
                        #reset level
                        world_data = []
                        world = reset_level(level)
                        game_over = 0
                        score = 0


        #close event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

        pygame.display.update()

    pygame.quit()