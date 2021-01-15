import pygame
pygame.init()
clock=pygame.time.Clock()
import definitions
worldMap=[

[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[2,2,0,0,0,0,0,3,0,0,0,0,0,3,0,0,0,0,0,3,0,0,0,0,0,0],
[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
[0,0,0,0,0,0,2,0,3,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,2,2],
[1,1,1,1,4,1,1,1,1,1,1,1,1,4,1,1,1,4,1,1,1,1,1,1,1,1],
]
slime_group = definitions.slime_group
platform_group = definitions.platform_group
lava_group = definitions.lava_group
coin_group = definitions.coin_group
exit_group = definitions.exit_group
water_group= definitions.water_group
def level1(fps,screeninfo,screen):
    run = True
    world = definitions.World(worldMap)
    player = definitions.Player(100, screeninfo.screenHeight - 130)
    sun = pygame.image.load("Preassets/img/sun.png")
    background = pygame.image.load("Preassets/img/sky.png")
    while run:
        clock.tick(fps)
        screen.blit(background,(0,0))
        screen.blit(sun,(100,100))
        world.draw()
        definitions.base_enemyGroup.update()
        definitions.base_enemyGroup.draw(screen)
        player.update(definitions.game_over,world)
        slime_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
        pygame.display.update()
    pygame.quit()