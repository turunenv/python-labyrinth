from maze import Maze
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.Qt import QGraphicsRectItem
from PyQt5.QtGui import QPainter, QBrush, qBlue, QPen
from PyQt5.QtCore import Qt



class GUI(QMainWindow):
    
    def __init__(self, maze, square_size):
        super().__init__()
        self.top= 150

        self.left= 150

        self.width = 500

        self.height = 500
        self.maze = maze
        

        self.square_size = square_size
        self.init_window()
        
        

       

        
        
    def init_window(self):
       
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Labyrintti')
        self.show()

       
        
        
    
                
                
                
    def paintEvent(self,event): 
        painter = QPainter()
        painter.begin(self)
        self.drawWalls(painter)
        painter.end()
        
    def drawWalls(self,painter):
         pen = QPen(Qt.black, 5, Qt.SolidLine)  
         painter.setPen(pen)
         painter.setBrush(QBrush(Qt.red, Qt.CrossPattern))
         length = self.square_size 
         for y in range (self.maze.height):
             for x in range (self.maze.width):
                square = self.maze.get_square(x,y)
                if square.has_this_wall('N'):
                    painter.drawLine((square.x*length),(square.y*length),(square.x*length + length),(square.y*length))
                if square.has_this_wall('S'):
                    painter.drawLine((square.x*length),((square.y+1)*length),(square.x*length + length),((square.y+1)*length))
                if square.has_this_wall('W'):
                    painter.drawLine((square.x*length),(square.y*length),(square.x*length),(square.y*length + length))
                if square.has_this_wall('E'):
                    painter.drawLine((square.x*length + length),((square.y)*length),(square.x*length + length),((square.y+1)*length))
                 
        
        
       
            
                
                
                
                
                
                
                
                