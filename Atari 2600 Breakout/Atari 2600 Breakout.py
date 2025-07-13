import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((1920, 1080), vsync = 1)
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(0)
pygame.display.set_caption("Atari 2600 Breakout")
pygame.display.toggle_fullscreen()

gameStarted = False
gameEnded = False
drawBat = False
isBallOut = True
totalBallHits = 0
isBatShort = False

# statystyki
points = 0
ballsLeft = 5

# ---CZCIONKI---
atari = pygame.font.Font("atari.otf", 60) # czcionka atari
freesansbold = pygame.font.Font("freesansbold.ttf", 30) # czcionka freesansbold

# ---DZWIEKI---

# elementy gry
wallLeftImg = pygame.image.load("wallLeft.png").convert()
wallRightImg = pygame.image.load("wallRight.png").convert()
wallTop = pygame.Rect(310, 130, 1300, 60)
bat = pygame.Rect(885, 1053, 150, 20)
ball = pygame.Rect(951, 560, 20, 20)
batShort = pygame.Rect(922, 1053, 80, 20)

# ---BALL---
ballSpeed = 5
speedMode = "bat"
canBreakBricks = False

# ---CEGLY---
brickWidth = 50
brickHeight = 25
columns = 26

redBrickPosX = 310
redBrickPosY = 290

orangeBrickPosX = 310
orangeBrickPosY = 315

dorangeBrickPosX = 310
dorangeBrickPosY = 340

yellowBrickPosX = 310
yellowBrickPosY = 365

greenBrickPosX = 310
greenBrickPosY = 390

blueBrickPosX = 310
blueBrickPosY = 415

def generateRedBricks():
    global redBricks, redBrick

    redBricks = []

    for column in range(columns): # 26 kolumn wiec 26 iteracji
        x = redBrickPosX + column * brickWidth # bazowa pozycja cegly i dodawanie do niej numeru kolumny razy dlugosc cegly i odstep awiec jak pierwsza kolumna to bedzie bazowa pozycja, jak druga kolumna to bazowa + 2 razy cegla + odstep wiec bedzie  w drugiej kolumnie i tak dalej.
        y = redBrickPosY + brickHeight # jesli pierwszy rzad to y pozostaje bez zmian

        redBrick = pygame.Rect(x, y, brickWidth, brickHeight) # rect czerwonej cegly w oparciu o wyzej stworzone zmienne
        redBricks.append(redBrick)
    
    return redBricks

def generateOrangeBricks():
    global orangeBricks, orangeBrick

    orangeBricks = []

    for column in range(columns):
        x = orangeBrickPosX + column * brickWidth
        y = orangeBrickPosY + brickHeight

        orangeBrick = pygame.Rect(x, y, brickWidth, brickHeight)
        orangeBricks.append(orangeBrick)
    
    return orangeBricks

def generateDorangeBricks():
    global dorangeBricks, dorangeBrick

    dorangeBricks = []

    for column in range(columns):
        x = dorangeBrickPosX + column * brickWidth
        y = dorangeBrickPosY + brickHeight

        dorangeBrick = pygame.Rect(x, y, brickWidth, brickHeight)
        dorangeBricks.append(dorangeBrick)
    
    return dorangeBricks

def generateYellowBricks():
    global yellowBricks, yellowBrick

    yellowBricks = []

    for column in range(columns):
        x = yellowBrickPosX + column * brickWidth
        y = yellowBrickPosY + brickHeight

        yellowBrick = pygame.Rect(x, y, brickWidth, brickHeight)
        yellowBricks.append(yellowBrick)
    
    return yellowBricks

def generateGreenBricks():
    global greenBricks, greenBrick

    greenBricks = []

    for column in range(columns):
        x = greenBrickPosX + column * brickWidth
        y = greenBrickPosY + brickHeight

        greenBrick = pygame.Rect(x, y, brickWidth, brickHeight)
        greenBricks.append(greenBrick)
    
    return greenBricks

def generateBlueBricks():
    global blueBricks, blueBrick

    blueBricks = []

    for column in range(columns):
        x = blueBrickPosX + column * brickWidth
        y = blueBrickPosY + brickHeight

        blueBrick = pygame.Rect(x, y, brickWidth, brickHeight)
        blueBricks.append(blueBrick)
    
    return blueBricks

def newListOfBricks():
    global redBricks, orangeBricks, dorangeBricks, yellowBricks, greenBricks, blueBricks

    redBricks = generateRedBricks()
    orangeBricks = generateOrangeBricks()
    dorangeBricks = generateDorangeBricks()
    yellowBricks = generateYellowBricks()
    greenBricks = generateGreenBricks()
    blueBricks = generateBlueBricks()

