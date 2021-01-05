import pygame
import level
from pygame.locals import *
from definitions import *
import tareklevel
pygame.init()
class SelectScreen():
    def __init__(self,*button,scale):
        self.scale=scale
        self.buttonsnames = []
        for i in range (0,len(button)):
            self.buttonsnames.append(button[i])

    def update(self):
        for button in self.buttons:
            button.update()
    def draw(self,vertical,PosX=screeninfo.screenWidth,PosY=screeninfo.screenHeight):
        global drawn
        screen.blit(bg,(0,0))
        counter=0
        pygame.image.load(self.buttonsnames[0][0])
        startposXDraw =PosX //2- (pygame.image.load(self.buttonsnames[0][0]).get_width() * len(self.buttonsnames) * self.scale) // 2
        startposXDrawn = PosX // 2
        startposYDraw = PosY // 2 - (pygame.image.load(self.buttonsnames[0][0]).get_height() * len(self.buttonsnames) * self.scale) // 2
        startposYDrawn = PosY // 2
        self.buttons=[]
        if vertical:
            for button in self.buttonsnames:
                x=Button(startposXDrawn,startposYDraw+pygame.image.load(button[0]).get_height()*self.scale*counter+counter*50*self.scale,button[0],1/2,button[1])
                self.buttons.append(x)
                screen.blit(x.image, (x.posXN,x.posYN))
                counter=counter+1
        else:
            for button in self.buttonsnames:
                x=Button(startposXDraw+ pygame.image.load(button[0]).get_width() * counter*self.scale+counter*50*self.scale, startposYDrawn,button[0],1/2,button[1])
                screen.blit(x.image, (x.posXN,x.posYN))
                self.buttons.append(x)
                counter=counter+1
        drawn=True

screen.blit(bg, (0, 0))


Level1 = ["D:\\Project\\Preassets\\img\\start_btn.png", "level1.level1(fps,screeninfo,screen)"]
Level2 = ["D:\\Project\\Preassets\\img\\start_btn.png", "level1.level1(fps,screeninfo,screen)"]
Level3 = ["D:\\Project\\Preassets\\img\\start_btn.png", "level1.level1(fps,screeninfo,screen)"]
Level4 = ["D:\\Project\\Preassets\\img\\start_btn.png", "tareklevel.run(main_menu,game_over,world,score)"]
Level5 = ["D:\\Project\\Preassets\\img\\start_btn.png", "level1.level1(fps,screeninfo,screen)"]
levels = SelectScreen(Level1, Level2, Level3, Level4, Level5, scale=1/2)
startButton = Button(startPosX, startPosY,"D:\\Project\\Preassets\\img\\start_btn.png", 1/2, "levels.draw(False)")
drawn=False
runs=True
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
            runs = False
    pygame.display.update()
pygame.quit()