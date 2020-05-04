from square import Square
import random
import queue
from corrupted_maze_file_error import *





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
    
    
    def find_shortest_path(self):
        paths = queue.Queue()
        paths.put("")
        add = ""
        iter = 0;
        
        #add directions to paths until we find the goal -> this has to be the shortest path
        while not self.findGoal(add):
            iter +=1
            
            add = paths.get()
            for direction in ["N","S","W","E"]:
                put = add + direction
                
                if self.validMove(put):
                    '''
                    shortest path will never be one where we turn right back after going to certain direction:
                    let's make the algorithm smarter by not putting those paths back to the queue:
                    '''
                    if len(add) ==0:
                        paths.put(put)
                       
                    elif not add[len(add)-1] == Square.walls_between_squares[direction]:
                    
                        paths.put(put)
                        
        print("Total iterations: {}".format(iter)) 
        return add            
          
        
        
        
        
        
    
    #check if given path has reached the goal
    def findGoal(self,path):
        start = self.get_mouse_square()
        goal = self.get_square(self.width-1, self.height-1)
        x = start.x
        y = start.y
        
        for direction in path:
            (x1,y1) = self.get_direction[direction]
            x += x1
            y += y1
        if self.get_square(x, y).x == goal.x and self.get_square(x, y).y == goal.y:
            
            return True
        return False
    
    
    #check if we can move to this direction
    def validMove(self,path):
        
        start = self.get_mouse_square()
        goal = self.get_square(self.width-1, self.height-1)
        
        #x1, y1 -> coordinates for the square we are trying to move into
        x1 = start.x
        y1 = start.y
        
        #x2, y2 -> coordinates for square we are moving from, a.k.a. one step behind from path
        x2 = start.x
        y2 = start.y
        
        
        for direction in path: #skip the under_square symbols
           
            
            (xi,yi) = self.get_direction[direction]
            x1 += xi
            y1 += yi
        
        # if len(path) is still 1, we are moving from mouse starting position
        if len(path) > 1:
            
            
            go_back = path[len(path)-1]
            
            
            (xb,yb) = self.get_direction[Square.walls_between_squares[go_back]]
            x2 =x1 + xb
            y2 =y1 + yb
            
        
       
        
        '''
        to see if we are under a square, we check if we "came through a wall" on our last turn, looking at the "surface squares",
        and if the square in the current coordinates actually has a square under it (because we also "go through a wall" when exiting the 
        under_square)
        '''
        
        if len(path) > 1 and self.get_square(x2,y2).walls[Square.walls_between_squares[path[len(path)-2]]] and self.get_square(x2, y2).has_square_under():
            #we are under a square, so we should check the under_square for possible directions
            if not self.get_square(x2, y2).get_under_square().walls[direction]:
                return True
        
        #check that the square we are trying to move into is within boundaries
        elif self.square_in_bounderies(x1, y1):
            #check that there is no wall in this direction 
             
            if not self.get_square(x2, y2).walls[direction]:
                
                return True
            
            
            #if there is a wall, does the square have a square that we can go under?
            else:
                 
                 if self.get_square(x1, y1).has_square_under():
                     
                     
                     
                     return True
        
        return False
    
    
    
    #return 1/5 of the shortest path
    def ask_for_tip(self):
        solution = self.find_shortest_path()
        tip = ""
        for i in range(int(len(solution)/5)): 
            tip += solution[i]
        return tip
        
    
    
    
    
    
    
    
    
    
    
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
                
                
    def save_to_file(self,filename):
        f = open(filename,"w")
        x = self.width
        y = self.height
        
        f.write("{}/{}/{}\n".format(x,y,self.mouse)) #mark labyrinth width,height and mouse_symbol to the first row
        
        
        for a in range(y):
            for b in range(x):
                square = self.get_square(b, a)
                for direction in ["N","E","S","W"]: #write squares to file, marking walls with '1's, no_walls with 0's, going clockwise
                    if square.walls[direction]:
                        f.write('1')
                    else:
                        f.write('0')
                
                if square.has_square_under(): #mark under-squares with true or false
                    f.write('T')
                else:
                    f.write('F')
                f.write('/') #separate squares to make the file more readable
            f.write("\n") #write each row of squares on its own row in the file
            
        mouse_square = self.get_mouse_square()
        x1 = mouse_square.x
        y1 = mouse_square.y
        if self.get_square(x1, y1).mouse: #check if mouse is on the surface or on the possible under-square and mark accordingly -> S=surface, U=under
            f.write("S/{}/{}\n".format(x1,y1))
        else:
           f.write("U/{}/{}\n".format(x1,y1))
        
        f.close()
        
    def load_from_file(filename):
        
            print("Trying to read file now...")
            try:
                f = open(filename,'r')
            except FileNotFoundError:
                raise CorruptedMazeFileError("File not found!")
            print("We made it!")
            line = f.readline()
            x = ""
            y = ""
            i = 0
            while line[i] != '/':
                x += line[i]
                i +=1
            i += 1
            
            while line[i] != '/':
                y += line[i]
                i += 1
            x = int(x)
            y = int(y)
            mouse = line[i+1]
            print("x: {}, y: {}, mouse: {}".format(x,y,mouse))
            
            if not isinstance(x,int) and not isinstance(y,int):
                raise CorruptedMazeFileError("Given measures for width and height not integers!")
            else:
                x_count = 0
                y_count = 0
                
                maze = Maze(x,y,mouse)
                for y1 in range (y):
                    line = f.readline()
                    for x1 in range (x): 
                        for s in range(6): #every square in the file contains 5 characters plus the separator, i.e. '1110F/'
                            if s == 5:
                                if line[x1*6 + s] != '/':
                                    raise CorruptedMazeFileError("Missing separator from squares!")
                            elif s == 4:
                                if line[x1*6 + 4] != 'F' and line[x1*6 + 4] != 'T':
                                    raise CorruptedMazeFileError("Incorrect symbol for marking undersquare!")
                                elif line[x1*6 + 4] == 'T':
                                    maze.get_square(x1,y1).add_under_square()
                                    
                            else:
                                if line[x1*6 + s] != '1' and line[x1*6 +s] != '0':
                                    raise CorruptedMazeFileError("Incorrect symbol in marking walls!")
                                if s == 0 and line[x1*6+s] == '0':
                                    maze.get_square(x1,y1).walls['N'] = False
                                if s == 1 and line[x1*6+s] == '0':
                                    maze.get_square(x1,y1).walls['E'] = False
                                if s == 2 and line[x1*6+s] == '0':
                                    maze.get_square(x1,y1).walls['S'] = False
                                if s == 3 and line[x1*6+s] == '0':
                                    maze.get_square(x1,y1).walls['W'] = False
                        
                        
                            
                         
                                
                        
                        
                line = f.readline()
                surface = line[0]
                if not surface == 'S' or surface == 'U':
                    raise CorruptedMazeFileError("Incorrect symbol in mouse location!") 
                x2 = ""
                y2 = ""
                i = 2
                
                while line[i] != '/':
                    x2 += line[i]
                    i +=1
                i+=1
                
                while line[i] != '\n':
                    y2 += line[i]
                    i +=1
                x2 = int(x2)
                y2 = int(y2)
                print("X: {}, Y: {}".format(x2,y2))
                if not isinstance(x2,int) or not isinstance(y2,int) or x2 < 0 or  x2 >= x or y2 < 0 or y2 >= y:
                    raise CorruptedMazeFileError("Incorrect symbol in mouse directions!") 
                elif surface == 'S':
                    maze.get_square(x2,y2).mouse = True
                else:
                    maze.get_square(x2,y2).get_under_square().mouse = True 
            
            return maze       
                             
               
            
     
            
                 
                    
                         
        
            
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
                    
            
        
        
                