import unittest
import numpy as np
from lattice import *

class PentomintoShape():
    def __init__(self, shape, index=0, num_orientations=0, name=''):
        self.shape = shape
        self.index = index
        self.num_orientations = num_orientations
        self.name = name
    
    def generate_orientations(self):
        orientations = []
        for i in range(0, 4):
            rotated_shape = np.rot90(self.shape, k=i)
            orientations.append(rotated_shape.tolist())
            orientations.append(np.flip(rotated_shape, axis=0).tolist())
            orientations.append(np.flip(rotated_shape, axis=1).tolist())
        
        unique_orientations = []
        for o in orientations:
            if o not in unique_orientations:
                unique_orientations.append(o)
        if len(unique_orientations) is not self.num_orientations and self.num_orientations is not 0:
            print(self.name + ": ERROR ERROR READ ALL ABOUT IT")
        return unique_orientations

def encode_board(board, shape_index, num_shapes=12):
    enc = []
    for i in range(num_shapes):
        enc.append(0)
    enc[shape_index] = 1
    for r in board:
        for c in r:
            enc.append(c)
    return enc

def generate_board(shape, board_shape=(6,10), shape_offset=(0,0)):
    board = []
    rows, cols = board_shape
    for i in range(rows):
        board.append([])
        for j in range(cols):
            board[i].append(0)
    r_offset, c_offset = shape_offset
    for r in range(0, len(shape)):
        for c in range(0, len(shape[0])):
            board[r + r_offset][c + c_offset] = shape[r][c]
    return board

def generate_positions(shape, shape_index, num_shapes=12, board_shape=(6,10)):
    board_rows, board_cols = board_shape
    shape_rows = len(shape)
    shape_cols = len(shape[0])
    encoded_positions = []
    for r in range(0, board_rows - shape_rows + 1):
        for c in range(0, board_cols - shape_cols + 1):
            generated_board = generate_board(shape, shape_offset=(r, c))
            encoded_board = encode_board(generated_board, shape_index)
            encoded_positions.append(encoded_board)
    return encoded_positions

def get_base_shapes():
    base_shapes = []

    #F
    shape = [[0, 1, 1],
             [1, 1, 0],
             [0, 1, 0]]
    base_shapes.append(PentomintoShape(shape, 7, 8, 'F'))

    # I
    shape = [[1],
             [1],
             [1],
             [1],
             [1]]
    base_shapes.append(PentomintoShape(shape, 0, 2, 'I'))

    #L
    shape = [[1, 0],
             [1, 0],
             [1, 0],
             [1, 1]]
    base_shapes.append(PentomintoShape(shape, 2, 8, 'L'))

    #P
    shape = [[1, 1],
             [1, 1],
             [1, 0]]
    base_shapes.append(PentomintoShape(shape, 6, 8, 'P'))

    #N
    shape = [[0, 1],
             [0, 1],
             [1, 1],
             [1, 0]]
    base_shapes.append(PentomintoShape(shape, 1, 8, 'N'))

    #T
    shape = [[1, 1, 1],
             [0, 1, 0],
             [0, 1, 0]]
    base_shapes.append(PentomintoShape(shape, 9, 4, 'T'))

    #U
    shape = [[1, 0, 1],
             [1, 1, 1]]
    base_shapes.append(PentomintoShape(shape, 3, 4, 'U'))

    #V
    shape = [[0, 0, 1],
             [0, 0, 1],
             [1, 1, 1]]
    base_shapes.append(PentomintoShape(shape, 10, 4, 'V'))

    #W
    shape = [[0, 0, 1],
             [0, 1, 1],
             [1, 1, 0]]
    base_shapes.append(PentomintoShape(shape, 5, 4, 'W'))


    #X
    shape = [[0, 1, 0],
             [1, 1, 1],
             [0, 1, 0]]
    base_shapes.append(PentomintoShape(shape, 4, 1, 'X'))

    #Y
    shape = [[0, 1],
             [1, 1],
             [0, 1],
             [0, 1]]
    base_shapes.append(PentomintoShape(shape, 11, 8, 'Y'))
    
    #Z
    shape = [[1, 1, 0],
             [0, 1, 0],
             [0, 1, 1]]
    base_shapes.append(PentomintoShape(shape, 8, 4, 'Z'))

    return base_shapes

def generate_all_orientations_with_encodings(shapes):
    encodings = []
    for s in shapes:
        for o in s.generate_orientations():
            for p in generate_positions(o, s.index):
                encodings.append(p)
    return encodings

def generate_exact_cover_solutions(lattice):
    pass

class Pentominto_UnitTest(unittest.TestCase):
    def test_generate_positions(self):
        shape = [[0, 1, 1],
                 [1, 1, 0],
                 [0, 1, 0]]
        shape_index = 1
        positions = generate_positions(shape, shape_index, board_shape=(6, 10))
        self.assertEqual(192, len(positions))

    def test_encode_board(self):
        board = [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                ]
        shape_index = 0
        num_shapes = 12
        encoded_board = encode_board(board, shape_index, num_shapes)
        expected = [ #1d array
            1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        self.assertEqual(expected, encoded_board)

    def test_generate_board1(self):
        # Test with no offset
        shape = [[1, 1, 1],
                [0, 1, 0],
                [0, 1, 0]]
        generated_board = generate_board(shape)
        expected_board = [
                 [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                ]
        self.assertEqual(expected_board, generated_board)
    
    def test_generate_board2(self):
        # Test with column offset
        shape = [[1, 1, 1],
                [0, 1, 0],
                [0, 1, 0]]
        generated_board = generate_board(shape, shape_offset=(0, 1))
        expected_board = [
                 [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                ]
        self.assertEqual(expected_board, generated_board)

    def test_generate_board3(self):
        # Test with row offset
        shape = [[1, 1, 1],
                [0, 1, 0],
                [0, 1, 0]]
        generated_board = generate_board(shape, shape_offset=(1, 0))
        expected_board = [
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                ]
        self.assertEqual(expected_board, generated_board)

    def test_generate_orientations1(self):
        # This is I
        base_shape = [[1],
                 [1],
                 [1],
                 [1],
                 [1]]
        shape = PentomintoShape(base_shape)
        orientations = shape.generate_orientations()
        self.assertEqual(2, len(orientations))

    def test_generate_orientations2(self):
        # This is Y
        base_shape = [[0, 1],
             [1, 1],
             [0, 1],
             [0, 1]]
        shape = PentomintoShape(base_shape)
        orientations = shape.generate_orientations()
        self.assertEqual(8, len(orientations))

    def test_generate_all_orientations_with_encodings(self):
        base_shapes = get_base_shapes()
        binary_matrix = generate_all_orientations_with_encodings(base_shapes)
        # Knuth says this should be 1568 in length but its about 25% more than that. Hmmm.
        print(len(binary_matrix))

    def test_exact_cover():
        base_shapes = get_base_shapes()
        binary_matrix = generate_all_orientations_with_encodings(base_shapes)
        lattice = Lattice(binary_matrix)
        solutions = generate_exact_cover_solutions(lattice)
        pass