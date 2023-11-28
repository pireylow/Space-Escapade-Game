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
import copy
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
            if pos[0] > userTopLeftIndex[0] and not map[newRow-1][newCol]:
                newRow -= 1
            elif pos[0] < userTopLeftIndex[0] and not map[newRow+1][newCol]:
                newRow += 1
            if pos[1] > userTopLeftIndex[1] and not map[newRow][newCol-1]:
                newCol -= 1
            elif pos[1] < userTopLeftIndex[1] and not map[newRow][newCol+1]:
                newCol += 1
                
            self.positions[i] = [newRow,newCol]
        
    def checkEnemyCollision(self,userTopLeftIndex):
        for i in range(len(self.positions)):
            pos  = self.positions[i]
            if abs(pos[0] - userTopLeftIndex[0])<2 and abs(pos[1] - userTopLeftIndex[1])<2:
                app.game = False
                app.gameOver = True
                if app.score > app.highscore:
                    app.highscore = app.score
            
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
        
    
    def add(self,map,screenTopLeftIndex,userTopLeftIndex):
        rowLower = int(screenTopLeftIndex[0])
        rowUpper = int(screenTopLeftIndex[0] + 99)
        colLower = int(screenTopLeftIndex[1])
        colUpper = int(screenTopLeftIndex[1] + 149)
        row = random.randint(rowLower,rowUpper)
        col = random.randint(colLower,colUpper)
        while ((userTopLeftIndex[0]-20 < row < userTopLeftIndex[0]+20 or
               userTopLeftIndex[1]-20 < col < userTopLeftIndex[1]+20) or
               map[row][col]):
            row = random.randint(rowLower,rowUpper)
            col = random.randint(colLower,colUpper)
        self.positions.append([row,col])
        
        
        
        

class PowerUps:
    def __init__(self):
        self.positions = []
        self.power = []
        
    def move(self,map,userTopLeftIndex):
        for i in range(len(self.positions)):
            pos  = self.positions[i]
            newRow = pos[0]
            newCol = pos[1]
            rowShift = random.randint(-1,1)
            colShift = random.randint(-1,1)
            newRow += rowShift
            newCol += colShift
            self.positions[i] = [newRow,newCol]
        
    def add(self,map,screenTopLeftIndex,userTopLeftIndex):
        rowLower = int(screenTopLeftIndex[0])
        rowUpper = int(screenTopLeftIndex[0] + 99)
        colLower = int(screenTopLeftIndex[1])
        colUpper = int(screenTopLeftIndex[1] + 149)
        count = 0
        for i in range(len(self.positions)):
            pos  = self.positions[i]
            if rowLower < pos[0] < rowUpper and colLower < pos[1] < colUpper:
                count+=1
            if count > 2:
                return
        row = random.randint(rowLower,rowUpper)
        col = random.randint(colLower,colUpper)
        while ((userTopLeftIndex[0]-20 < row < userTopLeftIndex[0]+20 or
               userTopLeftIndex[1]-20 < col < userTopLeftIndex[1]+20) or
               map[row][col]):
            row = random.randint(rowLower,rowUpper)
            col = random.randint(colLower,colUpper)
        self.positions.append([row,col])
        
        powerups = ['nuke', 'missiles', 'plasmaBeam', 'freeze']
        power = powerups[random.randint(0,3)]
        self.power.append(power)
        
    def checkPowerCollision(self,userTopLeftIndex):
        i=0
        while i < len(self.positions):
            pos  = self.positions[i]
            if abs(pos[0] - userTopLeftIndex[0])<3 and abs(pos[1] - userTopLeftIndex[1])<3:
                pos = self.positions.pop(i)
                power = self.power.pop(i)
                return (pos, power)
            else:
                i+=1
        return (None,None)
       
       
    # nuke         
    def nuke(self,powerPos,currentNukes,nukeTimes,nukeKillCount):
        currentNukes.append(powerPos)
        nukeTimes.append(0)
        nukeKillCount.append(0)
    
    def nukeKill(self,enemies,currentNukes,nukeKillCount):
        radius = 15
        for nuke in range(len(currentNukes)):
            i=0
            while i < len(enemies):
                row = enemies[i][0]
                col = enemies[i][1]
                if (row-currentNukes[nuke][0])**2 + (col-currentNukes[nuke][1])**2 <= radius**2:
                    enemies.pop(i)
                    nukeKillCount[nuke] += 1
                else:
                    i+=1
                    
    
    # plasmaBeam
    def plasmaBeam(self,plasmaBeamKillCount,plasmaBeamTimes):
        plasmaBeamKillCount.append(0)
        plasmaBeamTimes.append(0)
        
        
    def plasmaBeamKill(self,enemies,currentPlasmaBeams,plasmaBeamKillCount):
        radius = 10
        for plasmaBeam in range(len(plasmaBeamKillCount)):
            i=0
            while i < len(enemies):
                row = enemies[i][0]
                col = enemies[i][1]
                if (row-currentPlasmaBeams[plasmaBeam][0])**2 + (col-currentPlasmaBeams[plasmaBeam][1])**2 <= radius**2:
                    enemies.pop(i)
                    plasmaBeamKillCount[plasmaBeam] += 1
                else:
                    i+=1
                    
    def plasmaBeamMove(self,currentPlasmaBeams,plasmaBeamDirection):
        for i in range(len(currentPlasmaBeams)):
            currentPlasmaBeams[i][0] += plasmaBeamDirection[i][0]*2
            currentPlasmaBeams[i][1] += plasmaBeamDirection[i][1]*2
           
           
    # missiles
    def missiles(self,missilesMovement,missilesOrigin,missilesCurrent,powerPos,missilesKillCount,missilesTime):
        missilesKillCount.append(0)
        for _ in range(5):
            missilesTime.append(0)
            rowShift = random.randint(-3,3)
            colShift = random.randint(-3,3)
            missilesMovement.append([rowShift,colShift])
            missilesOrigin.append(copy.copy(powerPos))
            missilesCurrent.append(copy.copy(powerPos))
            
    def missilesKill(self,enemies,missilesExplosion,missilesKillCount):
        radius = 10
        for explosion in range(len(missilesExplosion)):
                i = 0
                while i < len(enemies):
                    row = enemies[i][0]
                    col = enemies[i][1]
                    if (row-missilesExplosion[explosion][0])**2 + (col-missilesExplosion[explosion][1])**2 <= radius**2:
                        enemies.pop(i)
                        missilesKillCount[explosion//5] += 1
                    else:
                        i+=1
    
    def missilesMove(self,index,missilesCurrent,missilesMovement):
        missilesCurrent[index][0] += missilesMovement[index][0]
        missilesCurrent[index][1] += missilesMovement[index][1]      
