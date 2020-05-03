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
        self.mouse.setFont(QtGui.QFont("Arial", square_size, QtGui.QFont.Bold))
        self.quitting = False
        self.path = None
        self.solved = False

        self.square_size = square_size
        
        self.init_window()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.move_mouse)
        self.timer.start(10) # Milliseconds
        
        
        
        
        
        
        

       

        
        
    def init_window(self):
        
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Labyrintti')
        
        self.move_mouse()
        self.show()
        
        
        
        
    
    def keyPressEvent(self,event):
        square = self.maze.get_mouse_square()
        moving = False
        #check if mouse if on top or on the under square
        if self.maze.get_square(square.x,square.y).mouse:
            we_are_under = False
        else:
            we_are_under = True
        direction = None
        
        
        
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
            
        if event.key() == Qt.Key_Q:
            
            self.quitting = True
            self.update()
            
            
            
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
                        
                        
                        
                        
            #if we are under a square, we can only get out from the direction we came from or the opposite
                
            else:
                 
                 if not square.walls[direction]:
                     square.remove_mouse()
                     self.maze.get_square(square.x+xi,square.y+yi).add_mouse()
                     we_are_under = False
                
        
        

       
    #look for mouse location in the maze and its location  
    def move_mouse(self):
        
        length = self.square_size
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                square = self.maze.get_square(x,y)
                if square.mouse:
                    self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size, QtGui.QFont.Bold))
                    self.mouse.move(length*square.x + (length-self.basic_font_size)/2,length*square.y + (length-self.basic_font_size)/2)
                
                #represent mouse being under a square by showing it with smaller fontsize
                elif square.has_square_under():
                    if square.get_under_square().mouse:
                        self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size/2, QtGui.QFont.Bold))
                        self.mouse.move(length*square.x + ((length-self.basic_font_size/2)/2),length*square.y + ((length-self.basic_font_size/2)/2))
                    
      
      
      
                
                
                
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
            
            self.drawWalls(painter,self.maze)
            self.drawSolution(painter,self.maze,self.path)
            
            painter.end()
        

        print("printcount: {}".format(self.count))        
         
       
            
        
       
                
        
        
        
        
    def drawWalls(self,painter,maze):
        pen = QPen(Qt.black, 5, Qt.SolidLine)  
        painter.setPen(pen)
        pen1 = QPen(Qt.darkBlue)
        pen1.setStyle(Qt.DotLine)
        
         
        
        length = self.square_size 
        
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                square = self.maze.get_square(x,y) 
                
                if square.has_this_wall('N'):
                            painter.drawLine((square.x*length),(square.y*length),(square.x*length + length),(square.y*length))
                            
                        
          
          
                if square.has_this_wall('S'):
                    painter.drawLine((square.x*length),((square.y+1)*length),(square.x*length + length),((square.y+1)*length))
                if square.has_this_wall('W'):
                    painter.drawLine((square.x*length),(square.y*length),(square.x*length),(square.y*length + length))
                if square.has_this_wall('E'):
                    painter.drawLine((square.x*length + length),((square.y)*length),(square.x*length + length),((square.y+1)*length))
                
                if square.has_square_under():
                    
                    painter.setPen(pen1)
                    
                    under_square = square.get_under_square()
                    if under_square.has_this_wall('N'):
                        painter.drawLine((square.x*length),(square.y*length),(square.x*length + length),(square.y*length))
                            
                        
          
          
                    if under_square.has_this_wall('S'):
                        painter.drawLine((square.x*length),((square.y+1)*length),(square.x*length + length),((square.y+1)*length))
                    if under_square.has_this_wall('W'):
                        painter.drawLine((square.x*length),(square.y*length),(square.x*length),(square.y*length + length))
                    if under_square.has_this_wall('E'):
                        painter.drawLine((square.x*length + length),((square.y)*length),(square.x*length + length),((square.y+1)*length))
                    painter.setPen(pen)
                    
    
                 
    def drawSolution(self,painter,maze,path):
        
            length = self.square_size   
            pen = QPen(Qt.black, 5, Qt.SolidLine)  
            painter.setPen(pen)
            
            square = maze.get_mouse_square()
            x = square.x
            y = square.y
            
            for p in path:
                
                (x2,y2) = maze.get_direction[p]
                x += x2
                y += y2
                painter.drawEllipse(length*x + length/4,length*y + length/4,length/2,length/2)
            
                
      
                            
                        
        
    
       
            
                
                
                
                
                
                
                
                