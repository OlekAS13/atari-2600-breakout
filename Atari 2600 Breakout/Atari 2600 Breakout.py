import pygame
import math
import random

pygame.init()

START_GAME = pygame.USEREVENT + 1

screen = pygame.display.set_mode((1920, 1080), vsync = 1)
clock = pygame.time.Clock()
running = True

pygame.mouse.set_visible(0)
pygame.display.set_caption("Atari 2600 Breakout")
pygame.display.toggle_fullscreen()

gameStarted = False
gameEnded = False
drawPaddle = False
isBallOut = True
totalBallHits = 0
isPaddleShort = False
infiniteLives = False
firstScreenCleared = False
showDebug = False

# statystyki
points = 0
ballsLeft = 5

# ---CZCIONKI---
atari = pygame.font.Font("atari.otf", 100) # czcionka atari
freesansbold = pygame.font.Font("freesansbold.ttf", 30) # czcionka freesansbold

# ---DZWIEKI---
paddleSound = pygame.mixer.Sound("paddle.mp3")
wallSound = pygame.mixer.Sound("wall.mp3")
blueSound = pygame.mixer.Sound("blue.mp3")
greenSound = pygame.mixer.Sound("green.mp3")
yellowSound = pygame.mixer.Sound("yellow.mp3")
dorangeSound = pygame.mixer.Sound("dorange.mp3")
orangeSound = pygame.mixer.Sound("orange.mp3")
redSound = pygame.mixer.Sound("red.mp3")

# elementy gry
wallLeftImg = pygame.image.load("wallLeft.png").convert()
wallRightImg = pygame.image.load("wallRight.png").convert()
wallTop = pygame.Rect(310, 130, 1300, 60)
paddle = pygame.Rect(885, 1053, 150, 20)
ball = pygame.Rect(951, 650, 20, 20)
paddleShort = pygame.Rect(922, 1053, 80, 20)
ballOutCheck = pygame.Rect(310, 1075, 1300, 30)

# ---BALL---
ballSpeed = 5
speedMode = "paddle"
canBreakBricks = False

# ---CEGLY---
brickWidth = 65
brickHeight = 25
columns = 20

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
    global drawPaddle, gameStarted
    
    gameStarted = True
    drawPaddle = True

def throwBall():
    global isBallOut, posX, ballAngleRad, ballVelX, ballVelY, ballSpeed, speedMode
    
    isBallOut = False
    speedMode = "paddle"
    ballSpeed = 5

    wallSound.stop()
    wallSound.play()

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

    ball = pygame.Rect(posX, 650, 20, 20)
    
    ballAngleRad = math.radians(ballAngle)

    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed

def checkOffset():
    offset = ball.centerx - paddle.centerx

    return offset

def resetGame():
    global gameStarted, gameEnded, drawPaddle, isBallOut, totalBallHits
    global isPaddleShort, infiniteLives, firstScreenCleared, points, ballsLeft
    global speedMode, ballSpeed, ball, ballVelX, ballVelY, ballAngle, ballAngleRad

    gameStarted = False
    gameEnded = False
    drawPaddle = False
    isBallOut = True
    totalBallHits = 0
    isPaddleShort = False
    infiniteLives = False
    firstScreenCleared = False
    points = 0
    ballsLeft = 5
    speedMode = "paddle"
    ballSpeed = 5

    ball = pygame.Rect(951, 650, 20, 20)

    whichAngle = random.randint(0, 1)
    if whichAngle == 0:
        ballAngle = 225
    else:
        ballAngle = 315

    ballAngleRad = math.radians(ballAngle)
    ballVelX = math.cos(ballAngleRad) * ballSpeed
    ballVelY = -math.sin(ballAngleRad) * ballSpeed

    newListOfBricks()


newListOfBricks()

pygame.time.set_timer(START_GAME, 50, loops = 1)

