import pygame
import random


imp =pygame.image.load('red-skull.jpg')

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
    (180, 134, 22),
    (180, 134, 122),
    (180, 134, 222),
    (180, 234, 22),
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x =   0
        self.y = 0
        self.zoom = 20
        self.figure = None
        self.height = height
        self.width = width
        self.startX = width // 2 - 2
        self.startY = height //2 - 2
        self.gravity = 'down'
        self.field = []
        self.score = 0
        self.state = "start"
        self.screen_rotation = 0
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    #display imp at the center of the field
            

    def new_figure(self):
        self.figure = Figure(self.startX, self.startY)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            i + self.figure.y < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                            

                        intersection = True
        return intersection

    def break_lines(self):
        mid_width = self.width // 2
        mid_height = self.height // 2
        lines = 0
        for i in range(0, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                if i > mid_height:
                    for i1 in range(i, 1, -1):
                        for j in range(self.width):
                            self.field[i1][j] = self.field[i1 - 1][j]
                else:
                    for i1 in range(i, self.height // 2 - 1, 1):
                        for j in range(self.width):
                            self.field[i1][j] = self.field[i1 + 1][j]

        for i in range(0, self.width):
            zeros = 0
            for j in range(self.height):
                if self.field[j][i] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                if i > mid_width:
                    for i1 in range(i, 1, -1):
                        for j in range(self.height):
                            self.field[j][i1] = self.field[j][i1 - 1]
                else:
                    for i1 in range(i, self.width // 2 - 1, 1):
                        for j in range(self.height):
                            self.field[j][i1] = self.field[j][i1 + 1]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            if self.gravity=='down':
                self.figure.y += 1
            elif self.gravity=='up':
                self.figure.y -= 1
            elif self.gravity=='left':
                self.figure.x -= 1
            elif self.gravity=='right':
                self.figure.x += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.gravity!='down':
            if self.intersects():
                self.figure.y -= 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_up(self):
        self.figure.y -= 1
        if self.gravity!='up':
            if self.intersects():
                self.figure.y += 1
        if self.intersects():
            self.figure.y += 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.gravity=='right'or self.gravity=='left':
            if self.intersects():
                self.figure.x = old_x
                self.freeze()
        if self.intersects():
            self.figure.x = old_x


    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation
    
    def gravity_switch(self):
        if self.gravity=='down':
            self.gravity='left'
        elif self.gravity=='left':
            self.gravity='up'
        elif self.gravity=='up':
            self.gravity='right'
        elif self.gravity=='right':
            self.gravity='down'

        #do not rotate the screen but every object in the game
        if self.gravity == 'down':
            self.screen_rotation = 0
        elif self.gravity == 'up':
            self.screen_rotation = 180
        elif self.gravity == 'left':
            self.screen_rotation = 90
        elif self.gravity == 'right':
            self.screen_rotation = 270


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

size = (400,400)
screen = pygame.display.set_mode(size)


pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 20)
counter = 0
image_down = pygame.image.load("Eyes/Eye_down.png").convert_alpha()
image_up = pygame.image.load("Eyes/Eye_up.png").convert_alpha()
image_left = pygame.image.load("Eyes/Eye_left.png").convert_alpha()
image_right = pygame.image.load("Eyes/Eye_right.png").convert_alpha()
center_x = game.x + (game.width // 2) * game.zoom
center_y = game.y + (game.height // 2) * game.zoom
#scale the image to the size of 4*4 squares
image_down = pygame.transform.scale(image_down, (game.zoom*4, game.zoom*4))
image_up = pygame.transform.scale(image_up, (game.zoom*4, game.zoom*4))
image_left = pygame.transform.scale(image_left, (game.zoom*4, game.zoom*4))
image_right = pygame.transform.scale(image_right, (game.zoom*4, game.zoom*4))
image_down.set_colorkey(WHITE)
image_up.set_colorkey(WHITE)
image_left.set_colorkey(WHITE)
image_right.set_colorkey(WHITE)


pressing_down = False

while not done:

    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 0.5) == 0 or pressing_down:
        if game.state == "start":
            if game.gravity=='down':
                game.go_down()
            elif game.gravity=='up':
                game.go_up()
            elif game.gravity=='left':
                game.go_side(-1)
            elif game.gravity=='right':
                game.go_side(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()

            if event.key == pygame.K_LEFT:
                    if game.gravity=='down':
                        game.go_side(-1)
                    elif game.gravity=='right':
                        game.go_down()
                    elif game.gravity=='up':
                        game.go_side(1)
                    elif game.gravity=='left':
                        game.go_up()
            if event.key == pygame.K_RIGHT:
                    if game.gravity=='left':
                        game.go_down()
                    elif game.gravity=='down':
                        game.go_side(1)
                    elif game.gravity=='up':
                        game.go_side(-1)
                    elif game.gravity=='right':
                        game.go_up()

            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_x:
                game.gravity_switch()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 20)
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_DOWN]:
        if game.gravity=='down':
            game.go_down()
        elif game.gravity=='up':
            game.go_up() 
        elif game.gravity=='left':
            game.go_side(-1)
        elif game.gravity=='right':
            game.go_side(1)  
    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)



    for i in range(game.height):
        for j in range(game.width):
                #if it is one of the 8 central squares, display the image
                if i in range(game.height//2-2,game.height//2+2) and j in range(game.width//2-2,game.width//2+2):
                    pygame.draw.rect(screen, RED, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    #display the image over the 8 central squares
                    center_x = game.x + (game.width // 2-2) * game.zoom
                    center_y = game.y + (game.height // 2-2) * game.zoom
                    if game.gravity=='down':
                        screen.blit(image_down, (center_x, center_y))
                    elif game.gravity=='up':
                        screen.blit(image_up, (center_x, center_y))
                    elif game.gravity=='left':
                        screen.blit(image_left, (center_x, center_y))
                    elif game.gravity=='right':
                        screen.blit(image_right, (center_x, center_y))
                else:
                    pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
    


    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    rotated_screen = pygame.transform.rotate(screen, game.screen_rotation)
    screen.blit(rotated_screen, rotated_screen.get_rect(center=screen.get_rect().center))

    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()