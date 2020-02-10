

z_coordinate= 0

class coloniesCache():

    def __init__(self):
        self.elements=[]
        self.redoCache=None

    def add(self,point=(0,0)):

        self.elements.append(point)

    def undo(self):
        self.redoCache=self.elements.pop()

    def redo(self):
        self.elements.append(self.redoCache)


