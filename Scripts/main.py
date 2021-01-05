import pygame
import level
from pygame.locals import *
from definitions import *
pygame.init()

screen.blit(bg, (0, 0))

startButton = Button(startPosX, startPosY,"D:\\Project\\Preassets\\img\\start_btn.png", 1/2, "levels.draw(False)",
                     "drawn=True")
drawn=False
while runs:
    clock.tick(5)
    screen.blit(bg, (0, 0))
    if not drawn:
        print(drawn)
        screen.blit(startButton.image, (startPosX-startButton.image.get_width()/2,startPosY-startButton.image.get_height()/2))
        startButton.update()
        if startButton.posXN + startButton.image.get_width() > pygame.mouse.get_pos()[0] > startButton.posXN:
            if startButton.posYN + startButton.image.get_height() > pygame.mouse.get_pos()[1] > startButton.posYN:
                if pygame.mouse.get_pressed(3)[0]:
                    drawn=True
    else:
        levels.draw(False)
        levels.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()