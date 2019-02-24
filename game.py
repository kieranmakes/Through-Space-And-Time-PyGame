import pygame
import sys
import random




def startMenu(highscore=None):
  WIDTH = 800
  HEIGHT = 600
  RED = (255,0,0)
  BACKGROUND_COLOUR = (0,0,0)
  BTN_WIDTH = 300
  BTN_HEIGHT = 75

  message = ""
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  pygame.display.set_caption('Through Space And Time')
  nothingSelected = True


  titleFont = pygame.font.SysFont("monospace", 60)
  messageFont = pygame.font.SysFont("monospace", 40)

  if highscore != None:
    message = "Your Score: {}".format(highscore)



  while nothingSelected: 
    

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pos()[0] >= 250 and pygame.mouse.get_pos()[1] >= 250:
          if pygame.mouse.get_pos()[0] <= 550 and pygame.mouse.get_pos()[1] <= 325:
            startGame()
            pygame.quit()

     
      if event.type == pygame.MOUSEBUTTONDOWN:
        if pygame.mouse.get_pos()[0] >= 250 and pygame.mouse.get_pos()[1] >= 350:
          if pygame.mouse.get_pos()[0] <= 550 and pygame.mouse.get_pos()[1] <= 425:
            sys.exit()
      

    # fills in the background 
    screen.fill(BACKGROUND_COLOUR)   

    pygame.draw.rect(screen, RED, ((WIDTH/2)-(BTN_WIDTH/2), (HEIGHT/2)-50 , BTN_WIDTH, BTN_HEIGHT))
    pygame.draw.rect(screen, RED, ((WIDTH/2)-(BTN_WIDTH/2), (HEIGHT/2)+50 , BTN_WIDTH, BTN_HEIGHT))

    titleText = "Through Space And Time"
    titleLabel = titleFont.render(titleText, 1, RED)
    screen.blit(titleLabel, ((WIDTH/2)-240, 50))
    
    
    messageText = message
    messageLabel = messageFont.render(messageText, 1, RED)
    screen.blit(messageLabel, ((WIDTH/2)-117, 160))

    startGameLabel = messageFont.render("Start Game", 1, BACKGROUND_COLOUR)
    screen.blit(startGameLabel, ((WIDTH/2)-70,(HEIGHT/2)-26))

    quitLabel = messageFont.render("Quit Game", 1, BACKGROUND_COLOUR)
    screen.blit(quitLabel, ((WIDTH/2)-70,(HEIGHT/2)+75))

    pygame.display.update()




