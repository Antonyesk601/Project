import pickle
from os import path
import pygame
import worldGridDraw as screeninfo
from gamemanager import *
tile_size = 50
fps = 60
pygame.display.set_caption("Game")
bg= pygame.Surface((screeninfo.screenWidth,screeninfo.screenHeight))
bg.set_alpha(255)
bg.fill((255,255,255))
screen_width = 1300
screen_height = 750
font = pygame.font.SysFont("Bauhaus 93", 70)
font_score = pygame.font.SysFont("Bauhaus 93", 30)
font_intro = pygame.font.SysFont("Matura MT Script Capitals", 60)
font_intro2 = pygame.font.SysFont("Snap ITC", 55)
white = (255,255,255)
blue = (100,0,255)
red = (255,0,0)
moon_glow = ((235,245,255))
levelno=4
tkbkg_img = pygame.image.load("level 4 images/level 4 intro.jpg")
tkbkg = pygame.transform.scale(tkbkg_img, (screen_width,screen_height))
tkbg_img = pygame.image.load("level 4 images/NightForest/Forestgrey.png") # Background
tkbg = pygame.transform.scale(tkbg_img,(screen_width,screen_height)) #fix background scale
tkrestart_img = pygame.image.load("level 4 images/restart_btn.png")
tkstart_img = pygame.image.load("level 4 images/start_btn.png")
tkexitbtn_img = pygame.image.load("level 4 images/exit_btn.png")

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
            if pygame.sprite.spritecollide(self, small_slime_group, False):
                game_over = -1
                pygame.mixer.music.stop()
                game_over_fx.play()

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()
            if pygame.sprite.spritecollide(self, water_group, False):
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
        screen.blit(self.image,(self.rect.x,self.rect.y))
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
    def __init__(self,data,enemysize=1): #constructor method takes the blueprint as an argument to process it
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
                    slime = Enemy(col_count * tile_size, row_count * tile_size,enemysize)
                    slime_group.add(slime)
                if tile == 11: # SmallEnemy
                    slime = SmolEnemy(col_count * tile_size+31, 25+row_count * tile_size,enemysize)
                    small_slime_group.add(slime)
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
                if tile == 10:
                    water = Water(col_count * tile_size, row_count * tile_size + 25)
                    water_group.add(water)
                col_count += 1  #move rectangle onto the next tile (x-coordinate)
            row_count += 1  #move rectangle onto the next tile (y-coordinate)

    def draw(self): #after processing and collecting useful data of world blueprint, this draws it into the level
        for tile in self.tile_list: #iterates over each tile in tile list which contains image and its rectangle and constantly draws them
            screen.blit(tile[0],tile[1]) #takes the image and puts it in its rectangle coordinates
            #display tile hitbox
            #pygame.draw.rect(screen,(255,255,255), tile[1], 2)

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('mkmk/mkmk/Water.png')
        self.image = pygame.transform.scale(self.image, (50, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("level 4 images/SlimeOrange/slime0.png")
        self.image = pygame.transform.scale(self.image,(int(62*scale),int(50*scale)))
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


class SmolEnemy(pygame.sprite.Sprite):
    def __init__(self,x,y,scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("level 4 images/SlimeOrange/slime0.png")
        self.image = pygame.transform.scale(self.image,(31,25))
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
def reset_level(level,player,mapdata,resetpositions):
    #reset player position and destroy all entities
    player.reset(resetpositions[0],resetpositions[1])
    slime_group.empty()
    small_slime_group.empty()
    platform_group.empty()
    lava_group.empty()
    exit_group.empty()
    water_group.empty()
    coin_group.empty()
    #load in level data and create world
    if mapdata=="":
        if path.exists(f"level{level}_data"):
            pickle_in = open(f"level{level}_data",
                             "rb")  # open file and read binary to process whatever info is in this file
            mapdata = pickle.load(pickle_in)
    world = World(mapdata)  # (runs once outside game loop)

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
