import Point
import Rectangle
from math import sqrt
import matplotlib.pyplot as plt 

class PointSET(object):
    def __init__(self, pointset):
        self.pointset = pointset
        
    def isEmpty(self):
        return self.pointset == None
    
    def size(self):
        return len(self.pointset)
    
    def insert(self, p):
        if p not in self.pointset:
            self.pointset.append(p)
            
    def set_contains(self, p):
        return p in self.pointset
    
    def drawset(self):
        for i in self.pointset:
            i.draw()
            
    def rec_range(self, rect):
        rect_set = []
        for i in self.pointset:
            if rect.contains(i):
                rect_set.append(i)
                
        return rect_set
    
    def nearest(self, p):
        nearest_dis = 1000000
        nearest = None
        for i in self.pointset:
            dis = i.distanceTo(p)
            if dis < nearest_dis:
                nearest_dis = dis
                nearest = i
                
        return nearest