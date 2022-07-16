'''Pong Game by Lorrin Shen'''
'''Bonuses: Highscore, Music/sound effects'''
import pygame
import time
import random
import pickle
pygame.init()

#game display dimensions
DISPLAY_WIDTH=900 
DISPLAY_HEIGHT=700

#colors
WHITE=(255,255,255)
BRIGHT_RED=(255,0,0)
RED=(150,0,0)
BRIGHT_GREEN=(0,255,0)
GREEN=(0,150,0)
BRIGHT_BLUE=(0,0,255)
BLUE=(0,0,150)
BLACK=(0,0,0)
GRAY=(200,200,200)
LIGHT_BROWN=(153,76,0)
SADDLE_BROWN=(139,69,19)
YELLOW=(200,200,0)
BRIGHT_YELLOW=(255,255,0)

#highscore and lives
highscore=0
lives=3

#make the game display, the window the game is run on
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

#set the name of the display
pygame.display.set_caption('Who Wood Pong')

#load in all images(backgrounds)
gameBackground=pygame.image.load('woodBackground.png')
menuBackground=pygame.image.load('menu2.jpg')
instructionsBackground=pygame.image.load('background3.jpg')

#load in music
backgroundMusic=pygame.mixer.music.load('crashBandicootTheme.mp3')
#play background music infinetly
pygame.mixer.music.play(-1)

#load in sound effects
oof=pygame.mixer.Sound('Oof.wav')
lose=pygame.mixer.Sound('sadTrombone.wav')

#set up clock later used for fps
clock = pygame.time.Clock()

def getBallDirection(x, y): #function that will return the direction the ball is travelling
    direction=str()
    if x*-1<0 and y *-1<0:
        direction='SE'
    if x*-1>0 and y*-1>0:
        direction='NW'
    if x*-1>0 and y*-1<0:
        direction='SW'
    if x*-1<0 and y*-1>0:
        direction='NE'
    if x==0 and y==0:
        direction='none'
    return direction

#function to draw the ball used in the game   
def ball(ballStartX, ballStartY, ballRadius): 
    pygame.draw.circle(gameDisplay, LIGHT_BROWN, [ballStartX, ballStartY], ballRadius)
    
#function to draw the paddle used in the game   
def paddle(paddleStartX, paddleStartY, paddleWidth, paddleHeight):
    pygame.draw.rect(gameDisplay, BLACK, [paddleStartX, paddleStartY, paddleWidth, paddleHeight])
    
#function that draws the rectangle that is the button to start the game
def startGameButton(buttonWidth, buttonHeight, buttonX, buttonY, color):
    pygame.draw.rect(gameDisplay, color, [buttonWidth, buttonHeight, buttonX, buttonY])
    
#function that draws the rectangle that is the button to quit the game    
def quitGameButton(buttonWidth, buttonHeight, buttonX, buttonY, color):
    pygame.draw.rect(gameDisplay, color, [buttonWidth, buttonHeight, buttonX, buttonY])
    
#function that draws the rectangle that is the button to go to the instructions
def rulesButton(buttonWidth, buttonHeight, buttonX, buttonY, color):
    pygame.draw.rect(gameDisplay, color, [buttonWidth, buttonHeight, buttonX, buttonY])
    
#function that draws the rectangle that is the button to go back to the menu   
def backButton(buttonWidth, buttonHeight, buttonX, buttonY, color):
    pygame.draw.rect(gameDisplay, color, [buttonWidth, buttonHeight, buttonX, buttonY])
    
#function that shows that you lose a life, and the oof sound plays. Then goes back to gameLoop
def ballOut():
    messageDisplay('-1 LIFE',RED , DISPLAY_WIDTH/2, DISPLAY_HEIGHT/2,100)
    pygame.display.update() #update display
    
    oof.play() #oof sound effect plays
    time.sleep(1) #wait for sound effect to finish
    
    gameLoop() #go back to the game
    
