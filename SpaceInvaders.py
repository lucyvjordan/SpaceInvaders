import pygame
import random
import time

win = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()

invaderImage = pygame.image.load("InvaderIcon.png")
shipImage = pygame.image.load("PlayerShip.png")
backgroundColour = (0,0,0)
projectileColour = (255,127,39)

speed = 0.5

def mainGame():
    running = True
    direction = "Right"
    shipLocation = [262.5, 450]
    shipHealth = 3
    invaderLocations = [[0, 40, 90, 140, 190, 240], [50, 40, 90, 140, 190, 240], [100, 40, 90, 140, 190, 240],
    [150, 40, 90, 140, 190, 240], [200, 40, 90, 140, 190, 240], [250, 40, 90, 140, 190, 240], [300, 40, 90, 140, 190, 240], 
    [350, 40, 90, 140, 190, 240], [400, 40, 90, 140, 190, 240], [450, 40, 90, 140, 190, 240]]
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

        for i in invaderLocations:
            # i references each column of invaders

            for j in range (len(i) - 1):
                # j references the individual elements of each array
               
                win.blit(invaderImage, (i[0], i[j + 1]))
                # the y-coordinate is referenced using i[j + 1] in order to skip over the first element which is the x-coordinate
                
            if invaderTimer > speed:
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

            if len(i) == 1:
                invaderLocations.remove(i)
                # this removes it from the array if there are no invaders left in that column


        win.blit(shipImage, shipLocation)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            shipLocation[0] -= 5
            # the ship is moved left by 5 pixels if a left key is pressed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            shipLocation[0] += 5
            # the ship is moved right by 5 pixels if a right key is pressed           
        if keys[pygame.K_SPACE] and playerProjectileTimer > 0.5 :
            # the player can fire a projectile every 0.5 seconds
            playerProjectileLocations.append([shipLocation[0] + 37, shipLocation[1]])
            playerProjectileTimer = 0
            # a projectile is added to the array at the ships current location if the space bar is clicked

        #if invaderProjectileTimer > 0.5:
            # the invaders fire a projectile every 0.5 seconds

        
        for projectile in playerProjectileLocations:
            pygame.draw.rect(win, projectileColour, (projectile[0], projectile[1], 2, 15))
            projectile[1] -= 5
            # each projectile is drawn and moved up the screen

            touchedInvader = isTouching(projectile, invaderLocations) 
            # runs a function to check if a projectile is hitting any invader
            if touchedInvader != []:
                # if no invader is being touched then the array of coordinates will be empty
                invaderLocations[touchedInvader[0]].pop((touchedInvader[1]))
                # the invader at the locations returned from the function is popped (pop allows you to remove an element at a specific index)
                playerProjectileLocations.remove(projectile)
                # it also removes the projectile that has hit the invader
    
        pygame.display.update()


def isTouching(projectile, invaderLocations):
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

mainGame()
pygame.quit()