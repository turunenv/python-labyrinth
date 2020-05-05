
from maze import Maze
import sys
from PyQt5.QtWidgets import QApplication
from corrupted_maze_file_error import CorruptedMazeFileError

from gui import GUI







def main():
    
    print("*** Welcome to the Labyrinth! ***\n")
    chosen = False
    while not chosen:
        try:
            choice = int(input("To load an existing game, enter 1\nTo start a new game, enter 2:\n"))
            if choice == 1 or choice == 2:
                chosen = True
        except ValueError:
            print("\nEnter '1' or '2' to start the game.\n")
    
    if choice == 1:
        filename = input("Enter filename:\n")
        loaded = False
        while not loaded:
            try:
                maze = Maze.load_from_file(filename)
                loaded = True
            except CorruptedMazeFileError:
                
                filename = input("Enter filename:\n")
                
    
    elif choice == 2:    
        player = input("Type in your username:\n")
        if len(player) >0:
            mouse_symbol = player[0] #Mouse symbol will be username's first symbol -> switched to uppercase if possible
            
            mouse_symbol = mouse_symbol.upper()
        else:
            mouse_symbol = 'M' #if user didn't enter anything, default symbol will be 'M'
        
        play = False
        while not play:
            try:
                width = int(input("Choose Labyrinth width:\n"))
                height = int(input("Choose Labyrinth height:\n"))
                if width > 0 and height > 0:
                    play = True
                else:
                    print("\nEnter positive numbers larger than 0!\n")
            except ValueError:
                print("\nEnter positive numbers larger than 0!\n")
        maze = Maze(width,height,mouse_symbol)
        maze.carve_maze()
        maze.set_mouse()
        print(maze)
        
    #figure out proportions for the maze based on size 
    bigger = max(maze.width,maze.height)
    if bigger <= 20:
        square_size = 50
    elif bigger < 30:
           
        square_size = 40
    else:
        square_size = 30
    
   
        
    

    
    
    
    '''
    
    maze = Maze(15,15,'A')
    maze.carve_maze()
    maze.set_mouse()
    square_size = 50
    print(maze)
    '''
    
    
    global app
    app = QApplication(sys.argv)
    gui = GUI(maze,square_size)

    
    
    sys.exit(app.exec_())
    
    
    
if __name__ == '__main__':
    main()