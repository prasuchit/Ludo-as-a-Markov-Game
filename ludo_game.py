import h5py
import graphics
import random
import os.path
from os import path
import numpy as np
import optimalAction
from time import sleep
from tkinter import Button, Label, PhotoImage, simpledialog
import pandas as pd
import time

c = 0                              #initializing variable and flags that are to be used in the game
cx = 0
cy = 0
lx = 0
bb = 0
nc = 0
rollc = 0

RED = graphics.RED
BLUE = graphics.BLUE
YELLOW = graphics.YELLOW
GREEN = graphics.GREEN
PLAYER_NAMES = ["Red", "Blue", "Yellow", "Green"] #Strings for each player's name.
whose = RED #The player whose turn it is. Can be adjusted later to choose a new player to go first.
rolled = False #Originally "TURN." Tracks if the rolls for a given player have finished.
box = 0
cboxes = 0
homes = 0
players = 0
# REDKILL = False
# BLUEKILL = False
# GREENKILL = False
# YELLOWKILL = False

#What type of player is playing for each color: a human, a random player, or a rational agent.
playerTypes = []
HUMAN = 0
RANDOM = 1
RATIONAL = 2

winners = [0, 0, 0, 0] #The win count for each player.

qTable = [] #The q table!
policies = [] #The policies! (Not needed?)
gamma = 0.5 #The discount value is quite low because the game is so unpredictable, so immediate reward takes priority.
alpha = 1 #The learning rate, which decays as the agent explores.
decay = .9999954 #The decay rate, which determines how long the agent learns.
learn = False #Whether or not the agent is supposed to learn. Change to false when the agent is done learning.
nextGame = False #Determines whether or not to loop into the next game if the current game finishes.
                #True if learning overnight / gathering data of games. False if troubleshooting or playing with humans (or demonstrating?).

totalActions = [i for i in range(24)] #All actions available to every player.
actionMaxAt = [[i,i,i,i] for i in range(24)]

done = False #Checks if the game is over. The game ends when someone wins.

rolls = [0, 0, 0] #The rolls of each die.

#Feature names.
DANGER = 0
SAFETY = 1
KILL = 2
GOAL = 3
DOUBLE = 4
DEPLOY = 5
GENERIC = 6

root = graphics.root
root.lift()
# root.attributes('-topmost',True)
# root.attributes('-fullscreen',True)
root.after_idle(root.attributes,'-topmost',False)
# Creating a photoimage object to use image 
dice = PhotoImage(file = r"dice.gif") 

#Likewise, create an image for each side of the die.
sides = [PhotoImage(file = r"die1.gif"),
         PhotoImage(file = r"die2.gif"),
         PhotoImage(file = r"die3.gif"),
         PhotoImage(file = r"die4.gif"),
         PhotoImage(file = r"die5.gif"),
         PhotoImage(file = r"die6.gif")]

#Number of games to be played.
GAME_COUNT = 1 #Adjust as needed!
games_played = 0 #Number of games that have been played.

#Prints the given player's turn.
def turn():
    L2 = Label(root, text= PLAYER_NAMES[whose] + "'s Turn    ", fg='Black', 
               background= PLAYER_NAMES[whose].lower(), font=("Arial", 24, "bold"))
    L2.place(x=770, y=50)
    
def clear():        #clears all the variable prior to next player's turn
    L1 = Label(root, text="                                       ", image = "", fg='Black', background='green', font=("Arial", 48, "bold"))
    L1.place(x=770, y=200)
    L3 = Label(root, text="        ", image = "", fg='Black', background='green', font=("Arial", 48, "bold"))
    L3.place(x=800, y=250)
    L4 = Label(root, text="        ", image = "", fg='Black', background='green', font=("Arial", 48, "bold"))
    L4.place(x=800, y=300)
    if not done:
        turn()
        
#Make the Q table and populate it either with values from a txt, or initialized to 0.
def makeQTable(qFile):
    global qTable
    #The size of the q table has to be realized in advance. Its dimensions are like so...
    #The number of players: 4.
    #The number of states: 2401 (the configuration of features).
    #The actions available for each player: 4 pieces, 6 actions each (for each die roll) = 24 actions... and 4 players.
    
    if (qFile): #If there is a q file here, populate the q table with those values.
        print("Loading Q table.")
        start = time.time()
        with h5py.File(qFile, 'r') as hf:
            qTable = hf['qSet'][:]
        elapsed = time.time() - start
        print(f"Loaded Q table in {elapsed} seconds.")
        # df = pd.read_csv(qFile)
        # qTable = df.values

        # f = open(qFile, 'rb')
        # qTable = np.reshape((np.load(f)), (4, 2401, 24, 24, 24, 24))
        # # qTable = np.reshape(qTable, (4, 2401, 24, 24, 24, 24))
        # f.close()
    else:
        qTable = np.zeros((4, 2401, 24, 24, 24, 24), dtype=float)

#Make the policy and populate it only if learning is false (thus it can be referenced for all decision making).        
def makePolicy(pFile):
    global policies
    # policies = np.zeros((2401, 6), dtype=int)
    if pFile:
        f = open(pFile, 'rb')
        policies = np.load(f)
        f.close()
    
