from square import Square
from maze import Maze





def main():
   
        
    test_maze = Maze(10,10)
    print(test_maze)
    test_maze.carve_maze()
    print(test_maze)
    
main()