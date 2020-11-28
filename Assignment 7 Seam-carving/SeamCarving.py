import numpy as np
import cv2

img = cv2.imread('6x5.png')

class SEWithBackPointerx():
    def __init__(self, energy, x_coordinate_in_previous_row=None):
        self.energy = energy
        self.x_coordinate_in_previous_row = x_coordinate_in_previous_row

class SEWithBackPointery():
    def __init__(self, energy, y_coordinate_in_previous_column=None):
        self.energy = energy
        self.y_coordinate_in_previous_column = y_coordinate_in_previous_column
        
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
        seam_energies = []
        seam_energies.append([SEWithBackPointery(pixel_energy) for pixel_energy in self.energy()[:,0]])
        
        for x in range(1, self.width()):
            pixel_energies_column = self.energy()[:,x]

            seam_energies_column = []
            for y, pixel_energy in enumerate(pixel_energies_column):
        
                y_top = max(y - 1, 0)
                y_bottom = min(y + 1, self.height()-1)
                y_range = range(y_top, y_bottom + 1)
                
                min_parent_y = min(y_range, key=lambda y_i: seam_energies[x-1][y_i].energy)
                min_seam_energy = SEWithBackPointery(pixel_energy + seam_energies[x-1][min_parent_y].energy, min_parent_y)
                seam_energies_column.append(min_seam_energy)

            seam_energies.append(seam_energies_column)
        
        min_seam_end_y = min(range(len(seam_energies[-1])),key=lambda y: seam_energies[-1][y].energy)
        
        seam = []
        seam_point_y = min_seam_end_y
        for x in range(len(seam_energies) - 1, -1, -1):
            seam.append((seam_point_y,x))

            seam_point_y = seam_energies[x][seam_point_y].y_coordinate_in_previous_column

        seam.reverse()
        
        return seam

    def findVerticalSeam(self):
        seam_energies = []
        seam_energies.append([SEWithBackPointerx(pixel_energy) for pixel_energy in self.energy()[0]])
        
        for y in range(1, len(self.energy())):
            pixel_energies_row = self.energy()[y]

            seam_energies_row = []
            for x, pixel_energy in enumerate(pixel_energies_row):
        
                x_left = max(x - 1, 0)
                x_right = min(x + 1, len(pixel_energies_row) - 1)
                x_range = range(x_left, x_right + 1)
                
                min_parent_x = min(x_range, key=lambda x_i: seam_energies[y - 1][x_i].energy)
                min_seam_energy = SEWithBackPointerx(pixel_energy + seam_energies[y - 1][min_parent_x].energy, min_parent_x)
                seam_energies_row.append(min_seam_energy)

            seam_energies.append(seam_energies_row)
            
        min_seam_end_x = min(range(len(seam_energies[-1])),key=lambda x: seam_energies[-1][x].energy)
        
        seam = []
        seam_point_x = min_seam_end_x
        for y in range(len(seam_energies) - 1, -1, -1):
            seam.append((seam_point_x, y))

            seam_point_x = seam_energies[y][seam_point_x].x_coordinate_in_previous_row

        seam.reverse()
        
        return seam

    def removeHorizontalSeam(self):
        for x in range(0, self.width()):
            for y in range(self.findHorizontalSeam()[x][0], self.height()):
                img[y][x] = img[y+1][x]
                
        return img
                
    def removeVerticalSeam(self):
        for y in range(0, self.height()):
            for x in range(self.findVerticalSeam()[y][0], self.width()):
                img[y][x] = img[y][x+1]
                
        return img
