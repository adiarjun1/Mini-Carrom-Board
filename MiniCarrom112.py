####################################################################
#########################     Classes        #######################
####################################################################
#Striker class
class Striker:

    def __init__(self, cx, cy, dx, dy):
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.radius = 20

#piece class
class Piece:

    def __init__(self, cx, cy, dx, dy, color):
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy
        self.color = color
        self.radius = 15

#slider class
class Slider:

    def __init__(self, cx, cy):
        self.cx = cx
        self.cy = cy


####################################################################
#################    App Starting Variables        #################
####################################################################
from cmu_graphics import *
import math

def onAppStart(app):
    newGame(app)

def newGame(app):
    app.score1 = 0
    app.score2 = 0
    app.boardWidth = 450
    app.boardHeight = 450
    app.selected = False
    app.dotLocation = None
    app.lineStartLocation = None
    app.lineEndLocation = None
    app.stepsPerSecond = 100
    app.tryingToDrawALine = True
    app.tryingToSlide = False
    app.turn = 1
    app.width = 600
    app.height = 600
    app.slider = Slider(app.width/2, app.height/1.07)
    app.striker = Striker(app.width/2, 450, 0, 0)
    app.bluePiece1 = Piece(375, 300, 0, 0, "blue")
    app.bluePiece2 = Piece(225, 300, 0, 0, "blue")
    app.redPiece1 = Piece(300, 375, 0, 0, "red")
    app.redPiece2 = Piece(300, 225, 0, 0, "red")
    app.greenPiece = Piece(300, 300, 0, 0, "green")
    app.pieces = [app.bluePiece1, app.bluePiece2, app.redPiece1, app.redPiece2, app.greenPiece]
    app.canCollide = False
    app.player1menuSteps = 0
    app.player2menuSteps = 0
    app.background = 'beige'

####################################################################
#########################     ReDrawAll's       ####################
####################################################################
def menu_redrawAll(app):
    drawLabel("Mini-Carrom-112", app.width/2, app.height/5, size = 50)
    drawLabel("Play Against A Friend", app.width/2, app.height/3, size = 20)
    drawRect(app.width/2, app.height/3, 220, 70, align = 'center', fill = None, border= 'black')
    drawLabel("How to Win:", app.width/2, app.height/2, size = 20)
    drawLabel("Either player most pocket all of their", app.width/2, app.height/2 + 30, size = 20)
    drawLabel("respective colored pieces or pocket the green ball", app.width/2, app.height/2 + 50, size = 20)

def win_redrawAll(app):
    drawLabel("Player 1 Wins!", app.width/2, app.height/4, size = 50)
    drawLabel("Play Again", app.width/2, app.height/2, size = 20)
    drawRect(app.width/2, app.height/2, 200, 100, align = 'center', fill = None, border= 'black')

def lose_redrawAll(app):
    drawLabel("Player 2 Wins!", app.width/2, app.height/4, size = 50)
    drawLabel("Play Again", app.width/2, app.height/2, size = 20)
    drawRect(app.width/2, app.height/2, 200, 100, align = 'center', fill = None, border= 'black')

def player1menu_redrawAll(app):
    drawLabel("Player 1's turn", app.width/2, app.height/4, size = 50)

def player2menu_redrawAll(app):
    drawLabel("Player 2's turn", app.width/2, app.height/4, size = 50)


