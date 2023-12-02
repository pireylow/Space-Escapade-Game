
# CELLULAR AUTOMATA ALGORITHM FOR MAP GENERATION
# Conway's Game of Life Citation: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

# If an alive cell has four or more alive neighbours, it remains alive, otherwise it is killed.
# If a dead cell has five or more alive neighbours, it becomes alive.

# 1. Create a 2D list of random True / False values
# 2. Loop through rows and columns and implement the aforementioned rules, and append the new result
# 3. Iterate this process to get a desired 'emptiness' of the map (more iterations result in an 'emptier' map)

import random

# ------------------------------------------------------------------------------
#                                Map Class
# ------------------------------------------------------------------------------    

class Map:
    def  __init__(self,rows,cols,extra=10):
        self.map = []
        self.rows = rows
        self.cols = cols
        self.extra = 10
        self.aliveChance = 0.55
        self.deathLimit = 4
        self.birthLimit = 5
        self.iterations = 25
        
    # generate a grid of True / False values randomly
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
            
    # run one iteration of actual map generation base on the cellular automata criteria 
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
        
    # find if the True value should be birthed or killed  
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
            
    # run all iterations of actual map generation
    def generateFinal(self):
        self.generateRandom()
        for iter in range(self.iterations):
            self.generateActual()
        return self.map