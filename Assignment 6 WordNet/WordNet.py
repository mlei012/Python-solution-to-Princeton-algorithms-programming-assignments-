from collections import defaultdict

class Graph:
    def __init__(self, synsets, hypernyms):
        self.graph = defaultdict(list)
        self.synsets = synsets
        self.hypernyms = hypernyms

    # Add edge into the graph
    def add_edge(self, s, d):
        self.graph[s].append(d)

    def build_graph(self):
        with open(self.hypernyms, 'r') as hyper:
            for line in hyper.read().splitlines():
                line = line.split(',')
                for i in range(1, len(line)):
                    self.add_edge(int(line[0]), int(line[i]))
                    
        return self.graph
    
    def BFS(self, v): 
        visited = [False] * len(self.graph)
        queue = [] 
        queue.append(v) 
        visited[v] = True
        path = []
  
        while queue: 
            s = queue.pop(0) 
            path.append(s)
 
            for i in self.graph[s]: 
                if visited[i] == False: 
                    queue.append(i) 
                    visited[i] = True
                    
        return path
        
class SAP:
    def __init__(self, synsets, hypernyms):
        self.Gh = Graph(synsets, hypernyms)
        self.synsets = synsets
        self.hypernyms = hypernyms
     
    #length of shortest ancestral path between v and w; -1 if no such path
    def length(self, v, w):
        self.Gh.build_graph()
        bfs_v = self.Gh.BFS(v)
        bfs_w = self.Gh.BFS(w)
        common = [item for item in bfs_v if item in bfs_w] 
        
        if len(common) == 0:
            length = -1
            
        else:
            if len(bfs_v) > len(bfs_w):
                length = len([item for item in bfs_v if item not in common]) + 1
            elif len(bfs_v) < len(bfs_w):
                length = len([item for item in bfs_w if item not in common]) + 1
        
        return length
    
    # a common ancestor of v and w that participates in a shortest ancestral path; -1 if no such path
    def ancestor(self, v, w):
        self.Gh.build_graph()
        bfs_v = self.Gh.BFS(v)
        bfs_w = self.Gh.BFS(w)
        common = [item for item in bfs_v if item in bfs_w] 
        
        if len(common) == 0:
            ancestor = -1
        else:
            ancestor = common[0]
            
        return ancestor
    
    #  length of shortest ancestral path between any vertex in v and any vertex in w; -1 if no such path
    def Iter_length(self, vset, wset):
        self.Gh.build_graph()
        shortest = 999999
        for v in vset:
            for w in wset:
                bfs_v = self.Gh.BFS(v)
                bfs_w = self.Gh.BFS(w)
                common = [item for item in bfs_v if item in bfs_w] 
        
                if len(common) == 0:
                    length = -1
                else:
                    length = len(bfs_v) + len(bfs_w) - len(common)*2
                    
                if length < shortest:
                    shortest = length
        
        return shortest
    
    # a common ancestor that participates in shortest ancestral path; -1 if no such path
    def Iter_ancestor(self, vset, wset):
        self.Gh.build_graph()
        shortest = 999999
        ancestor = None
    
        for v in vset:
            for w in wset:
                bfs_v = self.Gh.BFS(v)
                bfs_w = self.Gh.BFS(w)
                common = [item for item in bfs_v if item in bfs_w] 
              
                if len(common) == 0:
                    length = -1
                    ancestor = -1
                else:
                    length = len(bfs_v) + len(bfs_w) - len(common)*2
                    
                if length < shortest:
                    shortest = length
                    ancestor = common[0]
        return ancestor  
        
import numpy as np

class WordNet:
    def __init__(self, synsets, hypernyms):
        self.synsets = synsets
        self.hypernyms = hypernyms

        self.dic = {}
        self.Gh = Graph(synsets, hypernyms)
        
        with open(synsets, 'r') as syn:
            for line in syn.readlines():
                e = [elem.split(" ") for elem in line.split(",")]
                self.dic[e[1][0]] = int(e[0][0])
                
    def nouns(self):
        return self.dic.values()
    
    def isNoun(self, word):
        return word in self.dic.values()

    def distance(self, nounA, nounB):
        G = self.Gh.build_graph()
        Aid = self.dic[nounA]
        Bid = self.dic[nounB]
        Aset = G[Aid]
        Bset = G[Bid]
        
        return SAP.Iter_length(self, Aset, Bset)
    
    # a synset (second field of synsets.txt) that is the common ancestor of nounA and nounB 
    # in a shortest ancestral path
    def sap(self, nounA, nounB):
        G = self.Gh.build_graph()
        Aid = self.dic[nounA]
        Bid = self.dic[nounB]
        Aset = G[Aid]
        Bset = G[Bid]
        
        return SAP.Iter_ancestor(self, Aset, Bset)
    
    def outcast(self, nounslist):
        distance_list = []
        for i in nounslist:
            distance = 0
            for j in nounslist:
                distance += self.distance(i,j)
            distance_list.append(distance)
        
        distance_list = np.array(distance_list)
        
        return nounslist[distance_list.argmax()]
        #return distance_list

'''        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

a = WordNet('synsets.txt','hypernyms.txt')
a.outcast(['horse', 'cat', 'bear', 'table','zebra'])
>>>>>[54, 36, 33, 60, 41] 
>>>>> answer is 'table'

a.outcast(['water', 'bed', 'orange_juice', 'milk', 'apple_juice', 'tea', 'coffee'])
>>>>>[48, 64, 45, 40, 45, 58, 42]
>>>>> answer is 'bed'
'''