from math import sqrt
import matplotlib.pyplot as plt 

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def distanceTo(self, other):
        return sqrt((self.x-other.x)**2+(self.y-other.y)**2)
    
    def distanceSquaredTo(self, other):
        return (self.x-other.x)**2+(self.y-other.y)**2
    
    def compareTo(self, other):
        if self.y > other.y:
            return 1
        elif self.y < other.y:
            return -1
        else:
            if self.x > other.x:
                return 1
            elif self.x < other.x:
                return -1
            else:
                return 0
            
    def equals(self, other):
        return self.x == other.x and self.y == other.y
    
    def draw(self):
        plt.plot(self.x, self.y, 'ko')
        
    def toString(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])