def makeBoard():
    global box, cboxes, homes, players, playerTypes, whose, done
    
    graphics.initBoard(False, False, '1000x750', 'green', "Ludo as a Markov Game", "logos.txt")
    graphics.drawBoard()
    #These variables are ported over from the graphics module to shorten notation.
    box = graphics.box
    cboxes = graphics.cboxes
    homes = graphics.homes
    players = graphics.players
    #The user is then asked to give a mixture humans versus computers, if it's the first game.
    if games_played == 0:
        # humans = simpledialog.askinteger("Input", "How many humans are participating?", parent=root, minvalue=0, maxvalue=4)
        humans = 0  # Test input, comment out later
        randoms = 0
        rationals = 0
        #If there are any computers participating, the user is asked how many of those computers are to be random players.
        if humans < 4:  
            # randoms = simpledialog.askinteger("Input", "Of the computers, how many do you want to play randomly?", 
            #                                  parent=root, minvalue=0, maxvalue=(4 - humans))
            randoms = 2 # Test input, comment out later
            rationals = 4 - humans - randoms
            
            #Need to pull in the q table if there are any rational agents.
            if rationals > 0:
                # qTable = makeQTable('qTable.h5' if path.exists('qTable.h5') else None) #Probably don't need this if we're done learning 'qTable.csv'
                policies = makePolicy('policies.npy')
                # print("Done.")
            
        #With the split of players decided, they are now distributed to the playertypes list.
        for _ in range(humans):
            playerTypes.append(HUMAN)
        for _ in range(randoms):
            playerTypes.append(RANDOM)
        for _ in range(rationals):
            playerTypes.append(RATIONAL)
        print(playerTypes)
    
    #Last thing to do is decide who goes first.
    whose = random.randint(0,3)
    turn()
    
    #The game, of course, isn't done, it just got started.
    done = False
    
    #Also if there's any weirdness with the labels, that can be fixed.
    clear()
    
def main():                                 # Main game function.
    global box, cboxes, homes, players, playerTypes, whose, games_played
    if c == 0:                              #constructs the game pieces first time the code is ran.
        makeBoard()

    else:
        while games_played < GAME_COUNT:
            aTurns()
            if games_played < GAME_COUNT:
                makeBoard()

        typeNames = []
        for i in range(len(playerTypes)):
            typeNames.append("Human" if playerTypes[i] == 0 else ("Random" if playerTypes[i] == 1 else "Rational")) #Still gross!
        print(f"Types: {typeNames}")
        print(f"Results: {winners}")

    # elif not done:
    #     #What turn we take depends on the type of player at hand.
    #     #The non-human players can go automatically.
    #     aTurns()
    #     #With the AI turns out of the way (and they'll always be next to each other), the human(s) take their turns.
    #     if not done:
    #         playTurn()
    #     elif learn and (RATIONAL in playerTypes): #A qTable only exists if there is a rational agent, but if the game is done, save the policy and q values.
    #         #First save the qTable...
    #         print(f"Games played: {games_played}")
    #         if (games_played % 10) == 0:
    #             print("Game finished; writing to file.")
    #             start = time.time()
    #             with h5py.File('qTable.h5', 'w') as hf:
    #                 hf.create_dataset("qSet",  data=qTable)
    #             elapsed = time.time() - start
    #             print(f"Finished writing in {elapsed}.")
    #         # df = pd.DataFrame(qTable)
    #         # df.to_csv('qTable.csv',index=False)
    #         # f = open('qTable.npy', 'wb')
    #         # np.save(f, qTable)
    #         # f.close()
    #         #... now the policy.
    #         f = open('policies.npy', 'wb')
    #         np.save(f, policies)
    #         f.close()
    #         #Also, if we're repeating the games and the threshold hasn't been reached, go at it again!
    #         if (learn and alpha >= .1) or (games_played < GAME_COUNT):
    #             makeBoard()
    #             main()
    #         #But if the games are done, report on the results.
    #         else:
    #             typeNames = []
    #             for i in range(len(playerTypes)):
    #                 typeNames.append("Human" if playerTypes[i] == 0 else ("Random" if playerTypes[i] == 1 else "Rational")) #Gross.
    #             print(f"Types: {typeNames}")
    #             print(f"Results: {winners}")
        
    #     #If we're learning, the criteria for doing another game is if the learning rate is still above a certain threshold (.1 by default).
    #     #If we're not learning, then we just go to the desired threshold of games.
    #     if (learn and alpha >= .1) or (games_played < GAME_COUNT):
    #         games_played += 1
    #         makeBoard()
    #     #And otherwise, let's show the results.
    #     else:
    #         typeNames = []
    #         for i in range(len(playerTypes)):
    #             typeNames.append("Human" if playerTypes[i] == 0 else ("Random" if playerTypes[i] == 1 else "Rational")) #Still gross!
    #         # print(f"Types: {typeNames}")
    #         # print(f"Results: {winners}")
        

main()    #Main function is called once when c==0 to initialize all the gamepieces.

