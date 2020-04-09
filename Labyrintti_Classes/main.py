from square import Square
from maze import Maze
import sys
import PyQt5

from gui import GUI
from scipy.weave.examples.wx_example import app





def main():
   
        
    test_maze = Maze(10,10)
    print(test_maze)
    test_maze.carve_maze()
    print(test_maze)
    
    global app
    app = QApplication(sys.argv)
    gui = GUI(test_maze,50)
    
    sys.exit(app.exec_())
    
    
    
if __name__ == '__main__':
    main()