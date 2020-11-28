import numpy as np
import cv2

img = cv2.imread(file)

class SeamCarver():
    def __init__(self,img):
        self.img = img
        
    def width(self):
        w = self.img.shape[1]
        return w
        
    def height(self):
        h = self.img.shape[0]
        return h
        
    def energy(self):
        en = np.zeros((self.height(), self.width()))
        
        for y in range(1, self.height()-1): 
            for x in range(1, self.width()-1):
                for z in range(3):
                    en[y,x] += (int(img[y][x+1][z]) - int(img[y][x-1][z]))**2 + (int(img[y+1][x][z]) - int(img[y-1][x][z]))**2
 
        en = np.sqrt(en)
        
        for y in range(0, self.height()): 
            for x in range(0, self.width()):
                if y == 0 or y == self.height()-1 or x == 0 or x == self.width()-1:
                    en[y,x] = 1000
                
        return en  
    
    def findHorizontalSeam(self):
        rem = []
        for x in range(1, self.width()):
            if x == 1:
                minvalue = 99999999
                yminid = 0
                for y in range(0, self.height()):
                    if self.energy()[y][x] < minvalue:
                        minvalue = self.energy()[y][x]
                        yminid = y
                rem.append(yminid)
                rem.append(yminid)   # this is the index for x==0
                
            else:
                minvalue = 1000
                for y in range(yminid-1, yminid+2):
                    if 0 <= yminid-1 and yminid+1<self.height():
                        if self.energy()[y][x] < minvalue: 
                            minvalue = self.energy()[y][x]
                            yminid = y
                rem.append(yminid)
        return rem
    
    def findVerticalSeam(self):
        rem = []
        for y in range(1, self.height()):
           
            if y == 1:
                minvalue = 99999999
                xminid = 0
                for x in range(0, self.width()):
                    if self.energy()[y][x] < minvalue:
                        minvalue = self.energy()[y][x]
                        xminid = x
                rem.append(xminid)
                rem.append(xminid)   # this is the index for y==0
                
            else:
                minvalue = 1000
                for x in range(xminid-1, xminid+2):
                    if 0 <= xminid-1 and xminid+1<self.width():
                        if self.energy()[y][x] < minvalue: 
                            minvalue = self.energy()[y][x]
                            xminid = x
                rem.append(xminid)
        return rem
    
    def removeHorizontalSeam(self):
        for x in range(0, self.width()):
            for y in range(self.findHorizontalSeam()[x], self.height()):
                img[y][x] = img[y+1][x]
                
        return img
                
    def removeVerticalSeam(self):
        for y in range(0, self.height()):
            for x in range(self.findVerticalSeam()[y], self.width()):
                img[y][x] = img[y][x+1]
                
        return img