def playTurn():
    global RED, BLUE, YELLOW, GREEN, dice, rolled, bb, c, cx, cy, rolls, whose, nc, won
    #This process will need to be explained a bit more thoroughly now that there's the same logic for all players.
    if rolled: #A player's turn only goes if they are done rolling.
        #For now, console information will be displayed, but we probably should do away with this in the finished product.
        # print(PLAYER_NAMES[whose] + "'s turn")
        # print("Moves available: ")
        
        if (movecheck(players[whose], cboxes[whose], PLAYER_NAMES[whose])) == False: #If no move is available, pass the turn.
            passTurn()
            #This has to get added whenever the turn is passed, in case the next player is an AI.
        else: #Check for a click on a player's own game piece.
            for i in range(len(players[whose])):
                if ((((cx > players[whose][i].x0 + 13) and (cx < players[whose][i].x + 13)) and #Home spots.
                ((cy > players[whose][i].y0 + 14) and (cy < players[whose][i].y + 14))) and
                (players[whose][i].x0 == homes[whose][i].x) and (players[whose][i].y0 == homes[whose][i].y)):
                    # print("Player at home.")
                    if rolls[0 + nc] == 6: #If there's a 6 and a piece at home...
                        #^ THIS PART MAY BE ANOTHER ISSUE WITH THE ORIGINAL CODE.
                        movePiece(i, 0)
                        nc = nc + 1
                        
                        if nc >= len(rolls) or rolls[nc] == 0: #Checks if all rolls have been used. If so, pass the turn.
                            passTurn()
                            
                #This is a point of divergence between the colors--the coordinates for the last if-clause.
                #As a result, a new function has to be made that handles the rest of the logic that follows here.
                
                if (((cx > players[whose][i].x0 + 13) and (cx < players[whose][i].x + 13)) and 
                    ((cy > players[whose][i].y0 + 14) and (cy < players[whose][i].y + 14))):
                    #We need a flag to check if the move can actually be made for the given player.
                    validMove = False
                    #Red check.
                    if (whose == RED) and (players[whose][i].x0 > 270 or players[whose][i].y0 > 270):
                        validMove = True
                    elif (whose == BLUE) and (players[whose][i].x0 > 270 or players[whose][i].y0 < 470):
                        validMove = True
                    elif (whose == YELLOW) and (players[whose][i].x0 < 470 or players[whose][i].y0 < 470):
                        validMove = True
                    elif (whose == GREEN) and (players[whose][i].x0 < 470 or players[whose][i].y0 > 270): # < 470?
                        validMove = True
                    
                    #If the previous if-clause is satisfied for the given player, we can move on with the rest.
                    
                    if (validMove):
                        # print("Player somewhere else.")
                        bb = ((players[whose][i].num) + rolls[nc]) #bb here is the number of spaces traversed.
                        
                        if bb > 56:
                            break #Can't move greater than the allowed number of spaces.
                        
                        #These variables will shorten the notation for the kill call.
                        nex = (whose + 1) % 4 #The player after the current one. ("next" is a keyword.)
                        after = (whose + 2) % 4 #The player after that.
                        last = (whose + 3) % 4 #The last player in the line.
                        kill(cboxes[whose], players[nex], players[after], players[last], homes[nex], homes[after], homes[last])
                        
                        movePiece(i, bb)
                        doublecheck(players[whose]) #Check to see if a piece can be made a double.
                        
                        nc = nc + 1
                        
                        #Goal and win check.
                        goalCheck(i)
                        
                        if nc >= len(rolls) or rolls[nc] == 0: #Checks if all rolls have been used. If so, pass the turn.
                            passTurn()
                        break

def movePiece(whichPiece, whereTo):
    global players, cboxes, whose
    
    players[whose][whichPiece].x0 = cboxes[whose][whereTo].x
    players[whose][whichPiece].y0 = cboxes[whose][whereTo].y
    players[whose][whichPiece].x = cboxes[whose][whereTo].x + 25
    players[whose][whichPiece].y = cboxes[whose][whereTo].y + 25
    players[whose][whichPiece].num = whereTo
    players[whose][whichPiece].swap()

def movecheck(player, pbox, pname): #Check if the player can make a move. The new and improved version!
    if rolls[2] == 6: #If the third die rolled a 6, so did the first two. Three 6's means the turn ends.
        return False
     
    if not player: #If a player has no pieces left, they have won.
        # print("This player is done.")
        pass
        #TODO: ADD MORE HANDLING FOR WIN CONDITION
         
    #The CURRENT roll has to be checked.
    #If the current roll is a 6 and any pieces are at home, a move can be made.
    if rolls[nc] == 6:
        for i in range(len(player)):
            if (player[i].num == - 1):
                return True
    #If the current roll is NOT a 6, at least one piece is fielded, and the roll
    #would not cause the piece to overshoot the goal, a move can be made.
    else:
        for i in range(len(player)):
            if (player[i].num != -1 and player[i].num + rolls[nc] <= 56):
                return True
             
    #If we made it this far, there is no valid move to be made with the current roll.
    return False
    
#Passes the turn to the next player. Combined with clear() since they always occur together.                       
def passTurn():
    global nc, rolls, rolled, L1, L3, L4, whose
    whose = (whose + 1) % 4 #Passes the turn to the next player.
    
    #This can likely be removed now that if one player wins, the game is done.
