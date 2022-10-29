
import pygame, sys, time, random
from pygame.locals import *
from pygame import mixer

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKBLUE = (10,0,200)
DARKBROWN = (165,42,42)
LIGHTERBROWN = (160,82,45)
CHOCOLATE = (210,105,30)
LEMON = (255,250,205)
YELLOW = (255,255,0)
DARKGREEN = (0,128,0)

#3 rows of 6

def createInvadersBasePos(invadersBasePos):
    
    for x in range(0,18):
        invadersBasePos.append((0,0,300,300))
    for x in range(0,6):
        invadersBasePos[x] = [(x*111),0,300,300]
    for x in range(0,6):
        invadersBasePos[x+6] = [(x*111),111,300,300]
    for x in range(0,6):
        invadersBasePos[x+12] = [(x*111),222,300,300]
    
    return invadersBasePos

def invadersMovement(invaders, invaderMovementCoordList, invadersBasePos, sinceLastMovedInvaders):
    invaders = []
    for x in range(0,len(invadersBasePos)):
        invaders.append([invaderMovementCoordList[0][0] + invadersBasePos[x][0], invaderMovementCoordList[0][1] + invadersBasePos[x][1],100,111])
    tempIndex = invaderMovementCoordList[0]
    invaderMovementCoordList.remove(tempIndex)
    
    sinceLastMovedInvaders = 0
    return invaders, invaderMovementCoordList, sinceLastMovedInvaders
        
def spaceShipMovement(moveLeft, moveRight, spaceShip, upgrades):
    if moveLeft == True and spaceShip['rect'].left > 0:
        spaceShip['rect'].left -= (35 + upgrades[1])
        
    if moveRight == True and spaceShip['rect'].right < 1400:
        spaceShip['rect'].right += (35 + upgrades[1])

    return spaceShip

def spaceShipProjectiles(fireProjectile, projectileIDs, spaceShip, spaceShipLastFired, upgrades):
    
    if  spaceShipLastFired > 4:
        spaceShipLastFired = 0
        IDNotUsed = False
        while IDNotUsed == False:
            tempRandNum = random.randint(0,1000000)
            newID = 'i' + str(tempRandNum)# In case your strategy is holding down the spacebar
            if newID not in projectileIDs:
                projectileIDs.append(newID)
                latestAddition = len(projectileIDs)
                IDNotUsed = True
        projectileIDs[latestAddition-1] = {'rect':pygame.Rect((spaceShip['rect'].left + spaceShip['rect'].right)/2-30, spaceShip['rect'].top - 50, 10, 50)}

    for x in projectileIDs:
        if len(x) != 0:
            x['rect'].top -=(30 + upgrades[0])

    for x in projectileIDs:
        if len(x) != 0:
            if x['rect'].bottom < 0:
                projectileIDs.remove(x)
    return projectileIDs, spaceShipLastFired

def invaderProjectiles(invaders, invadersLastFired, invaderProjectile):
    if invadersLastFired > 150 or invaderProjectile['beRemade'] == True: #So they fire something every 5 seconds, since we run at 30 fps.
        
        if len(invaders)>0:
            randomPos = random.randint(0,len(invaders)-1)
            invaderProjectile['rect'] = pygame.Rect(invaders[randomPos][0]+50,invaders[randomPos][1]+55, 10, 50)
            invadersLastFired = 1
            invaderProjectile['beRemade'] = False
            return invadersLastFired, invaderProjectile
        else:
            invaderProjectile['rect'] = pygame.Rect(10000,100000, 10, 50)
            return invadersLastFired, invaderProjectile
        
    else:
        invaderProjectile['rect'].top += 10
        return invadersLastFired, invaderProjectile


def collisionDetection(projectileIDs, invaders, spaceShip, invaderProjectile, userLives, defenderWallList, invadersBasePos, userScore):
    z = -1
    breakOut = False
    for x in invaders:
        z += 1
        tempInvaderRect = {'rect':pygame.Rect(x), 'color':BLUE}
        for y in range(0,len(projectileIDs)):
            
            
            if len(projectileIDs[y]) == 0:
                projectileIDs.remove(projectileIDs[y])

            if projectileIDs[y]['rect'].colliderect(tempInvaderRect['rect']):
                tempInvaderBasePos = invadersBasePos[z]
                invadersBasePos.remove(tempInvaderBasePos)
                invaders.remove(x)
                projectileIDs.remove(projectileIDs[y])
                userScore += 10
                break
    
        
    if invaderProjectile['rect'].colliderect(spaceShip['rect']):
       invaderProjectile = {'rect':pygame.Rect(1000, 1000, 10, 50), 'color':GREEN, 'beRemade':True}
       userLives -= 1
    if invaderProjectile['rect'].bottom>800:
        invaderProjectile = {'rect':pygame.Rect(1000, 1000, 10, 50), 'color':GREEN, 'beRemade':True}       
    
    return projectileIDs, invaders, spaceShip, invaderProjectile, userLives, defenderWallList, invadersBasePos, userScore
    