def player1turn_redrawAll(app):
    #back Button
    drawLabel("<- Back", 5, app.height-5, align = 'left-bottom', size = 20)
    drawRect(0, app.height, 80, 30, align = "left-bottom", fill = None, border = 'black')
    #drawing the board    
    drawLabel(f'Player 1 (Red)', 5, 5, align= 'left-top',  size = 20)
    drawLabel(f'Score: {app.score1}', 5, 25, align= 'left-top',  size = 20)
    drawLabel(f'Player 2 (Blue)', app.width - 5 , 5, align= 'right-top',  size = 20)
    drawLabel(f'Score: {app.score2}', app.width - 5, 25, align= 'right-top',  size = 20)
    drawRect(app.width/2, app.height/2, app.boardWidth + 30 , app.boardHeight + 30 , align = 'center', fill = 'brown', border = 'black',borderWidth = 2)
    drawRect(app.width/2, app.height/2, app.boardWidth, app.boardHeight, align = 'center', fill = 'beige', border = 'black',borderWidth = 2)
    drawCircle(app.width/6.15, app.width/6.15, app.width/26.67, fill = None, border = 'black')
    drawCircle(app.width/1.2, app.width/6.15, app.width/26.67, fill = None, border = 'black')
    drawCircle(app.width/6.15, app.width/1.2, app.width/26.67, fill = None, border = 'black')
    drawCircle(app.width/1.2, app.width/1.2, app.width/26.67, fill = None, border = 'black')
    drawLine(app.width/4, app.width*0.75, app.width*0.75, app.width*0.75)
    drawLine(app.width/4, app.width/4, app.width*0.75, app.width/4)
    #Turns
    drawLabel("Player 1's Turn", app.width/2, app.height/18, size = 30)
    #drawing the slider
    drawRect(app.width/4, app.width/1.1, app.width/2, app.width/20, fill = 'white', border = 'black')
    drawCircle(app.slider.cx, app.slider.cy, app.width/45, fill = 'grey')
    #drawing the striker
    drawCircle(app.striker.cx,app.striker.cy, app.striker.radius, fill = 'black')
    #drawing the pieces
    for piece in app.pieces:
        drawCircle(piece.cx, piece.cy, piece.radius, fill = piece.color, border = 'black')
    #drawing the line
    if app.selected == True and app.lineEndLocation != None:
        x0, y0 = app.lineStartLocation
        x1, y1 = app.lineEndLocation
        drawLine(x0, y0, x1, y1, dashes=True)

def player2turn_redrawAll(app):
    #back Button
    drawLabel("<- Back", 5, app.height-5, align = 'left-bottom', size = 20)
    drawRect(0, app.height, 80, 30, align = "left-bottom", fill = None, border = 'black')
    #drawing the board    
    drawLabel(f'Player 1 (Red)', 5, 5, align= 'left-top',  size = 20)
    drawLabel(f'Score: {app.score1}', 5, 25, align= 'left-top',  size = 20)
    drawLabel(f'Player 2 (Blue)', app.width - 5 , 5, align= 'right-top',  size = 20)
    drawLabel(f'Score: {app.score2}', app.width - 5, 25, align= 'right-top',  size = 20)
    drawRect(app.width/2, app.height/2, app.boardWidth + 30 , app.boardHeight + 30 , align = 'center', fill = 'brown', border = 'black',borderWidth = 2)
    drawRect(app.width/2, app.height/2, app.boardWidth, app.boardHeight, align = 'center', fill = 'beige', border = 'black',borderWidth = 2)
    drawCircle(app.width/6.15, app.width/6.15, app.width/26.67, fill = None, border = 'black')
    drawCircle(app.width/1.2, app.width/6.15, app.width/26.67, fill = None, border = 'black')
    drawCircle(app.width/6.15, app.width/1.2, app.width/26.67, fill = None, border = 'black')
    drawCircle(app.width/1.2, app.width/1.2, app.width/26.67, fill = None, border = 'black')
    drawLine(app.width/4, app.width*0.75, app.width*0.75, app.width*0.75)
    drawLine(app.width/4, app.width/4, app.width*0.75, app.width/4)
    #Turns
    drawLabel("Player 2's Turn", app.width/2, app.height/16, size = 16)
    #drawing the slider
    drawRect(app.width/4, app.width/1.1, app.width/2, app.width/20, fill = "white", border = 'black')
    drawCircle(app.slider.cx, app.slider.cy, app.width/45, fill = 'grey')
    #drawing the striker
    drawCircle(app.striker.cx, app.striker.cy, app.striker.radius, fill = 'black')
    #drawing the pieces
    for piece in app.pieces:
        drawCircle(piece.cx, piece.cy, piece.radius, fill = piece.color, border = 'black')
    #drawing the line
    if app.selected == True and app.lineEndLocation != None:
        x0, y0 = app.lineStartLocation
        x1, y1 = app.lineEndLocation
        drawLine(x0, y0, x1, y1, dashes=True)

####################################################################
##################     Mouse + Key Events       ####################
####################################################################


