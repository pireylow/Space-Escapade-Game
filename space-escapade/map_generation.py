import random

class Map:
    def  __init__(self,rows,cols,extra=10):
        self.map = []
        self.rows = rows
        self.cols = cols
        self.extra = extra
        self.aliveChance = 0.55
        self.deathLimit = 4
        self.birthLimit = 5
        self.iterations = 20
        
    def generateRandom(self):
        for row in range(self.rows + 2 * self.extra):
            rowList = []
            for col in range(self.cols + 2 * self.extra):
                if (self.extra<row<self.rows-self.extra and 
                    self.extra<col<self.cols-self.extra):
                    if random.randint(1, 100) < (self.aliveChance * 100):
                        rowList.append(False)
                    else:
                        rowList.append(True)
                else:
                    rowList.append(True)
            self.map.append(rowList)
            
        
    def generateActual(self):
        currMap = []
        for row in range(self.rows):
            rowList = []
            for col in range(self.cols):
                if (self.extra<row<self.rows-self.extra and
                    self.extra<col<self.cols-self.extra):
                    rowList.append(self.aliveCell(row,col))
                else:
                    rowList.append(True)
            currMap.append(rowList)
        self.map = currMap
        
        
    def aliveCell(self,row,col):
        count = 0
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx,dy)!=(0,0):
                    currRow = row+dx
                    currCol = col+dy
                    if (0<=currRow<self.rows and
                        0<=currCol<self.cols):
                        if self.map[currRow][currCol] == True:
                            count += 1
                    else:
                        count += 1
        if self.map[row][col] == True:
            if count >= self.deathLimit:
                return True
            else:
                return False
        else:
            if count >= self.birthLimit:
                return True
            else:
                return False
            
    def generateFinal(self):
        self.generateRandom()
        for iter in range(self.iterations):
            self.generateActual()
        return self.map