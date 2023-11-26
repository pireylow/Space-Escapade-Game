# Pathfinding Algorithm
# loop over enemy list and find first few steps for each enemy in the direction of shortest path

from cmu_graphics import *
import random
import heapq


# def pathfind(map,userPos,enemyPos,L):
#     rows,cols = len(map), len(map[0])
#     if len(L)>0 and  abs(L[-1][0] - userPos[0])<10 and abs(L[-1][1] - userPos[1])<10:
#         return L
#     else:
#         for dx,dy in [(-10,0),(0,-10),(10,0),(0,10)]:
#             newRow = enemyPos[0]+dy
#             newCol = enemyPos[1]+dx
#             if not map[newRow][newCol]:
#                 L.append([newRow,newCol])
#                 enemyPos = [newRow,newCol]
#                 solution = pathfind(map,userPos,enemyPos,L)
#                 if solution != None:
#                     return solution
#                 L.pop()
#                 enemyPos = L[-1]
#         return None
    



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
        
    def manhattan(self,pos1,pos2):
        x0,y0 = pos1
        x1,y1 = pos2
        return abs(x0-x1) + abs(y0-y1)
    
    def getNeighbors(self,position):
        neighbors = []
        currRow, currCol = position
        for dx,dy in [(-1,0),(0,-1),(1,0),(0,1)]:
            newRow, newCol = currRow+dx, currCol+dy
            if (0<=newRow<=len(self.map) and 0<=newCol<=len(self.map[0]) and 
                app.map[newRow][newCol]):
                neighbors.append((newRow,newCol))
        return neighbors
    
    def astar(self):     
        frontier = []
        closed = set()
        startNode = Node(self.enemyPos,0,self.manhattan(self.enemyPos,self.userPos))
        print(startNode)
        heapq.heappush(frontier, startNode)
        print(frontier)
        
        while frontier:
            currentNode = heapq.heappop(frontier)
            if currentNode.position == self.userPos:
                path = []
                node = currentNode
                print("node", node)
                while node:
                    path.append(node.position)
                    node = node.parent
                return path[::-1]
        
            closed.add(tuple(currentNode.position))
            
            for neighborPos in self.getNeighbors(currentNode.position):
                if tuple(neighborPos) in closed:
                    continue
                gScore = currentNode.gScore + 1
                hScore = self.manhattan(neighborPos,self.userPos)
                fScore = gScore + hScore
                
                neighborNode = Node(neighborPos,gScore,hScore,parent = currentNode)
                
                if neighborPos not in frontier:
                    heapq.heappush(frontier,neighborNode)
                elif neighborNode.fScore < frontier[frontier.index(neighborNode)].fScore:
                    frontier.remove(neighborNode)
                    heapq.heappush(frontier,neighborNode)
                
        return None
            
                
                   