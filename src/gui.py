
from PyQt5 import QtWidgets, QtGui 
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class GUI(QMainWindow):
    
    def __init__(self, maze, square_size):
        super().__init__()
        self.top= 150

        self.left= 150

        self.width = 500
        
        self.height = 500
        self.maze = maze
        
        self.mouse = QtWidgets.QLabel(self)
        self.mouse.setText(self.maze.get_mouse_symbol())
        self.basic_font_size = square_size*0.6
        self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size, QtGui.QFont.Bold))
        
        
        self.god = False #allow frustrated players to enter god_mode, and go through walls
        
        
        self.quitting = False
        self.path = None
        self.solved = False
        
        self.quit_button = QtWidgets.QPushButton(self)
        self.save_button = QtWidgets.QPushButton(self)
        self.god_mode = QtWidgets.QPushButton(self)
        self.tip = QtWidgets.QPushButton(self) #user can ask for tip: gives 20% of the remaining solution
        
        

        self.square_size = square_size
        
        self.init_window()
        
             
    def init_window(self):
        
        self.setGeometry(300, 300, 700, 700)
        self.setWindowTitle('Labyrintti')
        
        self.quit_button.setText("QUIT")
        self.quit_button.setGeometry(550,5,145,40)
        self.quit_button.setStyleSheet("background-color:rgb(39,97,155)")
        self.quit_button.setToolTip("Quit the game and see the shortest path home.")
        self.quit_button.clicked.connect(self.show_solution_and_quit)
        
        self.save_button.setText("SAVE GAME")
        self.save_button.setGeometry(550,50,145,40)
        self.save_button.setStyleSheet("background-color:rgb(190,190,100)")
        self.save_button.setToolTip("Save your game into a file and continue later!")
        self.save_button.clicked.connect(self.save_to_file)
        
        self.god_mode.setText("GOD MODE: OFF")
        self.god_mode.setGeometry(550,95,145,40)
        self.god_mode.setStyleSheet("background-color:rgb(155,39,116)")
        self.god_mode.setToolTip("Feeling stuck? Clicking here might help...")
        self.god_mode.clicked.connect(self.god_mode_switch)
        
        self.tip.setText("ASK FOR TIP")
        self.tip.setGeometry(550,140,145,40)
        self.tip.setStyleSheet("background-color:rgb(0,255,77)")
        self.tip.setToolTip("Click here for some directions!")
        self.tip.clicked.connect(self.show_tip)
        
        
        
        
        self.show()
        
    def show_solution_and_quit(self):
            self.quitting = True
            self.update()
            
    def god_mode_switch(self):
        if not self.god:
            self.god = True
            
            self.god_mode.setText("GOD MODE: ON")
            self.mouse.setText("G")
        else:
            self.god = False
            self.mouse.setText(self.maze.get_mouse_symbol())
            self.god_mode.setText("GOD MODE: OFF")
            
    def show_tip(self):
        tip = self.maze.ask_for_tip()
        msg = QMessageBox()
        
        msg.setText("Following these directions will help you find home!\n {}".format(tip))
        msg.exec()
        
    def input_dialog(self):
        text,ok = QInputDialog.getText(self,"Save Game","Enter filename:")
        if ok:
            return text
        
        
    def save_to_file(self):
        value = self.input_dialog()
        if not value:
            msg = QMessageBox()
            msg.setText("Enter filename that you want to save the game into!")
            msg.exec()
        else:
            self.maze.save_to_file(value)
            msg = QMessageBox()
            msg.setText("Game saved into file {} successfully!".format(value))
            msg.exec()
            
        
        
        
        
        
        
    
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
                
                if self.god: #allow user to move through walls if in god-mode
                    
                    if self.maze.square_in_bounderies(square.x+xi,square.y+yi) == True:
                        square.remove_mouse()
                        self.maze.get_square(square.x+xi,square.y+yi).add_mouse()
                        self.update()
                    
                else:
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
                                    self.update()
                             
                            #else, we can move the mouse in to the next square       
                            else:
                                
                                square.remove_mouse()
                                self.maze.get_square(square.x+xi,square.y+yi).add_mouse()
                                if self.maze.made_it_home():
                                    self.congratulate()
                                    self.quitting = True
                                
                                self.update()
                                
                    else:
                         
                        if not square.walls[direction]:
                            square.remove_mouse()
                            self.maze.get_square(square.x+xi,square.y+yi).add_mouse()
                            we_are_under = False
                            if self.maze.made_it_home():
                                    self.congratulate()
                                    self.quitting = True
                            self.update()
                        
        
        

       
    #locate mouse correctly to the window, and check from mx,my weather its on the surface or under 
    def draw_mouse(self,loc_x,loc_y,mx,my):
        
        if self.maze.get_square(mx,my).mouse:
            self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size, QtGui.QFont.Bold))
            self.mouse.move(loc_x*self.square_size + (self.square_size - self.basic_font_size)/2,loc_y*self.square_size + (self.square_size - self.basic_font_size)/2)
        else:
            #demonstrate being under a square with smaller font
            self.mouse.setFont(QtGui.QFont("Arial", self.basic_font_size*0.6, QtGui.QFont.ExtraLight)) 
            self.mouse.move(loc_x*self.square_size + (self.square_size - self.basic_font_size*0.6)/2,loc_y*self.square_size + (self.square_size - self.basic_font_size*0.6)/2)
           
            
                    
      
      
      
                
                
                
    def paintEvent(self,event): 
        
        
        if not self.quitting:
            painter = QPainter()
            painter.begin(self)
            
            self.drawWalls(painter,self.maze)
            #print("printcount: {}".format)
            
            painter.end()
        else:
            if not self.solved:
                path = self.maze.find_shortest_path()
                self.path = str(path)
                self.solved = True
                
            painter = QPainter()
            painter.begin(self)
            
            
            self.drawSolution(painter,self.maze,self.path)
            
            painter.end()
        

               
         
       
            
        
       
    def hide_options(self):
        self.quit_button.hide()
        self.god_mode.hide()
        self.tip.hide()
        self.save_button.move(550,5)
    
    def congratulate(self):
        self.hide_options()
        msg = QMessageBox()
        msg.setText("You made it, congratulations!")
        msg.exec()      
        
        
        
        
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
        
        for y in range(mouse_square.y - int(squares_to_display/2), mouse_square.y - int(squares_to_display/2) + squares_to_display):
            count_x = 0
            for x in range(mouse_square.x - int(squares_to_display/2), mouse_square.x - int(squares_to_display/2) + squares_to_display):
                
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
            self.hide_options()
            
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
            pen2 = QPen(Qt.black,1, Qt.SolidLine)
            
            
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
            
            
            
            
            
            
            
            
            
            self.mouse.move(self.maze.width*length - 0.5*length,self.maze.height*length) #guide mouse to the exit
            
            
            
            
            
            
            square = maze.get_mouse_square()
            x = square.x
            y = square.y
            count = 0
            painter.setPen(pen2)
            for p in path:
                if count == 0:
                    pen2.setBrush(Qt.red) #mark the first step with red
                    painter.setPen(pen2)
                else:
                    pen2.setBrush(Qt.blue)
                    painter.setPen(pen2)
                (x2,y2) = maze.get_direction[p]
                x += x2
                y += y2
                count +=1
                
                
                painter.drawEllipse(length*x + length/4,length*y + length/4,length/2,length/2)
            
                
      
                            
                        
        
    
       
            
                
                
                
                
                
                
                
                