import pygame
import definitions
import tareklevel
import mklevel
import hossamlevel
import lujainlevel
pygame.init()
# Buttons
class Button():
    def __init__(self, posX, posY, imgPath, imgscale,*function):
        self.image = pygame.image.load(imgPath)
        self.scale = imgscale
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*self.scale),int(self.image.get_height()*self.scale)))
        self.rect = self.image.get_rect()
        self.posXN = posX-self.image.get_width()/2
        self.posYN = posY-self.image.get_height()/2
        self.rect.x = self.posXN
        self.rect.y = self.posYN
        self.function = function
    def update(self):

        if self.posXN+self.image.get_width()>pygame.mouse.get_pos()[0]>self.posXN:
            if self.posYN+self.image.get_height()>pygame.mouse.get_pos()[1]>self.posYN:
                s = pygame.Surface((self.rect.width, self.rect.height))  # the size of your rect
                s.set_alpha(128)  # alpha level
                s.fill((255, 255, 255))  # this fills the entire surface
                definitions.screen.blit(s, (self.posXN, self.posYN))  # (0,0) are the top-left coordinates
                if pygame.mouse.get_pressed(3)[0]:
                    definitions.screen.blit(definitions.bg,(0,0))
                    for function in self.function:
                        exec(function)

class SelectScreen():
    def __init__(self,*button,scale):
        self.scale=scale
        self.buttonsnames = []
        for i in range (0,len(button)):
            self.buttonsnames.append(button[i])

    def update(self):
        for button in self.buttons:
            button.update()
    def draw(self,vertical,PosX=definitions.screeninfo.screenWidth,PosY=definitions.screeninfo.screenHeight):
        global drawn
        definitions.screen.blit(definitions.bg,(0,0))
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
                y= definitions.draw_text(str(counter+1),definitions.font_intro2,(0,0,0),startposXDrawn,startposYDraw+pygame.image.load(button[0]).get_height()*self.scale*counter+counter*50*self.scale)
                self.buttons.append(x)
                definitions.screen.blit(x.image, (x.posXN,x.posYN))
                counter=counter+1
        else:
            for button in self.buttonsnames:
                x=Button(startposXDraw+ pygame.image.load(button[0]).get_width() * counter*self.scale+counter*50*self.scale, startposYDrawn,button[0],1/2,button[1])
                y= definitions.draw_text(str(counter+1),definitions.font_intro2,(0,0,0),startposXDraw+ pygame.image.load(button[0]).get_width() * counter*self.scale+counter*50*self.scale, startposYDrawn+pygame.image.load(button[0]).get_height()//2 )
                definitions.screen.blit(x.image, (x.posXN,x.posYN))
                self.buttons.append(x)
                counter=counter+1
        drawn=True

definitions.screen.blit(definitions.bg, (0, 0))



startButton = Button(definitions.startPosX, definitions.startPosY,"level 4 images/start_btn.png", 1/2,
                     "levels.draw(False)")
Level1 = ["level 4 images/start_btn.png", "definitions.reset_level(3,lujainlevel.player,lujainlevel.world_data,"
                                                        "lujainlevel.resetpositions),"
                                                        "lujainlevel.run(lujainlevel.game_over,lujainlevel.world,"
                                                        "definitions.score,lujainlevel.level,lujainlevel.world_data,"
                                                        "lujainlevel.resetpositions)"]
Level2 = ["level 4 images/start_btn.png", "definitions.reset_level(3,hossamlevel.player,hossamlevel.world_data,"
                                                        "hossamlevel.resetpositions),"
                                                        "hossamlevel.run(hossamlevel.game_over,hossamlevel.world,"
                                                        "definitions.score,hossamlevel.level,hossamlevel.world_data,"
                                                        "hossamlevel.resetpositions)"]
Level3 = ["level 4 images/start_btn.png", "definitions.reset_level(3,mklevel.player,mklevel.world_data,"
                                                        "mklevel.resetpositions),"
                                                        "mklevel.run(definitions.game_over,mklevel.world,"
                                                        "definitions.score,mklevel.level,mklevel.world_data,"
                                                        "mklevel.resetpositions)"]
Level4 = ["level 4 images/start_btn.png", "definitions.reset_level(4,tareklevel.player,"
                                                        "tareklevel.world_data,tareklevel.resetpositions),"
                                                        "tareklevel.run(tareklevel.main_menu,"
                                                        "definitions.game_over,tareklevel.world,definitions.score,"
                                                        "tareklevel.level,tareklevel.world_data,"
                                                        "tareklevel.resetpositions)"]
exitbutton=Button(definitions.startPosX, definitions.startPosY, "level 4 images/exit_btn.png", 1/4,"run=False")
levels = SelectScreen(Level1, Level2, Level3, Level4, scale=1/2)


drawn=False
runs=True
while runs:
    definitions.clock.tick(5)

    if not drawn:
        definitions.screen.blit(startButton.image, (definitions.startPosX-startButton.image.get_width()/2,definitions.startPosY-startButton.image.get_height()/2))
        startButton.update()
        if startButton.posXN + startButton.image.get_width() > pygame.mouse.get_pos()[0] > startButton.posXN:
            if startButton.posYN + startButton.image.get_height() > pygame.mouse.get_pos()[1] > startButton.posYN:
                if pygame.mouse.get_pressed(3)[0]:
                    drawn=True
    else:
        levels.draw(False)
        definitions.draw_text("Levels Done " + str(definitions.levelsfinished), definitions.font_intro2, (0, 0, 0), (definitions.screen_width // 2),
                              0,False)
        if definitions.levelsfinished==4:
            definitions.screen.blit(definitions.bg,(0,0))
            definitions.draw_text("Congratulations", definitions.font_intro2, (0, 0, 0),
                                  (definitions.screen_width // 2),
                                  0,False)
        levels.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = False

    pygame.display.update()
pygame.quit()