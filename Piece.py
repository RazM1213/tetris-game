from tetris import shape_colors,shapes

class Piece(object):
    rows = 20
    columns = 10

    def __init__(self,column,row,shape):
        self.x = column
        self.y = row
        self.shape = shape #The piece's shape out of the shapes list
        self.color = shape_colors[shapes.index(shape)] #Color index accordingly to the shape index
        self.rotation = 0 #For shapes that can be rotated - its the multidimensional index for the shapes formats
