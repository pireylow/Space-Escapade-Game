# handles user input (controller) and calls game.py (model) and graphics.py (view)
# mouse drag, mouse press, key press, key hold

from cmu_graphics import *
import random
import heapq
import numpy as np

import game
import graphics
import pathfinding
import map_generation

def onAppStart(app):
    reset(app)
    app.highscore = 0
    
def reset(app):
    app.cx = 750
    app.cy = 530
    app.r = 10
    app.height = 1000
    app.width = 1500
    app.startScreen = True
    app.paused = False
    app.gameOver = False
    app.game = False
    app.score = 0
    
    app.rows = 100
    app.cols = 150
    app.extra = 10
    initializeMap(app.rows,app.cols,app.extra)
    
def initializeMap(rows,cols,extra):
    app.map = map_generation.Map(rows,cols,extra).generateFinal()
    # convert map to image to be moved around

    
def redrawAll(app):
    if app.startScreen:
        graphics.drawStartScreen(app)
    elif app.gameOver:
        graphics.drawGameOverScreen(app)
    else:
        graphics.drawGame(app)
        if app.paused:
            graphics.drawPauseScreen(app)
    

'''     
def onStep(app):
    if app.game:
        game.Enemies.move()
'''
    
def onMouseDrag(app,mouseX,mouseY):
    if app.game and game.distance(mouseX,mouseY,app.cx,app.cy) <= 10:
        if (20+app.r) <= app.cx <= (app.width-app.r-20) and (80+app.r) <= app.cy <= (app.height-app.r-20):
            app.cx, app.cy = mouseX, mouseY
    
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
        d = 2
        if 'w' in keys or 'up' in keys:
            game.User.position[2] -= d
        if 'a' in keys or 'left' in keys:
            game.User.position[1] -= d
        if 's' in keys or 'down' in keys:
            game.User.position[2] += d
        if 'd' in keys or 'right' in keys:
            game.User.position[1] += d

def main():
    runApp()

main()