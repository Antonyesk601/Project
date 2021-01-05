import pygame,sys, random, time
from pygame import mixer
from os import path
import worldGridDraw as screeninfo
import pickle
tile_size = 50
score = 0
clock=pygame.time.Clock()
fps = 60
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
bkg_img = pygame.image.load("level 4 images/level 4 intro.jpg")
bkg = pygame.transform.scale(bkg_img, (screen_width,screen_height))
bg_img = pygame.image.load("level 4 images/NightForest/Forestgrey.png") # Background
bg = pygame.transform.scale(bg_img,(screen_width,screen_height)) #fix background scale

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

class TuTButton():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False #prevents output spam when reset button clicked

    def draw(self):
        action = False #variable to tell the game loop that reset was pressed

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos): #mouse is considered a point so this tests if button rect collided with it (mouse over it)
            #this following function produces a list with 0s and 1s depending on what has been clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: #left mouse button is index 0, clicked = 1
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        #draw button
        screen.blit(self.image, self.rect)

        return action
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x ,y))


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
                print("good lord")
                s = pygame.Surface((self.rect.width, self.rect.height))  # the size of your rect
                s.set_alpha(128)  # alpha level
                s.fill((255, 255, 255))  # this fills the entire surface
                screen.blit(s, (self.posXN, self.posYN))  # (0,0) are the top-left coordinates
                if pygame.mouse.get_pressed(3)[0]:
                    screen.blit(bg,(0,0))
                    for function in self.function:
                        print(function)
                        exec(function)


