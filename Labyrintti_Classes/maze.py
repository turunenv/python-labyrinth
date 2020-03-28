from square import Square
import random

class Maze():
    
    #create the initial maze with given width and height
    def __init__(self,width,height):
        self.squares = [[Square(x,y) for y in range(height)]for x in range(width)]
        self.width = width
        self.height = height
                
                
    
    def carve_maze(self):
       
        #generate random sell from which to start carving the maze
        x = random.randint(0,self.width)
        y = random.randint(0,self.height)
        self.squares[x][y].has_been_visited = True
        squarelist = [self.squares[x][y]]
        
    
    
    
    
    
    
    
    
    
    
    
    #returns list of unvisited neighbour squares 
    def unvisited_neighbours(self,square):
        
        #sets numeric tuples for possible directions
        directions = [('N',(0,-1)),('S',(0,1)),('W',(-1,0)),('E',(1,0))]
        
        unvisited = []
        
        #checks all directions for possible neighbour cells.
        for direction, (xi,yi) in directions:
            if (0 <= (square.x + xi) < self.width) and (0 <= square.y + yi < self.height):
                
                #checks if found neighbour has been visited, if not, adds to the list
                if (self.squares[square.x+xi][square.y+yi].has_been_visited()):
                    unvisited.append(direction,self.squares[square.x+xi][square.y+yi])
                
        return unvisited
    
    
    
    
    
    
    
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
                    
            
        
        
                