#quick key shortcuts to get to certain screens
def player1turn_onKeyPress(app, key):
    if key == 'escape':
        setActiveScreen('menu')
    elif key == 'o':
        setActiveScreen('win')
    elif key == 'p':
        setActiveScreen('lose')

def player2turn_onKeyPress(app, key):
    if key == 'escape':
        setActiveScreen('menu')
    elif key == 'o':
        setActiveScreen('win')
    elif key == 'p':
        setActiveScreen('lose')

#mouse releases on menu pages to get back to the game
def menu_onMouseRelease(app, mouseX, mouseY):
    if 190 < mouseX < 410 and 165 < mouseY < 235:
        newGame(app)
        setActiveScreen("player1turn")

def win_onMouseRelease(app, mouseX, mouseY):
    if 175 < mouseX < 375 and 250 < mouseY < 350:
        newGame(app)
        setActiveScreen("player1turn")
    
def lose_onMouseRelease(app, mouseX, mouseY):
    if 175 < mouseX < 375 and 250 < mouseY < 350:
        newGame(app)
        setActiveScreen("player1turn")

def player1turn_onMousePress(app, mouseX, mouseY):
    x = app.striker.cx
    y = app.striker.cy
    if x-15 < mouseX < x+15 and y-15 < mouseY< y+15:
        #How to draw a line: taken from CS academy
        app.tryingToDrawALine = True
        app.tryingToSlide = False
        app.lineStartLocation = (x, y)
        app.lineEndLocation = None
        if distance(mouseX, mouseY, x, y) < 15:
            app.selected = True
    #if the player is accessing the slider
    elif app.slider.cx-10 < mouseX < app.slider.cx+10 and app.slider.cy-10 < mouseY < app.slider.cy+10:
        app.tryingToSlide = True
        app.tryingToDrawALine = False
    else:
        app.tryingToDrawALine = False
        app.tryingToSlide = False

def player1turn_onMouseDrag(app, mouseX, mouseY):
    #taken from CS Academy
    if app.tryingToDrawALine == True:
        app.lineEndLocation = (mouseX, mouseY)
    #updates the striker cx depending on slider cx
    if app.tryingToSlide == True:
        if app.width/4 < mouseX < app.width*0.75 and app.width/1.11< mouseY < app.width/1.025:
            app.slider.cx = mouseX

def player1turn_onMouseRelease(app, mouseX, mouseY):
    app.tryingToSlide = False
    #back button press
    if 0 < mouseX < 80 and 570 < mouseY < 600:
        setActiveScreen("menu")
    x = app.striker.cx
    y = app.striker.cy
    #check if line ends in the striker or above the striker
    if x-15 < mouseX < x+15 and y-15 < mouseY< y+15:
        app.lineEndLocation = None
    elif mouseY < y:
        app.lineEndLocation = None
    #change the dx and dy of the striker depending on the length of the line
    else:
        if app.tryingToDrawALine == True:
            app.tryingToDrawALine = False
            app.selected = False
            if app.lineEndLocation != None:
                x1, y1 = app.striker.cx, app.striker.cy
                x2, y2 = app.lineEndLocation
                app.striker.dx = (x1-x2)/10
                app.striker.dy = (y1-y2)/10
                app.turn = app.turn * -1


##
## player 2 mouse events are exactly the same 
##
def player2turn_onMousePress(app, mouseX, mouseY):
    x = app.striker.cx
    y = app.striker.cy
    if x-15 < mouseX < x+15 and y-15 < mouseY< y+15:
        app.tryingToDrawALine = True
        app.tryingToSlide = False
        app.lineStartLocation = (x, y)
        app.lineEndLocation = None
        if distance(mouseX, mouseY, x, y) < 15:
            app.selected = True
    elif app.slider.cx-10 < mouseX < app.slider.cx+10 and app.slider.cy-10 < mouseY < app.slider.cy+10:
        app.tryingToSlide = True
        app.tryingToDrawALine = False
    else:
        app.tryingToDrawALine = False
        app.tryingToSlide = False

def player2turn_onMouseDrag(app, mouseX, mouseY):
    if app.tryingToDrawALine == True:
        app.lineEndLocation = (mouseX, mouseY)
    if app.tryingToSlide == True:
        if app.width/4 < mouseX < app.width*0.75 and app.width/1.11< mouseY < app.width/1.025:
            app.slider.cx = mouseX

