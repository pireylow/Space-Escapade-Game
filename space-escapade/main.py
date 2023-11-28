# handles user input (controller) and calls game.py (model) and graphics.py (view)
# mouse drag, mouse press, key press, key hold

from cmu_graphics import *
import random
import heapq
import numpy as np
from PIL import Image, ImageDraw
import os, pathlib
import copy

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
    app.userDirection = [0,0]
    app.userAngle = findUserAngle(app)
    
    app.enemies = game.Enemies()
    app.powers = game.PowerUps()
    
    app.currentNukes = []
    app.nukeTimes = []
    app.nukeKillCount = []
    
    app.currentPlasmaBeams = []
    app.plasmaBeamDirections = []
    app.plasmaBeamTimes = []
    app.plasmaBeamKillCount = []
    
    app.missilesCurrent = []
    app.missilesMovement = []
    app.missilesOrigin = []
    app.missilesKillCount = []
    app.missilesTimes = []
    app.missilesExplosionTime = []
    app.missilesExplosion = []

    app.currentFreezes = []
    app.freezeTimes = []
    
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
        drawLine(app.cx,app.cy+app.r,app.cx,app.cy-app.r,lineWidth=5,arrowEnd=True,fill='green',rotateAngle=app.userAngle)
        
        graphics.drawPowers(app.powers.positions,app.powers.power,app.screenTopLeftIndex)
        graphics.drawEnemies(app.enemies.positions,app.screenTopLeftIndex)

        graphics.drawGame(app)
        graphics.drawNuke(app)
        graphics.drawPlasmaBeam(app)
        graphics.drawMissiles(app)
        graphics.drawMissilesExplosion(app)
        
        if app.paused:
            graphics.drawPauseScreen(app)
    


def onStep(app):
    if app.game:
        app.timeCounter += 1
        
        # nuke
        app.powers.nukeKill(app.enemies.positions,app.currentNukes,app.nukeKillCount)
        nukeEvents(app)
                
        # plasmaBeam
        for i in range(len(app.plasmaBeamTimes)):
            app.plasmaBeamTimes[i]+=1
            if app.plasmaBeamTimes[i] >= 20:
                if len(app.currentPlasmaBeams) < len(app.plasmaBeamTimes):
                    app.currentPlasmaBeams.append(copy.copy(app.userTopLeft))
                if len(app.plasmaBeamDirections)<len(app.plasmaBeamTimes):
                    app.plasmaBeamDirections.append(copy.copy(app.userDirection))
                app.powers.plasmaBeamKill(app.enemies.positions,app.currentPlasmaBeams,app.plasmaBeamKillCount)
                app.powers.plasmaBeamMove(app.currentPlasmaBeams,app.plasmaBeamDirections)
                plasmaBeamOut(app)
                
        # missiles
        missilesEvent(app)
        missilesExplosionEvent(app)
                
        # freeze
        for i in range(len(app.freezeTimes)):
            app.freezeTimes[i]+=1
            if app.freezeTimes[i] == 60:
                app.freezeTimes.pop(i)
                app.currentFreezes.pop(i)
                
                
        # others       
        if app.timeCounter%10==0:
            app.enemies.add(app.map,app.screenTopLeftIndex,app.userTopLeft)
            app.enemies.move(app.map,app.userTopLeft)
            app.enemies.checkEnemyCollision(app.userTopLeft)
            app.powers.add(app.map,app.screenTopLeftIndex,app.userTopLeft)
            
            pos, power = app.powers.checkPowerCollision(app.userTopLeft)
            if power == 'nuke':
                app.powers.nuke(pos,app.currentNukes,app.nukeTimes,app.nukeKillCount)
              
            elif power == 'plasmaBeam':
                app.powers.plasmaBeam(app.plasmaBeamKillCount,app.plasmaBeamTimes) 
                  
            elif power == 'missiles':
                app.powers.missiles(app.missilesMovement,app.missilesOrigin,app.missilesCurrent,pos,app.missilesKillCount,app.missilesTimes)

            # elif power == 'freeze':
            #     game.freeze()
                
        if app.timeCounter%60==0:
            app.powers.move(app.map,app.userTopLeft)
            
def nukeEvents(app):
    i=0
    while i < len(app.nukeTimes):
        app.nukeTimes[i]+=1
        if app.nukeTimes[i] == 90:
            app.nukeTimes.pop(i)
            app.currentNukes.pop(i)
            app.score += app.nukeKillCount[i] ** 2
            app.nukeKillCount.pop(i)
        else:
            i+=1
            
