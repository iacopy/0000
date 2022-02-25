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

        self.functions = {
            'N': (self.move, {'y': -1}),
            'S': (self.move, {'y': 1}),
            'E': (self.move, {'x': 1}),
            'W': (self.move, {'x': -1}),
            '1': (self.move, {'x': 1, 'y': -1}),
            '2': (self.move, {'x': -1, 'y': -1}),
            '3': (self.move, {'x': -1, 'y': 1}),
            '4': (self.move, {'x': 1, 'y': 1}),
            'R': (self.reproduce, {}),
        }

    def step(self):
        """
        Perform a single step of the cell.
        """
        if self.dna_position >= len(self.genome):
            self.dna_position = 0
        action = self.genome[self.dna_position]
        if self.recorder is not None:
            self.recorder.append(action)

        if action in self.functions:
            self.dna_position += 1
            func, kwargs = self.functions[action]
            return func(**kwargs)
        raise ValueError(f'Unknown gene: {action}')

    def move(self, x=0, y=0):
        """
        Move the cell in the given direction.
        """
        self.x += x
        self.y += y

    def reproduce(self):
        """
        Reproduce the cell.
        """
        return Cell(self.genome, (self.x, self.y))
