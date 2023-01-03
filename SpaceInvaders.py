import pygame
import random
import time

pygame.init()

win = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()

invaderImage = pygame.image.load("InvaderIcon.png")
shipImage = pygame.image.load("PlayerShip.png")
backgroundColour = (0,0,0)
projectileColour = (255,127,39)


speed = 0.5

class Statistics():
    def __init__(self):
        self.level = 1
        self.health = 3
        self.points = 0

    def levelUp(self):
        self.level += 1
    
    def healthDown(self):
        self.health -= 1

    def pointsUp(self):
        self.points += 2 * self.level

    def reset(self):
        self.level = 1
        self.health = 3
        self.points = 0       


GameStats = Statistics()

def mainGame():
    running = True
    direction = "Right"
    playerLocation = [262.5, 450]
    invaderLocations = [[0, 40, 80, 120, 160, 200], [50, 40, 80, 120, 160, 200], [100, 40, 80, 120, 160, 200],
    [150, 40, 80, 120, 160, 200], [200, 40, 80, 120, 160, 200], [250, 40, 80, 120, 160, 200], [300, 40, 80, 120, 160, 200], 
    [350, 40, 80, 120, 160, 200], [400, 40, 80, 120, 160, 200], [450, 40, 80, 120, 160, 200]]
    # the first element of each array references the y-coordinate of each invader
    invaderTimer = 0
    playerProjectileTimer = 0
    invaderProjectileTimer = 0
    justMovedDown = True
    justMovedAcross = False
    playerProjectileLocations = []
    invaderProjectileLocations = []

    while running:
        clock.tick(15)
        invaderTimer += 0.0667
        # the speed will increase as levels progress
        playerProjectileTimer += 0.0667
        invaderProjectileTimer += 0.0667

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        win.fill(backgroundColour)
    
        win.blit(shipImage, playerLocation)

        pygame.draw.rect(win, (97, 109, 200), (0, 0, 600, 30))

        gameFont = pygame.font.SysFont('Consolas', 25)
        healthText = gameFont.render("Health:" + str(GameStats.health), True, (255, 255, 255))
        win.blit(healthText, (450, 5))
        pointsText = gameFont.render("Points:" + str(GameStats.points), True, (255, 255, 255))
        win.blit(pointsText, (20, 5))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            playerLocation[0] -= 5
            # the ship is moved left by 5 pixels if a left key is pressed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            playerLocation[0] += 5
            # the ship is moved right by 5 pixels if a right key is pressed           
        if keys[pygame.K_SPACE] and playerProjectileTimer > 0.5:
            # the player can fire a projectile every 0.5 seconds
            playerProjectileLocations.append([playerLocation[0] + 37, playerLocation[1]])
            playerProjectileTimer = 0
            # a projectile is added to the array at the ships current location if the space bar is clicked


        for i in invaderLocations:
            # i references each column of invaders

            for j in range (len(i) - 1):
                # j references the individual elements of each array
               
                win.blit(invaderImage, (i[0], i[j + 1]))
                # the y-coordinate is referenced using i[j + 1] in order to skip over the first element which is the x-coordinate
                # [0.5, 0.4, 0.3, 0.2, 0.1]    
            if invaderTimer > speed - GameStats.level*speed:
                if direction == "Right":
                    i[0] = i[0] + 5
                    # each x-coordinate is increased by 5
                    justMovedAcross = True
                if direction == "Left":
                    i[0] = i[0] - 5
                    # each x-coordinate is decreased by 5
                    justMovedAcross = True
                justMovedDown = False
            else: 
                justMovedAcross = False            
                
            
            if len(i) == 1:
                invaderLocations.remove(i)
                # this removes it from the array if there are no invaders left in that column

            
        if invaderLocations == []:
            GameStats.levelUp()
            mainGame()

        if justMovedAcross == True:
            # this resets the movement of the invaders if they have all just moved across
            invaderTimer = 0
        

        for i in invaderLocations:
            if i[0] + 40 == 600 and justMovedDown == False:
                # the invader icon is 40 pixels long, and it's drawn from the top left
                direction = "Left"
                for l in invaderLocations:
                    for j in range (len(l) - 1):
                        l[j + 1] = l[j + 1] + 10
                        # the y-coordinate is increased by 10 to move it down the screen
                justMovedDown = True


            if i[0] == 0 and justMovedDown == False:
                direction = "Right"
                for m in invaderLocations:
                    for j in range (len(m) - 1):
                        m[j + 1] = m[j + 1] + 10
                        # the y-coordinate is increased by 10 to move it down the screen
                justMovedDown = True

        

        for projectile in invaderProjectileLocations:
            pygame.draw.rect(win, projectileColour, (projectile[0], projectile[1], 2, 15))
            projectile [1] += 5

            if playerLocation[0] < projectile[0] < playerLocation[0] + 75:
                if playerLocation[1] < projectile[1] + 15 < playerLocation[1] + 90:
                    # if the player has been hit by an invader's projectile
                    GameStats.healthDown()
                    invaderProjectileLocations.remove(projectile)

        
        for projectile in playerProjectileLocations:
            # handles all the collisions of the players projectiles
            pygame.draw.rect(win, projectileColour, (projectile[0], projectile[1], 2, 15))
            # each projectile is drawn and moved up the screen

            touchedInvader = isTouchingInvader(projectile, invaderLocations) 
            touchedProjectile = isTouchingProjectile(projectile, invaderProjectileLocations)
            # runs functions to check if a projectile is hitting any invader or projectile

            if touchedInvader != []:
                # if no invader is being touched then the array of coordinates will be empty
                invaderLocations[touchedInvader[0]].pop((touchedInvader[1]))
                # the invader at the locations returned from the function is popped (pop allows you to remove an element at a specific index)
                playerProjectileLocations.remove(projectile)
                # it also removes the projectile that has hit the invader
                GameStats.pointsUp()
            
            elif touchedProjectile != []:
                # if no projectiles are touching then the array of coordinates will be empty
                invaderProjectileLocations.remove(touchedProjectile)
                # the invader projectile is removed
                playerProjectileLocations.remove(projectile)
                # it also removes the player's projectile that has hit the invaders projectile

            projectile[1] -= 5
    

        if invaderProjectileTimer > 0.5:
            # the invaders fire a projectile every 0.5 seconds
            projectileColumn = random.randint(0, len(invaderLocations)-1)
            # a random column is chosen
            projectileY = invaderLocations[projectileColumn][len(invaderLocations[projectileColumn])-1]
            # the y coordinate of the projectile is the last element of the column chosen
            invaderProjectileLocations.append([invaderLocations[projectileColumn][0] + 20, projectileY + 20])
            # the projectile is added to the array - 20 is added to each coordinate so it spawns at the invader's centre
            invaderProjectileTimer = 0

        if GameStats.health == 0:
            gameOver()
    
        pygame.display.update()