def plasmaBeamOut(app):
    i=0
    while i < len(app.currentPlasmaBeams):
        if (app.currentPlasmaBeams[i][0] + app.plasmaBeamDirections[i][0] <= 1 
            or app.currentPlasmaBeams[i][0] + app.plasmaBeamDirections[i][0] >= len(app.map)-1
            or app.currentPlasmaBeams[i][1] + app.plasmaBeamDirections[i][1] <= 1
            or app.currentPlasmaBeams[i][1] + app.plasmaBeamDirections[i][1] >= len(app.map)-1
            or app.screenTopLeftIndex[0]-app.currentPlasmaBeams[i][0] >= 200
            or app.screenTopLeftIndex[1]-app.currentPlasmaBeams[i][1] >= 200
            or app.currentPlasmaBeams[i][0]-app.screenTopLeftIndex[0] >= 300
            or app.currentPlasmaBeams[i][0]-app.screenTopLeftIndex[0] >= 350):
            app.currentPlasmaBeams.pop(i)
            app.plasmaBeamDirections.pop(i)
            app.plasmaBeamTimes.pop(i)
            app.score += app.plasmaBeamKillCount[i] ** 2
            app.plasmaBeamKillCount.pop(i)
        else:
            i+=1
 
def missilesEvent(app):
    i=0
    while i < len(app.missilesTimes):
        app.missilesTimes[i]+=1
        if app.missilesTimes[i] == 151:
            
            app.missilesExplosion.append(copy.copy(app.missilesCurrent.pop(i)))
            app.missilesTimes.pop(i)
            app.missilesOrigin.pop(i)
            app.missilesMovement.pop(i)
            app.missilesExplosionTime.append(0)
            
        else:
            if app.timeCounter%10==0:
                app.powers.missilesMove(i,app.missilesCurrent,app.missilesMovement)
            i+=1
            
def missilesExplosionEvent(app):
    i=0
    while i<len(app.missilesExplosionTime):
        app.missilesExplosionTime[i]+=1

        app.powers.missilesKill(app.enemies.positions,app.missilesExplosion,app.missilesKillCount)
        if len(app.missilesExplosion)==0:
            app.score += app.missilesKillCount[0] ** 2
            app.missilesKillCount.pop(0)
        
        if app.missilesExplosionTime[i]==45:
            app.missilesExplosion.pop(i)
            app.missilesExplosionTime.pop(i)
        else:
            i+=1
            
    
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
        if 'w' in keys: # check above
            if checkAbove(app):
                app.mapy += d
                app.screenTopLeftIndex[0] -= indexd
                app.userTopLeft[0] -= indexd
        if 'a' in keys: # check left
            if checkLeft(app):
                app.mapx += d
                app.screenTopLeftIndex[1] -= indexd
                app.userTopLeft[1] -= indexd
        if 's' in keys: # check below
            if checkBelow(app):
                app.mapy -= d
                app.screenTopLeftIndex[0] += indexd
                app.userTopLeft[0] += indexd
        if 'd' in keys: # check right
            if checkRight(app):
                app.mapx -= d
                app.screenTopLeftIndex[1] += indexd
                app.userTopLeft[1] += indexd
                
        if 'w' in keys and 's' not in keys:
            app.userDirection[0] = -1
        elif 's' in keys and 'w' not in keys:
            app.userDirection[0] = 1
        else:
            app.userDirection[0] = 0
            
        if 'a' in keys and 'd' not in keys:
            app.userDirection[1] = -1
        elif 'd' in keys and 'a' not in keys:
            app.userDirection[1] = 1
        else:
            app.userDirection[1] = 0
            
        app.userAngle = findUserAngle(app)
        
def findUserAngle(app):
    if app.userDirection == [0,0] or app.userDirection == [-1,0]:
        return 0
    elif app.userDirection == [-1,1]:
        return 45
    elif app.userDirection == [0,1]:
        return 90
    elif app.userDirection == [1,1]:
        return 135
    elif app.userDirection == [1,0]:
        return 180
    elif app.userDirection == [1,-1]:
        return 225
    elif app.userDirection == [0,-1]:
        return 270
    elif app.userDirection == [-1,-1]:
        return 315
        


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