from maze import Maze
from square import Square
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView,\
    QLineEdit, QLabel, QVBoxLayout,QPlainTextEdit
from PyQt5.Qt import QGraphicsRectItem
from PyQt5.QtGui import QPainter, QBrush, qBlue, QPen
from PyQt5.QtCore import Qt, QTimer, QBasicTimer
from PyQt5.QtTest import QTest






class GUI(QMainWindow):
    
    def __init__(self, maze, square_size):
        super().__init__()
        self.top= 150

        self.left= 150

        self.width = 500
        self.count = 0
        self.height = 500
        self.maze = maze
        
        self.mouse = QtWidgets.QLabel(self)
        self.mouse.setText(self.maze.get_mouse_symbol())
        self.basic_font_size = square_size*0.6
        self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size, QtGui.QFont.Bold))
        
        
        
        
        
        self.quitting = False
        self.path = None
        self.solved = False
        
        self.quit_button = QtWidgets.QPushButton(self)
        self.save_button = QtWidgets.QPushButton(self)
        self.god_mode = QtWidgets.QPushButton(self)
        
        

        self.square_size = square_size
        
        self.init_window()
        
        
        
        
        
        
         
        
        
        
        
        
        
        

       

        
        
    def init_window(self):
        
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Labyrintti')
        
        self.quit_button.setText("QUIT")
        self.quit_button.setGeometry(550,5,145,40)
        self.quit_button.setStyleSheet("background-color:rgb(39,97,155)")
        self.quit_button.clicked.connect(self.show_solution_and_quit)
        
        self.save_button.setText("SAVE GAME")
        self.save_button.setGeometry(550,50,145,40)
        self.save_button.setStyleSheet("background-color:rgb(190,190,100)")
        
        self.god_mode.setText("GOD MODE")
        self.god_mode.setGeometry(550,95,145,40)
        self.god_mode.setStyleSheet("background-color:rgb(155,39,116)")
        
        
        self.show()
        
    def show_solution_and_quit(self):
            self.quitting = True
            self.update()
        
        
        
        
    
    def keyPressEvent(self,event):
        square = self.maze.get_mouse_square()
        moving = False
        #check if mouse is on top or on the under square
        if self.maze.get_square(square.x,square.y).mouse:
            we_are_under = False
        else:
            we_are_under = True
        direction = None
        
        #check if user has quit the game
        if not self.quitting:
        
            if event.key() == Qt.Key_Right:
                direction = 'E'
                
                moving = True
            if event.key() == Qt.Key_Left:
                
                direction = 'W'
                moving = True
            if event.key() == Qt.Key_Up:
                
                direction = 'N'
                moving = True
            if event.key() == Qt.Key_Down:
                
                direction = 'S'
                moving = True
                
            
                
                
                
            #user pressed a command arrow
            if moving:
                
                (xi,yi) = self.maze.get_direction[direction]
                
                if not we_are_under:
                   
                    #check if square in the moving direction exists
                    if self.maze.square_in_bounderies(square.x+xi,square.y+yi) == True:
                        
                        
                        #does the mouse square have a wall in the moving direction?
                        if square.walls[direction]:
                            
                            #check if next square has a square under that we can move into
                            if self.maze.get_square(square.x+xi,square.y+yi).has_square_under():
                               
                                square.remove_mouse()
                                self.maze.get_square(square.x+xi,square.y+yi).get_under_square().add_mouse()
                                
                                
                                
                                
                                we_are_under = True
                         
                         #else, we can move the mouse in to the next square       
                        else:
                            
                            square.remove_mouse()
                            self.maze.get_square(square.x+xi,square.y+yi).add_mouse()
                            self.update()
                            
                            
                            
                            
                #if we are under a square, we can only get out from the direction we came from or the opposite
                    
                else:
                     
                     if not square.walls[direction]:
                         square.remove_mouse()
                         self.maze.get_square(square.x+xi,square.y+yi).add_mouse()
                         we_are_under = False
                         self.update()
                    
        
        

       
    #locate mouse correctly to the window, and check from mx,my weather its on the surface or under 
    def draw_mouse(self,loc_x,loc_y,mx,my):
        
        if self.maze.get_square(mx,my).mouse:
            self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size, QtGui.QFont.Bold))
            self.mouse.move(loc_x*self.square_size,loc_y*self.square_size)
        else:
           self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size*0.3, QtGui.QFont.ExtraLight)) 
           self.mouse.move(loc_x*self.square_size,loc_y*self.square_size)
           
            
                    
      
      
      
                
                
                
    def paintEvent(self,event): 
        
        self.count +=1
        if not self.quitting:
            painter = QPainter()
            painter.begin(self)
            
            self.drawWalls(painter,self.maze)
            #print("printcount: {}".format)
            
            painter.end
        else:
            if not self.solved:
                path = self.maze.find_shortest_path()
                self.path = str(path)
                self.solved = True
                
            painter = QPainter()
            painter.begin(self)
            
            
            self.drawSolution(painter,self.maze,self.path)
            
            painter.end()
        

        print("printcount: {}".format(self.count))        
         
       
            
        
       
                
        
        
        
        
    def drawWalls(self,painter,maze):
        pen = QPen(Qt.black, 5, Qt.SolidLine)  
        painter.setPen(pen)
        pen1 = QPen(Qt.darkBlue)
        pen1.setStyle(Qt.DotLine)
        
        squares_to_display = int(700/self.square_size) #calculate the amount of squares we can fit on the screen
        mouse_square = self.maze.get_mouse_square()
        mx = mouse_square.x
        my = mouse_square.y
        
        count_y = 0
        
        
        length = self.square_size 
        
        for y in range(mouse_square.y - int(squares_to_display/2 -1), mouse_square.y - int(squares_to_display/2 -1) + squares_to_display):
            count_x = 0
            for x in range(mouse_square.x - int(squares_to_display/2 - 1), mouse_square.x - int(squares_to_display/2 - 1) + squares_to_display):
                
                #check if x and y are within range
                if self.maze.square_in_bounderies(x,y):
                    square = self.maze.get_square(x,y)
                    if square.x == mx and square.y == my:
                        
                        self.draw_mouse(count_x, count_y,x,y)
                        
                    
                            
                    
                    if square.has_this_wall('N'):
                                painter.drawLine((count_x*length),(count_y*length),(count_x*length + length),(count_y*length))
                                
                            
              
              
                    if square.has_this_wall('S'):
                        painter.drawLine((count_x*length),((count_y+1)*length),(count_x*length + length),((count_y+1)*length))
                    if square.has_this_wall('W'):
                        painter.drawLine((count_x*length),(count_y*length),(count_x*length),(count_y*length + length))
                    if square.has_this_wall('E'):
                        painter.drawLine((count_x*length + length),((count_y)*length),(count_x*length + length),((count_y+1)*length))
                    
                    if square.has_square_under():
                        
                        painter.setPen(pen1)
                        
                        under_square = square.get_under_square()
                        if under_square.has_this_wall('N'):
                            painter.drawLine((count_x*length),(count_y*length),(count_x*length + length),(count_y*length))
                                
                            
              
              
                        if under_square.has_this_wall('S'):
                            painter.drawLine((count_x*length),((count_y+1)*length),(count_x*length + length),((count_y+1)*length))
                        if under_square.has_this_wall('W'):
                            painter.drawLine((count_x*length),(count_y*length),(count_x*length),(count_y*length + length))
                        if under_square.has_this_wall('E'):
                            painter.drawLine((count_x*length + length),((count_y)*length),(count_x*length + length),((count_y+1)*length))
                        painter.setPen(pen)
                    count_x +=1
                        
            count_y += 1
                 
    def drawSolution(self,painter,maze,path):
            
            #fit the whole labyrinth on the screen and show the solution
            size = max(self.maze.width,self.maze.height)
            if 650/size < self.square_size:
                length = 650/size
            else:
                length = self.square_size
            pen = QPen(Qt.black, 5, Qt.SolidLine)  
            painter.setPen(pen)
            pen1 = QPen(Qt.darkBlue)
            pen1.setStyle(Qt.DotLine)
            
            for y in range(self.maze.height):
                for x in range (self.maze.width):
                    square = self.maze.get_square(x,y)
                    
                        
                    
                            
                    
                    if square.has_this_wall('N'):
                                painter.drawLine((x*length),(y*length),(x*length + length),(y*length))
                                
                            
              
              
                    if square.has_this_wall('S'):
                        painter.drawLine((x*length),((y+1)*length),(x*length + length),((y+1)*length))
                    if square.has_this_wall('W'):
                        painter.drawLine((x*length),(y*length),(x*length),(y*length + length))
                    if square.has_this_wall('E'):
                        painter.drawLine((x*length + length),((y)*length),(x*length + length),((y+1)*length))
                    
                    if square.has_square_under():
                        
                        painter.setPen(pen1)
                        
                        under_square = square.get_under_square()
                        if under_square.has_this_wall('N'):
                            painter.drawLine((x*length),(y*length),(x*length + length),(y*length))
                                
                            
              
              
                        if under_square.has_this_wall('S'):
                            painter.drawLine((x*length),((y+1)*length),(x*length + length),((y+1)*length))
                        if under_square.has_this_wall('W'):
                            painter.drawLine((x*length),(y*length),(x*length),(y*length + length))
                        if under_square.has_this_wall('E'):
                            painter.drawLine((x*length + length),((y)*length),(x*length + length),((y+1)*length))
                        painter.setPen(pen)
            
            
            
            
            
            
            
            
            
            self.mouse.move(640,670)
            
            
            
            
            
            
            square = maze.get_mouse_square()
            x = square.x
            y = square.y
            
            for p in path:
                
                (x2,y2) = maze.get_direction[p]
                x += x2
                y += y2
                painter.drawEllipse(length*x + length/4,length*y + length/4,length/2,length/2)
            
                
      
                            
                        
        
    
       
            
                
                
                
                
                
                
                
                