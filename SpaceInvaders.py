import pygame
import random
import time

win = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()

invaderImage = pygame.image.load("InvaderIcon.png")
shipImage = pygame.image.load("PlayerShip.png")
backgroundColour = (0,0,0)
projectileColour = (255,127,39)


speed = 1

def mainGame():
    running = True
    direction = "Right"
    shipLocation = [262.5, 450]
    shipHealth = 3
    invaderLocations = [[40, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450], [90, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450],
    [140, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450], [190, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450], [240, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450]]
    # the first element of each array references the y-coordinate of each invader
    invaderTimer = 0
    projectileTimer = 0
    justMovedDown = True
    justMovedAcross = False
    projectileLocations = []
    while running:
        clock.tick(15)
        invaderTimer += 0.0667
        # the speed will increase as levels progress
        projectileTimer += 0.0667

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        win.fill(backgroundColour)

        for i in invaderLocations:
            # i references each layer of invaders
            for j in range (len(i) - 1):
                # j references the individual elements of each array
               
                win.blit(invaderImage, (i[j + 1], i[0]))
                # the x-coordinate is referenced using i[j + 1] in order to skip over the first element which is the y-coordinate
                
                if invaderTimer > speed:
                    if direction == "Right":
                        i[j + 1] = i[j + 1] + 5
                        # each x-coordinate is increased by 5
                        justMovedAcross = True
                    if direction == "Left":
                        i[j + 1] = i[j + 1] - 5
                        # each x-coordinate is decreased by 5
                        justMovedAcross = True
                    justMovedDown = False
                else: 
                    justMovedAcross = False
                
        if justMovedAcross == True:
            # this resets the movement of the invaders if they have all just moved across
            invaderTimer = 0
        
        for i in invaderLocations:
            for j in range (len(i) - 1):
                # this loop is to check whether any invader is touching the side of the screen

                if i[j + 1] + 40 == 600 and justMovedDown == False:
                    # the invader icon is 40 pixels long, and it's drawn from the top left
                    direction = "Left"
                    print(i)
                    for l in invaderLocations:
                        l[0] = l[0] + 10
                        # the y-coordinate is increased by 10
                    justMovedDown = True


                if i[j + 1] == 0 and justMovedDown == False:
                    direction = "Right"
                    for m in invaderLocations:
                        m[0] = m[0] + 10
                        # the y-coordinate is decreased by 10
                    justMovedDown = True
    


        win.blit(shipImage, shipLocation)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            shipLocation[0] -= 5
            # the ship is moved left by 5 pixels if a left key is pressed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            shipLocation[0] += 5
            # the ship is moved right by 5 pixels if a right key is pressed           
        if keys[pygame.K_SPACE] and projectileTimer > 0.5 :
            # the player can fire a projectile every 0.5 seconds
            projectileLocations.append([shipLocation[0] + 37, shipLocation[1]])
            projectileTimer = 0
            # a projectile is added to the array at the ships current location if the space bar is clicked
        
        for projectile in projectileLocations:
            pygame.draw.rect(win, projectileColour, (projectile[0], projectile[1], 2, 15))
            projectile[1] -= 5
            # each projectile is drawn and moved up the screen


        


        pygame.display.update()







mainGame()
pygame.quit()