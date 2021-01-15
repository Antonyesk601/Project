import pygame

import definitions

vec = pygame.math.Vector2  # 2Dimensional

# Load images
bg_color = (135, 206, 235)

tile_size = 50
game_over = 0
screen = definitions.screen
clock = pygame.time.Clock()
level = 3
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 2, 2, 2, 1],
    [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 2, 2, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
]
score_coin =  definitions.Coin(definitions.tile_size // 2, definitions.tile_size // 2)

slime_group = definitions.small_slime_group
platform_group = definitions.platform_group
lava_group = definitions.lava_group
coin_group = definitions.coin_group
exit_group = definitions.exit_group
score_coin = definitions.Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)
water_group = definitions.water_group
world = definitions.World(world_data)  # (runs once outside game loop)
# call player class with starting coordinates
resetpositions = [100, definitions.screen_height - 175]
player = definitions.Player(resetpositions[0], resetpositions[1])

# create buttons
restart_button = definitions.TuTButton(definitions.screen_width // 2 - 50, definitions.screen_height // 2 + 100,
                                       definitions.tkrestart_img)
start_button = definitions.TuTButton(definitions.screen_width // 2 - 350, definitions.screen_height // 2,
                                     definitions.tkstart_img)
exit_button = definitions.TuTButton(definitions.screen_width // 2 + 150, definitions.screen_height // 2,
                                    definitions.tkexitbtn_img)


def run(game_over, world, score, level, world_data, resetpositions):
    # game loop
    run = True
    bg_color = (135, 206, 235)
    coin_group.add(score_coin)
    score=  definitions.score
    scorepenalty=0
    while run:

        clock.tick(definitions.fps)  # adjust framerate

        screen.fill(bg_color)
        world.draw()
        if definitions.exit_button.draw():
            run = False
        if game_over == 0:
            slime_group.update()
            platform_group.update()
            # update score
            # check if a coin has been collected
            coin_collision = pygame.sprite.spritecollide(player, coin_group,
                                                         True)  # gives a list of the coins the player has collided with
            if coin_collision:
                definitions.coin_fx.play()
                score += 1
            definitions.draw_text("X " + str(score), definitions.font_score, definitions.white, tile_size - 10, 10)

        game_over = player.update(game_over, world)

        # if player has died
        if game_over == -1:
            coin_collision = []
            if restart_button.draw():  # used in if as it draws and returns true/false
                # recreate the level to reload collected coins before death
                world = definitions.reset_level(4, player, world_data, resetpositions)
                game_over = 0
                scorepenalty -= 1
                score = definitions.score+ scorepenalty
                pygame.mixer.music.play(-1, 0.0, 3000)
                coin_group.add(score_coin)
        elif game_over==1:
            definitions.score = score
            definitions.levelsfinished+=1
            run=False
        # close event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        slime_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        water_group.draw(screen)
        pygame.display.update()