#create an invisible rectangle that holds text
def textObjects(text, font, color):    
    textSurface = font.render(text, True, color)    
    return textSurface, textSurface.get_rect()

#Display a message on screen
def messageDisplay(text,color, x,y,size):   
    largeText = pygame.font.Font('freesansbold.ttf', size) #font and size(size is given when function is called)
    textSurf, textRect = textObjects(text, largeText, color) 
    textRect.center = (x, y)    #where to put the message
    gameDisplay.blit(textSurf, textRect) #put message on the display of the game
    
#Victory message
def victoryScreen():
    gameExit = False
    while gameExit==False:
        
        cursor=pygame.mouse.get_pos() #get the position of the mouse cursor
        click=pygame.mouse.get_pressed() #detect if mouse is clicked
        buttonX=0
        buttonY=0
        buttonWidth=50
        buttonHeight=20
        r=random.randrange(0,255)
        g=random.randrange(0,255)
        b=random.randrange(0,255)
        randomColor=(r,g,b)
        
        for event in pygame.event.get(): #if user wants to exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        for i in range(1000): #delay on when the background changes color
            gameDisplay.fill(randomColor)
            
        messageDisplay('You Win!',BLACK,DISPLAY_WIDTH//2,DISPLAY_HEIGHT//2,150) #send message to user saying they win
        
        #Button to go back to menu. If the cursor is on the button make it light up, otherwise(else) have the button on screen
        if buttonX+buttonWidth>cursor[0]>buttonX and buttonY+buttonHeight>cursor[1]>buttonY:
            backButton(buttonX,buttonY,buttonWidth,buttonHeight,WHITE)
            messageDisplay('Back',BLACK,25,10,15)
            if event.type==pygame.MOUSEBUTTONDOWN: #if the button is clicked on go to menu
                menu()
        else:
            backButton(buttonX,buttonY,buttonWidth,buttonHeight,BLACK)
            messageDisplay('Back',WHITE,25,10,15)
            
        pygame.display.update() #update screen
        
#Lose message
def loseScreen():
    gameDisplay.blit(gameBackground, (0, 0)) #put background on screen
    
    messageDisplay('Game Over', RED, DISPLAY_WIDTH//2,DISPLAY_HEIGHT//2,100) #show message to user that they lose
    
    pygame.mixer.music.pause() #pause the background music
    lose.play()     #play the sound for when they lose
    
    pygame.display.update() #update screen
    
    time.sleep(5) #wait 5 seconds(for the lose sound to finish)
    pygame.mixer.music.unpause() #continue playing the background music where it left off
    
    menu() #go back to menu
    
#instructions screen
def instructions():
    gameExit = False
    while gameExit==False:
        
        cursor=pygame.mouse.get_pos() #get position of mouse cursor
        click=pygame.mouse.get_pressed() #detect if the mouse gets clicked
        buttonX=0
        buttonY=0
        buttonWidth=50
        buttonHeight=20
        
        for event in pygame.event.get(): #if user wants to exit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.blit(instructionsBackground, (0,0)) #put background on screen
        
        #Put instructions of the game on the screen for user to read
        messageDisplay('How to play:',GRAY,DISPLAY_WIDTH//2,200,40)
        messageDisplay('use the arrow keys to move',BLACK,DISPLAY_WIDTH//2,240,20)
        messageDisplay('the paddle to the right and to the left',BLACK,DISPLAY_WIDTH//2,260,20)
        messageDisplay('How the game works:',GRAY,DISPLAY_WIDTH//2,290,40)
        messageDisplay('Everytime the ball bounces off the paddle you get 1 point',BLACK,DISPLAY_WIDTH//2,320,20)
        messageDisplay('Reach 20 points and you win',BLACK,DISPLAY_WIDTH//2,340,20)
        messageDisplay('Everytime the ball gets past the paddle and hits the bottom of the screen you lose 1 life and points reset',BLACK,DISPLAY_WIDTH//2,360,18)
        messageDisplay("if you lose all 3 lives, it's game over and you have to restart",BLACK,DISPLAY_WIDTH//2,378,20)
        
##      pygame.draw.rect(gameDisplay, BLACK, [x,y,width,height])   <--how the dif variables are arranged when drawing a rectangle on screen
        pygame.draw.rect(gameDisplay, BLACK, [150,500,200,25])
        messageDisplay('the paddle',GRAY,250,480,25)
        pygame.draw.circle(gameDisplay, LIGHT_BROWN, [550, 510], 20)
        messageDisplay('the ball',GRAY,550,480,25)
        
        #Button to go back to menu. If the cursor is on the button make it light up, otherwise(else) have the button on screen
        if buttonX+buttonWidth>cursor[0]>buttonX and buttonY+buttonHeight>cursor[1]>buttonY:
            backButton(buttonX,buttonY,buttonWidth,buttonHeight,BRIGHT_YELLOW)
            messageDisplay('Back',BLACK,25,10,15)
            if event.type==pygame.MOUSEBUTTONDOWN: #if the button is clicked on go to menu
                menu()
        else:
            backButton(buttonX,buttonY,buttonWidth,buttonHeight,YELLOW)
            messageDisplay('Back',WHITE,25,10,15)
            
        pygame.display.update() #update screen
        
#the menu screen
def menu():
    gameDisplay.blit(menuBackground, (0, 0))
    menu=True
    #open the highscore file, and read it, whatever is on the file is the highscore, if there is nothing on the file(except) then the highscore is 0
    try:
        with open("highscore.txt", "rb") as file:
            highscore=pickle.load(file)
    except:
        highscore=0
        
    while menu:
        buttonWidth=150
        buttonHeight=50
        rulesButtonWidth=180
        startButtonX=DISPLAY_WIDTH*0.2
        buttonY=DISPLAY_HEIGHT*0.8
        quitButtonX=DISPLAY_WIDTH*0.8
        rulesButtonX=DISPLAY_WIDTH*0.47
        cursor=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        
        #Display the title of the game on screen
        messageDisplay("Who wood pong", LIGHT_BROWN, DISPLAY_WIDTH*0.56, DISPLAY_HEIGHT//2,100)
        
        for event in pygame.event.get(): #if user wants to exit
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #The button to start game. If the cursor is on the button make it light up    
        if startButtonX+buttonWidth>cursor[0]>startButtonX and buttonY+buttonHeight>cursor[1]>buttonY:
            startGameButton(startButtonX,buttonY,buttonWidth,buttonHeight,BRIGHT_GREEN)
            messageDisplay('Start',BLACK,250,590,50)
            if event.type==pygame.MOUSEBUTTONDOWN: #if button is clicked on start game.
                with open("lives.txt","wb") as file:    #open the lives file, clear everything in the file, write in 3 lives
                    pickle.dump(3,file)
                gameLoop()
            
        #The button to quit game. If the cursor is on the button make it light up   
        elif quitButtonX+buttonWidth>cursor[0]>quitButtonX and buttonY+buttonHeight>cursor[1]>buttonY:
            quitGameButton(quitButtonX,buttonY,buttonWidth,buttonHeight,BRIGHT_RED)
            messageDisplay('Quit',BLACK,790,590,50)
            if event.type==pygame.MOUSEBUTTONDOWN: #if button is clicked on quit game
                pygame.quit()
                quit()
                
        #The button to go to instructions screen. If the cursor is on the button make it light up       
        elif rulesButtonX+rulesButtonWidth>cursor[0]>rulesButtonX and buttonY+buttonHeight>cursor[1]>buttonY:
            rulesButton(rulesButtonX,buttonY,rulesButtonWidth,buttonHeight,BRIGHT_BLUE)
            messageDisplay('Instructions',BLACK,512,590,28)
            if event.type==pygame.MOUSEBUTTONDOWN: #if the button is clicked on go to instructions screen
                instructions()
                
         #have the buttons on screen
        else:
            startGameButton(startButtonX,buttonY,buttonWidth,buttonHeight,GREEN)
            messageDisplay('Start',WHITE,250,590,50)
            quitGameButton(quitButtonX,buttonY,buttonWidth,buttonHeight,RED)
            messageDisplay('Quit',WHITE,790,590,50)
            rulesButton(rulesButtonX,buttonY,rulesButtonWidth,buttonHeight,BLUE)
            messageDisplay('Instructions',WHITE,512,590,28)
            
            #display the highscore on screen
            messageDisplay('Highscore: '+str(highscore),BLACK,470,430,45)
            
        pygame.display.update() #update the screen
        clock.tick(60) #fps
        
#the game itself
def gameLoop():
    #velocity of paddle
    xVelocity=0
    #x and y of the paddle
    paddleStartY = 580
    paddleStartX = 350
    #dimensions of the paddle
    paddleWidth=200
    paddleHeight=25
    #x and y of the ball
    ballStartX=(DISPLAY_WIDTH//2)
    ballStartY=210
    #dimension of the ball
    ballRadius=20
    #velocity of the ball's x and y movements
    ballVelocityY=0
    ballVelocityX=0
    
    score=0
    counter=int()
    
    gameExit = False
    while gameExit==False:
        
        cursor=pygame.mouse.get_pos() #get position of mouse cursor
        click=pygame.mouse.get_pressed()
        #variables for back button
        buttonX=0
        buttonY=0
        buttonWidth=50
        buttonHeight=20
        
        for event in pygame.event.get(): #if the user exits
            if event.type == pygame.QUIT:
                if score>highscore:     #record their score if it is bigger than the highscore
                    with open("highscore.txt", "wb") as file: #open highscore file, remove preious highscore, put in new highscore
                        pickle.dump(score,file)
                with open("lives.txt","wb") as file: #reset the lives count to 3
                    pickle.dump(3,file)
                pygame.quit()
                quit()
                
            #movement of paddle   
            if event.type == pygame.KEYDOWN: #if there is a key down
                if event.key == pygame.K_LEFT:  #if the key is the left arrow, move the paddle to the left
                    xVelocity-=5
                if event.key == pygame.K_RIGHT:    #if the key is the right arrow, move the paddle to the right
                    xVelocity += 5
            if event.type == pygame.KEYUP: #if there is no key being pressed down, don't move the paddle
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    xVelocity=0
                    
        ballDirection=getBallDirection(ballVelocityX, ballVelocityY) #call function to get the direction of the ball
        
        if paddleStartX == DISPLAY_WIDTH-paddleWidth and xVelocity>0: #do not let the paddle go throught the right wall
            xVelocity=0
            paddleStartX=DISPLAY_WIDTH-paddleWidth
        if paddleStartX==0 and xVelocity<0: #do not let the paddle through the left wall
            xVelocity=0
            paddleStartX=0
            
        if ballStartY==210 and ballStartX==450 and ballDirection=='none': #if the ball gets reset to starting position, make it move(start game again)
            ballVelocityY=5
            ballVelocityX=5
            counter+=1
            if counter%2==1 or counter==0:
                ballVelocityX=5
            if counter%2==0 and counter!=0:
                ballVelocityX=5

        if ballStartY>=DISPLAY_HEIGHT: # if the ball gets past the paddle and hits the bottom of screen
            lives-=1 #take away a life
            if score>highscore: #if the score is bigger than the current highscore 
                    with open("highscore.txt", "wb") as file: #open highscore file, remove preious highscore, put in new highscore
                        pickle.dump(score,file)
            with open("lives.txt", "wb") as file: #open lives file, and change the value of lives
                pickle.dump(lives,file)
            with open("lives.txt", "rb") as file: #open lives file, read it and use the value as the lives left
                lives=pickle.load(file)
            if lives==0: #if user runs out of lives play oof sound, go to lose screen
                oof.play()
                time.sleep(1)
                loseScreen()
            ballStartX=(DISPLAY_WIDTH//2)
            ballStartY=210
            paddleStartY = 580
            paddleStartX = 350
            ballOut() #do what happens when the ball goes out
            
        if ballDirection =='SE': #if the ball is going towards bottom right
            if (ballStartY+ballRadius)==paddleStartY and (ballStartX+ballRadius>=paddleStartX and ballStartX-ballRadius<=(paddleStartX+paddleWidth)): #top of paddle,ball collision detection
                ballVelocityY*=-1 #change direction of ball
                score+=1    #add 1 to the score
                
            if ballStartX+ballRadius>=DISPLAY_WIDTH: #right wall,ball collision detection
                ballVelocityX*=-1 #change direction of ball
                
            if ballStartX+ballRadius<=paddleStartX and ballStartX+ballRadius>=paddleStartX and ballStartY+ballRadius>=paddleStartY and ballStartY-ballRadius<=paddleStartY+paddleHeight: #left side of paddle,ball collision detection
                ballVelocityY=2 #change direction of ball
                ballVelocityX*=-1
                ballStartX=paddleStartX-ballRadius-5 #move the ball away from paddle
                if ballStartX-ballRadius<=0: #if the ball hits left side of paddle and wall at the same time, make the ball go above the paddle
                    ballStartY=600
                    ballVelocityX=10  #change direction of ball
                    ballVelocityY=-10
                if xVelocity<0: #if the paddle is moving, make ball move with it when it comes in contact with side of paddle
                    ballStartX-=10 #change direction of ball
                    
            if ballStartX-ballRadius<=paddleStartX+paddleWidth and ballStartX-ballRadius>=paddleStartX and ballStartY-ballRadius>=paddleStartY and ballStartY-ballRadius<=paddleStartY+paddleHeight: #right side of paddle, ball collision detection 
                ballVelocityY=2 #change direction of ball
                ballStartX=(paddleStartX+paddleWidth)+ballRadius+5 #move ball away from paddle
                if ballStartX+ballRadius>=DISPLAY_WIDTH: #if ball is touching wall and right side of paddle, put the ball above the paddle
                    ballStartY=600
                    ballVelocityX=-10 #change direction of ball
                    ballVelocityY=-10
                if xVelocity>0: #if the paddle is moving, make ball move with it when it comes in contact with side of paddle
                    ballStartX+=10
                    
        if ballDirection =='SW': # if ball is going towards bottom left of screen
            if (ballStartY+ballRadius)==paddleStartY and (ballStartX+ballRadius>=paddleStartX and ballStartX-ballRadius<=(paddleStartX+paddleWidth)): #top of paddle, ball collision detection
                score+=1 #add 1 to score 
                ballVelocityY*=-1 #change direction of ball
                
            if ballStartX-ballRadius<=0: #left wall, ball collision detection
                ballVelocityX*=-1 #change direction of ball
                
            if ballStartX+ballRadius<=paddleStartX and ballStartX-ballRadius>=paddleStartX and ballStartY-ballRadius>=paddleStartY and ballStartY+ballRadius<=paddleStartY+paddleHeight: #left side of paddle, ball collision detection
                ballVelocityY=2 #change directionof ball
                ballStartX=paddleStartX-ballRadius-5 #move ball away from paddle
                if ballStartX-ballRadius<=0: #if the ball is touching the left side of the paddle and the left wall, put the ball above the padle
                    ballStartY=600
                    ballVelocityX=10 #change direction of ball
                    ballVelocityY=-10
                if xVelocity<0:  #if the paddle is moving, make ball move with it when it comes in contact with side of paddle
                    ballStartX-=10
                    
            if ballStartX-ballRadius<=paddleStartX+paddleWidth and ballStartX-ballRadius>=paddleStartX and ballStartY-ballRadius>=paddleStartY and ballStartY-ballRadius<=paddleStartY+paddleHeight: #right side of paddle, ball collision detection
                ballVelocityY=2 #change direction of ball
                ballVelocityX*=-1
                ballStartX=(paddleStartX+paddleWidth)+ballRadius+5 #move ball away from paddle
                if ballStartX+ballRadius>=DISPLAY_WIDTH: #if ball is touching wall and right side of paddle, put the ball above the paddle
                    ballStartY=600
                    ballVelocityX=-10 #change direction of ball
                    ballVelocityY=-10
                if xVelocity>0: #if the paddle is moving, make ball move with it when it comes in contact with side of paddle
                    ballStartX+=10
                    
        if ballDirection =='NE': #if ball is moving towards top right of screen
            if ballStartY-ballRadius<=0: #top wall, ball collision detection
                ballVelocityY=5 #change direction of ball
                
            if ballStartX+ballRadius>=DISPLAY_WIDTH: #right wall, ball collision detection
                ballVelocityX=-5 #change direction of ball
                
        if ballDirection =='NW': #f ball is moving towards top left of screen
            if ballStartY-ballRadius<=0: #top wall, ball collision detection
                ballVelocityY=5 #change direction of ball
                
            if ballStartX-ballRadius<=0: #left wall, ball collision detection 
                ballVelocityX=5 #change direction of ball

        #put in the background
        gameDisplay.blit(gameBackground, (0, 0))

        #Button to go back to menu. If the cursor is on the button make it light up
        if buttonX+buttonWidth>cursor[0]>buttonX and buttonY+buttonHeight>cursor[1]>buttonY:
            backButton(buttonX,buttonY,buttonWidth,buttonHeight,BRIGHT_RED)
            messageDisplay('Back',BLACK,25,10,15)
            if event.type==pygame.MOUSEBUTTONDOWN: # if the button is clicked go to menu
                if score>highscore: #if the current score is bigger than highscore
                    with open("highscore.txt", "wb") as file: #open highscore file and replace highscore value with new highscore
                        pickle.dump(score,file)
                with open("lives.txt","wb") as file: #reset lives to 3
                    pickle.dump(3,file)
                menu()
        #if the cursor is not on the back button, draw it there.
        if (buttonX+buttonWidth>cursor[0]>buttonX and buttonY+buttonHeight>cursor[1]>buttonY)==False:
            backButton(buttonX,buttonY,buttonWidth,buttonHeight,RED)
            
        #display word 'back' on button to describe what button does
        messageDisplay('Back',GRAY,25,10,15)

        #if the user gets a score of 20
        if score==20:
            with open("highscore.txt", "wb") as file: #set highscore to 20
                pickle.dump(20,file)
            with open("lives.txt","wb") as file: #reset lives
                pickle.dump(3,file)
            victoryScreen() # go to the victory screen 
        else:
            messageDisplay("Score: "+str(score),BLACK,DISPLAY_WIDTH-40,10,15) # otherwise show score on screen while playing
            
        try:
            with open("lives.txt", "rb") as file: #open and read lives file to set the amount of lives left
                lives=pickle.load(file)
        except: #if nothing is in the lives file, default the lives count to 3
            lives=3
            
        paddleStartX+=xVelocity #paddle movement
        paddle(paddleStartX, paddleStartY, paddleWidth, paddleHeight) #draw paddle on screen
        
        ball(ballStartX, ballStartY, ballRadius) #draw ball on screen
        ballStartX+=ballVelocityX #ball movement
        ballStartY+=ballVelocityY #ball movement

        messageDisplay("Lives: "+str(lives),WHITE,paddleStartX+(paddleWidth//2),paddleStartY+(paddleHeight//2),20) #show user how many lives they have left on the paddle
        
        pygame.display.update() #update screen
        clock.tick(60) # fps

menu() #run the menu first, then run according to user
