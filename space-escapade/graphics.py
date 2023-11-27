# draw start screen
# draw the game -- game map, power-ups
# draw pause screen
# draw game over screen  

from cmu_graphics import *
import random
import heapq
import numpy as np
    
def drawStartScreen(app):
    drawLabel('SPACE ESCAPADE', app.width/2, app.height/2-app.height/6, size=80, font='orbitron', bold=True)
    drawLabel(f'highscore: {app.highscore}', app.width/2, app.height/2, size=45, font='orbitron')
    drawLabel('new game', app.width/2, app.height/2+app.height/5, size=60, font='orbitron')
    drawRect(app.width/2, app.height/2+app.height/5, 350, 100, align='center', fill=None, border='black')

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
                drawCircle(xindex,yindex,8,fill='khaki')
            elif powers[i] == 'plasmaBeam':
                drawCircle(xindex,yindex,8,fill='purple')
            elif powers[i] == 'freeze':
                drawCircle(xindex,yindex,8,fill='lightBlue')
 
 
# POWER UPS

def drawNuke(app):
    for nuke in app.currentNukes:
        nukeRow = nuke[0]
        nukeCol = nuke[1]
        xindex = 10 + (nukeCol - app.screenTopLeftIndex[1]) * 10
        yindex = 10 + (nukeRow - app.screenTopLeftIndex[0]) * 10
        drawCircle(xindex,yindex,150,fill='orange',opacity=60)
    
    
#def drawMissiles():
    
#def drawPlasmaBeam():
    
#def drawFreeze():

