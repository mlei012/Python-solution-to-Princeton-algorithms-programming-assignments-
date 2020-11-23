class Quick_UnionFind:
    def __init__(self, n):
        self._id = list(range(n))
        self._sz = [1] * n
        self.cc = n  # connected components

    def _root(self, i):
        while (i != self._id[i]):
            self._id[i] = self._id[self._id[i]]
            i = self._id[i]
        return i

    def find(self, p, q):
        return self._root(p) == self._root(q)

    def union(self, p, q):
        i = self._root(p)
        j = self._root(q)
        if i == j:
            return
        if (self._sz[i] < self._sz[j]):
            self._id[i] = j
            self._sz[j] += self._sz[i]
        else:
            self._id[j] = i
            self._sz[i] += self._sz[j]
        self.cc -= 1
        
import numpy as np
import random

class Percolation:
    def __init__(self, n):
        self.n = n
        self._grid = np.zeros((n, n)).astype(int)
        self.elements = Quick_UnionFind(n**2+2)
        
    def open_site(self,row,column):
        self._grid[row][column] = 1
        return self.elements._id[row*self.n+column]
            
    def is_open(self, row, column):
        return self._grid[row][column] == 1
            
    def num_of_opensite(self):
        m = 0
        for i in range(self.n):
            for j in range(self.n):
                if self.is_open(i, j):
                    m += 1
        return m/self.n**2
    
    def percolates(self,n):
        self.top = -1
        self.bottom = n**2
        #uf = Quick_UnionFind(n**2-1)
        last_row = n * (n-1)
        for k in range(0, n):
            self.elements.union(last_row + k, self.bottom)
            self.elements.union(k, self.top)
            
        if self.elements.find(self.top, self.bottom):
            return True
            
class PercolationStats:
    def __init__(self, n, num_trails):
        self.n = n
        self.num_trails = num_trails
     
    def open_num(self, n):
        
        test = Percolation(self.n)
        while not test.percolates(n):
            site = random.randint(0, self.n**2-1)
            row = int(site//n)
            column = int(site%n)
                
            open_one = test.open_site(row, column)
    
            for row_next, column_next in [(int(row+1), int(column)), (int(row-1), int(column)), (int(row), int(column+1)), (int(row), int(column-1))]:
                if 0 <= row_next < n and 0 <= column_next < n and test.is_open(row_next, column_next):
                    test.elements.union(open_one, test.open_site(row_next, column_next))
                        
            
        return test.num_of_opensite()
    
    def trails(self, n, num_trails):
        i = 1
        trails = []
        
        while i <= num_trails:
            trails.append(self.open_num(n))
            i += 1
            
        return trails
    
    def trails_mean(self, n, num_trails):
        return np.mean(self.trails(n, num_trails))
    
    def trails_std(self, n, num_trails):
        return np.std(self.trails(n, num_trails))
    
    def trails_confidenceLo(self, n, num_trails):
        return self.trails_mean(n, num_trails) - ((1.96 * self.trails_std(n, num_trails)) / np.sqrt(num_trails))
    
    def trails_confidenceHi(self, n, num_trails):
        return self.trails_mean(n, num_trails) + ((1.96 * self.trails_std(n, num_trails)) / np.sqrt(num_trails))
        
        
res = PercolationStats(50, 50)
res.trails(50, 50)
res.trails_mean(50, 50)