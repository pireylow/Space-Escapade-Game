from cmu_graphics import *
from map_generation import Map

def onAppStart(app):
    app.setMaxShapeCount(200000)
    app.mapRows = 100
    app.mapCols = 150
    app.boardTop = 100
    app.boardLeft = 20
    app.boardHeight = 900
    app.boardWidth = 1400

    app.mapCellHeight = app.boardHeight/app.mapRows
    app.mapCellWidth = app.boardWidth/app.mapCols

    
    mapgen = Map(app.mapRows, app.mapCols)
    app.map = mapgen.generateFinal()


def redrawAll(app):
    drawBoard(app)


def drawBoard(app):
    for row in range(app.mapRows):
        for col in range(app.mapCols):
            if app.map[row][col]:
                drawCell(app, row, col, 'black')
            else:
                drawCell(app, row, col, 'white')


def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    drawRect(cellLeft, cellTop, app.mapCellWidth, app.mapCellHeight,
             fill=color)
    
def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.mapCellWidth
    cellTop = app.boardTop + row * app.mapCellHeight
    return (cellLeft, cellTop)

def main():
    runApp()

main()