#     #If the next player has won, skip their turn.
#     while (won[whose]):
#         whose = (whose + 1) % 4
    
    nc = 0 #Resets the number of rolls to 0.
    for i in range(len(rolls)):
        rolls[i] = 0 #Resets the dice to "unrolled."
    rolled = False #The next player has yet to roll as the turn passes.
    L1 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 48, "bold"))
    L1.place(x=800, y=200)
    L3 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 48, "bold"))
    L3.place(x=800, y=250)
    L4 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 48, "bold"))
    L4.place(x=800, y=300)
    turn()

def kill(a,b,c,d,bh,ch,dh):   #function that determines if a gamepiece can be killed

    #if the game piece is not on a stop
    if ((a[bb].x0 != box[1].x and a[bb].y0 != box[1].y) and (a[bb].x0 != box[14].x and a[bb].y0 != box[14].y) and
        (a[bb].x0 != box[9].x and a[bb].y0 != box[9].y) and (a[bb].x0 != box[22].x and a[bb].y0 != box[22].y) and
        (a[bb].x0 != box[27].x and a[bb].y0 != box[27].y) and (a[bb].x0 != box[35].x and a[bb].y0 != box[35].y) and
        (a[bb].x0 != box[40].x and a[bb].y0 != box[40].y) and (a[bb].x0 != box[48].x and a[bb].y0 != box[48].y)):


        #if the game piece of another color and its on the same block and it is not a double, a kill is made
        for i in range (len(b)):
            if (b[i].x0 == a[bb].x and b[i].y0 == a[bb].y and (b[i].double == False)):
                b[i].x0 = bh[i].x
                b[i].y0 = bh[i].y
                b[i].x = bh[i].x + 25
                b[i].y = bh[i].y + 25
                b[i].num=-1
                b[i].swap()
                break

        for i in range (len(c)):
            if (c[i].x0 == a[bb].x and c[i].y0 == a[bb].y and (c[i].double == False)):
                c[i].x0 = ch[i].x
                c[i].y0 = ch[i].y
                c[i].x = ch[i].x + 25
                c[i].y = ch[i].y + 25
                c[i].num=-1
                c[i].swap()
                break

        for i in range (len(d)):
            if (d[i].x0 == a[bb].x and d[i].y0 == a[bb].y and (d[i].double == False)):
                d[i].x0 = dh[i].x
                d[i].y0 = dh[i].y
                d[i].x = dh[i].x + 25
                d[i].y = dh[i].y + 25
                d[i].num=-1
                d[i].swap()
                break

def doublecheck(a):        #makes a double is two or more gamepieces on top of another.

    for k in range (len(a)):
        a[k].double = False

    for i in range (len(a)):
        for j in range (len(a)):
            if (a[i].num == a[j].num) and (i != j):
                a[j].double = True
                a[i].double = True

def leftClick(event):  # Main play function is called on every left click.

    global c, cx, cy, RED, YELLOW
    c = c + 1
    cx = root.winfo_pointerx() - root.winfo_rootx()  # This formula returns the x,y co-ordinates of the mouse pointer relative to the board.
    cy = root.winfo_pointery() - root.winfo_rooty()

    # print("Click at: ", cx, cy)

    main()           #Main function called on every click to progress the game


root.bind("<Button-1>", leftClick)


def roll():   #Rolls a die, and repeats if it's a 6.
    global rollc, rolls, rolled, die

    if rolled == False:
        rollc = rollc + 1
        # print("roll: ", rollc)
        #Unfortunately due to the quirks of tkinter, this can't really be condensed, just changed to match the notation.
        #(Actually it could be changed with a list, but ehhhh it's fine.)
        if rollc == 1:
            die = random.randint(1, 6)
            L1 = Label(root, text=str(die), image = sides[die - 1], fg='Black', background='green', font=("Arial", 24, "bold")) #text?
            L1.place(x=800, y=200)
            # print("dice: ", die)
            rolls[0] = die
            if die != 6:
                rollc = 0
                rolled = True

        elif rollc == 2:
            if die == 6:
                die = random.randint(1, 6)
                L3 = Label(root, text=str(die), image = sides[die - 1], fg='Black', background='green', font=("Arial", 24, "bold"))
                L3.place(x=800, y=250)
                # print("dice: ", die)
                rolls[1] = die
                if die != 6:
                    rollc = 0
                    rolled = True

        else:
            if die == 6:
                die = random.randint(1, 6)
                L4 = Label(root, text=str(die), image = sides[die - 1], fg='Black', background='green', font=("Arial", 24, "bold"))
                L4.place(x=800, y=300)
                # print("dice: ", die)
                rolls[2] = die
                rollc = 0
                rolled = True

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#New non-agent functions!!!

#Checks if the given piece has reached the goal.
def goalCheck(piece):
    if players[whose][piece].num == 56: #If a piece went all the way, it's gone.
        players[whose].remove(players[whose][piece])
        #A piece reached the goal; check to see if that player has won.
        winCheck()

