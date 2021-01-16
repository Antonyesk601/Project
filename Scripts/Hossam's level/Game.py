import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

window = pygame.display.set_mode((1300, 750))
pygame.display.set_caption("Level 1")

# the_background_images
background_image = pygame.image.load('last.png')

# Defining game variables
game_over = 0
score = 0

"""Defining Fonts"""
score_font = pygame.font.SysFont('Bauhaus 93', 30)

"""Slicing the the background into boxes"""
box_size = 59

"""Defining colors"""
white = (255, 255, 255)


def drawing_text(text, font, text_colour, x, y):
    img = font.render(text, True, text_colour)
    window.blit(img, (x, y))


class Player:
    def __init__(self, x, y):

        """ For The animation """
        self.character_right = []
        self.character_left = []
        self.index = 0
        self.counter = 0
        for i in range(1, 5):
            character_right = pygame.image.load(f"guy{i}.png")
            character_right = pygame.transform.scale(character_right, (40, 80))
            character_left = pygame.transform.flip(character_right, True, False)
            self.character_left.append(character_left)
            self.character_right.append(character_right)
        self.character = self.character_right[self.index]
        self.direction = 0
        """Character dead"""
        self.dead_image = pygame.image.load('ghost.png')

        """for character assigning"""
        self.rect = self.character.get_rect()
        self.rect.x = x
        self.rect.y = y
        """ For Jumping """
        self.vel_y = 0
        self.jumped = False
        """For the Collision"""
        self.width_collision = self.character.get_width()
        self.height_collision = self.character.get_height()

    def update(self, game_over):
        # Key presses
        dx = 0
        dy = 0
        walking_slower = 5
        if game_over == 0:
            # Getting Key presses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.character = self.character_right[self.index]
                if self.direction == -1:
                    self.character = self.character_left[self.index]

            # Handling the animation
            if self.counter > walking_slower:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.character_right):
                    self.index = 0
                if self.direction == 1:
                    self.character = self.character_right[self.index]
                if self.direction == -1:
                    self.character = self.character_left[self.index]

            # Adding Gravity to jumping
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Checking for collision
            for tile in interface.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width_collision, self.height_collision):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width_collision, self.height_collision):
                    # check if below the ground ==  jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground is falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # Checking for collision with Snakes
            if pygame.sprite.spritecollide(self, snake_group, False):
                game_over = -1

            # updating player Coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.character = self.dead_image
            if self.rect.y > 120:
                self.rect.y -= 5

        # Drawing the Character in the screen
        window.blit(self.character, self.rect)

        return game_over


class Interface:
    def __init__(self, blocks):
        self.tile_list = []
        # assigning blocks images
        dirt_image = pygame.image.load('dirt.png')
        grass_image = pygame.image.load('grass.png')

        row_counter = 0
        for row in blocks:
            column_count = 0
            for tile in row:
                if tile == 1:
                    image = pygame.transform.scale(dirt_image, (box_size, box_size))
                    image_rectangle = image.get_rect()
                    image_rectangle.x = column_count * box_size
                    image_rectangle.y = row_counter * box_size
                    box = (image, image_rectangle)
                    self.tile_list.append(box)
                if tile == 2:
                    image = pygame.transform.scale(grass_image, (box_size, box_size))
                    image_rectangle = image.get_rect()
                    image_rectangle.x = column_count * box_size
                    image_rectangle.y = row_counter * box_size
                    box = (image, image_rectangle)
                    self.tile_list.append(box)
                if tile == 3:
                    snake = Snakes(column_count * box_size, row_counter * box_size + 28)
                    snake_group.add(snake)
                if tile == 4:
                    coin = Coin(column_count * box_size + (box_size // 2), row_counter * box_size + (box_size // 2))
                    coin_group.add(coin)
                column_count += 1
            row_counter += 1

    def drawing(self):
        for tile in self.tile_list:
            window.blit(tile[0], tile[1])


class Snakes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Icons_37.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        coin = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(coin, (box_size // 2, box_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


interface_blocks = [
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

"""Mentioning Classes"""
player = Player(120, 627)

snake_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

interface = Interface(interface_blocks)

run = True

while run:
    window.blit(background_image, (0, 0))

    clock.tick(fps)
    if game_over == 0:
        snake_group.update()
        # Updating The score
        """ Checking if the coin is collected or not"""
        if pygame.sprite.spritecollide(player, coin_group, True):
            score += 1
        drawing_text('X ' + str(score), score_font, white, box_size + 9, 65)

    snake_group.draw(window)
    coin_group.draw(window)
    game_over = player.update(game_over)

    interface.drawing()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