def startGame():
    
 
  # inits variables so they can be used in the itterations before an event has occured
  pressedLeft = False
  pressedRight = False
  pressedSpace = False
  score = 0

  WIDTH = 800
  HEIGHT = 600
  RED = (255,0,0)
  BLUE = (0,0,255)
  BLACK = (0,0,0)
  BACKGROUND_COLOUR = (0,0,0)
  
  # game set up
  pygame.init()
  screen = pygame.display.set_mode((WIDTH, HEIGHT))
  gameOver = False
  clock = pygame.time.Clock()
  font = pygame.font.SysFont("monospace", 25)
  pygame.display.set_caption('Through Space And Time')




  # background set up
  class BackgroundSprite(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load(image_file)
      self.rect = self.image.get_rect()
      self.rect.left, self.rect.top = location

  background = BackgroundSprite('space_image.jpg', [0,0])

  # sprite handling
  rocketImg = pygame.transform.scale(pygame.image.load('rocket.png'), [60, 100])
  def rocket(position):
     screen.blit(rocketImg, ((position[0] - 6), position[1]-20))

  meteorImg = pygame.transform.scale(pygame.image.load('meteor.png'), [50,50])
  def meteor(position):
    screen.blit(meteorImg, (position[0]-10, position[1]-10))






  # player variables
  playerSize = 50
  playerPos = [int(WIDTH/2), int(HEIGHT - 2*playerSize)]
  playerSpeed = playerSize/4
  bulletsList = []
  bulletSpeed = 5
  bulletSize = 10
  numberOfBullets = 2


  # enemy variables
  enemySize = 25
  enemyList = []
  numOfEnemies = 0 
  enemySpeed = 5







  # handles the levels
  def selectLevel(score):
    if score < 25:
      numOfEnemies = 2
      speed = 3
      playerSpeed = playerSize/7
      numberOfBullets = 2
    elif score > 24 and score < 50: 
      numOfEnemies = 4
      speed = 5
      playerSpeed = playerSize/6
      numberOfBullets = 3
    elif score > 49 and score < 300:
      numOfEnemies = 6
      speed = 8
      playerSpeed = playerSize/5
    elif score > 310 and score < 500:
      numOfEnemies = 8
      speed = 8
      playerSpeed = playerSize/4
    elif score > 550 and score < 800:
      numOfEnemies = 12
      speed = 10
      playerSpeed = playerSize/2
    elif score > 799 and score < 750:
      numOfEnemies = 12
      speed = 14
      playerSpeed = playerSize/4
    elif score > 760 and score <1600:
      numOfEnemies = 16
      speed = 12
      playerSpeed = playerSize/2
    else:
      numOfEnemies = 30
      speed = 18
      playerSpeed = playerSize
    return [speed, numOfEnemies, playerSpeed]




  # returns true if there is an overlap between the two paramaters and will return false if not
  def detectCollision(pos1, pos2, size1, size2):
    
    pos1X = pos1[0]
    pos1Y = pos1[1]

    pos2X = pos2[0]
    pos2Y = pos2[1]
      
    if (pos2X >= pos1X and pos2X < (pos1X + size1)) or (pos1X >= pos2X and pos1X < (pos2X + size2)):
      if (pos2Y >= pos1Y and pos2Y < (pos1Y + size1)) or (pos1Y >= pos2Y and pos1Y < (pos2Y + size2)):
        return True
    return False






  def generateBullet (bullets_list):
    if len(bullets_list) < numberOfBullets:
      xPos = int(playerPos[0]+20)
      yPos = int(playerPos[1])
      bulletsList.append([xPos, yPos])


  def drawBullets (bullets_list):
    for bulletPos in bullets_list:
      pygame.draw.rect(screen, RED, (bulletPos[0], bulletPos[1], bulletSize, bulletSize))
      

  def updateBulletPositions(bullets_list):
    i = -1
    for bulletPos in bullets_list:
      i += 1
      if bulletPos[1] > 40:
        bulletPos[1] -= bulletSpeed
      else:
        bulletsList.pop(i)


  def checkForBulletCollision(bullet_list, enemy_list, bulletSize, enemySize, score):
    j = -1
    for bulletPos in bullet_list:
      j += 1
      i = -1
      for enemyPos in enemy_list:
        i += 1
        if detectCollision(bulletPos, enemyPos, bulletSize, enemySize):
          score += 5
          enemyList.pop(i)
          bulletsList.pop(j)
    return score


  # adds an enemy to the enemyList if there is not 10 enemies 
  def generateEnemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < numOfEnemies and delay < 0.1:
      xPos = random.randint(0, WIDTH - enemySize)
      yPos = 0
      enemyList.append([xPos, yPos])


  # will draw the enemy to the screen
  def drawEnemies(enemies_list):
    for enemyPos in enemies_list:  
      #pygame.draw.rect(screen, BLUE, (enemyPos[0], enemyPos[1], enemySize, enemySize))
      meteor(enemyPos)


  # handles the positions of the enemies and makes them fall down the screen
  def updateEnemyPositions(enemyList, score):
   
    i = -1

    for enemyPos in enemyList:
      i += 1
      if enemyPos[1] >= 0 and enemyPos[1] < HEIGHT:
        enemyPos[1] += enemySpeed
      else:
        enemyList.pop(i) 
        score += 0.2
    return score


  # checks to see if there is an overlap of the player with any of the enemies
  def checkForEnemyCollision(enemy_list, playerPos, playerSize, enemySize):

    for enemyPos in enemy_list:
      if detectCollision(playerPos, enemyPos, playerSize, enemySize):
        return True
    return False



  # game loop
  while not gameOver:
    
    # changes some values in the game when the score gets to set values
    levelOutputs = selectLevel(score)
    enemySpeed = levelOutputs[0]
    numOfEnemies = levelOutputs[1]
    playerSpeed = levelOutputs[2]


    x = playerPos[0]
    y = playerPos[1]
    
    # event loop
    for event in pygame.event.get():
        
      # checks to see if the exit button has been clicked 
      if event.type == pygame.QUIT:
        sys.exit()
       
        # checks for left of right keypresses down and up
      if event.type == pygame.KEYDOWN:
              
        if event.key == pygame.K_LEFT:
          pressedLeft = True
        if event.key == pygame.K_RIGHT:
          pressedRight = True
        if event.key == pygame.K_SPACE:
          generateBullet(bulletsList)


      if event.type == pygame.KEYUP:
              
        if event.key == pygame.K_LEFT:
          pressedLeft = False
        if event.key == pygame.K_RIGHT:
          pressedRight = False

    # checks the state of the key and changes the player pos if state == true
    # updates the players position
    if pressedLeft:
      if (playerPos[0] > 1):
        x -= playerSpeed
        playerPos = [x,y]
    if pressedRight:
      if (playerPos[0] < WIDTH - playerSize):
        x += playerSpeed
        playerPos = [x,y]     



    # fills in the background 
    screen.fill(BACKGROUND_COLOUR)   
    screen.blit(background.image, background.rect)

    # generate enemies if needed
    generateEnemies(enemyList)
    
    # updates the enemies position
    score = updateEnemyPositions(enemyList, score)
    
    # will check to see if there is a collision and end the game if there is
    if checkForEnemyCollision(enemyList, playerPos, playerSize, enemySize):
      gameOver = True
      break
    
    # draws the enemies to the scree
    drawEnemies(enemyList)


    # will update the positon of the bullet on the screen
    updateBulletPositions(bulletsList)

    # checks to see if there is a collision with a bullet and an enemy
    # will remove the enemy if there is
    score = checkForBulletCollision(bulletsList, enemyList, bulletSize, enemySize, score)
    
    drawBullets(bulletsList)
    
    # draws the player to the screen 
    #pygame.draw.rect(screen, RED, (playerPos[0], playerPos[1], playerSize, playerSize))    
    rocket(playerPos)

    pygame.draw.rect(screen, BLACK, (-1, -1, WIDTH + 2, 25))
    
    scoreText = "Score: {}".format(round(score))
    scoreLabel = font.render(scoreText, 1, RED)
    
    bulletsText = "Bullets: {}".format(numberOfBullets)
    bulletsLabel = font.render(bulletsText, 1, RED)
    
    screen.blit(scoreLabel, ((WIDTH/2)-30, 5))
    screen.blit(bulletsLabel, ((WIDTH - 150), 5))


    clock.tick(30)
    pygame.display.update()
  startMenu(round(score))


startMenu()
