import numpy as np
import math
import random
import pygame as p
import sys

sys.setrecursionlimit(10000)

squareSize = 30

width, height = 40, 20
winWidth, winHeight = width*squareSize, height*squareSize

noOfMines = math.floor(width * height * 0.15)

load = lambda src : p.transform.scale(p.image.load(src), (squareSize, squareSize))
tileImg = load("Images/tile.png")
numbers = [load("Images/numbers/" + str(i+1) + ".png") for i in range(8)]
mine = load("Images/mine.png")
flag = load("Images/flag.png")

bgColour = (179, 179, 179)
black = (0, 0, 0)

canClick = False

p.init()
win = p.display.set_mode((winWidth, winHeight))
win.fill(bgColour)
p.display.flip()

class Board:
    def __init__(self):
        self.board = np.zeros((height, width), int)
        self.visited = np.zeros((height, width), int)
        self.mines = []

    def setup_game(self):
        b.generate_mines()
        b.create_count_map()
        b.display()

    def generate_mines(self):
        count = 0
        while count != noOfMines:
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            if not self.board[y][x] == -1:
                self.board[y][x] = -1
                self.mines.append((x, y))
                count += 1

    def get_neighbors_of(self, x, y, unvisited = False):
        neighbors = []
        for vector in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if y + vector[1] < height and y + vector[1] >= 0 and x + vector[0] >= 0 and x + vector[0] < width:
                if unvisited:
                    if self.visited[y + vector[1]][x + vector[0]] == 0:
                        neighbors.append((x + vector[0], y + vector[1]))
                else:
                    neighbors.append((x + vector[0], y + vector[1]))
        return neighbors

    def create_count_map(self):
        for y in range(height):
            for x in range(width):
                if self.board[y][x] != -1:
                    for neighbor in self.get_neighbors_of(x, y):
                        if neighbor[1] < height and neighbor[1] >= 0 and neighbor[0] >= 0 and neighbor[0] < width and self.board[neighbor[1]][neighbor[0]] == -1:
                                self.board[y][x] += 1

    def display(self):
        win.fill(bgColour)
        for x in range(0, width):
            for y in range(0, height):
                pos = (x * squareSize, y * squareSize, squareSize, squareSize)
                if self.visited[y][x] == 0:
                    win.blit(tileImg, pos)
                elif self.visited[y][x] == -1:
                    win.blit(flag, pos)
                else:
                    if self.board[y][x] == -1:
                        win.blit(mine, pos)
                    elif self.board[y][x] != 0:
                        win.blit(numbers[self.board[y][x] - 1], pos)
        for x in range(squareSize, winWidth, squareSize):
            p.draw.line(win, black, (x, 0), (x, winHeight))
        for y in range(squareSize, winHeight, squareSize):
            p.draw.line(win, black, (0, y), (winWidth, y))

        p.display.flip()

    def flood_uncover(self, x, y):
        for neighbor in b.get_neighbors_of(x, y):
            if b.board[neighbor[1]][neighbor[0]] != -1 and not b.visited[neighbor[1]][neighbor[0]]:
                b.visited[neighbor[1]][neighbor[0]] = 1
                if b.board[neighbor[1]][neighbor[0]] == 0:
                    self.flood_uncover(neighbor[0], neighbor[1])

def left_click(x, y):
    if b.visited[y][x] == 0:
        b.visited[y][x] = 1
        if b.board[y][x] == 0:
            b.flood_uncover(x, y)
        elif b.board[y][x] == -1:
            b.visited = np.ones((height, width), bool)

def right_click(x, y):
    if b.visited[y][x] == 0:
        b.visited[y][x] = -1
    elif b.visited[y][x] == -1:
        b.visited[y][x] = 0

b = Board()
b.setup_game()

if __name__ == "__main__":
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                exit()

        x, y = p.mouse.get_pos()
        x = x // squareSize
        y = y // squareSize
        
        mouse = p.mouse.get_pressed()

        if mouse[0] or mouse[2]:
            b.display()
            if canClick:
                if mouse[0]:
                    left_click(x, y)
                elif mouse[2]:
                    right_click(x, y)
            canClick = False

        else:
            canClick = True