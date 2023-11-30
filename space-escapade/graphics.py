from cmu_graphics import *
from PIL import Image
import random
import heapq

# ------------------------------------------------------------------------------
#                              Draw Screens
# ------------------------------------------------------------------------------    
    
def drawStartScreen(app):
    drawLabel('SPACE ESCAPADE', app.width/2, app.height/2-app.height/6, size=80, font='orbitron', bold=True, fill='white')
    drawLabel(f'highscore: {app.highscore}', app.width/2, app.height/2, size=45, font='orbitron',fill='white')
    drawLabel('new game', app.width/2, app.height/2+app.height/5, size=60, font='orbitron',fill='white')
    drawRect(app.width/2, app.height/2+app.height/5, 350, 100, align='center', fill=None, border='white')

def drawPauseScreen(app):
    drawRect(0,0,app.width,app.height,fill='white',opacity=90)
    drawLabel('paused',app.width/2,app.height/2-app.height/6,size=80,font='orbitron',bold=True)        
    
    greenPlay = rgb(74, 194, 140)
    drawRect(app.width/2-app.width/8,app.height/2+app.height/8, 100, 100, fill=greenPlay,align='center')
    drawLabel("play",app.width/2-app.width/8,app.height/2+app.height/8,size=30,font='orbitron', fill='white')
    
    drawRect(app.width/2+app.width/8,app.height/2+app.height/8, 100, 100, fill='red',align='center')
    drawLabel("quit",app.width/2+app.width/8,app.height/2+app.height/8,size=30,font='orbitron', fill='white')

def drawGameOverScreen(app):
    drawRect(app.width/2, app.height/2-app.height/6,600,300,fill='red',align='center')
    drawLabel("game over :'(", app.width/2, app.height/2-app.height/4,fill='white',font='orbitron',size=75)
    drawLabel(f'score: {app.score}', app.width/2, app.height/2-app.height/7,fill='white',font='orbitron',size=45)
    drawLabel(f'highscore: {app.highscore}', app.width/2, app.height/2-app.height/11,fill='white',font='orbitron',size=45)
    
    newGame = rgb(74, 194, 140)
    drawRect(app.width/2, app.height/2+app.height/5, 350, 100, align='center', fill=newGame)
    drawLabel('new game', app.width/2, app.height/2+app.height/5, size=60, font='orbitron',fill='white')
    
def drawGame(app):
    score = rgb(74, 194, 140)
    drawRect(120,30,240,60,align='center',fill=score)
    drawLabel(f'score: {app.score}',100,30,align='center',size=36,font='orbitron')
    drawRect(app.width-10,10,55,60,align='top-right',fill='white')
    drawRect(app.width-20,20,15,40,align='top-right')
    drawRect(app.width-40,20,15,40,align='top-right')
    
# ------------------------------------------------------------------------------
#                     Draw Enemies and Power-Ups Objects
# ------------------------------------------------------------------------------     
    
def drawEnemies(positions,topLeftIndex):
    for position in positions:
        erow = position[0]
        ecol = position[1]
        if (topLeftIndex[0] < erow < topLeftIndex[0] + 99 and 
            topLeftIndex[1] < ecol < topLeftIndex[1] + 149):
            xindex = 10 + (ecol - topLeftIndex[1]) * 10
            yindex = 10 + (erow - topLeftIndex[0]) * 10
            drawCircle(xindex,yindex,5,fill='red')
            
def drawPowers(positions,powers,topLeftIndex):
    for i in range(len(positions)):
        prow = positions[i][0]
        pcol = positions[i][1]
        if (topLeftIndex[0] < prow < topLeftIndex[0] + 99 and 
            topLeftIndex[1] < pcol < topLeftIndex[1] + 149):
            xindex = 10 + (pcol - topLeftIndex[1]) * 10
            yindex = 10 + (prow - topLeftIndex[0]) * 10
            if powers[i] == 'nuke':
                drawCircle(xindex,yindex,8,fill='orange')
            elif powers[i] == 'missiles':
                drawCircle(xindex,yindex,8,fill='yellow')
            elif powers[i] == 'plasmaBeam':
                drawCircle(xindex,yindex,8,fill='purple')
            elif powers[i] == 'freeze':
                drawCircle(xindex,yindex,8,fill='lightBlue')
 
 