def winCheck():
    global done, games_played, winners
    if not players[whose]: #If a player has no pieces left, they all reached the goal.
        games_played += 1
        winners[whose] += 1 #The given player has won yet another game.
        done = True
        clear() #Still has its use outside of passTurn().
        L1 = Label(root, text= PLAYER_NAMES[whose] + " Wins!             ", fg='Black', 
        background= PLAYER_NAMES[whose].lower(), font=("Arial", 24, "bold"))
        L1.place(x=770, y=200)
        

#Rolls all the dice one can for their turn.
def rollDice():
    while not rolled:
        roll()
    
#Returns the indices of the pieces that can move.        
def getValidMoves():
    validIndices = [] #The indices to be returned.
    
    for i in range(len(players[whose])):
        spot = players[whose][i].num #The current piece's position.
        #If the given piece is at home and the roll is a 6, that piece can move.
        if spot == -1 and rolls[nc] == 6 and not isBlocked(True, i):
            validIndices.append(i)
        #Otherwise, if the player isn't at home and the roll wouldn't overshoot the goal, that piece can move.
        elif spot > -1 and ((spot + rolls[nc]) <= 56) and not isBlocked(False, i):
            validIndices.append(i)
            
    return validIndices

#Checks if the desired move would be blocked by the double of another player.
#The logic for the block check differs slightly depending of if the player is at home or note.
def isBlocked(atHome, which):
    for i in range(3): #Stands for each of the players.
        #For all but one piece for that player--if the last is doubled, so is something else.
        otherTurn = (whose + i + 1) % 4
        for j in range(len(players[otherTurn]) - 1):
            otherSpot = players[otherTurn][j].num
            #Only need to check the piece if it's a double and on the outer ring.
            if players[otherTurn][j].double and otherSpot >= 0 and otherSpot <= 50:
                relativeSpot = ((otherSpot + (3 - i) * 13) % 50) #Other player's spot from the current player's perspective.
                #If the spot is at home, only the starting spot needs to be checked.
                if atHome and relativeSpot == 0:
                    return True
                #If the spot is not home, then the relative locations of the pieces have to be checked.
                else:
                    distance = relativeSpot - players[whose][which].num #If positive, the other piece is "in front."
                    #If the player is behind the doubled piece, and the movement would put them at or in front of it, it won't work.
                    if (distance > 0) and players[whose][which].num + rolls[nc] >= relativeSpot:
                        return True
                    
    #If we get through all that, there are no doubles in the piece's way.
    return False
                    
#The end of the new functions!!!
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

turn()            #prints "Red's turn" initially

button = Button(root, text="    Roll    ", image = dice, relief="raised", font=("Arial", 20),  command=roll)  # call roll function evertime this button is clicked
button.place(x=835, y=120)
























#-----Agent functions, behavior, and so on!-----
#All functions for agent behavior will be prefixed with an "a" to make it easy to differentiate.  

#Get the "feature" number of a given piece. A piece could be in multiple situations, but these describe the order of priority.
#0: Danger! (any enemy piece is 1 to 6 spaces behind)
#1: Safety opportunity (your piece is within 1 to 6 spaces of the home stretch)
#2: Attack opportunity (any enemy piece is 1 to 6 spaces in front)
#3: Goal opportunity (your piece is within 1 to 6 spaces of the goal)
#4: Double opportunity (your piece is within 1 to 6 spaces of another piece of yours)
#5: Deploy opportunity (your piece can leave home)
#6: Generic (none of the conditions are met)
def getFeature(state, player, position):
    nex = (player + 1) % 4 #The player after the current one. ("next" is a keyword.)
    after = (player + 2) % 4 #The player after that.
    last = (player + 3) % 4 #The last player in the line.
    
    #The difference in location between this piece and the other players' can find both danger and kill checks.
    #Also, it doesn't matter which player causes the danger or kill, just that it's there, so this list can be 1D!
    distances = []
    for i in range(len(state[nex])):
        otherSpot = state[nex][i] #Similar logic for blocking.
        if (otherSpot != -1):
            relativeSpot = ((otherSpot + (3) * 13) % 50) #Other player's spot from the current player's perspective.
            distances.append(position - relativeSpot)
    for i in range(len(state[after])):
        otherSpot = state[after][i]
        if (otherSpot != -1):
            relativeSpot = ((otherSpot + (2) * 13) % 50) #Other player's spot from the current player's perspective.
            distances.append(position - relativeSpot)
    for i in range(len(state[last])):
        otherSpot = state[last][i]
        if (otherSpot != -1):
            relativeSpot = ((otherSpot + (1) * 13) % 50) #Other player's spot from the current player's perspective.
            distances.append(position - relativeSpot)
        
    
    #Danger check: if the player's piece isn't at or past the home stretch and the distance is between -1 and -6, it's in danger.
    if position < 51:
        for distance in distances:
            if distance > -7 and distance < 0:
                return DANGER
    
    #Check for safety: if the player is within 6 spaces of the home stretch (between spaces 45 and 50), they can enter the home stretch..
    if position < 50 and position > 44:
        return SAFETY
    
    #Check for kill chances: if the player's piece + the distance to the other piece would still be in the outer ring, and that difference
    #is below 7, then a kill can be made. Not even worth checking if the piece is on the home stretch or one spot from it.
    if position < 49:
        for distance in distances:
            if distance > 0 and distance < 7 and (position + distance) < 50:
                return KILL
    
    #Check for the chance to move into a goal: if the piece is within 5 spaces of the goal (not 6, due to safety check), it can reach the goal.
    if position > 50 and position < 56:
        return GOAL
    
    #Check for the chance to get a double: if any of the other of the player's pieces are within 6 spaces (not at home/goal), can double.
    for i in range(len(state[player])):
        if state[player][i] != - 1 and position != -1:
            pieceDistance = state[player][i] - position
            if pieceDistance > 0 and pieceDistance < 7: #Inherently excludes the piece(s) on the same spot; this is the opportunity to MAKE a double.
                return DOUBLE
    
    #Check for the the chance for a piece to leave home: if a piece is at home, it's... at home.
    if position == -1:
        return DEPLOY
    #If none of these situations have been met, either the piece is at the goal or somewhere of no particular note.
    else:
        return GENERIC
    