def player2turn_onMouseRelease(app, mouseX, mouseY):
    app.tryingToSlide = False
    if 0 < mouseX < 80 and 570 < mouseY < 600:
        setActiveScreen("menu")
    x = app.striker.cx
    y = app.striker.cy
    if x-15 < mouseX < x+15 and y-15 < mouseY< y+15:
        app.lineEndLocation = None
    elif mouseY < y:
        app.lineEndLocation = None
    else:
        if app.tryingToDrawALine == True:
            app.tryingToDrawALine = False
            app.selected = False
            if app.lineEndLocation != None:
                x1, y1 = app.striker.cx, app.striker.cy
                x2, y2 = app.lineEndLocation
                app.striker.dx = (x1-x2)/10
                app.striker.dy = (y1-y2)/10
                app.turn = app.turn * -1

####################################################################
#####   Necessary functions for piece movement and collisons  ######
####################################################################

def movePiece(piece):
    #stop the piece if too slow
    if -0.1 < piece.dx < 0.1 and -0.1 < piece.dy < 0.1:
        piece.dx = 0
        piece.dy = 0

    #move the piece's center x coordinate
    piece.cx += piece.dx

    #make sure piece doesn't go past horizontal boundaries
    if piece.cx >= 525 - piece.radius: #app.width - margin - the piece radius
        piece.cx = 525 - piece.radius
        piece.dx = -piece.dx
    elif piece.cx <= piece.radius + 75:
        piece.cx = piece.radius + 75
        piece.dx = -piece.dx

    #move the piece's center y coordinate
    piece.cy += piece.dy

    #make sure piece doesn't go past vertical boundaries
    if piece.cy >= 525- piece.radius:
        piece.cy = 525- piece.radius 
        piece.dy = -piece.dy
    elif piece.cy <= piece.radius + 75:
        piece.cy = piece.radius + 75
        piece.dy = -piece.dy

    #friction of the board
    if piece.dx != 0 and piece.dy != 0:
        piece.dx *= 0.98
        piece.dy *= 0.98

#function that calculates how pieces collide and change their dx and dy's
def collide(piece1, piece2):
    #calculate ratios using trig
    x = piece1.cx - piece2.cx
    y = piece1.cy - piece2.cy
    cSquared = x**2 + y**2
    c = cSquared**0.5
    xRatio = x/c
    yRatio = y/c
    #total power is diminished a little simulating energy lost to sound and heat during collisons
    totalPower = (piece1.dx + piece2.dx + piece1.dy + piece2.dy)/1.5
    newDx = xRatio * totalPower
    newDy = yRatio * totalPower
    #new Dx and Dy's are done
    piece1.dx = -newDx 
    piece1.dy = -newDy 
    piece2.dx = newDx 
    piece2.dy = newDy 
    
def collision(piece1, piece2):
    x1, y1 = piece1.cx, piece1.cy
    x2, y2 = piece2.cx, piece2.cy
    offSet = (piece1.radius+piece2.radius)
    if x1-offSet < x2 < x1+offSet and y1-offSet < y2 < y1+offSet:
        #if abs(piece1.dx) != abs(piece2.dx) and abs(piece1.dy) != abs(piece2.dy):
            return True

####################################################################
#########################     On Step       ########################
####################################################################

def player1menu_onStep(app):
    app.player1menuSteps += 1
    if app.player1menuSteps == 100:
        app.player1menuSteps = 0
        setActiveScreen("player1turn")

def player2menu_onStep(app):
    app.player2menuSteps += 1
    if app.player2menuSteps == 100:
        app.player2menuSteps = 0
        setActiveScreen("player2turn")

