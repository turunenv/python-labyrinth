from maze import Maze
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView
from PyQt5.Qt import QGraphicsRectItem
from PyQt5.QtGui import QPainter, QBrush, qBlue




class GUI(QtWidgets.QMainWindow):
    
    def __init__(self, maze, square_size):
        super().__init__()
        self.setCentralWidget(QtWidgets.QWidget()) # QMainWindown must have a centralWidget to be able to add layouts
        self.horizontal = QtWidgets.QHBoxLayout() # Horizontal main layout
        self.centralWidget().setLayout(self.horizontal)
        self.maze = maze
        self.square_size = square_size
        self.init_window()
        
        

       

        
        
    def init_window(self):
        '''
        Sets up the window.
        '''
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Labyrintti')
        self.show()

        # Add a scene for drawing 2d objects
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 700, 700)

        # Add a view for showing the scene
        self.view = QtWidgets.QGraphicsView(self.scene, self)
        self.view.adjustSize()
        self.view.show()
        self.horizontal.addWidget(self.view)
        self.add_maze_squares()
        
    def add_maze_squares(self):
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                square = QGraphicsRectItem(i*self.square_size,j*self.square_size,self.square_size,self.square_size)
                self.scene.addItem(square)
                
                
                