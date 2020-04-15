import graphics
import sys
import os
import random
from tkinter import Button, Label, PhotoImage

c = 0                              #initializing variable and flags that are to be used in the game
cx = 0
cy = 0
lx = 0
bb = 0
nc = 0
rollc = 0
#
RED = graphics.RED
BLUE = graphics.BLUE
YELLOW = graphics.YELLOW
GREEN = graphics.GREEN
PLAYER_NAMES = ["Red", "Blue", "Yellow", "Green"] #Strings for each player's name.
whose = RED #The player whose turn it is. Can be adjusted later to choose a new player to go first.
rolled = False #Originally "TURN." This variable tracks if the rolls for a given player have finished.
# TURN = True
box = 0
cboxes = 0
homes = 0
players = 0
REDKILL = False
BLUEKILL = False
GREENKILL = False
YELLOWKILL = False

rolls = [0, 0, 0] #He made this way harder on himself than it needed to be.
# dice = 0
# dice1 = 0
# dice2 = 0

root = graphics.root
# Creating a photoimage object to use image 
dice = PhotoImage(file = r"dice.png") 
def main():                                 # Main game function.
    global box, cboxes, homes, players
    if c == 0:                              #constructs the game pieces first time the code is ran.

        graphics.initBoard(False, False, '1000x750', 'green', "Ludo as an MDP", "logos.txt")
        graphics.drawBoard()
        #These variables are ported over from the graphics module to shorten notation.
        box = graphics.box
        cboxes = graphics.cboxes
        homes = graphics.homes
        players = graphics.players

    else:
        playTurn()

main()    #Main function is called once when c==0 to initialize all the gamepieces.

def playTurn():
    global RED, BLUE, YELLOW, GREEN, dice, rolled, bb, c, cx, cy, rolls, whose, nc
    #This process will need to be explained a bit more thoroughly now that there's the same logic for all players.
    if rolled: #A player's turn only goes if they are done rolling.
        #For now, console information will be displayed, but we probably should do away with this in the finished product.
        print(PLAYER_NAMES[whose] + "' turn")
        print("Moves available: ")
        
        if (movecheck(players[whose], cboxes[whose], PLAYER_NAMES[whose])) == False: #If no move is available, pass the turn.
            passTurn()
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
                    elif (whose == GREEN) and (players[whose][i].x0 < 470 or players[whose][i].y0 < 470):
                        validMove = True #Yellow and green's check are the same. Is this intended behavior?
                    
                    #If the last if-clause is satisfied for the given player, we can move on with the rest.
                    
                    if (validMove):
                        print("Player somewhere else.")
                        bb = ((players[whose][i].num) + rolls[0 + nc]) #bb here is the number of spaces traversed.
                        
                        if bb > 57:
                            break #Can't move greater than the allowed number of spaces.
                        
                        #These variables will shorten the notation for the kill call.
                        nex = (whose + 1) % 4 #The player after the current one. ("next" is a keyword.)
                        after = (whose + 2) % 4 #The player after that.
                        last = (whose + 3) % 4 #The last player in the line.
                        kill(cboxes[whose], players[nex], players[after], players[last], homes[nex], homes[after], homes[last])
                        
                        movePiece(i, bb)
                        doublecheck(players[whose]) #Check to see if a piece can be made a double.
                        
                        nc = nc + 1
                        
                        if bb == 57: #If a piece went all the way, it's gone.
                            players[whose].remove(players[whose][i])
                        
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
                
def movecheck(player, pbox, pname): #Check if the player can make a move (originally included homes, but was never used).
    if rolls[2] == 6: #If the third die rolled a 6, so did the first two. Three 6's means the turn ends.
        return False
    
    win = True #Check if the game is won.
    for i in range(4):
        if (player[i].x0 != pbox[56].x) or (player[i].y0 != pbox[56].y): #Checks if a piece is at the goal.
            win = False
            i = 5 #Saves time, why not?

    if win == True: #Maybe remove the console information here, too.
        print("YOU HAVE WON")
        L2 = Label(root, text=(pname + " Wins"), fg='Black', background='green', font=("Arial", 24, "bold"))
        L2.place(x=770, y=500)
        return False

    if rolls[0] != 6: #If no die is a 6, and all players are in the home zone, no move is valid.
        for i in range(len(player)):
            if(player[i].num != -1):
                return True
        return False
    #THIS IS LIKELY WHERE THE BUG IN THE ORIGINAL CAME UP!
    #All this move function does is check if any player is outside the home zone. It doesn't check
    #if the move made will cause it to overshoot the goal.
    #It also assumes that if a 6 is rolled, something can always be done. But that isn't true;
    #if all pieces are on the field and none of them can move 6 forward, the game soft locks.
    #Chances are this entire function will need to be reworked--and perhaps called multiple times as movements
    #for the dice resolve. But this falls outside the scope of redundancy cleanup, and changing it would introduce complexity
    #so it will be left alone for now.
    
#Passes the turn to the next player. Combined with clear() since they always occur together.                       
def passTurn():
    global nc, rolls, rolled, L1, L3, L4, whose
    whose = (whose + 1) % 4 #Passes the turn to the next player.
    nc = 0 #Resets the number of rolls to 0 (delete?).
    for i in range(len(rolls)):
        rolls[i] = 0 #Resets the dice to "unrolled."
    rolled = False #The next player has yet to roll as the turn passes.
    L1 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L1.place(x=800, y=200)
    L3 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L3.place(x=800, y=250)
    L4 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L4.place(x=800, y=300)
    turn(whose)
    
#Prints the given player's turn (let's cut this down).
def turn(whose):
    L2 = Label(root, text= PLAYER_NAMES[whose] + "'s Turn    ", fg='Black', 
               background= PLAYER_NAMES[whose].lower(), font=("Arial", 24, "bold"))
    L2.place(x=770, y=50)

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
    global rollc, rolls, rolled, roll
#     global rollc, dice, dice1, dice2, TURN, rolls

    if rolled == False:
#     if TURN == True:
        rollc = rollc + 1
        print("roll: ", rollc)
        #Unfortunately due to the quirks of tkinter, this can't really be condensed, just changed to match the notation.
        if rollc == 1:
            roll = random.randint(1, 6)
            L1 = Label(root, text=str(roll), fg='Black', background='green', font=("Arial", 24, "bold"))
            L1.place(x=800, y=200)
            print("dice: ", roll)
            rolls[0] = roll
            if roll != 6:
                rollc = 0
                rolled = True

        elif rollc == 2:
            if roll == 6:
                roll = random.randint(1, 6)
                L3 = Label(root, text=str(roll), fg='Black', background='green', font=("Arial", 24, "bold"))
                L3.place(x=800, y=250)
                rolls[1] = roll
                if roll != 6:
                    rollc = 0
                    rolled = True

        else:
            if roll == 6:
                roll = random.randint(1, 6)
                L4 = Label(root, text=str(roll), fg='Black', background='green', font=("Arial", 24, "bold"))
                L4.place(x=800, y=300)
                rolls[2] = roll
                rollc = 0
                rolled = True


def clear():        #clears all the variable prior to next player's turn
    L1 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L1.place(x=800, y=200)
    L3 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L3.place(x=800, y=250)
    L4 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L4.place(x=800, y=300)
    turn()

turn(whose)            #prints "Red's turn" initially

button = Button(root, text="    Roll    ", relief="raised", font=("Arial", 20),  command=roll)  # call roll function evertime this button is clicked
button.place(x=805, y=120)

root.mainloop()