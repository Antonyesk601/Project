import pygame
pygame.init()
clock=pygame.time.Clock()
class Onscreentxt():
    def __init__(self,*button,scale,screeninfo,screen):
        self.scale=scale
        self.screeninfo=screeninfo
        self.screem=screen;
        self.buttonsnames = []
        for i in range (0,len(button)):
            self.buttonsnames.append(button[i])

    def update(self):
        for button in self.buttons:
            button.update()
            self.draw()
    def draw(self,vertical,font,PosX,PosY):
        text= pygame.font.Font(font,self.scale)
        counter=0
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