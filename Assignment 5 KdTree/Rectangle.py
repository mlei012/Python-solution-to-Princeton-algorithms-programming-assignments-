import Point
from math import sqrt
import matplotlib.pyplot as plt 

class Rectangle:

    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    
    def get_xmin(self):
        return self.xmin
    
    def get_ymin(self):
        return self.ymin
    
    def get_xmax(self):
        return self.xmax
    
    def get_ymax(self):
        return self.ymax
    
    def contains(self, p):   # p is a point
        return p.get_x() >= self.get_xmin() and p.get_x() <= self.get_xmax() and \
               p.get_y() >= self.get_ymin() and p.get_y() <= self.get_ymax()
    

    
    def intersects(self, other):
        if self.get_xmin() > other.get_xmax() or self.get_xmax() < other.get_xmin() or \
           self.get_ymin() > other.get_ymax() or self.get_ymax() < other.get_ymin():
            return False
        else:
            return True
        
    def distanceTo(self, p):
        dx = 0.0
        dy = 0.0
        if p.get_x() < self.get_xmin():
            dx = p.get_x() - self.get_xmin()
        elif p.get_x() > self.get_xmax():
            dx = p.get_x() - self.get_xmax()
        if p.get_y() < self.get_ymin():
            dy = p.get_y() - self.get_ymin()
        elif p.get_y() > self.get_ymax():
            dy = p.get_y() - self.get_ymax()
        return sqrt(dx*dx + dy*dy)
    
    def distanceSquaredTo(self, p):
        dx = 0.0
        dy = 0.0
        if p.get_x() < self.get_xmin():
            dx = p.get_x() - self.get_xmin()
        elif p.get_x() > self.get_xmax():
            dx = p.get_x() - self.get_xmax()
        if p.get_y() < self.get_ymin():
            dy = p.get_y() - self.get_ymin()
        elif p.get_y() > self.get_ymax():
            dy = p.get_y() - self.get_ymax()
        return dx*dx + dy*dy
    
    def equals(self, other):
        return self.get_xmin() == other.get_xmin() and self.get_xmax() == other.get_xmax() and \
           self.get_ymin() == other.get_ymin() and self.get_ymax() == other.get_ymax()
    
    def draw(self):
        plt.plot([self.get_xmin, self.get_xmax], [self.get_ymin, self.get_ymin],'r-')
        plt.plot([self.get_xmin, self.get_xmax], [self.get_ymax, self.get_ymax],'r-')
        plt.plot([self.get_xmin, self.get_xmin], [self.get_ymin, self.get_ymax],'r-')
        plt.plot([self.get_xmax, self.get_xmax], [self.get_ymin, self.get_ymax],'r-')
        
    def toString(self):
        return "".join(["rectangle(", str(self.get_xmin), ",", str(self.get_xmax), ",", str(self.get_ymin), ",", str(self.get_ymax),")"])
        
        