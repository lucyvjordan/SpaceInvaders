import pygame
import random
import time

win = pygame.display.set_mode((600,600))

clock = pygame.time.Clock()

invader = pygame.image.load("InvaderIcon.png")
backgroundColour = (0,0,0)

invaderLocations = [[40, 0, 50, 100, 150, 200, 250, 300, 350, 400], [90, 0, 50, 100, 150, 200, 250, 300, 350, 400],
[140, 0, 50, 100, 150, 200, 250, 300, 350, 400, 450], [190, 0, 50, 100, 150, 200, 250, 300, 350, 400], [240, 0, 50, 100, 150, 200, 250, 300, 350, 400]]
# the first element of each array references the y-coordinate of each invader


speed = 2
def mainGame():
    running = True
    direction = "Right"
    while running:
        clock.tick(speed)
        # the speed will increase as levels progress

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        win.fill(backgroundColour)

        for i in invaderLocations:
            # i references each layer of invaders
            for j in range (len(i) - 1):
                # j references the individual elements of each array
               
                win.blit(invader, (i[j + 1], i[0]))
                # the x-coordinate is referenced using i[j + 1] in order to skip over the first element which is the y-coordinate

                if direction == "Right":
                    i[j + 1] = i[j + 1] + 5
                    # each x-coordinate is increased by 5
                if direction == "Left":
                    i[j + 1] = i[j + 1] - 5
                    # each x-coordinate is decreased by 5
                
        for i in invaderLocations:
            for j in range (len(i) - 1):
                # this loop is to check whether any invader is touching the side of the screen

                if i[j + 1] + 40 == 600:
                    # the invader icon is 40 pixels long, and it's drawn from the top left
                    direction = "Left"
                    for l in invaderLocations:
                        l[0] = l[0] + 10
                        # the y-coordinate is increased by 10

                if i[j + 1] == 0:
                    direction = "Right"
                    for l in invaderLocations:
                        l[0] = l[0] + 10
                        # the y-coordinate is decreased by 10


        pygame.display.update()


            
        
            




mainGame()
pygame.quit()