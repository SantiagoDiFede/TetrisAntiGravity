import pygame
import random

from Figure import Figure





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
        self.switchRate = 5
        self.tyranny = 0
        self.uprising = 0
        self.order = 0
        self.chaos = 0
        self.forced_switch = 10
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

            

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
                    for i1 in range(i, self.height // 2, -1):
                        for j in range(self.width):
                            self.field[i1][j] = self.field[i1 - 1][j]
                    for j in range(self.width):
                        self.field[self.height // 2][j] = 0
                    self.tyranny += 1
                else:
                    for i1 in range(i, self.height//2 - 1, 1):
                        for j in range(self.width):
                            self.field[i1][j] = self.field[i1 + 1][j]
                    for j in range(self.width):
                        self.field[self.height//2 - 1][j] = 0
                    self.uprising += 1
                        
                        

        for i in range(0, self.width):
            zeros = 0
            for j in range(self.height):
                if self.field[j][i] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                if i > mid_width:
                    for i1 in range(i, self.width // 2 + 1, -1):
                        for j in range(self.height):
                            self.field[j][i1] = self.field[j][i1 - 1]
                    for j in range(self.height):
                        self.field[j][self.width // 2 + 1] = 0
                    self.order += 1
                else:
                    for i1 in range(i, self.width // 2 - 1, 1):
                        for j in range(self.height):
                            self.field[j][i1] = self.field[j][i1 + 1]
                    for j in range(self.height):
                        self.field[j][self.width // 2 - 1] = 0
                    self.chaos += 1
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
        if self.gravity=='down':
            self.figure.y -= 1
        elif self.gravity=='up':
            self.figure.y += 1
        elif self.gravity=='left':
            self.figure.x += 1
        elif self.gravity=='right':
            self.figure.x -= 1
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
        gravity_list = ['down', 'up', 'left', 'right']
        gravity_list.remove(self.gravity)
        self.gravity = random.choice(gravity_list)
        if self.gravity == 'down':
            self.screen_rotation = 0
        elif self.gravity == 'up':
            self.screen_rotation = 180
        elif self.gravity == 'left':
            self.screen_rotation = 90
        elif self.gravity == 'right':
            self.screen_rotation = 270


