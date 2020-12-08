class BoggleBoard:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.board = [[' '] * self.n for _ in range(self.m)]
        
    def BoggleBoard0(self, m, n):
        #m = 4
        #n = 4
        self.board = [[' '] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                letters = BOGGLE_1992[m*i+j]
                r = int(random.uniform(0, len(letters)))
                self.board[i][j] = letters[r]
                
        return self.board
    
    def BoggleBoard(self, m, n):
        self.board = [[' '] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                r = int(np.random.choice(np.arange(1, len(FREQUENCIES)+1), p=FREQUENCIES))
                self.board[i][j] = ALPHABET[r]
                
        return self.board
    
    def BoggleBoardf(self, filename):
        f = open(filename, "r")
        text = f.read()
        text = text.strip(' ').splitlines()
        text[0] = text[0].split(' ')
        m, n = int(text[0][0]), int(text[0][1])
        self.board = [[' '] * n for _ in range(m)]
        
        for i, line in enumerate(text[1:]):
            line = line.split(' ')
            line = list(filter(None, line))
            for j in range(n):
                self.board[i][j] = line[j]
                
        return self.board
    
    def BoggleBoard(self, a):
        m = len(a)
        n = len(a[0])
        self.board = [[' '] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                self.board[i][j] = a[i][j]
                
        return self.board
    
    def rows(self):
        return self.m
    
    def columns(self):
        return self.n
        
b = BoggleBoard(4, 4)
board = b.BoggleBoardf('board-q.txt')

class TrieNode: 
    def __init__(self): 
        self.children = [None]*26
        self.isEndOfWord = False

class Trie: 
    def __init__(self): 
        self.root = self.getNode() 
  
    def getNode(self): 
        return TrieNode() 
  
    def _charToIndex(self,ch): 
        return ord(ch)-ord('A') 
    
    def insert(self, key): 
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
  
            if not pCrawl.children[index]: 
                pCrawl.children[index] = self.getNode() 
            pCrawl = pCrawl.children[index] 
  
        pCrawl.isEndOfWord = True
        
        
class BoggleSolver:
    def __init__(self, dictionary):
        self.dictionary = dictionary
    
    def BoggleSolver(self):
        dic = self.load_dictionary()
        t = Trie()
        for d in dic:
            t.insert(d)
        return t
 
    def load_dictionary(self):
        words = []
        prefix = []
        with open(self.dictionary, 'r') as f:
            next(f)
            for line in f:
                word = line.rstrip()
                if len(word) >= 3:
                    words.append(word)
                    for i in range(len(word)):
                        prefix.append(word[:i])
  
        return words
    
    def getletter(self, w):
        rows = len(board)
        columns = len(board[0])
        r = w // rows
        c = w % rows
        return board[r][c]
    
    def searchvalidwords(self, v, x, prefix, visiting):
        if len(prefix) > 2 and x != None and x.isEndOfWord == True:
            self.validwords.append(prefix)
            
        for w in self.getadj()[v]:
            c = self.getletter(w)
            if not self.marked[w] and x != None and x.children[ord(c[0]) -ord('A')] != None:
                visiting.append(w)
                self.marked[w] = True
                
                if c == 'Qu':  
                    self.searchvalidwords(w, x.children[ord('Q')-ord('A')].children[ord('U')-ord('A')], prefix+"QU", visiting)
                else:
                    self.searchvalidwords(w, x.children[ord(c)-ord('A')], prefix+c, visiting)
            
                index = visiting.pop()
                self.marked[index] = False      
                
    def getadj(self):
        rows = len(board)
        columns = len(board[0])
        adj = {}
        
        for i in range(rows):
            for j in range(columns):
                v = i*columns + j
                valid = []
                for newi, newj in ((i-1,j-1), (i,j-1), (i+1,j-1), (i-1,j), (i+1,j), (i-1,j+1), (i,j+1), (i+1,j+1)):
                    if 0 <= newi < rows and 0 <= newj < columns:
                        valid.append(newi*columns + newj)
                adj[v] = valid
        
        return adj
        
    def getvalidwords(self):
        rows = len(board)
        columns = len(board[0])
        
        self.validwords = []
        for v in range(rows*columns):
            visiting = []
            self.marked = [False for i in range(rows*columns)]
            visiting.append(v)
            self.marked[v] = True
            
            Tr = self.BoggleSolver()
            
            if self.getletter(v) == 'Qu':
                self.searchvalidwords(v, Tr.root.children[ord('Q')-ord('A')].children[ord('U')-ord('A')], "QU", visiting)
            else:
                self.searchvalidwords(v, Tr.root.children[ord(self.getletter(v))-ord('A')], self.getletter(v) + "", visiting)
                
        res = [] 
        for i in self.validwords: 
            if i not in res: 
                res.append(i) 
        
        return res    
    
    def getscore(self):
        validwords = self.getvalidwords()
        score = 0
        for word in validwords:
            if len(word) == 3:
                score += 1
            elif len(word) == 4:
                score += 1
            elif len(word) == 5:
                score += 2
            elif len(word) == 6:
                score += 3
            elif len(word) == 7:
                score += 5
            else: 
                score += 11
                
        return score   