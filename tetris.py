import pygame
from Piece import Piece
import random

pygame.font.init()
pygame.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] #RGB decimals

#FUNCTIONS
def create_grid(locked_pos={}):#Keeps the grid updated
    grid = [[(0,0,0) for x in range(10)] for x in range(20)] #10X20 grid - 10 rows, and 20 columns in each row.
    #To check if we have a shape freezing in a given location  - (x,y) - (row,column)
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if (column,row) in locked_pos:
                c = locked_pos[(column,row)]
                grid[row][column] = c
    return grid

def convert_shape_format(shape): #Explaining the computer which shape we want to visualize - from the shape formats list:
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)] #shape.shape -> the list of the possible shape rotations. Each time we press the up key, the shape.rotation adds 1 - and we get the next indexed shape rotation from the shape.shape list.

    #Looping through every row in each shape rotation - to check where there are '.' and '0' - then do something based on it:
    for i,line in enumerate(format): #i - num of line, line - the combination of dots and zeros from x axis
        row = list(line)
        for j,column in enumerate(row): #j- number of columns, column - combination of dots and zeros from y axis
            if column == '0': #If encounter '0' in the column - add it's x and y to the shape's
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 1, pos[1] - 2) #Pushing up the grid the values of the position - to make sure that we get out of the grid when a shape is at it's border.

    return positions

def valid_space(shape, grid):#Checks if the shape is moving to an open space/ not getting out the board
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)] #-->[[(0,1)], [(1,2)], [(2,2)] ........]
    accepted_pos = [j for sub in accepted_pos for j in sub] #Flattenning the above to one dimension [(0,1), (1,2), (2,2) ......]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos: #Checking whether the formatted shape is acceptable or taken
            if pos[1] > -1: #Checks if the space is valid only when the piece starts falling on the screen - y value increments
                return False
    return True

def check_lost(positions): #Lose - when any of the positions passed the top of the game grid - it's y is less than 1
    for pos in positions:
        x,y = pos
        if y < 1: #The y value of the top of the game screen is 1. If we are below it - the game is lost.
            return True
    return False

def get_shape(): #Creates an instance of the Piece class - giving it it's initial attributes.
    return Piece(5, 0, random.choice(shapes))
    #x=5 - The piece will fall from point (5,0)


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, row,col):#Draws and blits the whole grid to the game window
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*block_size), (sx + play_width, sy + i * block_size))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * block_size, sy), (sx + j *block_size, sy + play_height))  # vertical lines
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4) #Drawing the red rect of the grid


def clear_rows(grid, locked):#"Deletes" completed row.
    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row: #If the color black doesn't appear in the row (the row is filled)
            inc += 1 #Number of rows to shift down
            ind = i
            for j in range(len(row)): #Case there's no black square in the row:
                try:
                    del locked[(j,i)] #Delete the colored square
                except:
                    continue #Loop through the row to clear more squares
    if inc > 0:
        for key in sorted(list(locked), key=lambda x:x[1])[::-1]: #Sorts the locked list by it's elements
            x,y = key #Locked position is a key - which has a unique color value
            if y < ind: #Ex: We delete row with index of 17. Then we only move the rows which their y index is lower than 17.
                newKey = (x,y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):#Shows the next shape on the side of the game grid
    font = pygame.font.SysFont('comicsans',30)
    label = font.render('Next shape:', 1, (255,255,255))
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)] #Get the original rotated shape (first index)
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface,shape.color,(sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label,(sx+ 10, sy - block_size))

def draw_window(surface,grid, score = 0):#Draws the whole game window
    surface.fill((0,0,0))#Black fill
    # Tetris Title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30)) #Blits the 'TETRIS' label to the screen

    #Score title:
    font = pygame.font.SysFont('comicsans',30)
    label = font.render(f"SCORE:      {score} ", 1, (255,255,255))
    sx = top_left_x + play_width + 50 #A little right to the game grid
    sy = top_left_y + play_height/2 - 100 #Centered with the grid's vertical axis
    surface.blit(label, (sx + 15, sy + 220))

    #Grid
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)


    draw_grid(surface, 20, 10)
    #Border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
