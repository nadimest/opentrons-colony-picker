
from math import  hypot

''' Operation on a list of points with format (x,y) '''
class coloniesCache():

    def __init__(self):
        self.elements=[]
        self.redoCache=None

    def add(self,point):

        self.elements.append(point)

    def undo(self):
        self.redoCache=self.elements.pop()

    def getCoordinates(self):
        return self.elements

    def redo(self):
        self.elements.append(self.redoCache)

    def remove(self,point):

        if point in self.elements:
            idx=self.elements.index(point)
            self.elements.pop(idx)

    def removeNearPoint(self,newpoint,distance_limit):

        for point in self.elements:
            dist= hypot(point[0]-newpoint[0],point[1]-newpoint[1])
            if dist < distance_limit:
                self.remove(point)
                return True

        return False