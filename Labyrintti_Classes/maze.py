from square import Square
import random
from numpy import square

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
        
        '''
        Using "growing tree" -algorithm for generating the weave-maze:
        - first we add randomly selected square to list squarelist
        - next we select random unvisited neighbour, carve the wall and add that square to the list
        -continue until select square with no unvisited neighbours:
            *then check weather carving under another passage is possible
            -> if yes, carve
            ->if not, remove squares from the list until faced with square with unvisited
        -when list is empty, maze is complete
        
        '''
        while(len(squarelist) != 0):
            len_squarelist = len(squarelist)
            current_square = squarelist[len_squarelist - 1] #select newest square in squarelist
            unvisited = self.unvisited_neighbours(current_square)
            num_options = len(unvisited)
            
            if (num_options == 0):
                '''
                if (possible_to_carve_under?):
                    carve_under
                
                *** requirements: ***
                -passage must be perpendicular to the passage we are carving under
                -square on the other side must be unvisited and within bounderies
                '''
                #no options to move into -> remove square from list
                unvisited.remove(current_square)
            else:
                #unvisited neighbours found, select one randomly from the list
                direction,random_neighbour = random.choise(unvisited)
                current_square.remove_wall(random_neighbour,direction)
                current_square = random_neighbour
                squarelist.append(current_square) 
                
                
    
    
    
    
    
    
    
    
    
    
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
                    
            
        
        
                