from string import printable
SYMBOLTABLE = list(printable) 

# for the class MoveToFront, I didn't use HexDump
class MoveToFront:
    def __init__(self, s, table):
        self.s = s
        self.table = table
        
    def encode(self):
        sequence, pad = [], self.table[::]
        for char in self.s:
            indx = pad.index(char)
            sequence.append(indx)
            pad = [pad.pop(indx)] + pad
        return sequence
    
    def decode(self):
        chars, pad = [], self.table[::]
        for indx in self.encode():
            char = pad[indx]
            chars.append(char)
            pad = [pad.pop(indx)] + pad
        return ''.join(chars)       
        

class CircularSuffixArray:
    def __init__(self, s):
        self.s = s
        
    def length(self):
        return len(s)
    
    def indexof(self, i):
        original = []
        for j in range(len(s)):
            suffix = s[j:] + s[:j]
            original.append(suffix)
            sor = sorted(original)
        tar = sor[i]
        return original.index(tar)
        
        
from collections import Counter

class BurrowsWheeler:
    def __init__(self, s):
        self.s = s
        
    def transform(self):
        original = []
        ans = []
        for j in range(len(s)):
            suffix = s[j:] + s[:j]
            original.append(suffix)
            sor = sorted(original)
        for line in sor:
            ans.append(line[-1])
        ans1 = ans.index(self.s[-1])
        ans = "".join(ans)
        return (ans1, ans)
        
    def inverseTransform(self):
        t = self.transform()[1]
        first = sorted(t)
        nextarray = [0]*len(self.s)
        dic = {}
        ori = [0]*len(self.s)
        
        for item in first:
            if self.s.count(item) != 1:
                indices = [j for j, it in enumerate(t) if it == item]
                dic[item] = indices
                
        for i, item in enumerate(first):
            if self.s.count(item) == 1:
                nextarray[i] = t.index(item)
            else:
                nextarray[i] = dic[item][0]
                dic[item].pop(0)
                
        firstrow = self.transform()[0]        
        for i in range(len(self.s)):
            ori[i] = first[firstrow] 
            firstrow = nextarray[firstrow]
            
        ori = "".join(ori)        
                
        return ori