# Player class
class Player():
    def __init__(self, x, y):   #takes x,y coordinates of player as arguments
        self.reset(x, y)
    def animate(self, dx, dy):
        animation_cooldown=15
        if self.counter>=animation_cooldown:
            self.counter=0
            if dx > 0:
                self.index += 1
                if self.index >= len(self.imagesright):
                    self.index = 0
                self.image = self.imagesright[self.index]
            elif dx < 0:
                self.index += 1
                if self.index >= len(self.imagesleft):
                    self.index = 0
                self.image = self.imagesleft[self.index]
        if self.left and dx == 0:
            self.image = self.imagesleft[0]
        elif (not self.left) and dx == 0:
            self.image = self.imagesright[0]

    def update(self, game_over,world): #what is actually called through game loop
        #calculate new player pos > check collision at new pos > adjust player pos
        #instead of moving rect using(self.rect.x or y) straight away
        dx = 0
        dy = 0
        walk_cooldown = 0 #number of iterations that need to pass before updating picture index
        collision_threshold = 20

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1 #used to be compared with walk_cooldown to update animation when moving
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False: #reset animation when not moving
                self.counter = 0
                self.index = 0
                # keep player facing the same direction when he stops
                if self.direction == 1:
                    self.image = self.images_right[self.index] #update display variable with the next pic on list
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False

            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right): #prevents index out of range err
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index] #update display variable with the next pic on list
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            #add gravity
            self.vel_y += 1 #speed of gravity
            # setting a limit for jump such that if it goes higher than 10 sets back to 10
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            self.in_air = True #assumes the player is in air before checking
            for tile in world.tile_list: #access tile list in world class and iterate over tiles
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height): #tests if player is about to collide with tile using a dummy rect
                    #check if below the ground i.e. jumping and about to hit head
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top #the distance between top of player`s head and the tile bottom
                        self.vel_y = 0 #prevents player from being stuck in air for a split sec after hitting his head
                    #check if above ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0 #prevents player from being stuck for a split sec after jumps
                        self.in_air = False

            #check for collision with enemies
            if pygame.sprite.spritecollide(self, slime_group, False):
                game_over = -1
                pygame.mixer.music.stop()
                game_over_fx.play()

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            #check for collision with exit
            if pygame.sprite.spritecollide(self, exit_group, False):
                pygame.mixer.music.stop()
                pygame.mixer.music.load("level 4 sounds/victory.mp3")
                pygame.mixer.music.play(-1, 0.0)
                game_over = 1

            #check for collision with platforms
            for platform in platform_group:
                #collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                #collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    #check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < collision_threshold:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    #check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < collision_threshold:
                        self.rect.bottom = platform.rect.top - 1 #places player 1px above platform to fix stuck bug
                        self.in_air = False #so that player can jump while on platform
                        dy = 0
                    #move sideways with the platform
                    if platform.move_x != 0: #if one of the horizontal platforms
                        self.rect.x += platform.move_direction


            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            #prevent player from moving off-screen
            if self.rect.right >= screen_width:
                self.rect.right = screen_width
            if self.rect.left <= 0:
                self.rect.left = 0


        # dead player image
        elif game_over == -1:
            pygame.mixer.music.stop()
            self.image = self.dead_image
            draw_text("GAME OVER!", font, (255,0,0), (screen_width // 2) - 180, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # draw player onto screen
        screen.blit(self.image,self.rect)
        #display player hitbox
        #pygame.draw.rect(screen,(0,255,0),self.rect, 2)

        return game_over

    def reset(self, x, y):
        # Player animation
        self.images_right = []  # list to have the four scaled animation images
        self.images_left = []
        self.index = 0  # index tracking
        self.counter = 0  # controls the speed of animation
        for num in range(20):  # iterate over the pics and rescale then add to list
            img_right = pygame.image.load("level 4 images/BlueWizard/BlueWizardWalk/wizard%d.png" %num)
            img_left = pygame.transform.flip(img_right, True, False)  # True vertically,False horizontally
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load("level 4 images/ghost.png")
        self.image = self.images_right[self.index]  # images variable which will be displayed using the update function
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()  # get tile width
        self.height = self.image.get_height()  # get tile height
        self.vel_y = 0  # velocity in y direction for smooth jumping
        self.jumped = False  # used for preventing hold-jump spam
        self.direction = 0  # to determine if walking right or left
        self.in_air = True #to fix infinite jumping

# World data class
class World():
    def __init__(self,data): #constructor method takes the blueprint as an argument to process it
        self.tile_list = [] #empty list to collect useful data of the world after processing blueprint
        #load images
        dirt_img = pygame.image.load("level 4 images/dirt.png")
        grass_img = pygame.image.load("level 4 images/grass.jfif")
        brick_img = pygame.image.load("level 4 images/brick.jfif")
        #Analyze the blueprint
        row_count = 0   #counter for determining rectangle y-coordinate of each tile
        for row in data:    #looks in a row of blueprint each iteration
            col_count = 0   #counter for determining rectangle x-coordinate of each tile
            for tile in row:    #looks in each individual column/tile in the row
                if tile == 1:   # Dirt
                    img = pygame.transform.scale(dirt_img, (tile_size,tile_size))#fix scale of image to tile size
                    img_rect = img.get_rect() #get rectangle of image which is now tile sized
                    img_rect.x = col_count * tile_size #x position of rectangle increasing with each tile
                    img_rect.y = row_count * tile_size #y position of rectangle increasing with each tile
                    tile = (img,img_rect)   #tuple containing the image and its rectangle
                    self.tile_list.append(tile) #adds the tile data to the tile list
                if tile == 2:  # Grass
                    img = pygame.transform.scale(grass_img,(tile_size, tile_size))  # fix scale of image to tile size
                    img_rect = img.get_rect()  # get rectangle of image which is now tile sized
                    img_rect.x = col_count * tile_size  # x position of rectangle increasing with each tile
                    img_rect.y = row_count * tile_size  # y position of rectangle increasing with each tile
                    tile = (img, img_rect)  # tuple containing the image and its rectangle
                    self.tile_list.append(tile)  # adds the tile data to the tile list
                if tile == 3: # Enemy
                    slime = Enemy(col_count * tile_size, row_count * tile_size)
                    slime_group.add(slime)
                if tile == 4: # Horizontal-moving platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5: # Vertical-moving platform
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6: # Lava
                    lava = Lava(col_count * tile_size, row_count * tile_size + tile_size // 2)
                    lava_group.add(lava)
                if tile == 7: # Coin
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8: # Exit
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 9: # Brick
                    img = pygame.transform.scale(brick_img, (tile_size, tile_size))  # fix scale of image to tile size
                    img_rect = img.get_rect()  # get rectangle of image which is now tile sized
                    img_rect.x = col_count * tile_size  # x position of rectangle increasing with each tile
                    img_rect.y = row_count * tile_size  # y position of rectangle increasing with each tile
                    tile = (img, img_rect)  # tuple containing the image and its rectangle
                    self.tile_list.append(tile)  # adds the tile data to the tile list
                col_count += 1  #move rectangle onto the next tile (x-coordinate)
            row_count += 1  #move rectangle onto the next tile (y-coordinate)

    def draw(self): #after processing and collecting useful data of world blueprint, this draws it into the level
        for tile in self.tile_list: #iterates over each tile in tile list which contains image and its rectangle and constantly draws them
            screen.blit(tile[0],tile[1]) #takes the image and puts it in its rectangle coordinates
            #display tile hitbox
            #pygame.draw.rect(screen,(255,255,255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("level 4 images/SlimeOrange/slime0.png")
        self.image = pygame.transform.scale(self.image,(62,50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1



class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("level 4 images/liquidLavaTop_mid.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("level 4 images/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


#reset level funciton
#reset level funciton
def reset_level(level,player):
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
    world = World(world_data)  # (runs once outside game loop)

    return world #take a receipt for game loop


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("level 4 images/platform.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1



class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("level 4 images/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

base_enemyGroup = pygame.sprite.Group()
class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Preassets/img/blob.png")
        self.image = pygame.transform.scale(self.image,(self.image.get_width()//2,self.image.get_height()//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.movespeed=1
        self.moveCounter=0
    def update(self) :
        self.rect.x+=self.movespeed
        self.moveCounter+=1
        if abs(self.moveCounter)>25:

            self.movespeed*=-1
            self.moveCounter*=-1
