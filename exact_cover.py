import unittest
import numpy as np
from lattice import Lattice

def choose_col(lattice):
    s = float('inf')
    c = None
    j = lattice.head.east
    while j is not lattice.head:
        if j.size < s:
            c = j
            s = j.size
        j = j.east
    return c

def cover_col(lattice, c):
    c = c.col_head
    c.east.west = c.west
    c.west.east = c.east

    i = c.south
    while i is not c:
        j = i.east
        while j is not i:
            j.south.north = j.north
            j.north.south = j.south
            j = j.east
        i = i.south
    return lattice

def uncover_col(lattice, c):
    c = c.col_head
    i = c.north
    while i is not c:
        j = i.west
        while j is not i:
            j.col_head.size += 1
            j.south.north = j
            j.north.south = j
            j = j.west
        i = i.north
    c.east.west = c
    c.west.east = c
    return lattice

def generate_exact_cover_solutions(lattice):
    """
	An implenetation of the dancing links solution to the exact cover problem.
  	:ivar lattice: The lattice for the algorithm to run on
    """
    solutions = []
    O = []

    def exact_cover_search(k):
        #If R[h] = h, print the current solution and return
        if lattice.head.east is lattice.head:
            print("Solution found!")
            solutions.append(O.copy())
            return lattice
        #Otherwise choose a column object c
        c = choose_col(lattice)
        #Cover column c
        cover_col(lattice, c)
        #for each r <- D[c], D[D[c]], ... , while r is not c,
        r = c.south
        while r is not c:
            #set O_k <- r
            O.insert(k, r)
            #for each j <- R[r], R[R[r]], ... , while j is not r,
            j = r.east
            while j is not r:
                # cover column C[j]
                cover_col(lattice, j)
                j = j.east
            #search(k + 1)
            exact_cover_search(k + 1)
            #set r <- O_k and c <- C[r]
            r = O[k]
            c = r.col_head
            #for each j <- L[r], L[L[r]], ... , while j is not r,
            j = r.west
            while j is not r:
                #uncover column C[j]
                uncover_col(lattice, j)
                j = j.west
            O.pop()
            r = r.south
        #uncover column c and return
        uncover_col(lattice, c)
    exact_cover_search(0)
    return solutions

class ExactCover_UnitTest(unittest.TestCase):

    def test_cover_col(self):
        col_names = ['a', 'b', 'c']
        matrix = [['1', '1', '1'],
                  ['0', '0', '1'],
                  ['0', '1', '1']]
        lattice = Lattice(matrix, col_names)
        c = lattice.head.east
        while c is not lattice.head:
            r = c.south
            while r is not c:
                if r.key is not None and r.key is '0':
                    lattice.delete(r)
                    print("Deleting lattice node")
                r = r.south
            c = c.east
        print(lattice.__str__())
        c = lattice.head.east
        new_lattice = cover_col(lattice, c)
        print(new_lattice.__str__())
        col_b_head = new_lattice.head.east
        self.assertEqual(col_b_head.col_name, 'b')
        cover_col(lattice, c.east)
        print(lattice)
        cover_col(lattice, c.east.east)
        print(lattice)

    def test_cover_col2(self):
        col_names = ['a', 'b', 'c']
        matrix = [['0', '1', '1'],
                  ['1', '0', '0'],
                  ['1', '1', '1']]
        lattice = Lattice(matrix, col_names)
        c = lattice.head.east
        while c is not lattice.head:
            r = c.south
            while r is not c:
                if r.key is not None and r.key is '0':
                    lattice.delete(r)
                    print("Deleting lattice node")
                r = r.south
            c = c.east
        a = lattice.head.east
        lattice = cover_col(lattice, a)
        b = a.east
        lattice = cover_col(lattice, b)
        c = b.east
        lattice = cover_col(lattice, c)
        print(lattice)

    def test_generate_simple_exact_cover_solution(self):
        col_names = ['a', 'b', 'c']
        matrix = [['0', '1', '1'],
                  ['1', '0', '0'],
                  ['1', '0', '1'],
                  ['0', '1', '0']]
        lattice = Lattice(matrix, col_names, delete_zeros=True)
        solutions = generate_exact_cover_solutions(lattice)
        solution_rows = []
        for s in range(len(solutions)):
            solution_rows.append([])
            for c in solutions[s]:
                solution_rows[s].append(c.row_num)
        # Sort the solutions so they appear in an order that is easy to test.
        for r in solution_rows:
            r = r.sort()
        self.assertEqual(2, len(solutions))
        self.assertEqual([[1, 2], [3, 4]], solution_rows)

    def test_generate_simple_exact_cover_solution2(self):
        col_names = ['a', 'b', 'c', 'd']
        matrix = [['0', '1', '1', '0'],
                  ['1', '0', '0', '0'],
                  ['1', '0', '1', '0'],
                  ['0', '1', '0', '0']]
        lattice = Lattice(matrix, col_names, delete_zeros=True)
        solutions = generate_exact_cover_solutions(lattice)
        self.assertEqual(0, len(solutions))


def main():
    unittest.main()

if __name__ == '__main__':
        main()