#Get the state number for the given player.
def getStateNumber(whoseTurn, state):
    #The states are reduced to low level features for the purpose of shrinking the state space (see getFeature()).
    pieces = [getFeature(state, whoseTurn, state[whoseTurn][i]) for i in range(len(state[whoseTurn]))] #Is it really that easy? (Use below commented if not)
    # pieces = []
    # for i in range(4):
    #     pieces.append(getFeature(whoseTurn, state[whoseTurn][i])) #This means the first piece of each will be added, then the second...

    #Suppose some of the pieces reached the goal... then it's safe to just say they're at a generic opportunity for the purpose of obtaining a state number.
    #They still have to be filled in to correspond to a given state number.
    #May have to introduce error checking to see if the suggested move is moving a piece at the goal.
    #(But also maybe not; the reachable states only come from actions that can be taken, so maybe moving the goal piece will never be suggested anyway!)
    while (len(pieces) < 4):
        pieces.append(GENERIC)
        
    stateNum = 0 #The state number.
    #Since we consider each configuration of a piece individually, it's akin to converting base 7 to base 10.
    #Configuration is xxxx, where x is a piece's feature for the current player, from 0 to 6.
    #We're converting from left to right instead of right to left, but that doesn't matter as long as we have consistency.
    for i in range(len(pieces)):
        stateNum += pieces[i] * pow(7, i)
        
    return stateNum #And there it is!

#Get the current state of the game, purely as the placement of the players.
def getStates():
    result = []
    sublist = []
    for i in range(len(players[RED])):
        sublist.append(players[RED][i].num)
    result.append(sublist)
    sublist.clear()
    for i in range(len(players[BLUE])):
        sublist.append(players[BLUE][i].num)
    result.append(sublist)
    sublist.clear()
    for i in range(len(players[YELLOW])):
        sublist.append(players[YELLOW][i].num)
    result.append(sublist)
    sublist.clear()
    for i in range(len(players[GREEN])):
        sublist.append(players[GREEN][i].num)
    result.append(sublist)
    return result

#Get the state that results from a player moving their given piece.    
def getNewState(states, who, which, roll):
    result = []
    for i in range(4):
        playerState = []
        for j in range(len(states[i])):
            #If the piece that is being moved is the one being considered, get its new position.
            if i == who and j == which:
                if states[who][j] == -1: #Piece is at home, meaning it's about to be deployed.
                    playerState.append(0)
                else: #Otherwise its new location has to be calculated.
                    playerState.append(states[who][j] + roll)
            else:
                playerState.append(states[who][j])
        result.append(playerState)
    return result

def getNewPos(playerPieces, player, piece, roll):
    spot = 0
    try:
        spot = playerPieces[player][piece]
    except Exception as e:
        # print("Player: ", player, " piece: ", piece, " Player pieces: ", playerPieces[player])
        # print("Actual player: ", [players[player][i].num for i in players[player][i].num])
        #First save the qTable...
        global games_played
        games_played += 1
        print(f"Games played: {games_played}")
        if (games_played % 10) == 0:
            print("Exception encountered; writing to file.")
            start = time.time()
            with h5py.File('qTable.h5', 'w') as hf:
                hf.create_dataset("qSet",  data=qTable)
            elapsed = time.time() - start
            print(f"Finished writing in {elapsed} seconds.")
        # df = pd.DataFrame(qTable)
        # df.to_csv('qTable.csv',index=False)
        # f = open('qTable.npy', 'wb')
        # np.save(f, qTable)
        # f.close()
        #... now the policy.
        f = open('policies.npy', 'wb')
        np.save(f, policies)
        f.close()
        if (alpha >= .1):
            makeBoard()
            main()
    if spot == -1:
        return 0
    else:
        try:
            return playerPieces[player][piece] + roll
        except Exception as e:
            #First save the qTable...
            f = open('qTable.npy', 'wb')
            np.save(f, qTable)
            f.close()
            #... now the policy.
            f = open('policies.npy', 'wb')
            np.save(f, policies)
            f.close()

