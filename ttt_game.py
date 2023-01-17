from random import randint
from ttt_interface import *
from ttt_minimax import *
 
'''
Tic-Tac-Toe board positions:
 
0|1|2
-|-|-
3|4|5
-|-|-
6|7|8
'''
class TTT_Game():
    def __init__(self):
        #start with an empty board
        self.gameBoard = self.getBlankBoard()
        self.gameOver = False
        self.gameBegun = False
        #bool for who's turn it is
        self.Xs_turn = True
        #set up the extra switch as game mode select
        setupExtraGPIO(self.chooseGameCallback)
        #this will hold game mode. Default is
        self.gameMode = 'OnePlayerOptimal'
        #bool used for asynchronously ending a game
        self.exit = False
        self.callingBack=False
       
    #flash all lights n times
    def flash(self, n):
        for j in range(n):
            print("flash")
            for i in range(9):
                turnOffX(i)
                turnOffO(i)
            time.sleep(.2)
            for i in range(9):
                turnOnX(i)
                turnOnO(i)
            time.sleep(.2)
            for i in range(9):
                turnOffX(i)
                turnOffO(i)
 
    #this function means the new game button has been pressed. Press to cycle through game modes
    def chooseGameCallback(self, pin):
        #this block is to ensure we exit all loops and thereby creates a fresh game
        #self.gameOver = True
        #self.Xs_turn = False
        #time.sleep(1)
        #self.Xs_turn = True
        #time.sleep(1)
        self.callingBack = True
        self.gameOver = False
        self.exit = True #this asynchronously exits game function
        print("game reset button pressed")
       
        # this button just starts a new game
        if (self.gameMode == 'OnePlayerOptimal'):
            self.gameMode = 'OnePlayerRandom'
        elif (self.gameMode == 'OnePlayerRandom'):
            self.gameMode = 'TwoPlayer'
        elif (self.gameMode == 'TwoPlayer'):
            self.gameMode = 'OnePlayerOptimal'
       
        while (self.exit == True):#this waits until the game function exits
            time.sleep(.50)
        print("loop exited")
        self.callingBack=False
       
       
 
 
           
        #self.gameBegun is still false after pressing this so we can cycle through  
 
   
    def findWinningLocations(self):#check for a win
        winningLocations = None
       
            #check for row wins
        if (self.gameBoard[0][0] == self.gameBoard[1][0] == self.gameBoard[2][0]) and (self.gameBoard[0][0] != '-'):
            winningLocations = [0, 0, 1, 0, 2, 0, self.gameBoard[0][0]]  
        if (self.gameBoard[0][1] == self.gameBoard[1][1] == self.gameBoard[2][1]) and (self.gameBoard[0][1] != '-'):
            winningLocations = [0, 1, 1, 1, 2, 1, self.gameBoard[0][1]]
        if (self.gameBoard[0][2] == self.gameBoard[1][2] == self.gameBoard[2][2]) and (self.gameBoard[0][2] != '-'):
            winningLocations = [0, 2, 1, 2, 2, 2, self.gameBoard[0][2]]
           
            #check for coulmn wins
        if (self.gameBoard[0][0] == self.gameBoard[0][1] == self.gameBoard[0][2]) and (self.gameBoard[0][0] != '-'):
            winningLocations = [0, 0, 0, 1, 0, 2, self.gameBoard[0][0]]  
        if (self.gameBoard[1][0] == self.gameBoard[1][1] == self.gameBoard[1][2]) and (self.gameBoard[1][0] != '-'):
            winningLocations = [1, 0, 1, 1, 1, 2, self.gameBoard[1][0]]
        if (self.gameBoard[2][0] == self.gameBoard[2][1] == self.gameBoard[2][2]) and (self.gameBoard[2][0] != '-'):
            winningLocations = [2, 0, 2, 1, 2, 2, self.gameBoard[2][0]]
           
        #check for diagonal wins
        if (self.gameBoard[0][0] == self.gameBoard[1][1] == self.gameBoard[2][2]) and (self.gameBoard[1][1] != '-'):
            winningLocations = [0, 0, 1, 1, 2, 2, self.gameBoard[0][0]]
        if (self.gameBoard[0][2] == self.gameBoard[1][1] == self.gameBoard[2][0]) and (self.gameBoard[1][1] != '-'):
            winningLocations = [0, 2, 1, 1, 2, 0, self.gameBoard[0][2]]
 
        return winningLocations
 
    def isPlayed(self, a, b):#check if a position has been played
        return (self.gameBoard[a][b] != '-')
 
    def makePlay(self, a, b, letter):#make a move
        print(letter +" is making play: ["+str(a)+"]["+str(b)+"]")
        if((letter == 'x') or (letter == 'o')):
            if (self.isPlayed(a, b) != True):
                self.gameBoard[a][b] = letter
                print("board:")
                print(str(self.gameBoard))
                if (letter == 'o'):
                    turnOnO(boardPositions[a][b])
                    self.Xs_turn = True
                elif (letter == 'x'):
                    turnOnX(boardPositions[a][b])
                    self.Xs_turn = False
 
               
    def playTwoPlayerGame(self):#begin a 2 player game
        self.gameBoard = self.getBlankBoard()
        self.gameOver = False
        self.gameBegun = False
        #bool for who's turn it is
        self.Xs_turn = True
               GPIO_Init()
        time.sleep(2)
        if(self.callingBack == False):
            self.flash(3)#flash 3 times
        while(self.gameOver == False):
            if(self.isTied() == True):#check for Ties
                self.flash(1)
                self.gameOver = True
            if (self.exit == True):#if reset button is pressed, exit.
                print("exiting")
                break
            setupGPIO(self.getPlayX)#set leds to light if corresponding buttons are pressed
            while(self.Xs_turn == True):
                if (self.exit == True):#if reset button is pressed, exit.
                    print("exiting")
                    break
                result = self.findWinningLocations()
                if (result != None):
                    self.Xs_turn = False
                    self.gameOver = True
                    print("X wins")
                    self.gameBegun = False
                    self.blink(result)
                    break
            if (self.exit == True):#if reset button is pressed, exit.
                print("exiting")
                break
            if(self.isTied() == True):#check for Ties
                self.flash(1)
                self.gameOver = True
            setupGPIO(self.getPlayO)#set leds to light if corresponding buttons are pressed
            while(self.Xs_turn == False):
                if (self.exit == True):#if reset button is pressed, exit.
                    print("exiting")
                    break
                result = self.findWinningLocations()
                if (result != None):
                    self.Xs_turn = True
                    self.gameBoard = True
                    print("O wins")
                    self.gameBegun = False
                    self.blink(result)
                    break
        self.exit = False#return control to asynchonous reset function. Only get here if reset asyncghronously
        print("exit2player")
    def playOnePlayerRandomGame(self):
 
        self.gameBoard = self.getBlankBoard()
        self.gameOver = False
        self.gameBegun = False
        #bool for who's turn it is
        self.Xs_turn = True
        GPIO_Init()
        time.sleep(2)
        if(self.callingBack == False):
            self.flash(2)#flash twice
        while(self.gameOver == False):
            if(self.isTied() == True):#check for Ties
                self.flash(1)
                self.gameOver = True
                break
            if (self.exit == True):#if reset button is pressed, exit.
                print("exiting")
                break
            setupGPIO(self.getPlayX)#set leds to light if corresponding buttons are pressed
            while(self.Xs_turn == True):
                if (self.exit == True):#if reset button is pressed, exit.
                    break
                result = self.findWinningLocations()
                if (result != None):
                    self.gameOver = True
                    self.Xs_turn = False
                    print("X wins")
                    self.gameBegun = False
                    self.blink(result)
                    break
            time.sleep(.15)#added wait because it looks cool
            if (self.exit == True):#if reset button is pressed, exit.
                print("exiting")
                break
            if(self.isTied() == True):#check for Ties
                self.flash(1)
                self.gameOver = True
                break
            while(self.Xs_turn == False):
                if (self.exit == True):#if reset button is pressed, exit.
                    print("exiting")
                    break
                #O guesses random locations. if it has been played already nothing will happen and a successful play will occur on a subsequent loop
                a = randint(0, 2)
                b = randint(0, 2)
                self.makePlay(a, b, 'o')
                result = self.findWinningLocations()
                if (result != None):
                    self.gameOver = True
                    self.Xs_turn = True
                    print("O wins")
                    self.gameBegun = False
                    self.blink(result)
                    break
        self.exit = False#return control to asynchonous reset function
        print("exit1playerrand")
               
    def playOnePlayerOptimalGame(self):#play an unwinnable game
        self.gameBoard = self.getBlankBoard()
        self.gameOver = False
        self.gameBegun = False
        #bool for who's turn it is
        self.Xs_turn = True
        GPIO_Init()
        time.sleep(2)
        if(self.callingBack == False):
            self.flash(1)#flash once
        while(self.gameOver == False):
            if(self.isTied() == True):#check for Ties
                self.flash(1)
                self.gameOver = True
                break
            if (self.exit == True):#if reset button is pressed, exit.
                print("exiting")
                break
            setupGPIO(self.getPlayX)#set leds to light if corresponding buttons are pressed
            while(self.Xs_turn == True):
                if (self.exit == True):#if reset button is pressed, exit.
                    print("exiting")
                    break
                result = self.findWinningLocations()
                if (result != None):
                    self.gameOver = True
                    self.Xs_turn = False
                    print("X wins")
                    self.gameBegun = False
                    self.blink(result)
                    break
            if (self.exit == True):#if reset button is pressed, exit.
                print("exiting")
                break
            time.sleep(.15)#added wait because it looks cool
            if(self.isTied() == True):#check for Ties
                self.flash(1)
                self.gameOver = True
                break
            while(self.Xs_turn == False):
                if (self.exit == True):#if reset button is pressed, exit.
                    print("exiting")
                    break
                a, b = findBestMove(self.gameBoard)
                print("minimax returned "+str(a)+", "+str(b))
                self.makePlay(a, b, 'o')
                result = self.findWinningLocations()
                if (result != None):
                    self.Xs_turn = True
                    self.gameOver = True
                    print("O wins")
                    self.gameBegun = False
                    self.blink(result)
                    break
        self.exit = False#return control to asynchonous reset function
        print("exit1playerOpt")
    #gets X's next move
    def getPlayX(self, pin):
        #if a play has been made the game has begun
        self.gameBegun = True
        #callback gives us the pin value. We need the key from the dictionary
        for key, value in Switch_Position.items():
            if value == pin:
                location = key
        col, row = self.getColumnAndRow(location)
        self.makePlay(row, col, 'x')
       
    #gets O's next move
    def getPlayO(self, pin):
        #callback gives us the pin value. We need the key from the dictionary
        for key, value in Switch_Position.items():
            if value == pin:
                location = key
        col, row = self.getColumnAndRow(location)
        self.makePlay(row, col, 'o')
       
    def blink(self, locations):#blinks the winning result until the game is reset
        if locations[6] == 'o':#if O won blink O
            #for i in range(3):#blink the winning row until an interrupt
            while(self.gameOver == True):
                turnOffO(3*locations[0] + locations[1])
                turnOffO(3*locations[2] + locations[3])
                turnOffO(3*locations[4] + locations[5])
                time.sleep(.25)
                turnOnO(3*locations[0] + locations[1])
                turnOnO(3*locations[2] + locations[3])
                turnOnO(3*locations[4] + locations[5])
                time.sleep(.25)
        else:#if X won blink X
            #for i in range(3):#blink the winning row until an interrupt
            while(self.gameOver == True):
                turnOffX(3*locations[0] + locations[1])
                turnOffX(3*locations[2] + locations[3])
                turnOffX(3*locations[4] + locations[5])
                time.sleep(.25)
                turnOnX(3*locations[0] + locations[1])
                turnOnX(3*locations[2] + locations[3])
                turnOnX(3*locations[4] + locations[5])
                time.sleep(.25)
    #find column and row of a position labeled 0 through 8
    def getColumnAndRow(self, position):
        return position % 3, position // 3
   
    def getBlankBoard(self):
        return [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]
   
    def isTied(self):
        foundBlank = False
        for i in range(9):
            c, r = self.getColumnAndRow(i)
            if(self.gameBoard[r][c] == '-'):
                foundBlank = False
        return foundBlank
 
   
if (__name__ == "__main__"):#main function
    game = TTT_Game()
    while(True):#Just choose a game to play. the rest is done asynchronously
        if (game.gameMode == 'OnePlayerOptimal'):
            print(game.gameMode)
            game.playOnePlayerOptimalGame()
        if (game.gameMode == 'OnePlayerRandom'):
            print(game.gameMode)
            game.playOnePlayerRandomGame()
        if (game.gameMode == 'TwoPlayer'):
            print(game.gameMode)
            game.playTwoPlayerGame