def player1turn_onStep(app):
    #make sure all pieces are stationary
    if app.turn == -1 and app.striker.dx == 0 and app.striker.dy == 0:
        bool = True
        for i in range(len(app.pieces)):
            if app.pieces[i].dx != 0 and app.pieces[i].dy != 0:
                bool = False
        if bool:
            for i in range(len(app.pieces)):
                app.pieces[i].cx = app.width - app.pieces[i].cx
                app.pieces[i].cy = app.height - app.pieces[i].cy
                print(app.pieces[i].cx, app.pieces[i].cy)
            setActiveScreen("player2menu")
        

    #check for win
    if app.score1 >= 2:
        setActiveScreen("win")
    elif app.score2 >= 2:
        setActiveScreen("lose")

    movePiece(app.striker)

    for i in range(len(app.pieces)):
        piece = app.pieces[i]
        movePiece(piece)

    #check for collisions and collision logic
    for i in range(len(app.pieces)):
        #collisions between striker and pieces
        if collision(app.pieces[i], app.striker):
            collide(app.pieces[i], app.striker)
            
        #collisions between pieces
        for j in range(i, len(app.pieces)):
            if collision(app.pieces[i], app.pieces[j]):
                if app.pieces[i].cx != app.pieces[j].cx and app.pieces[i].cy != app.pieces[j].cy:
                    collide(app.pieces[i], app.pieces[j])

    #check for pockets:
    for piece in app.pieces:
        if 75.5 < piece.cx < 120.5 and 75.5 < piece.cy < 120.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)
        if 75.5 < piece.cx < 120.5 and 477.5 < piece.cy < 522.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)
        if 477.5 < piece.cx < 522.5 and 75.5 < piece.cy < 120.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)
        if 477.5 < piece.cx < 522.5 and 477.5 < piece.cy < 522.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)

    #game set-up
    if app.striker.dx == 0 and app.striker.dy == 0:
        bool = True
        for i in range(len(app.pieces)):
            if app.pieces[i].dx != 0 and app.pieces[i].dy != 0:
                bool = False
        if bool:
            app.striker.cx, app.striker.cy = app.slider.cx, 450
        

def player2turn_onStep(app):
    #make sure all pieces are stationary
    if app.turn == 1 and app.striker.dx == 0 and app.striker.dy == 0:
        bool = True
        for i in range(len(app.pieces)):
            if app.pieces[i].dx != 0 and app.pieces[i].dy != 0:
                bool = False
        if bool:
            for i in range(len(app.pieces)):
                app.pieces[i].cx = app.width - app.pieces[i].cx
                app.pieces[i].cy = app.height - app.pieces[i].cy
                print(app.pieces[i].cx, app.pieces[i].cy)
            setActiveScreen("player1menu")

    #check for win
    if app.score1 >= 2:
        setActiveScreen("win")
    elif app.score2 >= 2:
        setActiveScreen("lose")

    movePiece(app.striker)

    for i in range(len(app.pieces)):
        piece = app.pieces[i]
        movePiece(piece)

    #check for collisions and collision logic
    for i in range(len(app.pieces)):
        #collisions between striker and pieces
        if collision(app.pieces[i], app.striker):
            collide(app.pieces[i], app.striker)
            
        #collisions between pieces
        for j in range(i, len(app.pieces)):
            if collision(app.pieces[i], app.pieces[j]):
                if app.pieces[i].cx != app.pieces[j].cx and app.pieces[i].cy != app.pieces[j].cy:
                    collide(app.pieces[i], app.pieces[j])

    #check for pockets:
    for piece in app.pieces:
        if 75.5 < piece.cx < 120.5 and 75.5 < piece.cy < 120.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)
        if 75.5 < piece.cx < 120.5 and 477.5 < piece.cy < 522.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)
        if 477.5 < piece.cx < 522.5 and 75.5 < piece.cy < 120.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)
        if 477.5 < piece.cx < 522.5 and 477.5 < piece.cy < 522.5:
            if piece.color == 'red':
                app.score1 += 1
            elif piece.color == 'blue':
                app.score2 += 1
            else:
                if app.turn == -1:
                    app.score1 = 10
                else:
                    app.score2 = 10
            index = app.pieces.index(piece)
            app.pieces.pop(index)

    #game set-up
    if app.striker.dx == 0 and app.striker.dy == 0:
        bool = True
        for i in range(len(app.pieces)):
            if app.pieces[i].dx != 0 and app.pieces[i].dy != 0:
                bool = False
        if bool:
            app.striker.cx, app.striker.cy = app.slider.cx, 450

def main():
    runAppWithScreens(initialScreen='menu')

main()
