from square import Square
from maze import Maze
import sys
from PyQt5.QtWidgets import QApplication


from gui import GUI






def main():
    
    print("*** Welcome to the Labyrinth! ***\n")
    player = input("Type in your username: ")
    if len(player) >0:
        mouse_symbol = player[0] #Mouse symbol will be username's first symbol -> switched to uppercase if possible
        
        mouse_symbol = mouse_symbol.upper()
    else:
        mouse_symbol = 'M' #if user didn't enter anything, default symbol will be 'M'
    
    play = False
    while not play:
        try:
            width = int(input("Choose Labyrinth width: "))
            height = int(input("Choose Labyrinth height: "))
            if width > 0 and height > 0:
                play = True
            else:
                print("\nEnter positive numbers larger than 0!\n")
        except ValueError:
            print("\nEnter positive numbers larger than 0!\n")
    
     #figure out proportions for the maze based on size 
    bigger = max(width,height)
    if bigger <= 15:
        square_size = 50
    else:
       
        square_size = 30
    
   
        
    test_maze = Maze(width,height,mouse_symbol)
    print(test_maze)

    test_maze.carve_maze()
    test_maze.set_mouse()
    print(test_maze)
    
    global app
    app = QApplication(sys.argv)
    gui = GUI(test_maze,square_size)
    
    sys.exit(app.exec_())
    
    
    
if __name__ == '__main__':
    main()