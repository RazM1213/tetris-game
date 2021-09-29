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




