# handles user input (controller) and calls game.py (model) and graphics.py (view)
# mouse drag, mouse press, key press, key hold

from cmu_graphics import *
import random
import heapq
import numpy as np

import game
import graphics
import pathfinding

def onAppStart(app):
    reset(app)
    app.highscore = 0
    
def reset(app):
    app.height = 1000
    app.width = 1500
    app.startScreen = True
    app.paused = False
    app.gameOver = False
    app.game = False
    app.score = 0

    
def redrawAll(app):
    if app.startScreen:
        drawStartScreen(app)
    elif app.paused:
        drawPauseScreen(app)
    elif app.gameOver:
        drawGameOverScreen(app)
    else:
        drawGame(app)
    
    
def drawStartScreen(app):
    pass       

def drawPauseScreen(app):
    pass

def drawGameOverScreen(app):
    pass

def drawGame(app):
    pass
        
        
def onStep(app):
    if app.game:
        game.Enemies.move()
    
def onMouseDrag(app,mouseX,mouseY):
    if app.game:
        game.User.position = (mouseX,mouseY)
    
def onMousePress(app,mouseX,mouseY):
    if app.startScreen:
        if insideStartGameButton:
            app.startScreen = not app.startScreen
            app.game = not app.game
            startGame()
    elif app.paused:
        if insideResumeButton or insideTopPlayButton:
            app.paused = not app.paused
            app.game = not app.game
        elif insideQuitButton:
            app.startScreen = not app.startScreen
            app.paused = not app.paused
    elif app.gameOver:
        if insideNewGameButton:
            reset(app)
    else:
        if insidePauseButton:
            app.paused = not app.paused
            app.game = not app.game
    
def onKeyPress(app,key):
    if app.startScreen:
        if key in ['space','enter','p']:
            app.startScreen = not app.startScreen
            app.game = not app.game
            startGame()
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
        if 'w' in keys or 'up' in keys:
            game.User.position[2] -= 2
        if 'a' in keys or 'left' in keys:
            game.User.position[1] -= 2
        if 's' in keys or 'down' in keys:
            game.User.position[2] += 2
        if 'd' in keys or 'right' in keys:
            game.User.position[1] += 2

def main():
    runApp()

main()