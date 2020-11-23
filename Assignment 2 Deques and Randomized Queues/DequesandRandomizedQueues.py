import random

class Node(object):
    def __init__(self, item):
        self.item = item
        self.next = None

class RandomizedQueue(object):
    def __init__(self):
        self.head = None     # head is a node, and has .item and .next attributes
        self.rear = None 
        
    def is_empty(self):
        return self.head is None  
    
    def size(self):
        count = 0
        cur = self.head
        while cur != None:
            count += 1
            cur = cur.next
        return int(count)
    
    def enqueue(self, item):
        p = Node(item)  
        if self.is_empty():
            self.head = p  
            self.rear = p  
        else:
            self.rear.next = p  
            self.rear = p  
            
    def dequeue(self):
        size = self.size()
        site = random.randint(0, int(size)-1)    # random.randint(a, b): Return a random int N such that a <= N <= b
        #print(site)
        if site == 0:
            print(self.head.item)
            self.head = self.head.next
        else:
            count = 1   # means the head(1st) node in the queue
            cur = self.head
            while site != count:
                cur = cur.next
                count += 1
            if cur.next.next == None:
                print(self.rear.item)
            else:
                print(cur.next.item)
            cur.next = cur.next.next
        
    def sample(self):
        size = self.size()
        site = random.randint(0, int(size)-1) 
        if site == 0:
            print(self.head.item)
        else:  
            count = 1
            cur = self.head
            while site != count:
                cur = cur.next
                count += 1
            if cur.next.next == None:
                print(self.rear.item)
            else:
                print(cur.next.item)
        
    def iterator(self):
        cur = self.head
        while cur != None:
            print(cur.item, end=',')
            cur = cur.next
        print('')
    
    def iterator1(self):
        print("queue:")
        temp = self.head
        myqueue = []  
        while temp is not None:
            myqueue.append(temp.item)
            temp = temp.next
        print(myqueue)
    