#Calculate the reward that comes from taking an action in a given state. The actions are not
#simultaneous, so it's difficult to calculate the reward that comes from other players' actions.
#This basically means that the reward from the function only considers the immediate reward...
#But that should be fine as the calculating of the Q value covers for future outcomes.
def getReward(state, player, action, roll):
    dest = getNewPos(getStates(), player, action, roll) #Where the piece ends up if it's moved.
    
    #The reward that can be obtained depends on if either...
    if dest == 56: #If the piece reaches a goal,
        return 10
    else:
        #if the piece can kill someone else's piece,
        canKill = False
        
        nex = (player + 1) % 4 #The player after the current one. ("next" is a keyword.)
        after = (player + 2) % 4 #The player after that.
        last = (player + 3) % 4 #The last player in the line.
        
        for i in range(len(state[nex])):
            if dest == state[nex][i]:
                canKill = True
        for i in range(len(state[after])):
            if dest == state[after][i]:
                canKill = True
        for i in range(len(state[last])):
            if dest == state[last][i]:
                canKill = True    
        if canKill:
            return 1    
        else:
            #if the piece can make a double,
            for i in range(len(state[player])):
                if i != action and dest == state[player][i]:
                    return 0
                else:
                    # # print("i != action and dest == state[player][i].num did not satisfy...")
                    pass
                
            #if the piece is leaving home,
            if dest == 0:
                return -0.01
            else: #or if not, the piece is just moving.
                return -0.1

#Get the valid moves from a given state.
def getValidMovesFromState(state, player, roll):
    validIndices = [] #The indices to be returned.
    
    for i in range(len(state[player])):
        spot = state[player][i] #The current piece's position.
        #If the given piece is at home and the roll is a 6, that piece can move.
        if spot == -1 and roll == 6:
            validIndices.append(i)
        #Otherwise, if the player isn't at home and the roll wouldn't overshoot the goal, that piece can move.
        elif spot > -1 and ((spot + roll) <= 56):
            validIndices.append(i)
            
    return validIndices

#Returns the action of moving a given piece, by a given distance, which allows for easy indexing.
def getAction(piece, roll):
    return (piece * 6) + (roll - 1)

#Calculate the q values for a given state and action, combined with the possibilities of any other actions.
def updateQValues(player, state, action):
    global qTable, alpha
    
    currentStateNum = getStateNumber(whose, state) #The current state number for this player, by the features.
    myAction = getAction(action, rolls[nc])
    
    #The reward first needs to be calculated.
    reward = getReward(state, player, action, rolls[nc])
    
    #The new state that comes from this action must be saved.
    nextState = getNewState(state, player, action, rolls[nc])
    
    #Now each subsequent player looks at each possible roll, gets the valid moves for that roll, and transitions to the next state.
    #The next player's turn.
    for i in range(1, 7):
        furtherIndices = getValidMovesFromState(nextState, ((player + 1) % 4), i)
        for nAction in furtherIndices:
            furtherAction = getAction(nAction, i) #The index of the next player's action.
            furtherState = getNewState(nextState, ((player + 1) % 4), nAction, i) #The state that comes from the next player making this move after the root player made theirs.
            #The player who goes after the next player's turn.
            for j in range(1, 7):
                afterIndices = getValidMovesFromState(furtherState, ((player + 2) % 4), j)
                for aAction in afterIndices: #The notation could be better, but this is the third player's action index.
                    afterAction = getAction(aAction, j)
                    afterState = getNewState(furtherState, ((player + 2) % 4), aAction, j)
                    #The player who goes after all the others.
                    for k in range(1, 7):
                        finalIndices = getValidMovesFromState(afterState, ((player + 3) % 4), k)
                        for fAction in finalIndices:
                            finalAction = getAction(fAction, k)
                            finalState = getNewState(afterState, ((player + 3) % 4), fAction, k)
                            #For each final state we have reached the original player's turn again, which means we can calculate the q-value for the root player.
                            #First we need to find the resulting state number.
                            nextValue = getStateNumber(whose, finalState)
                            #Now we calculate the q value based on the max q value from the next state, assuming all actions are available.
                            #This of course means we need to get the max q value for each action in that state, and then the highest q value from those actions.
                            maxActionQ = qTable[whose, nextValue, :, :, :, :].argmax()
                            qTable[whose, currentStateNum, myAction, furtherAction, afterAction, finalAction] = (
                            (1 - alpha) * qTable[whose, currentStateNum, myAction, furtherAction, afterAction, finalAction] + #Exploit
                            alpha * (reward + gamma * maxActionQ)) #Explore
                            
    alpha *= decay #Another step of learning complete, and so it's time to explore less.
                            

#All AI players take their turns.
def aTurns():
    while playerTypes[whose] != HUMAN and not done:
        # sleep(.1) #Can toggle if just gathering data.
        if playerTypes[whose] == RANDOM:
            aRandomTurn()
        else:
            aRationalTurn()
        root.update()

#The current random agent takes their turn.
def aRandomTurn():
    global rolls, rolled, dice, rolled, bb, c, rolls, whose, nc
    
    #First the rolls need to be acquired.
