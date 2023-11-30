from cmu_graphics import *
from map_generation import Map

# ------------------------------------------------------------------------------
#                   File to Test Functionality of Map Generation
# ------------------------------------------------------------------------------    

def onAppStart(app):
    app.setMaxShapeCount(200000)
    app.rows = 100
    app.cols = 150
    app.boardHeight = 900
    app.boardWidth = 1350
    app.height = 1000
    app.width = 1500

    app.cellHeight = app.boardHeight/app.rows
    app.cellWidth = app.boardWidth/app.cols

    
    mapgen = Map(app.rows, app.cols)
    app.map = mapgen.generateFinal()


def redrawAll(app):
    drawMap(app)


def drawMap(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.map[row][col]:
                drawCell(app, row, col, 'black')
            else:
                drawCell(app, row, col, 'white')


def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellTopLeft(app, row, col)
    drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight,
             fill=color)
    
def getCellTopLeft(app, row, col):
    cx = col * app.cellWidth
    cy = row * app.cellHeight
    return (cx, cy)

def main():
    runApp()

main()