def drawObjects(sinceLastSwitch,basicFont, windowSurface, projectileIDs, invaders, spaceShip, invaderProjectile, defenderWallList, userScore, userLives, backGround, invaderImage, invaderImage2, defenderImage, invaderBullet, defenderBullet,lastDefenderImage):
            
    windowSurface.blit(backGround,(0,0))

    for x in projectileIDs:
        if len(x) != 0:
            pygame.draw.rect(windowSurface, BLACK, x['rect'])
            windowSurface.blit(defenderBullet,x['rect'])
            
    
            
    for x in range(0, len(invaders)):
        if lastDefenderImage == 0:
            pr = pygame.draw.rect(windowSurface, BLACK, invaders[x])
            pygame.draw.rect(windowSurface, BLACK, invaders[x])
            windowSurface.blit(invaderImage,invaders[x])
        if lastDefenderImage == 1:
            pr = pygame.draw.rect(windowSurface, BLACK, invaders[x])
            pygame.draw.rect(windowSurface, BLACK, invaders[x])
            windowSurface.blit(invaderImage2,invaders[x])

    if sinceLastSwitch >30:        
        switched = False
        if lastDefenderImage == 0:
            print("f")
            lastDefenderImage = 1
            switched = True

        if lastDefenderImage == 1 and switched == True:
            print("d")
            lastDefenderImage = 0
        sinceLastSwitch = 0
        
    sinceLastSwitch = sinceLastSwitch + 1
    pygame.draw.rect(windowSurface, BLACK, spaceShip['rect'])
    windowSurface.blit(defenderImage,spaceShip['rect'])
    
            

            
    basicFont = pygame.font.SysFont(None, 35)

    
    text = basicFont.render("Score "+ str(userScore), True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.centerx = 100
    textRect.centery = 25
    windowSurface.blit(text, textRect)

    text2 = basicFont.render("Lives "+ str(userLives), True, WHITE, BLACK)
    textRect2 = text.get_rect()
    textRect2.centerx = 1300
    textRect2.centery = 25
    windowSurface.blit(text2, textRect2)

    pygame.draw.line(windowSurface, RED, (0,500),(1400,500),1)

    basicFont = pygame.font.SysFont(None, 48)

    pygame.draw.rect(windowSurface, BLACK, invaderProjectile['rect'])
    windowSurface.blit(invaderBullet,invaderProjectile['rect'])
    

def isGameOver(userLives, gameOver, invaders, message, allInvadersDead, invaderMovementCoordList):

    if userLives == 0 or gameOver == True or len(invaders) == 0:
        gameOver = True
        if userLives == 0:
            message = "Game Over"
        if len(invaders) == 0 or gameOver == True:
            
            message = "Game Over"
        else:
            message = "something"
            
    return gameOver, message, allInvadersDead
   

def saveGameFunction(userLives, userScore, upgrades):
    f = open("gameSaveFile" + ".txt", "w")
    
    start1 = ""
    start2 = ""
    userScore = str(userScore)
    upgrades1 = str(upgrades[0])
    upgrades2 = str(upgrades[1])
    if upgrades[0] == 0:
        upgrades1 = "0"
    if upgrades[1] == 0:
        upgrades2 = "0"
    
    if userScore == 0:
        userScore1 = "0"
        
    
    if len(str(userLives)) == 1:
        start1 = "0"
    if len(str(userScore)) == 2:
        start2 = "000"
    if len(str(userScore)) == 3:
        start2 = "00"
    if len(str(userScore)) == 4:
        start2 = "0"        
    f.write(start1 + str(userLives)+start2 + userScore +upgrades1 + upgrades2)
                                              
def renderMainMenu(menuMainPosition, scrollDown, scrollUp,startNewGame, loadGame, windowSurface, fireProjectile, basicFont):



    
        
    if menuMainPosition == 0:
        pygame.draw.rect(windowSurface, BLACK, (600,350,200,50))
        pygame.draw.rect(windowSurface, RED, (600,250,200,50))
    
    
    if menuMainPosition == 0 and fireProjectile == True:
        startNewGame = True
    
    text = basicFont.render("Start game", True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.centerx = 700
    textRect.centery = 250
    windowSurface.blit(text, textRect)

    

    pygame.display.update()


    

    return startNewGame, menuMainPosition, loadGame

def inGameMenu(gameOverUser,projectileInputHappened, scrollDownInputHappened,scrollUpInputHappened,scrollUp, scrollDown, fireProjectile, upgrades, saveGame,inGamePosition, windowSurface, basicFont, lockMenuState):
    
    print(inGamePosition)
    windowSurface.fill(BLACK)
    #In game menu Vars 0 is resume game, 1 is save game, 2 is leave game, 3 is upgrade BulletSpeed, 4 is upgradeUserSpeed 
    gameOver = False
    lockMenuState = True
    if scrollUp == True and (inGamePosition - 1) >= 0 and scrollUpInputHappened == False:
        print("Spooky scary")
        inGamePosition -= 1
        scrollUpInputHappened = True
    if scrollDown == True and (inGamePosition + 1) <= 4 and scrollDownInputHappened == False:
        inGamePosition += 1
        print("Skelingtons")
        scrollDownInputHappened == True
    
    if inGamePosition == 0:
        pygame.draw.rect(windowSurface, RED, (200,75,200,50))
    if inGamePosition == 1:
        pygame.draw.rect(windowSurface, RED, (225,125,150,50))
    if inGamePosition == 2:
        pygame.draw.rect(windowSurface, RED, (210,175,175,50))
    if inGamePosition == 3:
        pygame.draw.rect(windowSurface, RED, (5,225,590,50))
    if inGamePosition == 4:
        pygame.draw.rect(windowSurface, RED, (15,275,570,50))
        
    if inGamePosition == 0 and fireProjectile == True and projectileInputHappened == False:
        projectileInputHappened = True
        lockMenuState = False
    if inGamePosition == 1 and fireProjectile == True and projectileInputHappened == False:
        projectileInputHappened = True
        saveGame = True
    if inGamePosition == 2 and fireProjectile == True and projectileInputHappened == False:
        projectileInputHappened = True
        gameOverUser = True
    if inGamePosition == 3 and fireProjectile == True and (upgrades[0] + 1) != 10 and projectileInputHappened == False:
        projectileInputHappened = True
        upgrades[0] += 1
    if inGamePosition == 4 and fireProjectile == True and (upgrades[1] + 1) != 10 and projectileInputHappened == False:
        projectileInputHappened = True
        upgrades[1] += 1

    text = basicFont.render("Resume game", True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.centerx = 300
    textRect.centery = 100
    windowSurface.blit(text, textRect)

    text2 = basicFont.render("Save game", True, WHITE, BLACK)
    textRect2 = text2.get_rect()
    textRect2.centerx = 300
    textRect2.centery = 150
    windowSurface.blit(text2, textRect2)

    text3 = basicFont.render("Leave game", True, WHITE, BLACK)
    textRect3 = text3.get_rect()
    textRect3.centerx = 300
    textRect3.centery = 200
    windowSurface.blit(text3, textRect3)

    BulletSpeedInfo = "Upgrade bullet speed. Current level " + str(upgrades[0])
    text4 = basicFont.render(BulletSpeedInfo, True, WHITE, BLACK)
    textRect4 = text4.get_rect()
    textRect4.centerx = 300
    textRect4.centery = 250
    windowSurface.blit(text4, textRect4)

    UserSpeedInfo = "Upgrade ship speed. Current level " + str(upgrades[1])
    text5 = basicFont.render(UserSpeedInfo, True, WHITE, BLACK)
    textRect5 = text5.get_rect()
    textRect5.centerx = 300
    textRect5.centery = 300
    windowSurface.blit(text5, textRect5)

    pygame.display.update()

    return lockMenuState, upgrades, saveGame, inGamePosition, gameOverUser, scrollUpInputHappened, scrollDownInputHappened,projectileInputHappened

    
def main():
    # set up pygame
    pygame.init()

    # set up the window
    windowSurface = pygame.display.set_mode((1400,800), 0, 32)
    pygame.display.set_caption('Space invaders')

    invadersBasePos = []
    invaders = []
    projectileIDs = []
    basicFont = pygame.font.SysFont(None, 48)

    #Feel free to increase the lives if you are bad at gaems.
    userLives = 2

    #Loading the background
    backGround = pygame.image.load('background.png')
    
    mixer.music.load("Code_background.wav")
    mixer.music.play(-1)

    #UFO image
    invaderImage = pygame.image.load('alienf.png')
    

    defenderImage = pygame.image.load('jedi.png')
    

    invaderImage2 = pygame.image.load('alienf.png')
    

    invaderBullet = pygame.image.load('laserinvader.png')


    defenderBullet = pygame.image.load('laserdefender.png')
    

    #Feel free to increase if you need a confidence boost
    userScore = 0

    lastDefenderImage = 0
    sinceLastSwitch = 0
    #It's a spaceship! Whooo....
    spaceShip = {'rect':pygame.Rect(250, 650, 100, 25), 'color':BLUE}
    invaderProjectile = {'rect':pygame.Rect(0, 0, 10, 50), 'color':GREEN, 'beRemade':True}
    

    #Placeholder message
    message = "Game over!"

    #Amount of frames since last projectile launch. So if you will increase the fps,
    #You can shoot faster, but so can the enemy.
    invadersLastFired = 0
    spaceShipLastFired = 0

    #This is here to make sure that the invaders don't come closer to you
    #30 times a second
    sinceLastMovedInvaders = 0

    #Different defender walls
    defenderWall1 = {'rect':pygame.Rect(170, 575, 100, 25), 'color':BLUE, 'health':5}
    defenderWall2 = {'rect':pygame.Rect(410, 575, 100, 25), 'color':BLUE, 'health':5}
    defenderWall3 = {'rect':pygame.Rect(650, 575, 100, 25), 'color':BLUE, 'health':5}
    defenderWall4 = {'rect':pygame.Rect(890, 575, 100, 25), 'color':BLUE, 'health':5}
    defenderWall5 = {'rect':pygame.Rect(1130, 575, 100, 25), 'color':BLUE, 'health':5}

    defenderWallList = [defenderWall1,defenderWall2,defenderWall3,defenderWall4,defenderWall5]
    invadersMovementTime = 20
    
    
    #MainMenu element Vars 0 is on start game, 1 is on load game
    menuMainPosition = 0

    #In game menu Vars 0 is resume game, 1 is save game, 2 is leave game, 3 is upgrade BulletSpeed, 4 is upgrade UserSpeed.
    inGamePosition = 0

    #Starting off the booleans for the movement and firing.
    #I acknowledge that this whole section is a mess of badly named booleans, sorry about that.
    moveLeft = False
    moveRight = False
    fireProjectile = False
    gameOver = False
    openMenu = False
    startGame = False
    mainMenu = True
    scrollUp = False
    scrollDown = False
    lockMenuState = False
    saveGame = False
    firstTime = True
    scrollUpInputHappened = False
    scrollDownInputHappened = False
    resetTime = 0
    projectileInputHappened = False
    gameOverUser = False
    

    #BulletSpeed, UserSpeed
    upgrades = [0,0]
    
    nextLevel = True
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #Keypress checks
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True

                if event.key == K_LEFT or event.key == ord('a'): 
                    moveLeft = True
                    moveRight = False
                if event.key == K_SPACE:
                    fireProjectile = True
                if event.key == K_ESCAPE:
                    openMenu = True
                if event.key == K_UP:
                    scrollUp = True
                    scrollDown = False
                if event.key == K_DOWN:
                    scrollDown = True
                    scrollUp = False
            
            if event.type == KEYUP:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_SPACE:
                    fireProjectile = False
                if event.key == K_ESCAPE:
                    openMenu = False
                if event.key == K_UP:
                    scrollDown = False 
                if event.key == K_DOWN:
                    scrollDown = False
        loadGame = False
        if mainMenu == True:
            startGame, menuMainPosition, loadGame = renderMainMenu(menuMainPosition, scrollDown, scrollUp, startGame, loadGame, windowSurface, fireProjectile, basicFont)
            if startGame == True:
                nextLevel = True
                mainMenu = False

        if loadGame == True:
            f = open("gameSaveFile" + ".txt", "r")
            info = f.read(9)
            print(len(info))
            userLives = int(str(info[0]) + str(info[1]))
            userScore = int(str(info[2]) + (info[3]) + (info[4]) + (info[5]) + (info[6]))
            upgrades[0] = int(info[7])
            upgrades[1] = int(info[8])
            loadGame = False
                                                      
        if openMenu == True or lockMenuState == True:
            resetTime += 1
            if scrollUp == True:
                scrollUpInputHappened = True
            if scrollDown == True:
                scrollDownInputHappened = True

            if fireProjectile == True:
                projectileInputHappened = True
                
            if resetTime > 10 and (scrollUpInputHappened or scrollDownInputHappened or projectileInputHappened):
                resetTime = 0
                scrollDownInputHappened = False
                scrollUpInputHappened = False
                projectileInputHappened = False
            lockMenuState, upgrades, saveGame,inGamePosition, gameOverUser, scrollUpInputHappened, scrollDownInputHappened, projectileInputHappened = inGameMenu(gameOverUser,projectileInputHappened,scrollDownInputHappened,scrollUpInputHappened,scrollUp, scrollDown, fireProjectile, upgrades, saveGame,inGamePosition, windowSurface, basicFont, lockMenuState)
                
            if lockMenuState == True:
                startGame = False
                openMenu = True
            if lockMenuState == False:
                startGame = True
                openMenu = False
        if nextLevel == True:
            #This is the "track" that the invaders use for movement. I then will add these positions
            #To the "invaders" list.
            invaderMovementCoordList = [[110,30],[220,30],[330,30],[440,30],[550,30],[660,30],
                                [660,60],[550,60],[440,60],[330,60],[220,60],[110,60],
                                [110,90],[220,90],[330,90],[440,90],[550,90],[660,90],
                                [660,120],[550,120],[440,120],[330,120],[220,120],[110,120],
                                [110,150],[220,150],[330,150],[440,150],[550,150],[660,150],
                                [660,180],[550,180],[440,180],[330,180],[220,180],[110,180]]
            
            #Creating the list of the invaders and their positions relative to the "track" of movement.
            if firstTime == False:
                invadersBasePos = createInvadersBasePos(invadersBasePos)
                invaders, invaderMovementCoordList, sinceLastMovedInvaders = invadersMovement(invaders, invaderMovementCoordList, invadersBasePos, sinceLastMovedInvaders)
            if invadersMovementTime - 1 > 0:
                invadersMovementTime -= 1
            userLives += 1
            allInvadersDead = False
            nextLevel = False
            firstTime = False
        if gameOver != True and startGame == True:            
            invadersLastFired += 1
            spaceShipLastFired += 1
            sinceLastMovedInvaders +=1
            
            #Everything involving the S.S. spaceShip
            spaceShip = spaceShipMovement(moveLeft, moveRight, spaceShip, upgrades)

            if sinceLastMovedInvaders > invadersMovementTime:
                #Everything involving the general movment of the invaders
                if len(invaderMovementCoordList) != 0:
                    invaders, invaderMovementCoordList, sinceLastMovedInvaders = invadersMovement(invaders, invaderMovementCoordList, invadersBasePos, sinceLastMovedInvaders)
                else:
                    allInvadersDead = True
            
            #This function is responsible for managing all of the spaceship projectiles
            projectileIDs, spaceShipLastFired = spaceShipProjectiles(fireProjectile, projectileIDs, spaceShip, spaceShipLastFired, upgrades)

            if len(invaders)>0:
                #This function manages the invaders projectiles.
                invadersLastFired, invaderProjectile = invaderProjectiles(invaders, invadersLastFired, invaderProjectile)
            
            #This function looks for collisions between all the objects
            projectileIDs, invaders, spaceShip, invaderProjectile, userLives, defenderWallList, invadersBasePos, userScore = collisionDetection(projectileIDs, invaders, spaceShip, invaderProjectile, userLives, defenderWallList, invadersBasePos, userScore)
            
            windowSurface.fill(BLACK)
            
            #Drawing whatever is left onto the surface.
            drawObjects(sinceLastSwitch,basicFont, windowSurface, projectileIDs, invaders, spaceShip, invaderProjectile, defenderWallList, userScore, userLives, backGround, invaderImage, invaderImage2, defenderImage, invaderBullet, defenderBullet,lastDefenderImage)
            
            pygame.display.update()

            
            gameOver, message, allInvadersDead = isGameOver(userLives, gameOver, invaders, message, allInvadersDead,invaderMovementCoordList)
            if gameOver == True and userLives > 0:
                gameOver = False
                nextLevel = True
            if gameOver == True and userLives == 0:
                gameOver = True
                
            if saveGame == True:
                saveGameFunction(userLives, userScore, upgrades)
                
            #This games projectiles and general movement are dependent on the fps
            #Feel free to lower this if you aren't doing so well, and vice-versa
            fpsClock = pygame.time.Clock()
            fpsClock.tick(30)

        if gameOver == True or gameOverUser == True:
            openMenu = False
            lockMenuState = False
            windowSurface.fill(BLACK)
            text = basicFont.render(message, True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.centerx = windowSurface.get_rect().centerx
            textRect.centery = windowSurface.get_rect().centery
            windowSurface.blit(text, textRect)
            
            pygame.display.update()
        

    # draw the window onto the screen
    pygame.display.update()
    
main()
