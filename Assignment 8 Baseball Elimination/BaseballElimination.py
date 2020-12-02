import numpy as np

f = open(file, "r")
text = f.read()
text = text.strip(' ').splitlines()
num_team = int(text[0])

finish = []
remain = []
teamid = []
teams = []

for team in text[1:]:
    team = team.split(' ')
    team = list(filter(None, team))
    finish.append(team[0:4])
    remain.append(team[4:])

dic = {}
dic2 = {}
for i, t in enumerate(finish):
    tid, [teamname, win, loss, left] = i, t
    teamid.append(tid)
    teams.append([teamname, int(win), int(loss), int(left)])
    dic[teamname] = tid
    dic2[i]= [int(win), int(loss), int(left)]
            
g = np.zeros((num_team, num_team), dtype=int)
for i in range(num_team):
    for j in range(num_team):
        g[i][j] = int(remain[i][j])
        
from collections import defaultdict

class FlowEdge(object):  
    def __init__(self, v, w, capacity, flow=0):
        self.v = v
        self.w = w
        self.capacity = capacity
        self.flow = flow
    
    def fm(self):
        return self.v
    
    def to(self):
        return self.w
    
    def other(self, vertex):
        if vertex == self.v:
            return self.w
        elif vertex == self.w:
            return self.v
        else:
            print('Illegal endpoint')
            
    def capacity(self):
        return self.capacity
    
    def flow(self):
        return self.flow
    
    def residualCapacityTo(self, vertex):
        if vertex == self.v:
            return self.flow
        elif vertex == self.w:
            return self.capacity - self.flow
        else:
            print('Illegal endpoint')
            
    def addResidualFlowTo(self, vertex, delta):
        if vertex == self.v:
            self.flow -= delta
        elif vertex == self.w:
            self.flow += delta
        else:
            print('Illegal endpoint')
        
    def toString(self):
        return "%s->%s:%s" % (self.v, self.w, self.capacity)
      
class FlowNetwork(object):  
    def __init__(self,size):
        self.size = size
        self.box = np.zeros((size, size), dtype=int)

    def add_edge(self, v, w, capacity):
        self.box[v][w] = capacity
        self.box[w][v] = 0
        
    def box(self):
        return self.box
        
import FordFulkerson

class BaseballElimination:
    def __init__(self, team):
        self.team = team
        
    def BE(self, team):
        x = dic[team]
        num_gameVertices = int(num_team * (num_team - 1)/2)
        num_vertices = int(num_gameVertices + num_team + 2)
        
        s = 0
        t = num_vertices - 1
        index = 1
        self.flow = 0
        f = FlowNetwork(num_vertices)
        
        for i in range(num_team):
            if i == x:
                continue
    
            for j in range(i+1, num_team):
                if j == x:
                    continue
            
                f.add_edge(s, index, g[i][j])
                f.add_edge(index, int(i + num_gameVertices + 1), 99999999)
                f.add_edge(index, int(j + num_gameVertices + 1), 99999999)
                index += 1
                self.flow += g[i][j]
                
            wx = dic2[x][0]
            rx = dic2[x][2]
            wi = dic2[i][0]
            
            if wx + rx - wi < 0:
                return None
            else:
                f.add_edge(int(i + num_gameVertices + 1), int(t), int(wx + rx - wi))
                
        f = FordFulkerson.FordFulkerson(f, s, t)
        
        return f.FordFulkerson(s,t)
    
    def connectednode(self, team):
        x = dic[team]
        num_gameVertices = num_team * (num_team - 1)/2
        num_vertices = num_gameVertices + num_team + 2
        
        s = 0
        t = num_vertices - 1
        index = 1
        self.flow = 0
        f = FlowNetwork(int(num_vertices))
        
        for i in range(num_team):
            if i == x:
                continue
    
            for j in range(i+1, num_team):
                if j == x:
                    continue
            
                f.add_edge(s, index, g[i][j])
                f.add_edge(index, int(i + num_gameVertices + 1), 99999999)
                f.add_edge(index, int(j + num_gameVertices + 1), 99999999)
                index += 1
                self.flow += g[i][j]
                
            wx = dic2[x][0]
            rx = dic2[x][2]
            wi = dic2[i][0]
            
            if wx + rx - wi < 0:
                return None
            else:
                f.add_edge(int(i + num_gameVertices + 1), int(t), int(wx + rx - wi))
                
        f = FordFulkerson.FordFulkerson(f, s, t)
        
        return f.minCut(0, num_vertices-1)
    
    def isEliminated(self, team):
        maxflow = self.BE(team)
        if maxflow == None:
            return True
        else:
            return float(self.flow) > float(maxflow)
        
    def certificateOfElimination(self, team):
        if not self.isEliminated(team):
            return None
        
        lst = []
        x = dic[team]
        num_gameVertices = num_team * (num_team - 1)/2
        num_vertices = num_gameVertices + num_team + 2
        maxflow = self.BE(team)
       
        for index in range(num_team):
            if index == x:
                continue
                
            if maxflow == None:
                wx = dic2[x][0]
                rx = dic2[x][2]
                wi = dic2[index][0]
                
                if wx + rx - wi < 0:
                    lst.append([teamname for teamname, teamid in dic.items() if teamid == index])
                         
        if maxflow != None:
            for i in self.connectednode(team):
                inx = i - num_gameVertices - 1
                if inx >= 0:
                    lst.append([teamname for teamname, teamid in dic.items() if teamid == inx])
        return lst       