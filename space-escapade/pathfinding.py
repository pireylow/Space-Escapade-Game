# Pathfinding Algorithm
# loop over enemy list and find first few steps for each enemy in the direction of shortest path

from cmu_graphics import *
import random
import heapq
import numpy as np

class Pathfinding:
    def __init__(self,):
        
    def heuristic(x0,y0,x1,y1):
        return ((x0-x1)**2 + (y0-y1)**2)**0.5
    
    def astar()
    
    def getNeighbors(position):
        neighbors = []
        currRow, currCol = position
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx,dy) != (0,0):
                    newRow, newCol = currRow+dx, currCol+dy
                    if (app.extra<=newRow<=app.rows-app.extra and app.extra<=newCol<=app.cols-app.extra and 
                        app.map[newRow][newCol]):
                        neighbors.append((newRow,newCol))
        return neighbors
    
