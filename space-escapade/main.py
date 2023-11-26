# handles user input (controller) and calls game.py (model) and graphics.py (view)
# mouse drag, mouse press, key press, key hold

from cmu_graphics import *
import random
import heapq
import numpy as np
from PIL import Image, ImageDraw
import os, pathlib

import game
import graphics
import pathfinding
import map_generation

def onAppStart(app):
    reset(app)
    app.highscore = 0
    
def reset(app):
    app.r = 10
    app.height = 1000
    app.width = 1500
    app.startScreen = True
    app.paused = False
    app.gameOver = False
    app.game = False
    app.score = 0
    app.timeCounter = 0
    
    app.cx = app.width/2
    app.cy = app.height/2
    app.mapx = app.width/2
    app.mapy = app.height/2
    app.sizeX = app.width
    app.sizeY = app.height
    app.rows = 100
    app.cols = 150
    app.extra = 10
    initializeMap(app,app.rows,app.cols,app.extra)
    app.map = expandMap(app.map)
    app.originalTopLeft = (len(app.map)//2-1, len(app.map[0])//2-1)
    app.userTopLeft = [int(app.originalTopLeft[0]-(app.mapy - app.cy)//10),int(app.originalTopLeft[1]-(app.mapx - app.cx)//10)]
    app.screenTopLeftIndex = [len(app.map)//2-100//2, len(app.map[0])//2-150//2]
    
    app.enemies = game.Enemies()
    
def initializeMap(app,rows,cols,extra):
    app.map = map_generation.Map(rows,cols,extra).generateFinal()
    while (app.map[len(app.map)//2-1][len(app.map[0])//2-1] or
           app.map[len(app.map)//2][len(app.map[0])//2] or 
           app.map[len(app.map)//2-1][len(app.map[0])//2] or 
           app.map[len(app.map)//2][len(app.map[0])//2-1]):
        app.map = map_generation.Map(rows,cols,extra).generateFinal()
    getMapImage(app.map)
    app.mapImage = Image.open("map.png")
    app.imageWidth,app.imageHeight = app.mapImage.width,app.mapImage.height
    app.mapImage = CMUImage(app.mapImage)
    
def getMapImage(map):
    mapHeight = len(map)
    mapWidth = len(map[0])
    image = Image.new('RGB', (mapWidth*50, mapHeight*50), color='white')
    wallColor = (0, 0, 0)   #black
    draw = ImageDraw.Draw(image)
    for y, row in enumerate(map):
        for x, value in enumerate(row):
            if value:
                draw.rectangle([(x*50, y*50), ((x + 1)*50, (y + 1)*50)], fill=wallColor)
    image.save('map.png')
    
def expandMap(map):
    expanded = []
    for row in map:
        rowList = []
        for val in row:
            for _ in range(10):
                rowList.append(val)
        for _ in range(10):
            expanded.append(rowList[:])
    return expanded
                

def redrawAll(app):
    if app.startScreen:
        graphics.drawStartScreen(app)
    elif app.gameOver:
        graphics.drawGameOverScreen(app)
    else:
        drawImage(app.mapImage,app.mapx,app.mapy,width=app.sizeX*10,height=app.sizeY*10,align='center')
        drawCircle(app.cx,app.cy,app.r,fill='green')
        drawEnemies(app.enemies.positions,app.screenTopLeftIndex)
        graphics.drawGame(app)
        if app.paused:
            graphics.drawPauseScreen(app)
    
def drawEnemies(positions,topLeftIndex):
    for position in positions:
        erow = position[0]
        ecol = position[1]
        if (topLeftIndex[0] < erow < topLeftIndex[0] + 99 and 
            topLeftIndex[1] < ecol < topLeftIndex[1] + 149):
            xindex = 10 + (ecol - topLeftIndex[1]) * 10
            yindex = 10 + (erow - topLeftIndex[0]) * 10
            drawCircle(xindex,yindex,5,fill='red')
 

def onStep(app):
    if app.game:
        app.timeCounter+=1
        if app.timeCounter%150==0:
            app.enemies.add(app.screenTopLeftIndex,app.userTopLeft)
            app.enemies.move(app.map,app.userTopLeft)


    
def onMousePress(app,mouseX,mouseY):
    if app.startScreen:
        if 575<=mouseX<=925 and (app.height/2+app.height/5-50) <=mouseY<= (app.height/2+app.height/5+50):   #insideStartGameButton
            app.startScreen = not app.startScreen
            app.game = not app.game
            #startGame()
    elif app.paused:
        if 512.5<=mouseX<=612.5 and (app.height/2+app.height/8-50) <=mouseY<= (app.height/2+app.height/8+50):   #insideResumeButton
            app.paused = not app.paused
            app.game = not app.game
        elif 887.5<=mouseX<=987.5 and (app.height/2+app.height/8-50) <=mouseY<= (app.height/2+app.height/8+50):   #insideQuitButton
            app.startScreen = not app.startScreen
            app.paused = not app.paused
    elif app.gameOver:
        if 575<=mouseX<=925 and (app.height/2+app.height/5-50) <=mouseY<= (app.height/2+app.height/5+50):   #insideNewGameButton
            reset(app)
    else:
        if app.width-55<=mouseX<=app.width-20 and 20<=mouseY<=60:   #insidePauseButton:
            app.paused = not app.paused
            app.game = not app.game
    
def onKeyPress(app,key):
    if app.startScreen:
        if key in ['space','enter','p']:
            app.startScreen = not app.startScreen
            app.game = not app.game
            #startGame()
    elif app.paused:
        if key in ['space','p']:
            app.paused = not app.paused
            app.game = not app.game
    elif app.gameOver:
        if key in ['space','n','r']:
            reset(app)
    else:
        if key in ['space','p']:
            app.paused = not app.paused
            app.game = not app.game
    
def onKeyHold(app,keys):
    if app.game:
        d = 5
        indexd = 0.5
        if 'w' in keys or 'up' in keys: # check above
            if checkAbove(app):
                app.mapy += d
                app.screenTopLeftIndex[0] -= indexd
        if 'a' in keys or 'left' in keys: # check left
            if checkLeft(app):
                app.mapx += d
                app.screenTopLeftIndex[1] -= indexd
        if 's' in keys or 'down' in keys: # check below
            if checkBelow(app):
                app.mapy -= d
                app.screenTopLeftIndex[0] += indexd
        if 'd' in keys or 'right' in keys: # check right
            if checkRight(app):
                app.mapx -= d
                app.screenTopLeftIndex[1] += indexd


def checkAbove(app):
    dx = app.mapx - app.cx
    dy = app.mapy - app.cy
    if dy % 10 != 0:
        return True
    if dx % 10 == 0:
        if (app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10)] or 
            app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10+1)]):
            return False
        return True
    else:
        if (app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10-1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10)] or 
            app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10+1)]):
            return False
        return True

def checkLeft(app):
    dx = app.mapx - app.cx
    dy = app.mapy - app.cy
    if dx % 10 != 0:
        return True
    if dy % 10 == 0:
        if (app.map[int(app.originalTopLeft[0]-dy//10)][int(app.originalTopLeft[1]-dx//10-1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10-1)]):
            return False
        return True
    else:
        if (app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10-1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10)][int(app.originalTopLeft[1]-dx//10-1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10-1)]):
            return False
        return True

def checkBelow(app):
    dx = app.mapx - app.cx
    dy = app.mapy - app.cy
    if dy % 10 != 0:
        return True
    if dx % 10 == 0:
        if (app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10+1)]):
            return False
        return True
    else:
        if (app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10-1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10+1)]):
            return False
        return True


def checkRight(app):
    dx = app.mapx - app.cx
    dy = app.mapy - app.cy
    if dx % 10 != 0:
        return True
    if dy % 10 == 0:
        if (app.map[int(app.originalTopLeft[0]-dy//10)][int(app.originalTopLeft[1]-dx//10+1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10+1)]):
            return False
        return True
    else:
        if (app.map[int(app.originalTopLeft[0]-dy//10-1)][int(app.originalTopLeft[1]-dx//10+1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10)][int(app.originalTopLeft[1]-dx//10+1)] or 
            app.map[int(app.originalTopLeft[0]-dy//10+1)][int(app.originalTopLeft[1]-dx//10+1)]):
            return False
        return True

def main():
    runApp()

main()