"""
A cell can move and reproduce within the 2D grid world,
based on the steps encoded in the cell DNA (genome).

The 2D grid is a matrix representing an image which is
painted during the cell movement.

The DNA is a list of characters that define the behaviour of the cell:

N = forward
S = backward
E = right
W = left
1 = north-east
2 = north-west
3 = south-west
4 = south-east
R = reproduce

The total behaviour, and final image, is determined by the single starting DNA.
"""


class Apocalypse(Exception):
    """
    Exception raised when the last cell dies.
    """


class World:
    """
    A 2D grid world.

    The world is a matrix of cells, where each cell is represented by a 2D list.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        self.image = [[0 for _ in range(width)] for _ in range(height)]

    def add_cell(self, cell, position):
        """
        Add a cell to the world.
        """
        cell.x = position[0]
        cell.y = position[1]
        self.cells.append(cell)

    def update_image(self):
        """
        Update the current image of the world.
        """
        for cell in self.cells:
            self.image[cell.y][cell.x] = cell.color

    def step(self):
        """
        Perform a single step of the world.
        """
        if not self.cells:
            raise Apocalypse()

        new_cells = []
        i = 0
        while i < len(self.cells):
            cell = self.cells[i]
            new_cell = cell.step()
            if new_cell:
                new_cells.append(new_cell)
            # if a cell goes out of the world, it is removed
            if cell.x < 0 or cell.x >= self.width or cell.y < 0 or cell.y >= self.height:
                self.cells.pop(i)
            else:
                i += 1

        if new_cells:
            self.cells.extend(new_cells)
        self.update_image()

    def get_image(self):
        """
        Return the current image of the world.
        """
        return self.image
