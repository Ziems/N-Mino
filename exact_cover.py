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
    print("Covering col: ", c.col_head.col_name)
    c.east.west = c.west
    c.west.east = c.east
    i = c.south
    while i is not c:
        #print('0')
        j = i.east
        assert i.west.east.east is j
        while j is not i:
            #print('1')
            if j is not lattice.head:
                #print('2')
                j.south.north = j.north
                j.north.south = j.south
                j.col_head.size -= 1
            # if j.east is None:
            #     print("J.east is none!")
            #     print("J.key", j.key)
            #     print("J.head_name", j.col_name)
            # else:
            #     print("j.east is not none!")
            #     print("j.east.east.key", j.east.east.key)
            #     print("J.east.col_name", j.east.east.col_name)
            j = j.east
        i = i.south
    return lattice

def uncover_col(lattice, c):
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

    O = []

    def exact_cover_search(k):
        #If R[h] = h, print the current solution and return
        if lattice.head.east is lattice.head:
            return lattice
        #Otherwise choose a column object c
        c = choose_col(lattice)
        #Cover column c
        if c.col_head.col_name is 'b':
            print("LATTICE1: ", lattice)
        cover_col(lattice, c)
        #for each r <- D[c], D[D[c]], ... , while r is not c,
        r = c.south
        while r is not c:
            #set O_k <- r
            O.append(r) 
            #for each j <- R[r], R[R[r]], ... , while j is not r,
            j = r.east
            while j is not r:
                # cover column C[j]
                if j.col_head.col_name is 'b':
                    print("LATTICE2: ", lattice)
                cover_col(lattice, j)
                j = j.east
            #search(k + 1)
            exact_cover_search(k)
            #set r <- O_k and c <- C[r]
            r = O[k]
            c = r.col_head
            #for each j <- L[r], L[L[r]], ... , while j is not r,
            j = r.west
            while j is not r:
                #uncover column C[j]
                uncover_col(lattice, j)
                j = j.west
            r = r.south
        #uncover column c and return
        uncover_col(lattice, c)
    exact_cover_search(0)
    return O

class ExactCover_UnitTest(unittest.TestCase):

    def test_cover_col(self):
        col_names = ['a', 'b', 'c']
        matrix = [['0', '1', '1'],
                  ['1', '0', '0'],
                  ['1', '1', '1']]
        lattice = Lattice(matrix, col_names)
        print(lattice.__str__())
        c = lattice.head.east.east
        new_lattice = cover_col(lattice, c)
        print(new_lattice.__str__())
        col_a_head = new_lattice.head.east
        self.assertEqual(col_a_head.east.col_name, 'c') 

    # def test_generate_simple_exact_cover_solution(self):
    #     col_names = ['a', 'b', 'c']
    #     matrix = [['0', '1', '1'],
    #               ['1', '0', '0'],
    #               ['1', '1', '1']]
    #     lattice = Lattice(matrix, col_names)
    #     generate_exact_cover_solutions(lattice)

def main():
    unittest.main()

if __name__ == '__main__':
        main()