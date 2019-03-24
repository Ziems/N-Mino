#!/usr/bin/python3

import unittest
import numpy as np

class LatticeNode():
    """ A lattice element.

	:ivar key: the key value
	:ivar north: reference to the node to the north
	:ivar south: reference to the node to the south 
	:ivar east: reference to the node to the east
	:ivar west: reference to the node to the west

	"""
    def __init__(self, key, north = None, south = None, east = None, west = None, col_head = None):
        """ Initializes a new Lattice Node """
        self.key = key
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.col_head = col_head

    def set_north(self, new_north):
        """ Helper function: set the node to the north, and set that nodes south to this"""
        self.north = new_north
        new_north.south = self

    def set_south(self, new_south):
        """ Helper function: set the node to the south, and set that nodes north to this"""
        self.south = new_south
        new_south.north = self

    def set_east(self, new_east):
        """ Helper function: set the node to the east, and set that nodes west to this"""
        self.east = new_east
        new_east.west = self
        
    def set_west(self, new_west):
        """ Helper function: set the node to the west, and set that nodes east to this"""
        self.west = new_west
        new_west.east = self
    
    def __str__(self):
        return str(self.key)

class Lattice():
    """
	A lattice data structure implementation.
  	:ivar matrix: the 2-dimensional array to be created into a lattice. The array can be of ANY type. the contents of the array become the keys of the Lattice
    """

    def __init__(self, matrix):
        assert matrix is not None
        assert matrix[0] is not None
        assert matrix[0][0] is not None

        self.ancor = LatticeNode(matrix[0][0])

        lattice_node_matrix = []
        # Initialize the LatticeNodes
        for r in range(0, len(matrix)):
            lattice_node_matrix.append([])
            for c in range(0, len(matrix[r])):
                lattice_node_matrix[r].append(LatticeNode(matrix[r][c]))
        lattice_node_matrix[0][0] = self.ancor
        
        # TRIVIALLY Connect the lattice nodes horizontally
        for r in range(0, len(lattice_node_matrix)):
            for c in range(0, len(lattice_node_matrix[c]) - 1):
                lattice_node_matrix[r][c].set_east(lattice_node_matrix[r][c+1])

        # TRIVIALLY Connect the lattice nodes vertically
        for r in range(0, len(lattice_node_matrix) - 1):
            for c in range(0, len(lattice_node_matrix[c])):
                lattice_node_matrix[r][c].set_south(lattice_node_matrix[r+1][c])

        # Connect the nodes of the first row with the nodes of the last row
        for c in range(0, len(lattice_node_matrix[0])):
            lattice_node_matrix[0][c].set_north(lattice_node_matrix[len(lattice_node_matrix) - 1][c])

        # Connect the nodes of the first column with the nodes of the last column
        for r in range(0, len(lattice_node_matrix)):
            lattice_node_matrix[r][0].set_west(lattice_node_matrix[r][len(lattice_node_matrix[0])-1])
        
    def delete(self, lattice_node):
        # Here you just have to make 2 new connections that skip over lattice_node
        lattice_node.east.set_west(lattice_node.west)
        lattice_node.north.set_south(lattice_node.south)
        return lattice_node

    def restore(self, lattice_node):
        # Here you have to manually restore all 4 connections
        lattice_node.east.set_west(lattice_node)
        lattice_node.west.set_east(lattice_node)
        lattice_node.north.set_south(lattice_node)
        lattice_node.south.set_north(lattice_node)
        return lattice_node

    def __str__(self):
        # Printing solution that does not depend on rows or cols
        res = ""
        i = 0
        row_ref = self.ancor
        while row_ref is not self.ancor or i == 0:
            res += "("
            col_ref = row_ref
            j = 0
            while col_ref is not row_ref or j == 0:
                res += col_ref.key + ", "
                col_ref = col_ref.east
                j += 1
            res = res[:-2]
            i += 1
            row_ref = row_ref.south
            res += "), "
        res = res[:-2]
        return res

