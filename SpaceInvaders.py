import pygame
import random
import os, sys

pygame.init()

win = pygame.display.set_mode((700,800))

clock = pygame.time.Clock()

backgroundColour = (0,0,0)
pProjectileColour = (34,203,0)
iProjectileColour = (255,255,255)

class Game():
    # main game class
    def __init__(self):
        self.level = 1
        self.health = 3
        self.points = 0

    def levelUp(self):
        self.level += 1
        if Invader.speed > 0.1:
            Invader.speed -= 0.1
        self.reset(new = False)
        # new is passed as False so that the level, health and points are not reset
    
    def healthDown(self):
        self.health -= 1
        if self.health == 0:
            self.gameOver(win)
        Player.x = 330
        Player.y = 700
        

    def pointsUp(self, row):
        self.points += Invader.invaderStats[row][-1]
        # the points awarded for each row is stored as the last element in the invaaderStats dictionary

    def reset(self, new = True):
        # this resets all the class attributes when a new game is started
        if new == True:
            self.level = 1
            self.health = 3
            self.points = 0   
        Invader.invaderLocations = [[0, 1, 2, 3, 4, 5], [50, 1, 2, 3, 4, 5], [100, 1, 2, 3, 4, 5],
        [150, 1, 2, 3, 4, 5], [200, 1, 2, 3, 4, 5], [250, 1, 2, 3, 4, 5], [300, 1, 2, 3, 4, 5], 
        [350, 1, 2, 3, 4, 5], [400, 1, 2, 3, 4, 5], [450, 1, 2, 3, 4, 5], [500, 1, 2, 3, 4, 5]]
        Invader.invaderStats = {1: [120, Invader.image1, Invader.image2, 30], 2:[160, Invader.image3, Invader.image4, 20], 3:[200, Invader.image3, Invader.image4, 20],
        4:[240, Invader.image5, Invader.image6, 10], 5:[280, Invader.image5, Invader.image6, 10]}
        Invader.invaderProjectileLocations = []
        Invader.direction = "Right"
        Invader.invaderTimer = 0
        Invader.invaderProjectileTimer = 0
        Invader.invaderAtBottom = False
        Invader.justMovedDown = True
        Invader.justMovedAcross = False
        Invader.imageShown = 1
        Invader.explosionLocation = []
        UFO.location = [-100, 50]
        UFO.timer = 0
        Player.x = 330
        Player.y = 700
        Player.projectileTimer = 0
        Player.playerProjectile = []


    def welcomeScreen(self, win):
        running = True
        
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_p]:
                    running = False

            win.fill(backgroundColour)

            text = []
            scoreText = []
            text.append("PLAY") 
            text.append("PRESS [P] TO PLAY")
            text.append("USE ARROW KEYS OR A/D TO MOVE")
            text.append("USE THE SPACEBAR TO SHOOT")
            text.append("-- SCORE TABLE --")
            scoreText.append("= 100 POINTS")
            scoreText.append("= 30 POINTS")
            scoreText.append("= 20 POINTS")
            scoreText.append("= 10 POINTS")

            win.blit(UFO.image, (183, 540))
            win.blit(Invader.image1, (200, 600))
            win.blit(Invader.image3, (200, 650))
            win.blit(Invader.image5, (200, 700))

        
            for i in range(len(text)):
                displayedFont = pygame.font.SysFont("Consolas", 40)
                displayedText = displayedFont.render(text[i], True, (255,255,255))
                textLocation = displayedText.get_rect(center = (350, 100 + 100*i))
                win.blit(displayedText, textLocation)

            for i in range(len(scoreText)):
                displayedFont = pygame.font.SysFont("Consolas", 30)
                displayedText = displayedFont.render(scoreText[i], True, (255,255,255))
                textLocation = displayedText.get_rect(center = (400, 560 + 54*i))
                win.blit(displayedText, textLocation)
             

            pygame.display.update()

    def mainGame(self, win):
        running = True
        while running:
            clock.tick(15)
            Invader.invaderTimer += 0.0667
            Player.projectileTimer += 0.0667
            Invader.invaderProjectileTimer += 0.0667
            UFO.timer += 0.0667

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            win.blit(pygame.image.load(os.path.join(sys.path[0],"Images/Background.png")), (0,0))

            pygame.draw.rect(win, (97, 109, 200), (0, 688, 700, 150))
            pygame.draw.rect(win, (97, 109, 200), (0, 0, 700, 30))

            gameFont = pygame.font.SysFont('Consolas', 25)
            healthText = gameFont.render("Health:", True, (255, 255, 255))
            win.blit(healthText, (500, 5))

            for h in range(self.health):
                win.blit(pygame.image.load(os.path.join(sys.path[0],"Images/HealthIcon.png")), (605 + h*25, 7))            
                # this displays the player's health as a number of hearts (3 down to 0)
            
            pointsText = gameFont.render("Points:" + str(SpaceInvaders.points), True, (255, 255, 255))
            win.blit(pointsText, (20, 5))
            levelText = gameFont.render("Level:" + str(SpaceInvaders.level), True, (255, 255, 255))
            levelTextCenter = levelText.get_rect(center = (350, 17))
            win.blit(levelText, levelTextCenter)
        
            if Invader.explosionLocation != []:
                for explosion in Invader.explosionLocation:
                    explosion[-2] += 0.0667
                # if there is an explosion is shown, this timer makes sure it doesnt stay on screen forever
                    if explosion[-2] > 0.25:
                        Invader.explosionLocation.remove(explosion)
                        # the explosion attributes are reset

            for i in Invader.invaderLocations:
                # i references each column of invaders
                for j in range (len(i) - 1):
                    # j references the individual elements of each array
                    win.blit(Invader.invaderStats[i[j+1]][Invader.imageShown], (i[0], Invader.invaderStats[i[j+1]][0]))
                    ''' i[j+1] references which index in the column the invader is, as the invader array is stored as such [x, 1, 2, 3, 4, 5]
                    so this index element is used as the keys in the invaderStats dictionary. the imageShown is either 1 or 2, referencing the 1st or 2nd
                    index in the dictionary. it is then displayed at the first element of the invader array (the x-coordinate) and the first element of the 
                    dictionary value at the key chosen (the y-coordinate)'''

                    if Invader.invaderStats[j+1][0] + 40 > 688:
                        '''the first element of each dictionary value is the y-coordinate, so this checks if it has reached the bottom
                        this is performed after the invader is displayed to screen so that the player can see why the game is over '''
                        Invader.invaderAtBottom = True  
    
            if Invader.explosionLocation != []:
                # the tuple is empty if there is no explosion to be shown
                for explosion in Invader.explosionLocation:

                    win.blit(pygame.image.load(os.path.join(sys.path[0], Invader.explosionImages[explosion[-1]])), (explosion[0], explosion[1]))


            win.blit(Player.image, (Player.x, Player.y))
            win.blit(UFO.image, (UFO.location[0], UFO.location[1]))
            AllProjectiles.drawProjectiles(win)
            # this draws the player, the ufo, and the projectiles

            pygame.display.update()                
            
            Player.move()
            Invader.move()
            UFO.move()    
            # these methods move the player, invader, and UFO


    def gameOver(self, win):
        running = True
        mouseDown = False
        highScore = self.checkHighScore()

        while running:
            pygame.draw.rect(win, (0,0,0), (140, 140, 420, 420))
            pygame.draw.rect(win, (97, 109, 200), (150, 150, 400, 400))
            
            playRect = pygame.Rect(200, 325, 130, 130)
            exitRect = pygame.Rect(370, 325, 130, 130)

            mouseCoords = pygame.mouse.get_pos()
            playCollide = playRect.collidepoint(mouseCoords) 
            exitCollide = exitRect.collidepoint(mouseCoords) 

            playColour = (118,227,149) if playCollide else (14,209,69)
            exitColour = (255,99,99) if exitCollide else (255,0,0)            

            pygame.draw.rect(win, playColour, playRect)
            pygame.draw.rect(win, exitColour, exitRect)

            if mouseDown and playCollide:
                self.reset()
                self.mainGame(win)
            elif mouseDown and exitCollide:
                pygame.quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown = True
                else:
                    mouseDown = False

            endFont = pygame.font.SysFont('Consolas', 40)

            endText = endFont.render(str(self.points) + " points!", True, (255,255,255))
            endText2 = endFont.render("Play again?", True, (255,255,255))

            if highScore:
                endText3 = endFont.render("HIGH SCORE!", True, (255,255,255))
                textLocation3 = endText3.get_rect(center = (350, 240))
                win.blit(endText3, textLocation3)

            textLocation = endText.get_rect(center = (350, 200))
            textLocation2 = endText2.get_rect(center = (350, 280))
            win.blit(endText, textLocation)        
            win.blit(endText2, textLocation2)
        

            pygame.display.update()

    def checkHighScore(self):
        with open(os.path.join(sys.path[0], 'HighScores.txt'), 'r') as score_file:
            contents = score_file.read()
        if int(contents) < self.points:
            with open(os.path.join(sys.path[0], 'HighScores.txt'), 'w') as score_file:
                score_file.write(str(self.points))   
            return True
        else:
            return False