# ------------------------------------------------------------------------------
#                           Draw Power-Ups Events
# ------------------------------------------------------------------------------    

def drawNuke(app):
    for nuke in app.currentNukes:
        nukeRow = nuke[0]
        nukeCol = nuke[1]
        xindex = 10 + (nukeCol - app.screenTopLeftIndex[1]) * 10
        yindex = 10 + (nukeRow - app.screenTopLeftIndex[0]) * 10
        drawImage(app.explosionImage,xindex,yindex,width=400,height=400,opacity=60,align='center')
        
def drawPlasmaBeam(app):
    for plasmaBeam in range(len(app.currentPlasmaBeams)):
        if app.plasmaBeamTimes[plasmaBeam] >= 20:
            plasmaBeamRow = app.currentPlasmaBeams[plasmaBeam][0]
            plasmaBeamCol = app.currentPlasmaBeams[plasmaBeam][1]
            xindex = 10 + (plasmaBeamCol - app.screenTopLeftIndex[1]) * 10
            yindex = 10 + (plasmaBeamRow - app.screenTopLeftIndex[0]) * 10
            plasmaBeamAngle = app.plasmaBeamAngle[plasmaBeam]
            drawImage(app.plasmaBeamImage,xindex,yindex,width=360,height=240,opacity=60,align='center',rotateAngle=plasmaBeamAngle)
    
def drawMissiles(app):
    for missiles in range(len(app.missilesCurrent)):
        if app.missilesTimes[missiles] < 150:
            missilesRow = app.missilesCurrent[missiles][0]
            missilesCol = app.missilesCurrent[missiles][1]
            originRow = app.missilesOrigin[missiles][0]
            originCol = app.missilesOrigin[missiles][1]
            startx = 10 + (originCol - app.screenTopLeftIndex[1]) * 10
            starty = 10 + (originRow - app.screenTopLeftIndex[0]) * 10
            endx = 10 + (missilesCol - app.screenTopLeftIndex[1]) * 10
            endy = 10 + (missilesRow - app.screenTopLeftIndex[0]) * 10
            drawLine(startx,starty,endx,endy,arrowEnd=True,lineWidth=3,fill='yellow')
                  
def drawMissilesExplosion(app):
    for explosion in range(len(app.missilesExplosion)):
        explosionRow = app.missilesExplosion[explosion][0]
        explosionCol = app.missilesExplosion[explosion][1]
        cx = 10 + (explosionCol - app.screenTopLeftIndex[1]) * 10
        cy = 10 + (explosionRow - app.screenTopLeftIndex[0]) * 10
        drawImage(app.explosionImage,cx,cy,width=270,height=270,opacity=60,align='center')
    
def drawFreeze(app):
    for freeze in range(len(app.currentFreezes)):
        freezeRow = app.currentFreezes[freeze][0]
        freezeCol = app.currentFreezes[freeze][1]
        cx = 10 + (freezeCol - app.screenTopLeftIndex[1]) * 10
        cy = 10 + (freezeRow - app.screenTopLeftIndex[0]) * 10
        drawImage(app.freezeImage,cx,cy,width=450,height=450,opacity=60,align='center')

def drawFrozenEnemies(app):
    for frozen in range(len(app.frozenEnemies)):
        frozenRow = app.frozenEnemies[frozen][0]
        frozenCol = app.frozenEnemies[frozen][1]
        cx = 10 + (frozenCol - app.screenTopLeftIndex[1]) * 10
        cy = 10 + (frozenRow - app.screenTopLeftIndex[0]) * 10
        drawRect(cx,cy,18,18,fill='lightBlue',opacity=60,align='center',rotateAngle=45)
        drawCircle(cx,cy,5,fill='red')