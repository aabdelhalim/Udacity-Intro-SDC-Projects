import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1 and self.w==1:
            d= self
        else:
            d= self[0][0]*self[1][1]-self[0][1]*self[1][0]
        return d
    
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
        t=0
        for i in range(self.h):
            for j in range(self.w):
                if i==j:
                    t= t+self[i][j]
        return t
        
    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        
        #invert 1x1 matrix
        if self.h == 1 and self.w==1:
            self[0][0]= 1/self[0][0]
    
        #invert 2x2 matrix
        else:
            det= self.determinant()
            a = self[0][0]
            b = self[0][1]
            c = self[1][0]
            d = self[1][1]
        
            self[0][0] = d
            self[0][1] = -b
            self[1][0] = -c
            self[1][1] = a
            
            for i in range(self.h):
                for j in range(self.w):
                    self[i][j]= 1/det*self[i][j]
        return self

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """    
        trans = zeroes(self.w, self.h)
    
        for i in range(self.h):
            for j in range(self.w):
                trans.g[j][i] = self.g[i][j]
        return trans
    
    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same")
            
        add= zeroes(self.h, other.w)
        for i in range(add.h):
            for j in range(add.w):
                add[i][j] += self[i][j] + other[i][j]
        return add

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        neg= zeroes(self.h, self.w)
        
        for i in range(neg.h):
            for j in range(neg.w):
                neg[i][j] += self[i][j]*-1
        
        return neg

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        sub= zeroes(self.h, other.w)
        for i in range(sub.h):
            for j in range(sub.w):
                sub[i][j] = self[i][j] - other[i][j]
        return sub

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        
        mult = zeroes(self.h, other.w)
    
    
        for i in range(mult.h):
            for j in range(mult.w):
                mult[i][j] = sum(self[i][k]*other[k][j] for k in range(self.w))
    
   
        return mult

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
        
        rmul= self.g
        
        for i in range(self.h):
            for j in range(self.w):
                rmul[i][j]= self.g[i][j]*other
        return Matrix(rmul)