SpaceInvaders = Game()


class PlayerShip():
    def __init__(self):
        self.image = pygame.image.load(os.path.join(sys.path[0],"Images/ShipSprite.png"))
        self.x = 330
        self.y = 700
        self.projectileTimer = 0
        self.playerProjectile = []


    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if Player.x > 10:
                Player.x -= 15
                # the ship is moved left by 15 pixels if a left key is pressed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if Player.x < 650:
                Player.x += 15
                # the ship is moved right by 15 pixels if a right key is pressed           
        if keys[pygame.K_SPACE] and self.playerProjectile == []:
            # the player can only fire 1 projectile at a time
            self.playerProjectile = [Player.x + 24, Player.y]
            self.projectileTimer = 0


Player = PlayerShip()


class Invaders():
    def __init__(self):
        self.image1 = pygame.image.load(os.path.join(sys.path[0],"Images/Invader1.1.png"))
        self.image2 = pygame.image.load(os.path.join(sys.path[0],"Images/Invader1.2.png"))
        self.image3 = pygame.image.load(os.path.join(sys.path[0],"Images/Invader2.1.png"))
        self.image4 = pygame.image.load(os.path.join(sys.path[0],"Images/Invader2.2.png"))
        self.image5 = pygame.image.load(os.path.join(sys.path[0],"Images/Invader3.1.png"))
        self.image6 = pygame.image.load(os.path.join(sys.path[0],"Images/Invader3.2.png"))
        self.invaderLocations = [[0, 1, 2, 3, 4, 5], [50, 1, 2, 3, 4, 5], [100, 1, 2, 3, 4, 5],
        [150, 1, 2, 3, 4, 5], [200, 1, 2, 3, 4, 5], [250, 1, 2, 3, 4, 5], [300, 1, 2, 3, 4, 5], 
        [350, 1, 2, 3, 4, 5], [400, 1, 2, 3, 4, 5], [450, 1, 2, 3, 4, 5], [500, 1, 2, 3, 4, 5]]
        # the first element is the x-coordinate, the following elements are the index in the column of the invaders that are still alive
        self.invaderProjectileLocations = []
        self.direction = "Right"
        self.invaderTimer = 0
        self.invaderProjectileTimer = 0
        self.explosionLocation = []
        self.explosionImages = ["Images/Explosion.png", "Images/ProjectileExplosion.png", "Images/PlayerExplosion.png"]
        self.explosionTimer = 0
        self.invaderAtBottom = False
        self.justMovedDown = True
        self.justMovedAcross = False
        self.imageShown = 1
        self.speed = 0.5
        self.invaderStats = {1: [120, self.image1, self.image2, 30], 2:[160, self.image3, self.image4, 20], 3:[200, self.image3, self.image4, 20],
        4:[240, self.image5, self.image6, 10], 5:[280, self.image5, self.image6, 10]}
        # this dictionary gives stats about each row (1-5) of the invaders, including their y-coordinate, the 2 images that are to be shown continually and their points worth


    def move(self):
        for i in self.invaderLocations:
            # iterates through each column of invaders
            if self.invaderTimer > self.speed:
                # this controls how often they move
                if self.direction == "Right":
                    i[0] = i[0] + 16
                    # each x-coordinate is increased by 16
                    self.justMovedAcross = True
                if self.direction == "Left":
                    i[0] = i[0] - 16
                    # each x-coordinate is decreased by 16
                    self.justMovedAcross = True
                    # this ensures they only move across once, not once for each element in the array
                self.justMovedDown = False
            else: 
                self.justMovedAcross = False       

        if self.imageShown == 1:
            if self.justMovedAcross == True:
                self.imageShown = 2
        else:
            if self.justMovedAcross == True:
                self.imageShown = 1
            # this changes the invader shown each time it moves between two images
        
        if self.invaderLocations == []:
            SpaceInvaders.levelUp()
            # if there are no invaders left, then the level is increased

        if self.justMovedAcross == True:
            # this resets the movement timer of the invaders if they have all just moved across
            self.invaderTimer = 0
        
        if self.invaderAtBottom:
            SpaceInvaders.gameOver(win)
            # the game is over if the invaders reach the bottom 

        for i in self.invaderLocations:
            # this checks if any column of invaders are at the side of the screen
            if i[0] + 40 > 690 and self.justMovedDown == False:
                # the invader icon is 40 pixels long, and it's drawn from the top left
                self.direction = "Left"
                for j in range(5):
                    Invader.invaderStats[j+1][0] += 25
                    # the first element of each value in the dictionary is the y-coord, so it is increased by 25 
                self.justMovedDown = True

            if i[0] < 10 and self.justMovedDown == False:
                self.direction = "Right"
                for j in range(5):
                    Invader.invaderStats[j+1][0] += 25
                    # the first element of each value in the dictionary is the y-coord, so it is increased by 25 
                self.justMovedDown = True
   

