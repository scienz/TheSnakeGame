from gametypes import CellType

class Cell:
    def __init__(self, x, y, cellType = CellType.SNAKEPART):
        self.type = cellType
        self.x = x
        self.y = y
        self.visited = False
    
    def __eq__(self, oc):
        # oc: other cell
        if type(oc) == Cell:
            return self.getX() == oc.getX() and self.getY() == oc.getY()
        else:
            raise TypeError(f"type {type(oc)} not supported in Cell comparision.")
    
    def __hash__(self):
        return hash(repr(self))
    
    def getType(self):
        return self.type
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def setType(self, cellType : CellType):
        self.type = cellType 
    
    def isVisited(self):
        return self.visited
    
    def setVisit(self, visited):
        self.visited = visited