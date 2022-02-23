"""
Unit tests for the Cell class.
"""
# 3rd party
import pytest

# My stuff
from cell import Cell


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
