from square import Square
import random


class Maze():
    #sets numeric tuples for possible directions
    directions = [('N',(0,-1)),('S',(0,1)),('W',(-1,0)),('E',(1,0))]
    get_direction = {'N':(0,-1),'S':(0,1),'W':(-1,0),'E':(1,0)}
    
    #create the initial maze with given width and height
    def __init__(self,width,height,mouse_symbol):
        self.squares = [[Square(x,y) for y in range(height)]for x in range(width)]
        self.width = width
        self.height = height
        self.mouse = mouse_symbol
               
                
    
    def carve_maze(self):
       
        #generate random sell from which to start carving the maze
        x = random.randint(0,self.width-1)
        y = random.randint(0,self.height-1)
        squarelist = []
        squarelist.append(self.squares[x][y])
        
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
               #can we carve under surrounding squares?
                carving_options = self.able_to_carve_under(current_square)
                if(len(carving_options) != 0):
                   direction, random_square = random.choice(carving_options)
                   (xb,yb) = self.get_direction[direction]
                   #create a new square under the neighbour in the right direction
                   under_square = self.get_square(current_square.x + xb, current_square.y + yb).add_under_square()
                   squarelist.append(under_square)
                   next = self.get_square(current_square.x + xb * 2,current_square.y + yb * 2)
                   next.knock_down_single_wall(Square.walls_between_squares[direction])
                   squarelist.append(next)
                #no options to move into -> remove square from squarelist
                else:
                    squarelist.remove(current_square)
                    while (num_options == 0 and len(squarelist) != 0):
                        
                        #do not carve under others while backtracking in order to make the maze visually more clear
                        current_square = squarelist[len(squarelist)-1]
                        unvisited = self.unvisited_neighbours(current_square)
                        num_options = len(unvisited)
                        if num_options == 0:
                            squarelist.remove(current_square)
                    
                        
            else:
                #unvisited neighbours found, select one randomly from the list
                direction,random_neighbour = random.choice(unvisited)
                current_square.remove_wall(random_neighbour,direction)
                current_square = random_neighbour
                squarelist.append(current_square) 
                
                
    
        #make the exit
        self.get_square(self.width-1, self.height-1).knock_down_single_wall('S')
    
    
    
    
    
    
    
    
    #returns list of tuples with unvisited neighbour squares, and their direction 
    def unvisited_neighbours(self,square):
        
        
        
        
        unvisited = []
        
        #checks all directions for possible neighbour cells.
        for direction, (xi,yi) in Maze.directions:
            if (self.square_in_bounderies(square.x + xi, square.y + yi)):
                
                #checks if found neighbour has been visited, if not, adds to the list with the direction
                if (self.get_square(square.x+xi,square.y+yi).has_not_been_visited()):
                    unvisited.append((direction,self.get_square(square.x+xi,square.y+yi)))
                
        return unvisited
    
    def able_to_carve_under(self,square):
        #return list of options to carve under, if found
        options = []
        for direction, (xi,yi) in Maze.directions:
          if (self.square_in_bounderies(square.x + xi, square.y + yi)):
              '''
              For carving horizontally, we need the neighbour-square to have a vertical
              carved passage, and vice versa.
              '''
              if ((direction == 'E' or 'W' and self.get_square(square.x+xi,square.y+yi).vertical_passage()
                   and square.horizontal_passage())
                  or (direction == 'S' or 'N' and self.squares[square.x+xi][square.y+yi].horizontal_passage())
                    and square.vertical_passage()):
                  #square we are going under needs to have a wall on the opposite side of our direction and the direction
                  #itself to make #the visual representation clear
                 
                  if(self.get_square(square.x+xi, square.y+yi).has_this_wall(Square.walls_between_squares[direction])
                     and self.get_square(square.x+xi, square.y+yi).has_this_wall(direction)):
                  
                      #is the square on the other side in bounderies and free?
                      if (self.square_in_bounderies(square.x + xi * 2, square.y + yi * 2)):
                          if (self.get_square(square.x + xi * 2, square.y + yi * 2).has_not_been_visited()):
                              options.append((direction,self.get_square(square.x+xi*2, square.y+yi*2)))                       
                      
        return options      
    
    
    #checks if square with coordinates x,y exist in our maze
    def square_in_bounderies(self,x,y):
        if (0 <= x < self.width) and (0 <= y  < self.height):
            return True
       
    def get_square(self,x,y):
        return self.squares[x][y]
    
    def set_mouse(self):
        w = int(self.width/2)
        h = int(self.height/2)
        #drop mouse in the middle of the maze 
        self.get_square(w, h).add_mouse()
    
    def get_mouse_symbol(self):
        return self.mouse
    def get_mouse_square(self):
        mouse_found = False
        for y in range(self.height):
            if mouse_found:
                break
            for x in range(self.width):
                
                if self.get_square(x, y).mouse:
                    square = self.get_square(x, y)
                    mouse_found = True
                if self.get_square(x, y).has_square_under():
                    if self.get_square(x, y).get_under_square().mouse:
                        square = self.get_square(x, y).get_under_square()
                        mouse_found = True
                        
        if mouse_found:
            return square
            print("MOUSE FOUND IN {},{}".format(square.x,square.y))
            if not self.get_square(x, y).mouse:
                print("mouse is not on the surface but...")
            if self.get_square(x,y).has_mouse_under():
                print("it is under it!!")
        else:
            return self.get_square(0,0)
    
    
    def __str__(self):
        #print a string representation of the maze
        
        #print northern walls of the maze
        rows = ['|' + '-*'*self.width]
        
        #print maze row by row
        for y in range(self.height):
            row = ['|'] #set initial western wall to first square
            for x in range(self.width):
                
                    
                if self.squares[x][y].walls['E'] == True: #check every square for eastern wall
                    if self.squares[x][y].has_square_under():
                           row.append('5|')
                    else: 
                        row.append(' |')
                
                else:
                    if x+1 < self.width and self.squares[x+1][y].walls['W'] == True:
                        '''
                        Because we have removed also single walls with the carving under-method,
                        we have to also check scenarios where the square has no eastern wall but its
                        neighbour has the western wall -> same with southern and northern walls
                        '''
                        if self.squares[x][y].has_square_under():
                            row.append('5|')
                        else:
                            row.append(' |')
                    
                    elif self.squares[x][y].has_square_under():
                        row.append('5 ')
                    else:    
                        row.append('  ')
                    
            rows.append(''.join(row))
            
            #check every square for the southern walls
            row = ['|']
            for x in range(self.width):
                if self.squares[x][y].walls['S'] == True:
                    row.append('-*')
                elif y+1 < self.height and self.squares[x][y+1].walls['N'] == True:
                    row.append('-*')
                else:
                    row.append(' *')
            rows.append(''.join(row))
            
        return '\n'.join(rows)
                    
            
        
        
                