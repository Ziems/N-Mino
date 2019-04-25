#!/usr/bin/python3

import unittest
import numpy as np

class Node():
    """ A lattice element.

	:ivar key: the key value
	:ivar north: reference to the node to the north
	:ivar south: reference to the node to the south 
	:ivar east: reference to the node to the east
	:ivar west: reference to the node to the west
    :ivar col_head: reference to the head node of the column
    :ivar col_name: the name of the column. Only not null if the node is a head

	"""
    def __init__(self, key=None, row_num = None, north = None, south = None, east = None, west = None, col_head = None, col_name=None):
        """ Initializes a new Lattice Node """
        self.key = key
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.col_head = col_head
        self.col_name = col_name
        self.row_num = row_num
        self.size = 0

    def init_size(self):
        count = 0
        ref = self.south
        while ref is not self:
            if ref.key is '1':
                count += 1
            ref = ref.south
        self.size = count
        return count

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
    :ivar col_names: the list of names where index i corresponds to column i
    """

    def __init__(self, matrix, col_names, delete_zeros=False):
        assert matrix is not None
        assert matrix[0] is not None
        assert matrix[0][0] is not None

        self.head = Node()

        lattice_node_matrix = [[]]

        # Insert the Column Headers
        for c in range(0, len(matrix[0])):
            new_head = Node(col_name=col_names[c])
            new_head.col_head = new_head
            lattice_node_matrix[0].append(new_head)

        # Initialize the LatticeNodes
        for r in range(0, len(matrix)):
            lattice_node_matrix.append([])
            for c in range(0, len(matrix[r])):
                lattice_node_matrix[r+1].append(Node(matrix[r][c], row_num= r + 1, col_head=lattice_node_matrix[0][c]))
        
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
        
        # Insert the head node(no north or south)
        self.head.set_east(lattice_node_matrix[0][0])
        self.head.set_west(lattice_node_matrix[0][-1])
        self.head.north = self.head
        self.head.south = self.head
        self.head.col_head = self.head
        self.head.col_name = 'head'

        c = self.head.east
        while c is not self.head:
            c.init_size()
            c = c.east

        if delete_zeros:
            c = self.head.east
            while c is not self.head:
                r = c.south
                while r is not c:
                    if r.key is not None and r.key is '0':
                        self.delete(r)
                    r = r.south
                c = c.east
        
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
        row_ref = self.head.east
        while row_ref.col_name == None or i == 0:
            res += "("
            col_ref = row_ref
            j = 0
            while (col_ref is not row_ref or j == 0) and col_ref is not self.head:
                if col_ref.key is not None:
                    res += col_ref.key + ", "
                elif col_ref.col_name is not None:
                    res += col_ref.col_name + ", "
                col_ref = col_ref.east
                j += 1
            res = res[:-2]
            i += 1
            row_ref = row_ref.south
            res += "), "
        res = res[:-2]
        return res
        # res = ""
        # c = self.head.east
        # cs = {}
        # res += "("
        # while c is not self.head:
        #     res += c.col_name + ", "
        #     cs[c.col_name] = []
        #     r = c.south
        #     while r is not c:
        #         cs[c.col_name].append(r.key)
        #         r = r.south
        #     c = c.east
        # res = res[:-2] + ")\n"
        # for i in cs.keys():
        #     res += "[" + i + "]: "
        #     for j in cs[i]:
        #         res += j + ", "
        #     res = res[:-2] + "\n"
        # return res

class LatticeNode_UnitTest(unittest.TestCase):
    def test_trivial_north(self):
        ancor_node = Node(True)
        north_node = Node(False)
        ancor_node.set_north(north_node)
        self.assertEqual(ancor_node.north, north_node)
        self.assertEqual(north_node.south, ancor_node)

    def test_trivial_south(self):
        ancor_node = Node(True)
        south_node = Node(False)
        ancor_node.set_south(south_node)
        self.assertEqual(ancor_node.south, south_node)
        self.assertEqual(south_node.north, ancor_node)

    def test_trivial_east(self):
        ancor_node = Node(True)
        east_node = Node(False)
        ancor_node.set_east(east_node)
        self.assertEqual(ancor_node.east, east_node)
        self.assertEqual(east_node.west, ancor_node)

    def test_trivial_west(self):
        ancor_node = Node(True)
        west_node = Node(False)
        ancor_node.set_west(west_node)
        self.assertEqual(ancor_node.west, west_node)
        self.assertEqual(west_node.east, ancor_node)

class Lattice_UnitTest(unittest.TestCase):
    def test_constructor(self):
        """Tests on a simple 3x3 lattice where each key is a character unique to the lattice""" 
        expected =  "(1, 2, 3), (a, b, c), (d, e, f), (g, h, i)"
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, ['1', '2', '3'])
        self.assertEqual(expected, lattice.__str__())

    def test_row_wrap(self):
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        west_edge = lattice.head.east.south
        east_edge = lattice.head.east.east.east.south # The lattice node with the key of c
        for i in range(3):
            self.assertEqual(west_edge.west, east_edge)
            self.assertEqual(east_edge.east, west_edge)
            west_edge = west_edge.south
            east_edge = east_edge.south
    
    def test_head_wrap(self):
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        west_edge = lattice.head
        east_edge = lattice.head.east.east.east# The column head lattice node with the name of 3
        self.assertEqual(west_edge.west, east_edge)
        self.assertEqual(east_edge.east, west_edge)
        
    def test_col_wrap(self):
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        north_edge = lattice.head.east
        south_edge = lattice.head.east.south.south.south # The lattice node with the key of c
        for i in range(3):
            self.assertEqual(north_edge.north, south_edge)
            self.assertEqual(south_edge.south, north_edge)
            north_edge = north_edge.east
            south_edge = south_edge.east

    def test_delete1(self):
        # Deleting 'e'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        lattice.delete(lattice.head.east.east.south.south)
        exptected = "(1, 2, 3), (a, b, c), (d, f), (g, h, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore1(self):
        # Deleting then restoring 'e'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.head.east.east.south)
        # lattice is now (1, 2, 3), (a, b, c), (d, f), (g, h, i)
        lattice.restore(deleted_node)
        # lattice should now be (1, 2, 3), (a, b, c), (d, e, f), (g, h, i)
        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_delete2(self):
        # Deleting 'b;
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        lattice.delete(lattice.head.east.south.east)
        exptected = "(1, 2, 3), (a, c), (d, e, f), (g, h, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore2(self):
        # Deleting then restoring 'b'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.head.east.south.east)

        lattice.restore(deleted_node)

        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_delete3(self):
        # Deleting 'c'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        lattice.delete(lattice.head.east.east.east.south)
        exptected = "(1, 2, 3), (a, b), (d, e, f), (g, h, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore3(self):
        # Deleting then restoring 'c'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.head.east.east.east.south)

        lattice.restore(deleted_node)

        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_delete4(self):
        # Deleting 'h'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        lattice.delete(lattice.head.east.east.south.south.south)
        exptected = "(1, 2, 3), (a, b, c), (d, e, f), (g, i)"
        actual = lattice.__str__()
        self.assertEqual(exptected, actual)

    def test_restore4(self):
        # Deleting then restoring 'h'
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        pre_delete = lattice.__str__()
        deleted_node = lattice.delete(lattice.head.east.east.south.south.south)

        lattice.restore(deleted_node)

        post_restore = lattice.__str__()
        self.assertEqual(pre_delete, post_restore)

    def test_col_head(self):
        col_names = ['1', '2', '3']
        matrix = [['a', 'b', 'c'],
                  ['d', 'e', 'f'],
                  ['g', 'h', 'i']]
        lattice = Lattice(matrix, col_names)
        a = lattice.head.east.south
        self.assertEqual(lattice.head.east, a.col_head)
        b = a.east
        self.assertEqual(lattice.head.east.east, b.col_head)
        e = b.south
        self.assertEqual(lattice.head.east.east, e.col_head)
        i = b.south.east
        self.assertEqual(lattice.head.east.east.east, i.col_head)
    
    def test_col_size(self):
        col_names = ['1', '2', '3']
        matrix = [['0', '1', '0'],
                  ['0', '1', '0'],
                  ['0', '0', '0']]
        lattice = Lattice(matrix, col_names)
        second_col = lattice.head.east.east
        self.assertEqual(2, second_col.size)

    def test_south_north(self):
        col_names = ['a', 'b', 'c']
        matrix = [['0', '1', '1'],
                  ['1', '0', '0'],
                  ['1', '1', '1']]
        lattice = Lattice(matrix, col_names)
        b1 = lattice.head.east.east.south
        self.assertEqual(b1, b1.south.north)

def main():
    unittest.main()

if __name__ == '__main__':
        main()