
class CorruptedMazeFileError(Exception):

    def __init__(self, message):
        self.message = message
        print("Error found in file: {}\n".format(self.message))
        
    
        
        
