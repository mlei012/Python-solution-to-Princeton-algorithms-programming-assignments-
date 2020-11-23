import matplotlib.pyplot as plt 

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        plt.plot(self.x, self.y, 'ro')
        
    def drawTo(self, other):
        plt.plot([self.x, other.x], [self.y, other.y], 'o-',)
        
    def __str__(self):
        return "x=" + str(self.x) + ", y=" + str(self.y)
     
    def compareTo(self, other): 
        if self.y < other.y: 
            return -1
        elif self.y > other.y: 
            return 1
        elif self.y == other.y: 
            if self.x > other.x: 
                return 1
            elif self.x < other.x: 
                return -1
            else:
                return 0
            
    def slopeTo(self, other):
        return (self.y-other.y)/(self.x-other.x) if self.x != other.x else float('inf')
    
    def slopeOrder(self, other1, other2):
        slope1 = self.slopeTo(self, other1)
        slope2 = self.slopeTo(self, other2)
        if slope1 < slope2:
            return -1
        elif slope1 > slope2:
            return 1
        else:
            return 0       
            

point1 = Point(19000,10000)
point2 = Point(18000,10000)
point3 = Point(32000,10000)
point4 = Point(21000,10000)
point5 = Point(1234,5678)
point6 = Point(14000,10000)
points = [point1, point2, point3, point4, point5, point6]

def BruteCollinearPoints(points):
    N = len(points)
    
    for i in range(0, N-3):
        for j in range(i+1,N-2):
            slope1 = points[i].slopeTo(points[j])
            for k in range(j+1,N-1):
                slope2 = points[j].slopeTo(points[k])
                if slope1 != slope2:
                    continue
                for m in range(k+1,N):
                    slope3 = points[k].slopeTo(points[m])
                    if slope1 != slope3:
                        continue
                    
                    points[i].drawTo(points[j])
                    points[j].drawTo(points[k])
                    points[k].drawTo(points[m])
                    
def FastCollinearPoints(points):
    N = len(points)
    points.sort(key=lambda points: points.x)
    p = points[0]
    #print(p.__str__())
    count = 1
    
    points.sort(key=lambda points: p.slopeTo(points)) 
    
    #for i in points:
    #   print(i.__str__())

    for i in range(0, N):
        for j in range(1, N):
            if(points[i].slopeTo(points[j-1]) == points[i].slopeTo(points[j])):
                count += 1
                print((i,j-1), (i,j))
                print("I have: {0}".format(count))
                
            else:
                count = 1

            if count >= 3:
                points[i].drawTo(points[j])                      
                
                
                