def startGame():
    global drawBat, gameStarted
    
    gameStarted = True
    drawBat = True

def throwBall():
    global isBallOut, posX, ballAngleRad, ballVelX, ballVelY
    
    isBallOut = False

    whichPosX = random.randint(0,2) # losowanie startowej pozycji X ball

    if whichPosX == 0:
        posX = 330
    
    elif whichPosX == 1:
        posX = 950
    
    elif whichPosX == 2:
        posX = 1570

    whichAngle = random.randint(0, 1) # losowanie kata

    if whichAngle == 0:
        ballAngle = 225
    
    elif whichAngle == 1:
        ballAngle = 315
    
    ballAngleRad = math.radians(ballAngle)

    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed

def checkOffset():
    offset = ball.centerx - bat.centerx

    return offset

newListOfBricks()

while running:
    pressedKeys = pygame.key.get_pressed()

    mousex, mousey = pygame.mouse.get_pos()

    bat.centerx = mousex
    batShort.centerx = mousex

    # obsluga eventow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if pressedKeys[pygame.K_LCTRL]:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameStarted == False and gameEnded == False: # start gry
                startGame()

            elif gameStarted == True and isBallOut == True: # wyrzucenie pilki
                throwBall()

    # ---RYSOWANIE EKRANU---
    screen.fill("black")

    # rysowanie scian
    wallLeft = screen.blit(wallLeftImg, [250, 130])
    wallRight = screen.blit(wallRightImg, [1610, 130])
    pygame.draw.rect(screen, [142, 142, 142], wallTop)

    # rysowanie paletki
    if drawBat == True and isBatShort == False:
        pygame.draw.rect(screen, [211, 85, 70], bat)
    
    elif drawBat == True and isBatShort == True:
        pygame.draw.rect(screen, [211, 85, 70], batShort)
    
    # rysowanie pilki
    if isBallOut == False:
        pygame.draw.rect(screen, [211, 85, 70], ball)

        ball = ball.move(ballVelX, ballVelY)

    # rysowanie red bricks
    for redBrick in redBricks:    
        pygame.draw.rect(screen, [211, 85, 70], redBrick)

    # rysowanie orange bricks
    for orangeBrick in orangeBricks:    
        pygame.draw.rect(screen, [198, 108, 58], orangeBrick)

    # rysowanie dorange bricks
    for dorangeBrick in dorangeBricks:    
        pygame.draw.rect(screen, [180, 122, 48], dorangeBrick)

    # rysowanie yellow bricks
    for yellowBrick in yellowBricks:    
        pygame.draw.rect(screen, [162, 162, 42], yellowBrick)
    
    # rysowanie green bricks
    for greenBrick in greenBricks:
        pygame.draw.rect(screen, [73, 160, 73], greenBrick)

    # rysowanie blue bricks
    for blueBrick in blueBricks:
        pygame.draw.rect(screen, [66, 73, 200], blueBrick)

    # ---LOGIKA---

    # odbijanie od scian
    if ball.colliderect(wallLeft) or ball.colliderect(wallRight):
        ballVelX *= -1
    
    # odbijanie od walltop
    if ball.colliderect(wallTop):
        ballVelY *= -1
        isBatShort = True
    
    # odbijanie od bat STATIC
    if ball.colliderect(bat) or ball.colliderect(batShort):
        totalBallHits += 1
        canBreakBricks = True

        if checkOffset() > 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, uderza bat od prawej strony
            if totalBallHits == 4:
                if speedMode == "bat": 
                    ballAngle = 60
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "bat": 
                    ballSpeed = 6

                    ballAngle = 30
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "bat": 
                    ballSpeed = 7

                    ballAngle = 38
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelX *= -1
                ballVelY *= -1

        
        elif checkOffset() < 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, udeza bat od lewej strony
            if totalBallHits == 4:
                if speedMode == "bat": 
                    ballAngle = 120
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "bat": 
                    ballSpeed = 6

                    ballAngle = 150
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "bat": 
                    ballSpeed = 7

                    ballAngle = 142
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelY *= -1

        elif checkOffset() < 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza bat od lewej strony
            if totalBallHits == 4:
                if speedMode == "bat": 
                    ballAngle = 120
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "bat": 
                    ballSpeed = 6

                    ballAngle = 150
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "bat": 
                    ballSpeed = 7

                    ballAngle = 142
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelX *= -1
                ballVelY *= -1

        elif checkOffset() > 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza bat od prawej strony
            if totalBallHits == 4:
                if speedMode == "bat": 
                    ballAngle = 60
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "bat": 
                    ballSpeed = 6

                    ballAngle = 30
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "bat": 
                    ballSpeed = 7

                    ballAngle = 38
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelY *= -1
    

    pygame.display.flip()

    clock.tick(240)