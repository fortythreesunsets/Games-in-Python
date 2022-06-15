import math
import random

import pygame
import tkinter as tk
from tkinter import messagebox

pygame.init()


# Objects
class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.position = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.position = (self.position[0] + self.dirnx, self.position[1] + self.dirny)

    def draw(self, surface, eyes=False):
        distance = self.w // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(surface, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))

        if eyes:
            centre = distance // 2
            radius = 3
            circle_middle = (i * distance + centre - radius, j * distance + 8)
            circle_middle2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


# the snake is a list of cubes
class Snake(object):
    body = []
    turns = {}

    # Create the snake
    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    # Move the snake
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

        for i, s_cube in enumerate(self.body):
            pos = s_cube.position[:]
            if pos in self.turns:  # check if position is in the turn list
                turn = self.turns[pos]  # move in the turn list at the p index
                s_cube.move(turn[0], turn[1])
                if i == len(self.body) - 1:  # if we are in the last cube, we are going to remove the turn
                    self.turns.pop(pos)
            else:
                # check if the snake has reached the end of the screen
                if s_cube.dirnx == -1 and s_cube.position[0] <= 0:
                    s_cube.position = (s_cube.rows - 1, s_cube.position[1])  # if left border, change direction to right
                elif s_cube.dirnx == 1 and s_cube.position[0] >= s_cube.rows - 1:
                    s_cube.position = (0, s_cube.position[1])  # if right border, change direction to left
                elif s_cube.dirny == 1 and s_cube.position[1] >= s_cube.rows - 1:
                    s_cube.position = (s_cube.position[0], 0)  # if down border, change direction to up
                elif s_cube.dirny == -1 and s_cube.position[1] <= 0:
                    s_cube.position = (s_cube.position[0], s_cube.rows - 1)  # if up border, change direction to down
                else:
                    s_cube.move(s_cube.dirnx, s_cube.dirny)

    def reset(self, position):
        self.head = Cube(position)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        # add cube when the snake eats the snack
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.position[0] - 1, tail.position[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.position[0] + 1, tail.position[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.position[0], tail.position[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.position[0], tail.position[1] + 1)))

        # get the current direction of the tail so the cube moves in that direction
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, s_cube in enumerate(self.body):
            # if the cube is the 1st in the list, draw eyes on it
            if i == 0:
                s_cube.draw(surface, True)
            else:
                s_cube.draw(surface)


# Functions
def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for line in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


def redraw_window(surface):
    global rows, width, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    snack_positions = item.body

    while True:
        # generate random numbers for x,y
        x = random.randrange(rows)
        y = random.randrange(rows)
        # check if the random numbers fall into the snake to avoid putting a snack on top of the snake
        if len(list(filter(lambda z: z.position == (x, y), snack_positions))) > 0:
            continue
        else:
            break
    return x, y


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, snake, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = Snake((255, 0, 0), (10, 10))
    snack = Cube(random_snack(rows, snake), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.add_cube()
            snack = Cube(random_snack(rows, snake), color=(0, 255, 0))

        for x in range(len(snake.body)):
            if snake.body[x].position in list(map(lambda z: z.position, snake.body[x + 1:])):
                print('Score: ', len(snake.body))
                message_box('You lost!', 'Play again...')
                snake.reset((10, 10))
                break

        redraw_window(win)


main()