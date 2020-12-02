from collections import defaultdict 
   
class FordFulkerson: 
   
    def __init__(self, graph, source, sink): 
        self.graph = graph 
        self.org_graph = [i[:] for i in self.graph.box]  
        self.ROW = graph.size 
        self.source = source
        self.sink = sink

    def BFS(self,s, t, parent): 
        visited =[False]*(self.ROW) 
        queue=[] 
        queue.append(s) 
        visited[s] = True
           
        while queue: 
            u = int(queue.pop(0))
            for ind, val in enumerate(self.graph.box[u]): 
                if visited[int(ind)] == False and val > 0: 
                    queue.append(int(ind)) 
                    visited[int(ind)] = True
                    parent[int(ind)] = u 
  
        return True if visited[int(t)] else False

    def dfs(self, graph,s,visited): 
        visited[s]=True
        for i in range(self.ROW): 
            if graph.box[int(s)][i]>0 and not visited[i]: 
                self.dfs(graph,i,visited) 
  
    def minCut(self, source, sink):  
        parent = [-1]*(self.ROW)  
        max_flow = 0 
  
        while self.BFS(source, sink, parent):  
            path_flow = 9999999999
            s = sink  
            while(s != source):  
                path_flow = min(path_flow, self.graph.box[parent[int(s)]][int(s)])  
                s = parent[int(s)]  
  
            max_flow += path_flow  
  
            v = sink  
            while(v != source):  
                u = parent[int(v)]  
                self.graph.box[int(u)][int(v)] -= path_flow  
                self.graph.box[int(v)][int(u)] += path_flow  
                v = parent[int(v)]  
  
        visited=self.ROW*[False] 
        self.dfs(self.graph,s,visited) 
  
        node = []
        for i in range(self.ROW):  
            if visited[i]:
                node.append(i)  
                    
        return node

    def FordFulkerson(self, source, sink): 
        parent = [-1]*(self.ROW) 
        max_flow = 0 
  
        while self.BFS(source, sink, parent): 
            path_flow = 99999999
            s = sink 
            while(s !=  source): 
                path_flow = min (path_flow, self.graph.box[parent[int(s)]][int(s)]) 
                s = parent[int(s)] 
  
            max_flow +=  path_flow 
  
            v = sink 
            while(v !=  source): 
                u = parent[int(v)] 
                self.graph.box[int(u)][int(v)] -= path_flow 
                self.graph.box[int(v)][int(u)] += path_flow 
                v = parent[int(v)] 
  
        return max_flow