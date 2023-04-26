class Square:
    # The Class Square represents a single square in the labyrinth.
    # A Square may be surrounded by walls from north, south, east and west.
    # At initialization, squares are surrounded by all four walls.

    # walls separate two squares in north-south and west-east directions
    walls_between_squares = {"N": "S", "S": "N", "W": "E", "E": "W"}

    # initialize square at position x,y with all walls.
    # initially, none of the squares have the mouse in it.
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"N": True, "S": True, "W": True, "E": True}
        self.mouse = False
        # tells us weather the square has another square under itself
        self.has_under = False
        self.under_square = None

    # remove wall between square and neighbour
    def remove_wall(self, neighbour, wall):
        self.walls[wall] = False
        neighbour.walls[Square.walls_between_squares[wall]] = False

    # knock down one wall: used in carving under squares
    def knock_down_single_wall(self, direction):
        self.walls[direction] = False

    # square has not been visited, if it still has all four walls
    def has_not_been_visited(self):
        return all(self.walls.values())

    def has_this_wall(self, direction):
        return self.walls[direction]

    # check for vertical straight carved passages for weave-carving
    def vertical_passage(self):
        if self.walls["N"] or self.walls["S"]:
            return False
        return True

    def horizontal_passage(self):
        if self.walls["W"] or self.walls["E"]:
            return False
        return True

    def add_under_square(self):
        self.has_under = True

        under_square = Square(self.x, self.y)

        if self.horizontal_passage():
            under_square.walls["N"] = False
            under_square.walls["S"] = False
        else:
            under_square.walls["W"] = False
            under_square.walls["E"] = False
        self.under_square = under_square

        return under_square

    def get_under_square(self):
        return self.under_square

    # check if a square has a square under itself
    def has_square_under(self):
        if self.has_under:
            return True

    def add_mouse(self):
        self.mouse = True

    def remove_mouse(self):
        self.mouse = False