class LatticeNode_UnitTest(unittest.TestCase):
    def test_trivial_north(self):
        ancor_node = LatticeNode(True)
        north_node = LatticeNode(False)
        ancor_node.set_north(north_node)
        self.assertEqual(ancor_node.north, north_node)
        self.assertEqual(north_node.south, ancor_node)

    def test_trivial_south(self):
        ancor_node = LatticeNode(True)
        south_node = LatticeNode(False)
        ancor_node.set_south(south_node)
        self.assertEqual(ancor_node.south, south_node)
        self.assertEqual(south_node.north, ancor_node)

    def test_trivial_east(self):
        ancor_node = LatticeNode(True)
        east_node = LatticeNode(False)
        ancor_node.set_east(east_node)
        self.assertEqual(ancor_node.east, east_node)
        self.assertEqual(east_node.west, ancor_node)

    def test_trivial_west(self):
        ancor_node = LatticeNode(True)
        west_node = LatticeNode(False)
        ancor_node.set_west(west_node)
        self.assertEqual(ancor_node.west, west_node)
        self.assertEqual(west_node.east, ancor_node)

class Lattice_UnitTest(unittest.TestCase):
    def test_constructor(self):
        """Tests on a simple 3x3 lattice where each key is a character unique to the lattice""" 
        expected =  "(a, b, c), (d, e, f), (g, h, i)"
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        self.assertEqual(expected, lattice.__str__())
        self.assertEqual(lattice.ancor.key, 'a')

    def test_row_wrap(self):
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        west_edge = lattice.ancor
        east_edge = lattice.ancor.east.east # The lattice node with the key of c
        for i in range(3):
            self.assertEqual(west_edge.west, east_edge)
            self.assertEqual(east_edge.east, west_edge)
            west_edge = west_edge.south
            east_edge = east_edge.south
        # after 3 they should have wrapped col-wise back to the first col
        self.assertEqual(west_edge, lattice.ancor)
        self.assertEqual(east_edge, lattice.ancor.east.east)
        
    def test_col_wrap(self):
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        north_edge = lattice.ancor
        south_edge = lattice.ancor.south.south # The lattice node with the key of c
        for i in range(3):
            self.assertEqual(north_edge.north, south_edge)
            self.assertEqual(south_edge.south, north_edge)
            north_edge = north_edge.east
            south_edge = south_edge.east
        # after 3 they should have wrapped row-wise back to the first row
        self.assertEqual(north_edge, lattice.ancor)
        self.assertEqual(south_edge, lattice.ancor.south.south)

    def test_delete1(self):
        # Deleting 'e'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        lattice.delete(lattice.ancor.east.south)
        exptected = "(a, b, c), (d, f), (g, h, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore1(self):
        # Deleting then restoring 'e'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.ancor.east.south)
        # lattice is now (a, b, c), (d, f), (g, h, i)
        lattice.restore(deleted_node)
        # lattice should now be (a, b, c), (d, e, f), (g, h, i)
        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_delete2(self):
        # Deleting 'b;
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        lattice.delete(lattice.ancor.east)
        exptected = "(a, c), (d, e, f), (g, h, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore2(self):
        # Deleting then restoring 'b'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.ancor.east)

        lattice.restore(deleted_node)

        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_delete3(self):
        # Deleting 'c'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        lattice.delete(lattice.ancor.east.east)
        exptected = "(a, b), (d, e, f), (g, h, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore3(self):
        # Deleting then restoring 'c'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.ancor.east.east)

        lattice.restore(deleted_node)

        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_delete4(self):
        # Deleting 'h'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        lattice.delete(lattice.ancor.east.south.south)
        exptected = "(a, b, c), (d, e, f), (g, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore4(self):
        # Deleting then restoring 'h'
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.ancor.east.south.south)

        lattice.restore(deleted_node)

        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

def main():
    unittest.main()

if __name__ == '__main__':
        main()