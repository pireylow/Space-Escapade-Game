# Game Logic

# User Class
# position
# functions: updateMovement


# Enemy Class
# position of all enemies (random)
# functions: updateMovement (using pathfinding algorithm)


# Game Class
# initialize with user, list of enemies, game map, powerups
# functions: 
# 1. update -- move enemies and user, check for collisions
# 2. power-up collision
# 3. enemy collision

from cmu_graphics import *
import random
import heapq
import random
import pathfinding


def distance(x0,y0,x1,y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

    
class Enemies:
    def __init__(self):
        self.positions = []
        
    def move(self,map,userTopLeftIndex):
        for i in range(len(self.positions)):
            pos  = self.positions[i]
            newRow = pos[0]
            newCol = pos[1]
            if pos[0] > userTopLeftIndex[0]:
                newRow -= 1
            elif pos[0] < userTopLeftIndex[0]:
                newRow += 1
            if pos[1] > userTopLeftIndex[1]:
                newCol -= 1
            elif pos[1] < userTopLeftIndex[1]:
                newCol += 1
                
            self.positions[i] = [newRow,newCol]
        
    def checkEnemyCollision(self,userTopLeftIndex):
        for i in range(len(self.positions)):
            pos  = self.positions[i]
            if pos[0] == userTopLeftIndex[0] and pos[1] == userTopLeftIndex[1]:
                app.game = False
                app.gameOver = True
            
        # pathfinding algorithm
        # for i in range(len(self.positions)):
        #     pos = self.positions[i]
        #     pathfind = pathfinding.Pathfinding(map, userTopLeftIndex, pos)
        #     print(pathfind)
        #     pathToUser = pathfind.astar()
        #     print(pathToUser)
        #     if pathToUser and len(pathToUser) > 1: 
        #         newPos = pathToUser[10]
        #         self.positions[i] = newPos
                
        # recursion
        # for i in range(len(self.positions)):
        #     pos = self.positions[i]
        #     path = pathfinding.pathfind(map,userTopLeftIndex,pos,[])
        #     newPos = path[1]
        #     self.positions[i] = newPos
        
    
    def add(self,screenTopLeftIndex,userTopLeftIndex):
        rowLower = int(screenTopLeftIndex[0])
        rowUpper = int(screenTopLeftIndex[0] + 99)
        colLower = int(screenTopLeftIndex[1])
        colUpper = int(screenTopLeftIndex[1] + 149)
        row = random.randint(rowLower,rowUpper)
        col = random.randint(colLower,colUpper)
        while (userTopLeftIndex[0]-20 < row < userTopLeftIndex[0]+20 or
               userTopLeftIndex[1]-20 < col < userTopLeftIndex[1]+20):
            row = random.randint(rowLower,rowUpper)
            col = random.randint(colLower,colUpper)
        self.positions.append([row,col])
        
        
        
        

    # class PowerUps:
    # def __init__(self):
    #     self.positions = []
    #     self.power = []
    #     self.drift = []
        
    # def move(self):
        
    # def add(self):
        



# class Game:
#     def __init__(self,enemies,enemyR,map,powerups,powers,powerR,userX,userY,userR):
#         self.enemies = enemies
#         self.enemyR = enemyR
#         self.map = map
#         self.powerups = powerups
#         self.powers = powers
#         self.powerR = powerR
#         self.userX = userX
#         self.userY = userY
#         self.userR = userR

#     def checkPowerCollision(self):
#         for i in range(len(self.powerups)):
#             powerX,powerY = self.powerups[i]
#             if distance(powerX,powerY,self.userX,self.userY) <= self.powerR + self.userR:
#                 activated = self.powers[i]
#                 break
#         if activated == 'nuke':
#             graphics.nuke()
#         elif activated == 'missiles':
#             graphics.missiles()
#         elif activated == 'plasmaBeam':
#             graphics.plasmaBeam()
#         elif activated == 'freeze':
#             graphics.freeze()

#     def checkEnemyCollision(self):
#         for i in range(len(self.enemies)):
#             enemyX,enemyY = self.enemies[i]
#             if distance(enemyX,enemyY,self.userX,self.userY) <= self.enemyR + self.userR:
#                 app.gameOver = True
#                 app.game = False