while running:
    dt = clock.get_time() / 1000.0 # delta time w sekundach
    pressedKeys = pygame.key.get_pressed()

    mousex, mousey = pygame.mouse.get_pos()

    paddle.centerx = mousex
    paddleShort.centerx = mousex

    # obsluga eventow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if pressedKeys[pygame.K_LCTRL]:
            running = False
        
        if event.type == START_GAME:
            startGame()

        if event.type == pygame.MOUSEBUTTONDOWN or pressedKeys[pygame.K_g]:
            if gameStarted == True and isBallOut == True:
                throwBall()
        
        if pressedKeys[pygame.K_r]:
            if gameEnded:
                resetGame()
                startGame()

        
        if pressedKeys[pygame.K_i] and isBallOut == True:
            infiniteLives = True
        
        if pressedKeys[pygame.K_d]:
            if showDebug == False:
                showDebug = True

            elif showDebug == True:
                showDebug = False

    # ---RYSOWANIE EKRANU---
    screen.fill("black")

    # rysowanie scian
    wallLeft = screen.blit(wallLeftImg, [250, 130])
    wallRight = screen.blit(wallRightImg, [1610, 130])
    pygame.draw.rect(screen, [142, 142, 142], wallTop)
    pygame.draw.rect(screen, "black", ballOutCheck)

    # rysowanie paletki
    if drawPaddle == True and isPaddleShort == False:
        pygame.draw.rect(screen, [211, 85, 70], paddle)
    
    elif drawPaddle == True and isPaddleShort == True:
        pygame.draw.rect(screen, [211, 85, 70], paddleShort)
    
    # rysowanie pilki
    if isBallOut == False:
        if ball.top <= 465 and ball.top > 440: # pilka niebieska
            pygame.draw.rect(screen, [66, 73, 200], ball)
        
        elif ball.top <= 440 and ball.top > 415: # pilka zielona
            pygame.draw.rect(screen, [73, 160, 73], ball)

        elif ball.top <= 415 and ball.top > 390: # pilka zolta
            pygame.draw.rect(screen, [162, 162, 42], ball)
        
        elif ball.top <= 390 and ball.top > 365: # pilka ciemnopomaranczowa
            pygame.draw.rect(screen, [180, 122, 48], ball)
        
        elif ball.top <= 365 and ball.top > 340: # pilka pomaranczowa
            pygame.draw.rect(screen, [198, 108, 58], ball)
        
        elif ball.top <= 340 and ball.top > 315: # pilka czerwona
            pygame.draw.rect(screen, [211, 85, 70], ball)

        else:
            pygame.draw.rect(screen, [211, 85, 70], ball)

        ball = ball.move(ballVelX * dt * 200, ballVelY * dt * 200)

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

        wallSound.stop()
        wallSound.play()

        # anti-clip
        if ball.left < wallLeft.right:
            ball.left = wallLeft.right
        
        if ball.right > wallRight.left:
            ball.right = wallRight.left
    
    # odbijanie od walltop
    if ball.colliderect(wallTop):
        ballVelY *= -1
        isPaddleShort = True
        canBreakBricks = True

        paddleSound.stop()
        paddleSound.play()

        # anti-clip
        if ball.top < wallTop.bottom:
            ball.top = wallTop.bottom

    # pilka wypada
    if ball.colliderect(ballOutCheck):
        isBallOut = True
        isPaddleShort = False
        totalBallHits = 0

        if infiniteLives == False:
            ballsLeft -= 1

        ball = pygame.Rect(951, 650, 20, 20)

        if ballsLeft == 0:
            gameStarted = False
            gameEnded = True
        

    # odbijanie od cegiel
    if canBreakBricks == True:
        allBrickRows = [
            (blueBricks, 1, blueSound, False),
            (greenBricks, 1, greenSound, False),
            (yellowBricks, 4, yellowSound, False),
            (dorangeBricks, 4, dorangeSound, True),
            (orangeBricks, 7, orangeSound, True),
            (redBricks, 7, redSound, True),
        ]

        for brickList, pointValue, sound, affectsSpeed in allBrickRows:
            for idx, brick in enumerate(brickList):
                if ball.colliderect(brick):
                    if affectsSpeed and speedMode == "paddle":
                        ballSpeed = 8
                        if ballVelX > 0 and ballVelY < 0:
                            ballAngle = 315
                        elif ballVelX < 0 and ballVelY < 0:
                            ballAngle = 225
                        elif ballVelX > 0 and ballVelY > 0:
                            ballAngle = 45
                        elif ballVelX < 0 and ballVelY > 0:
                            ballAngle = 135

                        ballAngleRad = math.radians(ballAngle)
                        ballVelX = math.cos(ballAngleRad) * ballSpeed
                        ballVelY = -math.sin(ballAngleRad) * ballSpeed
                        speedMode = "brick"
                    else:
                        ballVelY *= -1

                    points += pointValue
                    canBreakBricks = False
                    del brickList[idx]

                    sound.stop()
                    sound.play()
                    break
            if not canBreakBricks:
                break

    """if canBreakBricks == True:
        for idx, blueBrick in enumerate(blueBricks): # niebieska
            if ball.colliderect(blueBrick):
                ballVelY *= -1
                points += 1
                canBreakBricks = False
                del blueBricks[idx]

                blueSound.stop()
                blueSound.play()
        
        for idx, greenBrick in enumerate(greenBricks): # zielona
            if ball.colliderect(greenBrick):
                ballVelY *= -1
                points += 1
                canBreakBricks = False
                del greenBricks[idx]
                
                greenSound.stop()
                greenSound.play()

        for idx, yellowBrick in enumerate(yellowBricks): # zolta
            if ball.colliderect(yellowBrick):
                ballVelY *= -1
                points += 4
                canBreakBricks = False
                del yellowBricks[idx]

                yellowSound.stop()
                yellowSound.play()
            
        for idx, dorangeBrick in enumerate(dorangeBricks): # ciemnopomaranczowa
            if ball.colliderect(dorangeBrick):
                if speedMode == "bat":
                    ballSpeed = 8
                    if ballVelX > 0 and ballVelY < 0:
                        ballAngle = 315
                    
                    elif ballVelX < 0 and ballVelY < 0:
                        ballAngle = 225
                    
                    elif ballVelX > 0 and ballVelY > 0:
                        ballAngle = 45
                    
                    elif ballVelX < 0 and ballVelY > 0:
                        ballAngle = 135
                    
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
                else:
                    ballVelY *= -1

                points += 4
                canBreakBricks = False
                del dorangeBricks[idx]
                speedMode = "brick"

                dorangeSound.stop()
                dorangeSound.play()
        
        for idx, orangeBrick in enumerate(orangeBricks): # pomaranczowa
            if ball.colliderect(orangeBrick):
                if speedMode == "bat":
                    ballSpeed = 8
                    if ballVelX > 0 and ballVelY < 0:
                        ballAngle = 315
                    
                    elif ballVelX < 0 and ballVelY < 0:
                        ballAngle = 225
                    
                    elif ballVelX > 0 and ballVelY > 0:
                        ballAngle = 45
                    
                    elif ballVelX < 0 and ballVelY > 0:
                        ballAngle = 135
                    
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
                else:
                    ballVelY *= -1

                points += 7
                canBreakBricks = False
                del orangeBricks[idx]
                speedMode = "brick"

                orangeSound.stop()
                orangeSound.play()
        
        for idx, redBrick in enumerate(redBricks): # czerwona
            if ball.colliderect(redBrick):
                if speedMode == "bat":
                    ballSpeed = 8
                    if ballVelX > 0 and ballVelY < 0:
                        ballAngle = 315
                    
                    elif ballVelX < 0 and ballVelY < 0:
                        ballAngle = 225
                    
                    elif ballVelX > 0 and ballVelY > 0:
                        ballAngle = 45
                    
                    elif ballVelX < 0 and ballVelY > 0:
                        ballAngle = 135
                    
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
                else:
                    ballVelY *= -1

                points += 7
                canBreakBricks = False
                del redBricks[idx]
                speedMode = "brick"

                redSound.stop()
                redSound.play()"""
        
    # odbijanie od paddle STATIC
    if ball.colliderect(paddle) and isPaddleShort == False:
        totalBallHits += 1
        canBreakBricks = True

        paddleSound.stop()
        paddleSound.play()

        if not redBricks and not orangeBricks and not dorangeBricks and not yellowBricks and not greenBricks and not blueBricks and firstScreenCleared == False:
            newListOfBricks()
            firstScreenCleared = True

        if checkOffset() > 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, uderza bat od prawej strony
            if totalBallHits == 4:
                if speedMode == "paddle": 
                    ballAngle = 60
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 30
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
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
                if speedMode == "paddle": 
                    ballAngle = 120
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 150
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
                    ballSpeed = 7

                    ballAngle = 142
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelY *= -1

        elif checkOffset() < 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza bat od lewej strony
            if totalBallHits == 4:
                if speedMode == "paddle": 
                    ballAngle = 120
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 150
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
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
                if speedMode == "paddle": 
                    ballAngle = 60
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 30
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
                    ballSpeed = 7

                    ballAngle = 38
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelY *= -1
    
    if ball.colliderect(paddleShort) and isPaddleShort == True:
        totalBallHits += 1
        canBreakBricks = True

        paddleSound.stop()
        paddleSound.play()

        if not redBricks and not orangeBricks and not dorangeBricks and not yellowBricks and not greenBricks and not blueBricks and firstScreenCleared == False:
            newListOfBricks()
            firstScreenCleared = True

        if checkOffset() > 0 and ballVelX < 0 and ballVelY > 0: # ball leci z prawej w dol, uderza bat od prawej strony
            if totalBallHits == 4:
                if speedMode == "paddle": 
                    ballAngle = 60
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 30
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
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
                if speedMode == "paddle": 
                    ballAngle = 120
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 150
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
                    ballSpeed = 7

                    ballAngle = 142
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelY *= -1

        elif checkOffset() < 0 and ballVelX > 0 and ballVelY > 0: # ball leci z lewej w dol, udeza bat od lewej strony
            if totalBallHits == 4:
                if speedMode == "paddle": 
                    ballAngle = 120
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 150
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
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
                if speedMode == "paddle": 
                    ballAngle = 60
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
            
            elif totalBallHits == 8:
                if speedMode == "paddle": 
                    ballSpeed = 6

                    ballAngle = 30
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed
                
            elif totalBallHits == 12:
                if speedMode == "paddle": 
                    ballSpeed = 7

                    ballAngle = 38
                    ballAngleRad = math.radians(ballAngle)
                    ballVelX = math.cos(ballAngleRad) * ballSpeed
                    ballVelY = -math.sin(ballAngleRad) * ballSpeed

            else:
                ballVelY *= -1

    # ---TEKSTY STATYSTYK---
    # punkty
    pointsHundered = atari.render("{}".format(points // 100), True, [142, 142, 142])
    pointsTen = atari.render("{}".format((points // 10) % 10), True, [142, 142, 142])
    pointsOne = atari.render("{}".format(points % 10), True, [142, 142, 142])

    screen.blit(pointsHundered, [500, 5])
    screen.blit(pointsTen, [600, 5])
    screen.blit(pointsOne, [700, 5])

    # pilki
    ballsLeftText = atari.render("{}".format(ballsLeft), True, [142, 142, 142])
    
    screen.blit(ballsLeftText, [1050, 5])

    # rodzaj gry STALE
    whichGameText = atari.render("1", True, [142, 142, 142])

    screen.blit(whichGameText, [1350, 5])

    # ---DEBUG---
    text1 = freesansbold.render("SPEED: {}".format(ballSpeed), True, "white")
    text2 = freesansbold.render("SMODE: {}".format(speedMode), True, "white")
    text3 = freesansbold.render("INFLIVES: {}".format(infiniteLives), True, "white")

    if showDebug == True:
        screen.blit(text1, [0, 0])
        screen.blit(text2, [0, 30])
        screen.blit(text3, [0, 60])

    pygame.display.flip()

    clock.tick(240)