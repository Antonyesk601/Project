import pygame

pygame.init()
vec = pygame.math.Vector2  # 2Dimensional

Height = 750
Width = 1300

#Load images
bg_color = (135, 206, 235)

tile_size = 50
game_over = 0
class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_tile = pygame.image.load('dirt.png')
        block_tile = pygame.image.load('block1.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_tile, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(block_tile, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    slime = Enemy(col_count * tile_size, row_count * tile_size + 25)
                    slime_group.add(slime)
                if tile == 4:
                    water = Water(col_count * tile_size, row_count * tile_size + 25)
                    water_group.add(water)


                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)

class Player():
    def __init__(self,x,y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,21):
            img_right = pygame.image.load(f'2BlueWizardWalk/chara{num}.png')
            img_right = pygame.transform.scale(img_right, (41, 71))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0



    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 20

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 1
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 1
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]


            #animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]





            #gravity
            self.vel_y += 1
            if self.vel_y > 1:
                self.vel_y = 1
            dy += self.vel_y

            #collision
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            #enemies
            if pygame.sprite.spritecollide(self, slime_group, False):
                game_over = -1
            #water
            if pygame.sprite.spritecollide(self, water_group, False):
                game_over = -1




            self.rect.x += dx
            self.rect.y += dy



        #draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)
        return game_over

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('SlimeOrange_00000.png')
        self.image = pygame.transform.scale(self.image, (45, 28))
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

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Water.png')
        self.image = pygame.transform.scale(self.image, (50, 28))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




world_data =[

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


player = Player(100, Height - 175)

slime_group = pygame.sprite.Group()

water_group = pygame.sprite.Group()



world = World(world_data)




screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Game")

run = True
while run == True:

    screen.fill(bg_color)


    world.draw()
    if game_over == 0:
        slime_group.update()
    slime_group.draw(screen)
    water_group.draw(screen)

    game_over = player.update(game_over)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()




