import numpy as np
import copy
import priority_queue
import Node

class Board(object):
    def __init__(self, board):
        self.n = n
        self.board = board
        
    def tostring(self):
        print(n, end = '\n')
        for i in self.board:
            print(i, end = '\n')
            
    def dimension(self):
        return n
    
    def hamming(self,bd):
        num = 0
        bd = np.array(bd).reshape(-1)
        for i in range(0, n**2):
            if bd[i] != i+1 and bd[i] != 0:
                num += 1
        return num
    
    def manhattan(self,bd):
        dis = 0
        bd = np.array(bd).reshape(-1)
        for i in range(0, n**2):
            if bd[i] != i+1 and bd[i] != 0:
                dis = dis + np.abs(bd[i]-i-1)//n + np.abs(bd[i]-i-1)%n
        return dis
    
    def isgoal(self,bd):
        return self.hamming(bd) == 0
            
    def equals(self, y):
        self.board = np.array(self.board).reshape(-1)
        y = np.array(self.board).reshape(-1)
        for i in range(0, n):
            if self.board[i] == y[i]:
                return True
            else:
                return False
            
    def neighbors(self,bd):
        zerorow = 0
        zerocolumn = 0
        bd = np.array(bd).reshape(n,n)
        for i in range(0, n):
            for j in range(0, n):
                if bd[i][j] == 0:
                    zerorow = i
                    zerocolumn = j
                
        neighbors = []
        for (row_move, column_move) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            board_cy = copy.deepcopy(bd)
            if 0 <= (zerorow + row_move) < n and 0 <= (zerocolumn + column_move) < n:
                board_cy[zerorow][zerocolumn], board_cy[zerorow + row_move][zerocolumn + column_move] = \
                board_cy[zerorow + row_move][zerocolumn + column_move], board_cy[zerorow][zerocolumn]
                
                neighbors.append(board_cy)
        return neighbors
        
    def twin(self, bd):
        twins = []
        for i in range(0, n):
            for j in range(0, n):
                for (row_move, column_move) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    board_cy = copy.deepcopy(bd)
                    if 0 <= (i + row_move) < n and 0 <= (j + column_move) < n and board_cy[i][j] != 0 and \
                    board_cy[i+row_move][j+column_move] != 0:
                    
                        board_cy[i][j], board_cy[i + row_move][j + column_move] = \
                        board_cy[i + row_move][j + column_move], board_cy[i][j]
                
                        twins.append(board_cy)
                
        return twins
    
    # Now just consider n is odd. For completeness, 
    # visit https://www.cs.princeton.edu/courses/archive/fall12/cos226/assignments/8puzzle.html
    def isSolvable(self, bd):
        bd = np.array(bd).reshape(-1)
        num = 0
        for i in range(0, n**2):
            for j in range(i+1, n**2):
                if bd[i] != 0 and bd[j] != 0 and bd[i] > bd[j]:
                    num +=1
        
        return num % 2 == 0
        
    def solution(self, board):
        if self.isSolvable(board) == False:
            print ("Unsolvable puzzle")
        
        else:
            start = self.board
            num_move = 1
            nodes = []
            items = []
            path = []
            #state_seen = []
            while not self.isgoal(start):
                for state in self.neighbors(start):
                    #for i in state_seen:
                        #if not state.equals(i) or len(state_seen) == 0:
                    man = self.manhattan(state)
                    #num_move += 1
                    priority = man + num_move
                    node = Node.Node(state, priority)
                    #dic[str(state)] = priority
                    #        state_seen.append(state)
                #print(state_seen)
                    nodes.append(node.get_val())
                    items.append(node)
            #print(nodes)
             
                pq = priority_queue.priority_queue()
                pq.buildHeap(list(i for i in nodes))
                val = pq.delMin()
                for i in items:
                    if i.get_val() == val:
                        start = i.get_key() 
                path.append(start)
                num_move += 1
            #print(start)
            return path  