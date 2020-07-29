
from math import  hypot

''' Operation on a list of points with format (x,y) or (x,y,z) '''
class pointsManager():

    def __init__(self):
        self.elements=[]
        self.redoCache=None

    def add(self,point):

        self.elements.append(point)

    def undo(self):
        self.redoCache=self.elements.pop()

    def getPoints(self):
        return self.elements

    def redo(self):
        self.elements.append(self.redoCache)

    def remove(self,point):

        if point in self.elements:
            idx=self.elements.index(point)
            self.elements.pop(idx)

    def removeNearPoint(self,newpoint,distance_limit):

        for point in self.elements:
            difference=[x1 - x2 for (x1, x2) in zip(point, newpoint)]
            dist= hypot(*difference)
            if dist < distance_limit:
                self.remove(point)
                return True

        return False