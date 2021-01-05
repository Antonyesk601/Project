import pickle  # module for importing level files
from os import path  # to check whether the file exsists in the first place to avoid error

import pygame
from pygame.locals import *


# game loop
def levelrun(main_menu,world,game_over,player,score):
    run = True
    # load in level data and create world
    if path.exists(f"level{level}_data"):
        pickle_in = open(f"level{level}_data",
                         "rb")  # open file and read binary to process whatever info is in this file
        world_data = pickle.load(pickle_in)
    world = World(world_data)  # (runs once outside game loop)

    # call player class with starting coordinates
    player = Player(screen_width - 50, screen_height - 170)

    # create buttons
    restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
    start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
    exit_button = Button(screen_width // 2 + 150, screen_height // 2, exitbtn_img)
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