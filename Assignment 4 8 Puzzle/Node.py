class Node(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value
        
    def get_val(self):
        return self.value
    
    def get_key(self):
        return self.key