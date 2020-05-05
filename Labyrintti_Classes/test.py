import unittest

from maze import Maze


from corrupted_maze_file_error import CorruptedMazeFileError





class Test(unittest.TestCase):
    
    #test functions with working 10x10 maze
    


    def test_maze_features(self):

            
            try:
                self.maze1 = Maze.load_from_file("maze.txt")
            except CorruptedMazeFileError:
                self.fail("Loading correctly structured file caused an exception.")
                
            self.assertEqual(self.maze1.find_shortest_path(),"WSWWNESSEESSSWWSEE")
            self.assertEqual(self.maze1.ask_for_tip(),"WSW")
            self.assertEqual(self.maze1.get_mouse_symbol(),"V")
            self.assertEqual(self.maze1.get_mouse_square(),self.maze1.get_square(9,3))
            
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
            
            self.maze1.get_square(0,0).remove_wall(self.maze1.get_square(0,1),'S')
            self.assertFalse(self.maze1.get_square(0,0).walls['S'])
            self.assertFalse(self.maze1.get_square(0,1).walls['N'])
            
            
            
            self.assertTrue(self.maze1.get_square(0,0).has_this_wall('W'))
            
            
            self.assertTrue(self.maze1.get_square(5,1).vertical_passage())
            
            self.assertFalse(self.maze1.get_square(4,3).vertical_passage())
            self.assertFalse(self.maze1.get_square(4,3).horizontal_passage())
            
            self.assertTrue(self.maze1.get_square(1,3).has_square_under())
            
                
                
    
    
    

        
        

if __name__ == '__main__':
    unittest.main()
        

