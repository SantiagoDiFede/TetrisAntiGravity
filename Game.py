import random
import time
import pygame

from Tetris import Tetris


neutral_colors = [
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


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

size = (400,400)
screen = pygame.display.set_mode(size)

pressed_right_time = 0
pressed_left_time = 0
key_repeat_interval = 0.1
pressing_right = False
pressing_left = False

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
image_blank = pygame.image.load("Eyes/1174418.png").convert_alpha()
center_x = game.x + (game.width // 2) * game.zoom
center_y = game.y + (game.height // 2) * game.zoom
game.uprising = 0
game.order = 0
game.tyranny = 0
game.chaos = 0
image_down = pygame.transform.scale(image_down, (game.zoom*4, game.zoom*4))
image_up = pygame.transform.scale(image_up, (game.zoom*4, game.zoom*4))
image_left = pygame.transform.scale(image_left, (game.zoom*4, game.zoom*4))
image_right = pygame.transform.scale(image_right, (game.zoom*4, game.zoom*4))
image_blank = pygame.transform.scale(image_blank, (game.zoom*4, game.zoom*4))
image_down.set_colorkey(WHITE)
image_up.set_colorkey(WHITE)
image_left.set_colorkey(WHITE)
image_right.set_colorkey(WHITE)
image_blank.set_colorkey(WHITE)
center_x = game.x + (game.width // 2-2) * game.zoom
center_y = game.y + (game.height // 2-2) * game.zoom
ready_to_switch = False
switch_count = 15


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
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 20)
                switch_count = 15
                counter = 0
            if event.key == pygame.K_a:
                if game.forced_switch > 0:
                    game.gravity_switch()
                    game.forced_switch -= 1
                    switch_count = 15
    
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

    if keys[pygame.K_LEFT]:
        current_time = time.time()
        if not pressing_left or current_time - pressed_left_time > key_repeat_interval:
            pressing_left = True
            pressed_left_time = current_time

            if game.gravity == 'down':
                game.go_side(-1)
            elif game.gravity == 'right':
                game.go_down()
            elif game.gravity == 'up':
                game.go_side(1)
            elif game.gravity == 'left':
                game.go_up()

    if keys[pygame.K_RIGHT]:
        current_time = time.time()
        if not pressing_right or current_time - pressed_right_time > key_repeat_interval:
            pressing_right = True
            pressed_right_time = current_time

            if game.gravity == 'left':
                game.go_down()
            elif game.gravity == 'down':
                game.go_side(1)
            elif game.gravity == 'up':
                game.go_side(-1)
            elif game.gravity == 'right':
                game.go_up()

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    

            

    screen.fill(WHITE)

    if counter % fps == 0:
        if switch_count > 0:
            switch_count -= 1

    if switch_count == 0:
            ready_to_switch = True

    if switch_count <= 3:
        current_mood = (0, 0, 255)
    else:
        current_mood = RED

    for i in range(game.height):
        for j in range(game.width):
                if i in range(game.height//2-2,game.height//2+2) and j in range(game.width//2-2,game.width//2+2):
                    pygame.draw.rect(screen, current_mood, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                    

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
                    pygame.draw.rect(screen, neutral_colors[game.field[i][j]],
                                [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
    

    if ready_to_switch:
        ready_to_switch = False
        game.gravity_switch()
        switch_count = 15

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, neutral_colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
                    

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 45, True, False)
    rotated_screen = pygame.transform.rotate(screen, game.screen_rotation)
    screen.blit(rotated_screen, rotated_screen.get_rect(center=screen.get_rect().center))

    text = font.render("Score: " + str(game.score), True, BLACK)
    text_time = font.render("Time: " + str(counter // fps), True, BLACK)
    a_counter = font.render("down: " + str(game.uprising), True, BLACK)
    z_counter = font.render("up: " + str(game.tyranny), True, BLACK)
    e_counter = font.render("left: " + str(game.chaos), True, BLACK)
    r_counter = font.render("right: " + str(game.order), True, BLACK)
    forced_switch = font.render("Switch: " + str(game.forced_switch), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))
    text_won = font1.render("Demo Level Cleared", True, (205, 0, 125))
    text_won2 = font1.render("Enter to continue", True, (205, 0, 215))
    

    screen.blit(text, [0, 0])
    screen.blit(forced_switch, [120, 0])
    screen.blit(text_time, [0, 20])
    screen.blit(a_counter, [310, 0])
    screen.blit(z_counter, [310, 20])
    screen.blit(e_counter, [310, 40])
    screen.blit(r_counter, [310, 60])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    
    pygame.display.flip()
    clock.tick(fps)

    if game.uprising >= 3 and game.order >= 3 and game.tyranny >= 3 and game.chaos >= 3:
        game.state = "won"
        screen.blit(text_won, [20, 200])
        screen.blit(text_won2, [25, 265])
        screen.blit(text_game_over1, [35, 265])
        pygame.display.flip()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game.uprising = 0
                game.order = 0
                game.tyranny = 0
                game.chaos = 0
                game.state = "start"
            elif event.key == pygame.K_ESCAPE:
                game.__init__(20, 20)
        


pygame.quit()