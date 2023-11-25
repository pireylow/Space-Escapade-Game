# Pathfinding Algorithm
# loop over enemy list and find first few steps for each enemy in the direction of shortest path

from cmu_graphics import *
import random
import heapq
import numpy as np

class Node:
    def __init__(self, position, gScore, hScore, parent = None):
        self.position = position
        self.gScore = gScore
        self.hScore = hScore
        self.fScore = gScore + hScore
        self.parent = parent

    def __lt__(self, other):
        if isinstance(other,Node):
            return self.fScore < other.fScore


class Pathfinding:
    def __init__(self,map,userPos,enemyPos):
        self.map = map
        self.userPos = userPos
        self.enemyPos = enemyPos
        
    def euclidean(pos1,pos2):
        x0,y0 = pos1
        x1,y1 = pos2
        return ((x0-x1)**2 + (y0-y1)**2)**0.5
    
    def getNeighbors(self,position):
        neighbors = []
        currRow, currCol = position
        for dx in range(-1,2):
            for dy in range(-1,2):
                if (dx,dy) != (0,0):
                    newRow, newCol = currRow+dx, currCol+dy
                    if (0<=newRow<=len(self.map) and 0<=newCol<=len(self.map[0]) and 
                        app.map[newRow][newCol]):
                        neighbors.append((newRow,newCol))
        return neighbors
    
    def astar(self):     
        frontier = []
        closed = set()
        startNode = Node(self.enemyPos,0,self.euclidean(self.enemyPos,self.userPos))
        heapq.heappush(frontier, startNode)
        
        while frontier:
            currentNode = heapq.heappop(frontier)
            if currentNode.position == self.userPos:
                path = []
                node = currentNode
                while node:
                    path.append(node.position)
                    node = node.parent
                return path[::-1]
        
            closed.add(currentNode.position)
            
            for neighborPos in self.getNeighbors(currentNode.position):
                if neighborPos in closed:
                    continue
                gScore = currentNode.gScore + 1
                hScore = self.euclidean(neighborPos,self.userPos)
                fScore = gScore + hScore
                
                neighborNode = Node(neighborPos,gScore,hScore,parent = currentNode)
                
                if neighborPos not in frontier:
                    heapq.heappush(frontier,neighborNode)
                elif neighborNode.fScore < frontier[frontier.index(neighborNode)].fScore:
                    frontier.remove(neighborNode)
                    heapq.heappush(frontier,neighborNode)
                
        return None
            
                
                   