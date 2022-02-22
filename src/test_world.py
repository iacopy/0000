"""
Test suite for the world.
"""
# 3rd party
import pytest

# My stuff
from world import Apocalypse
from world import Cell
from world import World


def test_unexpected_gene():
    """
    Test that the cell raises an exception when it encounters unexpected genes.
    """
    cell = Cell("X")
    with pytest.raises(ValueError):
        cell.step()


def test_all_genes():
    """
    Test a cell with all possible genes.
    """
    cell = Cell("NSWE1234", recorder=[])
    assert cell.x == 0
    assert cell.y == 0
    assert cell.dna_position == 0
    assert cell.recorder == []
    assert cell.genome == "NSWE1234"
    cell.step()
    assert cell.dna_position == 1
    assert cell.recorder == ["N"]
    assert (cell.x, cell.y) == (0, -1)
    cell.step()
    assert cell.dna_position == 2
    assert cell.recorder == ["N", "S"]
    assert (cell.x, cell.y) == (0, 0)
    cell.step()
    assert cell.dna_position == 3
    assert cell.recorder == ["N", "S", "W"]
    assert (cell.x, cell.y) == (-1, 0)
    cell.step()
    assert cell.dna_position == 4
    assert cell.recorder == ["N", "S", "W", "E"]
    assert (cell.x, cell.y) == (0, 0)
    cell.step()
    assert cell.dna_position == 5
    assert cell.recorder == ["N", "S", "W", "E", "1"]
    assert (cell.x, cell.y) == (1, -1)
    cell.step()
    assert cell.dna_position == 6
    assert cell.recorder == ["N", "S", "W", "E", "1", "2"]
    assert (cell.x, cell.y) == (0, -2)
    cell.step()
    assert cell.dna_position == 7
    assert cell.recorder == ["N", "S", "W", "E", "1", "2", "3"]
    assert (cell.x, cell.y) == (-1, -1)
    cell.step()
    assert cell.dna_position == 8
    assert cell.recorder == ["N", "S", "W", "E", "1", "2", "3", "4"]
    assert (cell.x, cell.y) == (0, 0)


def test_single_move():
    """
    Test the smallest genome with a single 'N' move, in a 3 x 3 world.

    At the beginning, the cell is placed in the center:

        [
            0, 0, 0,
            0, 1, 0,
            0, 0, 0,
        ]

    Based on its genome ('N') the cell should move to the north, and the resulting image should be:

        [
            0, 1, 0,
            0, 1, 0,
            0, 0, 0,
        ]
    """
    world = World(3, 3)
    cell = Cell("N")
    world.add_cell(cell, (1, 1))
    world.update_image()

    assert world.cells == [cell]
    assert world.get_image() == [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]

    assert cell.dna_position == 0
    world.step()
    assert cell.dna_position == 1

    assert world.get_image() == [
        [0, 1, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]


def test_nre():
    """
    0. The cell (cell_1) is placed in the center of the 5x5 world: pos=(2, 2).
    1. cell_1 moves to the north (N) --> pos=(2, 1)
    2. cell_1 reproduces -> cell_2 is placed in (2, 1)
    3. cell_1 moves (E) -> pos=(3, 1); cell_2 moves (N) -> pos=(2, 0)
    4. cell_2 moves (E) -> pos=(3, 0).
    """

    # 0. The cell (cell_1) is placed in the center of the 5x5 world: pos=(2, 2).
    world = World(5, 5)
    cell_1 = Cell("NRE")
    world.add_cell(cell_1, (2, 2))
    world.update_image()

    # 1. cell_1 moves to the north (N) --> pos=(2, 1)
    world.step()
    assert cell_1.x, cell_1.y == (2, 1)
    assert world.get_image() == [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    assert len(world.cells) == 1

    # 2. cell_1 reproduces -> cell_2 is placed in (2, 1)
    world.step()
    assert len(world.cells) == 2
    assert cell_1.x, cell_1.y == (2, 1)
    cell_2 = world.cells[1]
    assert cell_2.x, cell_2.y == (2, 1)

    # 3. cell_1 moves (E) -> pos=(3, 1); cell_2 moves (N) -> pos=(2, 0)
    world.step()
    assert cell_1.x, cell_1.y == (3, 1)
    assert cell_2.x, cell_2.y == (2, 0)
    assert world.get_image() == [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]


def test_dna_read_cycle():
    """
    Test that the cell reads the dna in a cycle.
    """
    # Create a 1x2 world and a cell with a DNA of 'SN'
    world = World(2, 1)
    cell = Cell("EW", recorder=[])
    world.add_cell(cell, (0, 0))
    world.update_image()
    assert world.get_image() == [
        [1, 0],
    ]
    world.step()
    assert cell.recorder == ["E"]
    assert world.get_image() == [
        [1, 1],
    ]
    world.step()
    assert cell.recorder == ["E", "W"]
    world.step()
    assert cell.recorder == ["E", "W", "E"]
    world.step()
    assert world.get_image() == [
        [1, 1],
    ]
    assert cell.recorder == ["E", "W", "E", "W"]


def test_death_by_world_limit():
    """
    Test the death of the cell by the world limit.
    """
    # Create a 2x2 world
    world = World(2, 2)
    # Create a cell in the bottom right corner
    cell = Cell("NWNW", recorder=[])
    world.add_cell(cell, (1, 1))
    world.update_image()

    # The cell should be alive
    assert world.cells == [cell]
    assert world.get_image() == [
        [0, 0],
        [0, 1],
    ]
    assert cell.recorder == []

    world.step()
    assert cell.recorder == ["N"]
    assert world.cells == [cell]
    assert world.get_image() == [
        [0, 1],
        [0, 1],
    ]

    world.step()
    # After 2 steps, the cell should be still alive
    assert cell.recorder == ["N", "W"]
    assert world.cells == [cell]
    assert world.get_image() == [
        [1, 1],
        [0, 1],
    ]

    world.step()
    # After 3 steps, the cell should be dead
    assert len(world.cells) == 0
    assert world.get_image() == [
        [1, 1],
        [0, 1],
    ]

    # The next world step should raise an exception
    with pytest.raises(Apocalypse):
        world.step()