#     # print(PLAYER_NAMES[whose] + "'s turn")
    rollDice()
    
    #For each roll, check if there are any valid moves.
    validMoves = getValidMoves()
    while validMoves:
        #Choose randomly between the moves that can be made.
        moveIndex = validMoves[random.randint(0, len(validMoves) - 1)]
        
        aiMove(moveIndex)
        
        #If the player has no more rolls, or if they won with this one, the turn is over.
        if done or nc >= len(rolls) or rolls[nc] == 0:
            break
        #Otherwise, move on to the next roll.
        else:
            validMoves = getValidMoves()
            
    #If the game isn't over, pass the turn.
    if not done:
        passTurn()

#The current rational agent takes their turn.          
def aRationalTurn():
    global rolls, rolled, dice, rolled, bb, c, rolls, whose, nc, learn, policies
    
    rollDice()
    
    validMoves = getValidMoves()
    while validMoves:
        #This is where the random agent and the rational agent diverge--if we've told the agent to keep learning,
        #it'll update its q values.

        #########################################################################################
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #########################################################################################
        if learn:
            for move in validMoves:
                updateQValues(whose, getStates(), move)
        
        moveIndex = 0
        #There's no point doing any maximax if there's only one move available.
        if len(validMoves) == 1:
            moveIndex = validMoves[0]
        else:
            #Get the state number, for use in multiple places later.
            stateNum = getStateNumber(whose, getStates())
            #The action is supplied by maximax if we're still learning.
            if learn:
                #Determine the player list.
                playerList = []
                for i in range(4):
                    playerList.append((whose + i) % 4)
                #Then translate the valid actions from moving pieces to moving pieces with their rolls (to obtain a value 0 to 23).
                validActions = []
                for i in range(len(validMoves)):
                    validActions.append(getAction(validMoves[i], rolls[nc]))
                #Create the modified Q table to pass in.
                modifiedQtable = optimalAction.modifiedQtable(qTable, stateNum, totalActions, validActions, playerList)
                #Now choose the best action via Q maximax (have to convert back to which roll we had, hence the mod 4).
                #Looks like the list of next states should be an empty list, seeing as it just gets replaced on the first iteration.
                #Likewise for actionMaxAt.
                #Maybe set the policy instead? With this roll, and this state number, this is what the player should do. Might not be valid!
                try:
                    bestAction = optimalAction.maximax(playerList=playerList, modifiedQtable=modifiedQtable, actionMaxAt=actionMaxAt, coinPositions=getStates())
                    # print("stateNum: ",type(stateNum), "roll: ",type(rolls[nc]), " Best action: ", type(bestAction))
                    policies[stateNum, rolls[nc] - 1] = bestAction % 6
                except Exception as e:
                    # print("The exception is: ",e)
                    pass
                #If the policy is can be executed in the current state, do that. If not, choose a move from the valid moves at random.
                canDoPolicy = False
                # for move in validMoves:
                if policies[stateNum, rolls[nc] - 1] in validMoves: #It's one of the valid moves!
                    canDoPolicy = True
                        
                if canDoPolicy: #We can do the policy! So, do it.
                    moveIndex = policies[stateNum, rolls[nc] - 1]
                    # print("Can do the policy; executing.")
                else: #Dang, the policy doesn't work here. Choose a move at random instead.
                    moveIndex = validMoves[random.randint(0, len(validMoves) - 1)]
                    # print("Can't do the policy, do random moves.")
            else:
                #Choose from the policy if we're not learning instead, and as before, pick a random move if the policy doesn't work.
                #If the policy is can be executed in the current state, do that. If not, choose a move from the valid moves at random.
                canDoPolicy = False
                # for move in validMoves:
                if policies[stateNum, rolls[nc] - 1] in validMoves: #It's one of the valid moves!
                    canDoPolicy = True
                        
                if canDoPolicy: #We can do the policy! So, do it.
                    moveIndex = policies[stateNum, rolls[nc] - 1]
                else: #Dang, the policy doesn't work here. Choose a move at random instead.
                    moveIndex = validMoves[random.randint(0, len(validMoves) - 1)]
        
        #The rest of the logic is identical.
        aiMove(moveIndex)
        
        #If the player has no more rolls, or if they won with this one, the turn is over.
        if done or nc >= len(rolls) or rolls[nc] == 0:
            break
        #Otherwise, move on to the next roll.
        else:
            validMoves = getValidMoves()
    
    #If the game isn't over, pass the turn.
    if not done:
        passTurn()
    
def aiMove(moveIndex):
    global rolls, rolled, dice, rolled, bb, c, rolls, whose, nc
    
    if players[whose][moveIndex].num == -1: #Piece is at home.
        movePiece(moveIndex, 0)
    else: #Piece is somewhere else.
        movePiece(moveIndex, players[whose][moveIndex].num + rolls[nc])
        
    #This index needs to be updated to be used in the kill check.
    bb = players[whose][moveIndex].num
        
    #Kill check.
    nex = (whose + 1) % 4 #The player after the current one. ("next" is a keyword.)
    after = (whose + 2) % 4 #The player after that.
    last = (whose + 3) % 4 #The last player in the line.
    kill(cboxes[whose], players[nex], players[after], players[last], homes[nex], homes[after], homes[last])
        
    #Double check.
    doublecheck(players[whose])
    
    #Goal and win check.
    goalCheck(moveIndex)
    
    #Move to the next roll (if there is one).
    nc = nc + 1
    
root.mainloop()

#A change, so that commit may go through