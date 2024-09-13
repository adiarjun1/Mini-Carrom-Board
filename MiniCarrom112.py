####################################################################
#########################     Imports         ######################
####################################################################
from cmu_graphics import *
import math

####################################################################
#########################     Classes         ######################
####################################################################
class Striker:
    def __init__(self, cx, cy, dx=0, dy=0):
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.radius = 20

class Piece:
    def __init__(self, cx, cy, dx=0, dy=0, color=""):
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = 15

class Slider:
    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy

####################################################################
#################    App Starting Variables    #####################
####################################################################
def onAppStart(app):
    newGame(app)

def newGame(app):
    app.score1 = 0
    app.score2 = 0
    app.boardWidth = 450
    app.boardHeight = 450
    app.selected = False
    app.lineStartLocation = None
    app.lineEndLocation = None
    app.stepsPerSecond = 100
    app.turn = 1
    app.width = 600
    app.height = 600

    # Initialize Striker and Pieces
    app.slider = Slider(app.width / 2, app.height / 1.07)
    app.striker = Striker(app.width / 2, 450)
    
    app.pieces = [
        Piece(375, 300, color="blue"),
        Piece(225, 300, color="blue"),
        Piece(300, 375, color="red"),
        Piece(300, 225, color="red"),
        Piece(300, 300, color="green")
    ]
    
    app.background = 'beige'

####################################################################
#########################    RedrawAll         #####################
####################################################################
def drawBoard(app):
    drawRect(app.width / 2, app.height / 2, app.boardWidth + 30, app.boardHeight + 30, 
             align='center', fill='brown', border='black', borderWidth=2)
    drawRect(app.width / 2, app.height / 2, app.boardWidth, app.boardHeight, 
             align='center', fill='beige', border='black', borderWidth=2)
    
    for corner in [(app.width / 6.15, app.width / 6.15), 
                   (app.width / 1.2, app.width / 6.15), 
                   (app.width / 6.15, app.width / 1.2), 
                   (app.width / 1.2, app.width / 1.2)]:
        drawCircle(*corner, app.width / 26.67, fill=None, border='black')
    
    drawLine(app.width / 4, app.width * 0.75, app.width * 0.75, app.width * 0.75)
    drawLine(app.width / 4, app.width / 4, app.width * 0.75, app.width / 4)

def drawScore(app):
    drawLabel(f'Player 1 (Red)', 5, 5, align='left-top', size=20)
    drawLabel(f'Score: {app.score1}', 5, 25, align='left-top', size=20)
    drawLabel(f'Player 2 (Blue)', app.width - 5, 5, align='right-top', size=20)
    drawLabel(f'Score: {app.score2}', app.width - 5, 25, align='right-top', size=20)

def drawSlider(app):
    drawRect(app.width / 4, app.width / 1.1, app.width / 2, app.width / 20, fill='white', border='black')
    drawCircle(app.slider.cx, app.slider.cy, app.width / 45, fill='grey')

def drawPiecesAndStriker(app):
    drawCircle(app.striker.cx, app.striker.cy, app.striker.radius, fill='black')
    for piece in app.pieces:
        drawCircle(piece.cx, piece.cy, piece.radius, fill=piece.color, border='black')

def drawTurnLabel(app):
    turn = "Player 1's Turn" if app.turn == 1 else "Player 2's Turn"
    drawLabel(turn, app.width / 2, app.height / 18, size=30)

def drawBackButton(app):
    drawLabel("<- Back", 5, app.height - 5, align='left-bottom', size=20)
    drawRect(0, app.height, 80, 30, align="left-bottom", fill=None, border='black')

def playerTurnRedrawAll(app):
    drawBackButton(app)
    drawBoard(app)
    drawScore(app)
    drawTurnLabel(app)
    drawSlider(app)
    drawPiecesAndStriker(app)

    if app.selected and app.lineEndLocation:
        drawLine(*app.lineStartLocation, *app.lineEndLocation, dashes=True)

####################################################################
##################     Mouse Events           ######################
####################################################################
def handleMousePress(app, mouseX, mouseY):
    x, y = app.striker.cx, app.striker.cy
    
    if x - 15 < mouseX < x + 15 and y - 15 < mouseY < y + 15:
        app.tryingToDrawALine = True
        app.tryingToSlide = False
        app.lineStartLocation = (x, y)
        app.lineEndLocation = None
        if distance(mouseX, mouseY, x, y) < 15:
            app.selected = True
    elif app.slider.cx - 10 < mouseX < app.slider.cx + 10 and app.slider.cy - 10 < mouseY < app.slider.cy + 10:
        app.tryingToSlide = True
        app.tryingToDrawALine = False
    else:
        app.tryingToDrawALine = False
        app.tryingToSlide = False

def handleMouseDrag(app, mouseX, mouseY):
    if app.tryingToDrawALine:
        app.lineEndLocation = (mouseX, mouseY)
    elif app.tryingToSlide and app.width / 4 < mouseX < app.width * 0.75:
        app.slider.cx = mouseX

def handleMouseRelease(app, mouseX, mouseY):
    app.tryingToSlide = False
    if 0 < mouseX < 80 and app.height - 30 < mouseY < app.height:
        setActiveScreen("menu")
    
    if app.tryingToDrawALine:
        if app.lineEndLocation:
            x1, y1 = app.striker.cx, app.striker.cy
            x2, y2 = app.lineEndLocation
            app.striker.dx = (x1 - x2) / 10
            app.striker.dy = (y1 - y2) / 10
            app.turn *= -1
        app.lineEndLocation = None
        app.selected = False

####################################################################
#################    Helper Functions         ######################
####################################################################
def movePiece(piece):
    if abs(piece.dx) < 0.1 and abs(piece.dy) < 0.1:
        piece.dx = 0
        piece.dy = 0

    piece.cx += piece.dx
    piece.cy += piece.dy

    # Boundary checks for both x and y coordinates
    if piece.cx >= 525 - piece.radius:
        piece.cx = 525 - piece.radius
        piece.dx = -piece.dx
    elif piece.cx <= piece.radius + 75:
        piece.cx = piece.radius + 75
        piece.dx = -piece.dx
    
    if piece.cy >= 525 - piece.radius:
        piece.cy = 525 - piece.radius
        piece.dy = -piece.dy
    elif piece.cy <= piece.radius + 75:
        piece.cy = piece.radius + 75
        piece.dy = -piece.dy

    # Apply friction
    piece.dx *= 0.98
    piece.dy *= 0.98

def collide(piece1, piece2):
    x, y = piece1.cx - piece2.cx, piece1.cy - piece2.cy
    c = (x**2 + y**2) ** 0.5
    xRatio, yRatio = x / c, y / c
    
    totalPower = (piece1.dx + piece2.dx + piece1.dy + piece2.dy) / 1.5
    newDx = xRatio * totalPower
    newDy = yRatio * totalPower

    piece1.dx, piece1.dy = -newDx, -newDy
    piece2.dx, piece2.dy = newDx, newDy
