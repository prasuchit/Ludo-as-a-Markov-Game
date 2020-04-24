import graphics
import random
from time import sleep
from tkinter import Button, Label, PhotoImage, simpledialog

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

done = False #Checks if the game is over. The game ends when someone wins.

rolls = [0, 0, 0] #The rolls of each die.

root = graphics.root
# Creating a photoimage object to use image 
dice = PhotoImage(file = r"dice.gif") 

#Likewise, create an image for each side of the die.
sides = [PhotoImage(file = r"die1.gif"),
         PhotoImage(file = r"die2.gif"),
         PhotoImage(file = r"die3.gif"),
         PhotoImage(file = r"die4.gif"),
         PhotoImage(file = r"die5.gif"),
         PhotoImage(file = r"die6.gif")]

#Prints the given player's turn.
def turn():
    L2 = Label(root, text= PLAYER_NAMES[whose] + "'s Turn    ", fg='Black', 
               background= PLAYER_NAMES[whose].lower(), font=("Arial", 24, "bold"))
    L2.place(x=770, y=50)

def main():                                 # Main game function.
    global box, cboxes, homes, players, playerTypes, whose
    if c == 0:                              #constructs the game pieces first time the code is ran.

        graphics.initBoard(False, False, '1000x750', 'green', "Ludo as a Markov Game", "logos.txt")
        graphics.drawBoard()
        #These variables are ported over from the graphics module to shorten notation.
        box = graphics.box
        cboxes = graphics.cboxes
        homes = graphics.homes
        players = graphics.players
        #The user is then asked to give a mixture humans versus computers.
        humans = simpledialog.askinteger("Input", "How many humans are participating?", parent=root, minvalue=0, maxvalue=4)
        randoms = 0 #Scopes are going to be the death of me.
        rationals = 0
        #If there are any computers participating, the user is asked how many of those computers are to be random players.
        if humans < 4:
            randoms = simpledialog.askinteger("Input", "Of the computers, how many do you want to play randomly?", 
                                             parent=root, minvalue=0, maxvalue=(4 - humans))
            rationals = 4 - humans - randoms
        #With the split of players decided, they are now distributed to the playertypes list.
        for _ in range(humans):
            playerTypes.append(HUMAN)
        for _ in range(randoms):
            playerTypes.append(RANDOM)
        for _ in range(rationals):
            playerTypes.append(RATIONAL)
        #As a stretch goal, we could randomly shuffle these player types around, but it shouldn't matter much.
        
        #Last thing to do is decide who goes first.
        whose = random.randint(0,3)
        turn()    

    elif not done:
        #What turn we take depends on the type of player at hand.
        #The non-human players can go automatically.
        aTurns()
        #With the AI turns out of the way (and they'll always be next to each other), the human(s) take their turns.
        if not done:
            playTurn()
        

main()    #Main function is called once when c==0 to initialize all the gamepieces.

def playTurn():
    global RED, BLUE, YELLOW, GREEN, dice, rolled, bb, c, cx, cy, rolls, whose, nc, won
    #This process will need to be explained a bit more thoroughly now that there's the same logic for all players.
    if rolled: #A player's turn only goes if they are done rolling.
        #For now, console information will be displayed, but we probably should do away with this in the finished product.
        print(PLAYER_NAMES[whose] + "'s turn")
        print("Moves available: ")
        
        if (movecheck(players[whose], cboxes[whose], PLAYER_NAMES[whose])) == False: #If no move is available, pass the turn.
            passTurn()
            #This has to get added whenever the turn is passed, in case the next player is an AI.
        else: #Check for a click on a player's own game piece.
            for i in range(len(players[whose])):
                if ((((cx > players[whose][i].x0 + 13) and (cx < players[whose][i].x + 13)) and #Home spots.
                ((cy > players[whose][i].y0 + 14) and (cy < players[whose][i].y + 14))) and
                (players[whose][i].x0 == homes[whose][i].x) and (players[whose][i].y0 == homes[whose][i].y)):
                    print("Player at home.")
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
                        print("Player somewhere else.")
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
        print("This player is done.")
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

    print("Click at: ", cx, cy)

    main()           #Main function called on every click to progress the game


root.bind("<Button-1>", leftClick)


def roll():   #Rolls a die, and repeats if it's a 6.
    global rollc, rolls, rolled, die

    if rolled == False:
        rollc = rollc + 1
        print("roll: ", rollc)
        #Unfortunately due to the quirks of tkinter, this can't really be condensed, just changed to match the notation.
        #(Actually it could be changed with a list, but ehhhh it's fine.)
        if rollc == 1:
            die = random.randint(1, 6)
            L1 = Label(root, text=str(die), image = sides[die - 1], fg='Black', background='green', font=("Arial", 24, "bold")) #text?
            L1.place(x=800, y=200)
            print("dice: ", die)
            rolls[0] = die
            if die != 6:
                rollc = 0
                rolled = True

        elif rollc == 2:
            if die == 6:
                die = random.randint(1, 6)
                L3 = Label(root, text=str(die), image = sides[die - 1], fg='Black', background='green', font=("Arial", 24, "bold"))
                L3.place(x=800, y=250)
                print("dice: ", die)
                rolls[1] = die
                if die != 6:
                    rollc = 0
                    rolled = True

        else:
            if die == 6:
                die = random.randint(1, 6)
                L4 = Label(root, text=str(die), image = sides[die - 1], fg='Black', background='green', font=("Arial", 24, "bold"))
                L4.place(x=800, y=300)
                print("dice: ", die)
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
    global done
    if not players[whose]: #If a player has no pieces left, they all reached the goal.
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

def clear():        #clears all the variable prior to next player's turn
    L1 = Label(root, text="        ", image = "", fg='Black', background='green', font=("Arial", 48, "bold"))
    L1.place(x=800, y=200)
    L3 = Label(root, text="        ", image = "", fg='Black', background='green', font=("Arial", 48, "bold"))
    L3.place(x=800, y=250)
    L4 = Label(root, text="        ", image = "", fg='Black', background='green', font=("Arial", 48, "bold"))
    L4.place(x=800, y=300)
    if not done:
        turn()

turn()            #prints "Red's turn" initially

button = Button(root, text="    Roll    ", image = dice, relief="raised", font=("Arial", 20),  command=roll)  # call roll function evertime this button is clicked
button.place(x=835, y=120)

#-----Agent functions, behavior, and so on!-----
#All functions for agent behavior will be prefixed with an "a" to make it easy to differentiate.

#All AI players take their turns.
def aTurns():
    while playerTypes[whose] != HUMAN and not done:
        sleep(.1)
        if playerTypes[whose] == RANDOM:
            aRandomTurn()
        else:
            aRationalTurn()
        root.update()

#The current random agent takes their turn.
def aRandomTurn():
    global rolls, rolled, dice, rolled, bb, c, rolls, whose, nc
    
    #First the rolls need to be acquired.
    print(PLAYER_NAMES[whose] + "'s turn")
    rollDice()
    
    #For each roll, check if there are any valid moves.
    validMoves = getValidMoves()
    while validMoves:
        #Choose randomly between the moves that can be made.
        moveIndex = validMoves[random.randint(0, len(validMoves) - 1)]
        #The movement depends on if the piece in question is at home or on the board.
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
    pass

root.mainloop()