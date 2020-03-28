from square import Square
import random

class Maze():
    
    #create the initial maze with given width and height
    def __init__(self,width,height):
        self.squares = [[Square(x,y) for y in range(height)]for x in range(width)]
        self.width = width
        self.height = height
                
                
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def __str__(self):
        #print a string representation of the maze
        
        #print northern walls of the maze
        rows = ['|' + '-*'*self.width]
        
        #print maze row by row
        for y in range(self.height):
            row = ['|'] #set initial western wall to first square
            for x in range(self.width):
                if self.squares[x][y].walls['E'] == True: #check every square for eastern wall
                    row.append(' |')
                else:
                    row.append('  ')
            rows.append(''.join(row))
            
            #check every square for the southern walls
            row = ['|']
            for x in range(self.width):
                if self.squares[x][y].walls['S'] == True:
                    row.append('-*')
                else:
                    row.append(' *')
            rows.append(''.join(row))
            
        return '\n'.join(rows)
                    
            
        
        
                