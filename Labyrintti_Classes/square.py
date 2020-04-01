from __builtin__ import False, True
from Carbon.Aliases import true
class Square():
    
    # The Class Square represents a single square in the labyrinth.
    # A Square may be surrounded by walls from north, south, east and west.
    # At initialization, squares are surrounded by all four walls.
    
    #walls separate two squares in north-south and west-east directions
    walls_between_squares = {'N':'S','S':'N','W':'E','E':'W'}
    
    #initialize square at position x,y with all walls.
    #initially, none of the squares have the mouse in it.
    def __init__(self,x,y):
        
        self.x = x
        self.y = y
        self.walls = {'N':True,'S':True,'W':True,'E':True}
        self.mouse = False
        #tells us weather the square is under another square
        self.is_under = False
        
        
    
    #remove wall between square and neighbour
    def remove_wall(self,neighbour,wall):
        self.walls[wall] = False
        neighbour.walls[Square.walls_between_squares[wall]] = False
        
    #square has not been vi sited, if it still has all four walls
    def has_not_been_visited(self):
        return all(self.walls.values())
    
    
    #check for vertical straight carved passages for weave-carving
    def vertical_passage(self):
        if not (self.walls['N'] and self.walls['S']):
            return True
    def horizontal_passage(self):
        if not(self.walls['W'] and self.walls['E']):
            return True