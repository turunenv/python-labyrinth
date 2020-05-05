import unittest
from io import StringIO
from maze import Maze
from square import Square
from gui import GUI
from corrupted_maze_file_error import CorruptedMazeFileError





class Test(unittest.TestCase):
    
    #test functions with working 10x10 maze
    


    def test_maze_features(self):

            
            try:
                self.maze1 = Maze.load_from_file("maze.txt")
            except CorruptedMazeFileError:
                self.fail("Loading correctly structured file caused an exception.")
                
            self.assertEqual(self.maze1.find_shortest_path(),"SSWSSSWWNENEEESWSESSSS")
            self.assertEqual(self.maze1.ask_for_tip(),"SSWS")
            self.assertEqual(self.maze1.get_mouse_symbol(),"V")
            self.assertEqual(self.maze1.get_mouse_square(),self.maze1.get_square(8,0))
            
            #test that there is only one mouse
            count = 0
            for y in range (self.maze1.height):
                for x in range (self.maze1.width):
                    if self.maze1.get_square(x,y).mouse:
                        count +=1
            self.assertEqual(1,count)
            
    def test_squares(self):
            try:
                self.maze1 = Maze.load_from_file("maze.txt")
            except CorruptedMazeFileError:
                self.fail("Loading correctly structured file caused an exception.")
            
            self.maze1.get_square(0,0).remove_wall()
            self.assertEqual()
                
                
    
    
    

        
        

if __name__ == '__main__':
    unittest.main()
        