Invader = Invaders()


class UFOs():
    def __init__(self):
        self.location = [-100, 50]
        self.timer = 0
        self.image = pygame.image.load(os.path.join(sys.path[0],"Images/UFOSprite.png"))
        
    def move(self):
        if self.timer > 15:
            self.location[0] += 10

            if self.location[0] > 800:
                self.location = [-100, 50]
                self.timer = 0
                # if it reaches the right-edge of the screen it is reset

UFO = UFOs()


class AllProjectiles():
    def drawProjectiles(win):
        if Player.playerProjectile != []:
            # this only runs the loop if the player has a projectile on screen
            pygame.draw.rect(win, pProjectileColour, (Player.playerProjectile[0], Player.playerProjectile[1], 2, 15))
            Player.playerProjectile[1] -= 30
            # the player projectile is moved up the screen
            
            if Player.playerProjectile[1] < 40:
                Invader.explosionLocation.append([Player.playerProjectile[0] - 15, Player.playerProjectile[1] + 10, 0, 1])
                Player.playerProjectile = []
                # if the projectile reaches the top of the screen, it is removed

            column = 0
            for i in Invader.invaderLocations:
            # checks if a projectile is hitting an invader
                column += 1
                for j in range (len(i)-1):
                    # j will be used for the index of the elements in the array
                    if Player.playerProjectile != []:  
                        if i[0] - 5 < Player.playerProjectile[0] < i[0] + 45:
                            # i[0] is the x-coord of the column, and allows 5 pixels leeway either side
                            if Invader.invaderStats[j + 1][0] < Player.playerProjectile[1] < Invader.invaderStats[j + 1][0] + 40:
                                # compares the y-coords of the projectile and invader (referenced by the 1st element of the dictionary value where the key is its position in the column)
                                Invader.explosionLocation.append([Invader.invaderLocations[int(column)-1][0] + 3, Invader.invaderStats[int(j)+ 1][0] + 5, 0, 0])
                                # the invader has been hit, so the x,y coords are saved so an explosion can be shown
                                del Invader.invaderLocations[int(column)-1][int(j)+ 1]
                                # the invader is deleted from the array
                                if len(Invader.invaderLocations[int(column) - 1]) == 1:
                                    Invader.invaderLocations.remove(i)
                                    # if the length = 1, then the only element in the column is the x-coord, so the whole column can be removed from the array
                                Player.playerProjectile = []
                                SpaceInvaders.pointsUp(j + 1)
                                # the points are increased, j + 1 is passed as this stores what position the invader was in the column
        

            for i in Invader.invaderProjectileLocations:
            # checks if the player's projectile is hitting an invader's projectile
                if Player.playerProjectile != []: 
                    if i[0] - 6 < Player.playerProjectile[0] < i[0] + 8:
                        if i[1] < Player.playerProjectile[1] < i[1] + 40:
                            # checks whether the projectile is within range of the enemy projectile
                            Invader.explosionLocation.append([i[0] - 15, i[1] + 10, 0, 0])
                            Invader.invaderProjectileLocations.remove(i)
                            Player.playerProjectile = []
                            break
 
            if Player.playerProjectile != []:
                if UFO.location[0] < Player.playerProjectile[0] < UFO.location[0] + 75:
                    if UFO.location[1] < Player.playerProjectile[1] < UFO.location[1] + 38:
                        # if the UFO is hit, its location & timer is reset and the player gains 100 points
                        Invader.explosionLocation.append([UFO.location[0] + 22.5, UFO.location[1] + 4, 0, 0])
                        UFO.location = [-100, 50]
                        SpaceInvaders.points += 100
                        UFO.timer = 0
                        Player.playerProjectile = []


        for projectile in Invader.invaderProjectileLocations:
            pygame.draw.rect(win, iProjectileColour, (projectile[0], projectile[1], 2, 15))
            projectile [1] += 5      
            # the invader projectiles are moved down the screen


            if Player.x - 3 < projectile[0] < Player.x + 43:
                if Player.y + 5 < projectile[1] + 15 < Player.y + 25:
                    # if the player has been hit by an invader's projectile
                    Invader.explosionLocation.append([Player.x + 5, Player.y, 0, 2])
                    pygame.time.wait(100)
                    Invader.invaderProjectileLocations.remove(projectile)
                    SpaceInvaders.healthDown()
                    

            if projectile[1] > 750:
                Invader.invaderProjectileLocations.remove(projectile)
                # if the projectile reaches the bottom of the screen, it is removed
                Invader.explosionLocation.append([projectile[0] - 15, projectile[1] + 10, 0, 1])
                

    
        if Invader.invaderProjectileTimer > 1:
            # the invaders fire a projectile every 1 second
            projectileColumn = random.randint(0, len(Invader.invaderLocations)-1)
            # a random column is chosen
            projectileY = Invader.invaderLocations[projectileColumn][-1]
            # the y-coordinate of the projectile is the last element of the column chosen
            Invader.invaderProjectileLocations.append([Invader.invaderLocations[projectileColumn][0] + 20, Invader.invaderStats[projectileY][0] + 20])
            # the projectile is added to the array, 20 is added to each coordinate so it spawns at the invader's centre
            Invader.invaderProjectileTimer = 0

SpaceInvaders.welcomeScreen(win)
SpaceInvaders.mainGame(win)
pygame.quit()