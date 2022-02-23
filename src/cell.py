"""
This module defines the Cell class.
"""


class Cell:
    """
    The cell is a container for the genome.
    """

    def __init__(self, genome, position=(0, 0), recorder=None):
        self.genome = genome
        self.x = position[0]
        self.y = position[1]
        self.color = 1
        self.dna_position = 0
        #: record actions of the cell if is not None
        self.recorder = recorder

    def step(self):
        """
        Perform a single step of the cell.
        """
        if self.dna_position >= len(self.genome):
            self.dna_position = 0
        action = self.genome[self.dna_position]
        ret = self.move(action)
        self.dna_position += 1
        if self.recorder is not None:
            self.recorder.append(action)
        return ret

    def move(self, direction):  # pylint: disable=too-many-return-statements
        """
        Move the cell in the given direction.
        """
        if direction == "N":
            self.y -= 1
            return None
        if direction == "S":
            self.y += 1
            return None
        if direction == "E":
            self.x += 1
            return None
        if direction == "W":
            self.x -= 1
            return None
        if direction == "1":
            self.x += 1
            self.y -= 1
            return None
        if direction == "2":
            self.x -= 1
            self.y -= 1
            return None
        if direction == "3":
            self.x -= 1
            self.y += 1
            return None
        if direction == "4":
            self.x += 1
            self.y += 1
            return None
        if direction == "R":
            return self.reproduce()

        raise ValueError(f'Unknown direction: {direction}')

    def reproduce(self):
        """
        Reproduce the cell.
        """
        return Cell(self.genome, (self.x, self.y))
