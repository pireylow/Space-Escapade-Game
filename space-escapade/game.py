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
import numpy as np

import graphics
import pathfinding


def distance(x0,y0,x1,y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

    
class Enemies:
    def __init__(self):
        self.positions = []
        
    def move(self):
        # pathfinding algorithm
        for i in range(len(self.positions)):
            pos = self.positions[i]
            pathToUser = pathfinding.astar(pos,(app.cx,app.cy))
            if pathToUser and len(pathToUser) > 1:
                newPos = pathToUser[1]
                self.positions[i] = newPos
        
    
    def add(self):
        
    
class PowerUps:
    def __init__(self):
        self.positions = []
        self.power = []
        self.drift = []
        
    def move(self):
        
    def add(self):
        
    
    
    
class Game:
    def __init__(self,enemies,enemyR,map,powerups,powers,powerR,userX,userY,userR):
        self.enemies = enemies
        self.enemyR = enemyR
        self.map = map
        self.powerups = powerups
        self.powers = powers
        self.powerR = powerR
        self.userX = userX
        self.userY = userY
        self.userR = userR

    def checkPowerCollision(self):
        for i in range(len(self.powerups)):
            powerX,powerY = self.powerups[i]
            if distance(powerX,powerY,self.userX,self.userY) <= self.powerR + self.userR:
                activated = self.powers[i]
                break
        if activated == 'nuke':
            graphics.nuke()
        elif activated == 'missiles':
            graphics.missiles()
        elif activated == 'plasmaBeam':
            graphics.plasmaBeam()
        elif activated == 'freeze':
            graphics.freeze()
    
    def checkEnemyCollision(self):
        for i in range(len(self.enemies)):
            enemyX,enemyY = self.enemies[i]
            if distance(enemyX,enemyY,self.userX,self.userY) <= self.enemyR + self.userR:
                app.gameOver = True
                app.game = False