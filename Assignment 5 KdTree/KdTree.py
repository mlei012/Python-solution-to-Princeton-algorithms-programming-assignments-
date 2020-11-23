class KdTree:
    def __init__(self, tree):
        self.tree = tree
        
    def isempty(self):
        return self.tree == None
    
    def insertTree(self, root, p, vertical):
        if root == None:
            return p
        if root.val == p.val:
            return root
        
        if vertical:
            if root.val.get_x() > p.get_x():
                root.left = self.insertTree(root.left, p, vertical=False)
            else:
                root.right = self.insertTree(root.right, p, vertical=False)
        
        else:
            if root.val.get_y() > p.get_y():
                root.left = self.insertTree(root.left, p, vertical=True)
            else:
                root.right = self.insertTree(root.right, p, vertical=True)
                
        root.count = 1
        if root.left != None:
            root.count += root.left.count
        if root.right != None:
            root.count += root.right.count
            
        return root
    
    def addpoint(self, p):
        self.tree = self.insertTree(self.tree, p, vertical=True)
        
    # seach the tree, does the point in the tree
    def searchtree(self, root, p, vertical):
        if root == None:
            return False
        if root.val.equals(p):
            return True
        
        if vertical:
            if root.val.get_x() > p.get_x():
                return self.searchtree(root.left, p, False)
            else:
                return self.searchtree(root.right, p, False)
        else:
            if root.val.get_y() > p.get_y():
                return self.searchtree(root.left, p, True)
            else:
                return self.searchtree(root.right, p, True)
            
    # does the set contain point p?
    def contain_p(self, p):
        return self.searchtree(self.tree, p, True)
    
    def drawTree(self, root, rect, vertical):
        if root == None:
            return
        root.val.draw()
        
        if vertical:
            
            plt.plot([root.val.get_x(), root.val.get_x()], [rect.get_ymin(), rect.get_ymax()], 'r-')
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            left_rect = Rectangle.Rectangle(rect.get_xmin(), root.val.get_x(), rect.get_ymin(), rect.get_ymax())
            right_rect = Rectangle.Rectangle(root.val.get_x(), rect.get_xmax(), rect.get_ymin(),rect.get_ymax())
            self.drawTree(root.left, left_rect, False)
            self.drawTree(root.right, right_rect, False)
            
        else:
            plt.plot([rect.get_xmin(), rect.get_xmax()], [root.val.get_y(), root.val.get_y()], 'b-')
            plt.xlim(0, 1)
            plt.ylim(0, 1)
            bottom_rect = Rectangle.Rectangle(rect.get_xmin(), rect.get_xmax(), rect.get_ymin(), root.val.get_y())
            top_rect = Rectangle.Rectangle(rect.get_xmin(), rect.get_xmax(), root.val.get_y(), rect.get_ymax())
            self.drawTree(root.left, bottom_rect, True)
            self.drawTree(root.right, top_rect, True)
            
            
    def drawall(self):
        self.drawTree(self.tree, rect=Rectangle.Rectangle(0,1,0,1), vertical = True)
     
    # 'curr' is the current rectangle, and rect is the rect used to do the search
    def rangesearch(self, root, curr, rect, point_set, vertical):
        if root == None:
            return
        if rect.contains(root.val):
            point_set.append(root.val)
            
        left_rect = None
        right_rect = None
        
        if vertical:
            left_rect = Rectangle.Rectangle(curr.get_xmin(), root.val.get_x(),curr.get_ymin(), curr.get_ymax())
            right_rect = Rectangle.Rectangle(root.val.get_x(), curr.get_xmax(), curr.get_ymin(), curr.get_ymax())
        
        else:
            left_rect = Rectangle.Rectangle(curr.get_xmin(), curr.get_xmax(),curr.get_ymin(), root.val.get_y())
            right_rect = Rectangle.Rectangle(curr.get_xmin(), curr.get_xmax(),root.val.get_y(), curr.get_ymax())
        
        if left_rect.intersects(rect):
            self.rangesearch(root.left, left_rect, rect, point_set, not vertical)
        if right_rect.intersects(rect):
            self.rangesearch(root.right, right_rect, rect, point_set, not vertical)
                      
    #all points that are inside the rectangle (or on the boundary)
    def inside(self, rect):
        tar = []
        self.rangesearch(self.tree, Rectangle.Rectangle(0,1,0,1), rect, tar, True)
        return tar
                      
    def nearestTree(self, root, curr, rect, p, vertical):
        if root == None:
            return curr
        if root.val.distanceSquaredTo(p) < curr.distanceSquaredTo(p):
            curr = root.val
                      
        left_rect = None
        right_rect = None
        
        if vertical == True:
            left_rect = Rectangle.Rectangle(rect.get_xmin(), root.val.get_x(), rect.get_ymin(), rect.get_ymax())
            right_rect = Rectangle.Rectangle(root.val.get_x(), rect.get_xmax(), rect.get_ymin(), rect.get_ymax())
                      
        else:
            left_rect = Rectangle.Rectangle(rect.get_xmin(), rect.get_xmax(), rect.get_ymin(), root.val.get_y())
            right_rect = Rectangle.Rectangle(rect.get_xmin(), rect.get_xmax(),root.val.get_y(), rect.get_ymax())
                
        left_dis = left_rect.distanceSquaredTo(p)
        right_dis = right_rect.distanceSquaredTo(p)
        
        if left_dis < right_dis:
            if left_dis < curr.distanceSquaredTo(p):
                curr = self.nearestTree(root.left, curr, left_rect, p, not vertical)
            if right_dis < curr.distanceSquaredTo(p):
                curr = self.nearestTree(root.right, curr, right_rect, p, not vertical)
        
        else:
            if right_dis < curr.distanceSquaredTo(p):
                curr = self.nearestTree(root.right, curr, right_rect, p, not vertical)
            if left_dis < curr.distanceSquaredTo(p):
                curr = self.nearestTree(root.left, curr, left_rect, p, not vertical)

        return curr
    
    #nearest neighbor
    def nn(self, p):
        rect = Rectangle.Rectangle(0.0, 1.0, 0.0, 1.0)
        return self.nearestTree(self.tree, self.tree.val, rect, p, True)
        