def isTouchingInvader(projectile, invaderLocations):
    column = 0
    # the column will be passed back to the main function, showing which array-column the invader belongs to
    for i in invaderLocations:
        column += 1
        for j in range (len(i)-1):
            if i[0] < projectile[0] < i[0] + 40:
                if i[j + 1] < projectile[1] < i[j + 1] + 40:
                    # checks whether the projectile is within the coordinates of the projectile
                    return [int(column)-1, int(j)+ 1]
                    # returns the column and the position of the invader in the column
    return []
    # if there are no collisions, an empty array is returned

def isTouchingProjectile(projectile, invaderProjectileLocations):
    for i in invaderProjectileLocations:
        if i[0] - 6 < projectile[0] < i[0] + 8:
            if i[1] < projectile[1] < i[1] + 40:
                # checks whether the projectile is within range of the enemy projectile
                return i
                # returns the coordinates of the enemy projectile touched
    return []
    # if there are no collisions, an empty array is returned

def gameOver():
    running = True
    mouseDown = False
    while running:
        pygame.draw.rect(win, (0,0,0), (140, 140, 320, 320))
        pygame.draw.rect(win, (97, 109, 200), (150, 150, 300, 300))
        pygame.draw.rect(win, (14,209,69), (200, 325, 75, 75))
        pygame.draw.rect(win, (255,0,0), (325, 325, 75, 75))

        mouseX, mouseY = pygame.mouse.get_pos()

        if 200 < mouseX < 275 and 325 < mouseY < 400:
            pygame.draw.rect(win, (118,227,149), (200, 325, 75, 75))
            if mouseDown:
                GameStats.reset()
                mainGame()
        if 325 < mouseX < 400 and 325 < mouseY < 400:
            pygame.draw.rect(win, (255,99,99), (325, 325, 75, 75))
            if mouseDown:
                pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            else:
                mouseDown = False

        endFont = pygame.font.SysFont('Consolas', 40)

        endText = endFont.render("Game Over!!!", True, (255,255,255))
        endText2 = endFont.render("Play again?", True, (255,255,255))

        textLocation = endText.get_rect(center = (300, 200))
        textLocation2 = endText2.get_rect(center = (300, 250))
        win.blit(endText, textLocation)        
        win.blit(endText2, textLocation2)

        pygame.display.update()

mainGame()
pygame.quit()