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

# Global Variables
startX = 200
startY = 200

def distance(x0,y0,x1,y1):
    return ((x0-x1)**2 + (y0-y1)**2)**0.5

    
class Enemies:
    def __init__(self):
        self.positions = []
        
    def move(self):
        # pathfinding algorithm
        pass
    
class GameMap:
    def __init__(self):
        self.maps = []
        self.map = self.maps[random.randrange(0,5)]
        
    def changeMap(self):
        self.map = self.maps[random.randrange(0,5)]
    
class Game:
    def __init__(self):
        self.user = User().position
        self.enemies = Enemies().positions
        self.map = GameMap().map

