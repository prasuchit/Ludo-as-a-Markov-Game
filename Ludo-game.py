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
rolls = []
RED = True
BLUE = False
GREEN = False
YELLOW = False
TURN = True
REDKILL = False
BLUEKILL = False
GREENKILL = False
YELLOWKILL = False
dice = 0
dice1 = 0
dice2 = 0
root = graphics.root
# Creating a photoimage object to use image 
dice = PhotoImage(file = r"dice.png") 
def main():                                 # Main game function.
    global RED, BLUE, GREEN, YELLOW, dice, nc, TURN, bb, c, cx, cy
    if c == 0:                              #constructs the game pieces first time the code is ran.

        graphics.initBoard(False, False, '1000x750', 'green', "Ludo as an MDP", "logos.txt")
        graphics.drawBoard()

    else:  # HERE ALL THE GAME OCCURS ... IF WAGHAIRA, MOVEMENT IDHAR HOGI !!!

        if c >= 1:                                #This condition is true when a click is made.

            if RED == True and TURN == False:      #Red players turn
                print("Red's Turn")
                print("moves available: ", rolls)
                la = "RED"
                if (movecheck(graphics.red, graphics.redhome, graphics.redbox, la)) == False:  #Checks if player can take a turn.
                    BLUE = True
                    RED = False
                    clear()                                          #clears variable, next players turn

                if RED == True:                                   # searches if click is made on a graphics.red game piece.
                    for i in range(len(graphics.red)):
                        if ((((cx > graphics.red[i].x0 + 13) and (cx < graphics.red[i].x + 13)) and (
                            (cy > graphics.red[i].y0 + 14) and (cy < graphics.red[i].y + 14)))
                            and (graphics.red[i].x0 == graphics.redhome[i].x) and (graphics.red[i].y0 == graphics.redhome[i].y)):
                            print("woila ")

                            if rolls[0 + nc] == 6:                 #If a six occurs and gamepiece is in home
                                                                    #Game piece is moved onto the home graphics.box
                                graphics.red[i].x0 = graphics.redbox[0].x
                                graphics.red[i].y0 = graphics.redbox[0].y
                                graphics.red[i].x = graphics.redbox[0].x + 25
                                graphics.red[i].y = graphics.redbox[0].y + 25
                                graphics.red[i].num = 0
                                graphics.red[i].swap()
                                nc = nc + 1

                                if nc > len(rolls) - 1:           # check if all moves are made. so next players turn.
                                    BLUE = True
                                    RED = False
                                    clear()
                                break

                        if ((((cx > graphics.red[i].x0 + 13) and (cx < graphics.red[i].x + 13)) and (       #if gamepiece is outside home
                            (cy > graphics.red[i].y0 + 14) and (cy < graphics.red[i].y + 14)))
                            and ((graphics.red[i].x0 > 270) or (graphics.red[i].y0 > 270))):
                            print("woila ")
                            bb = ((graphics.red[i].num) + rolls[0 + nc])
                            # Winning condition

                            if bb > 57:                        #prevents moves greater than allowed number
                                break
                                #bb = ((graphics.red[i].num) + rolls[0 + nc]) - 57

                            kill(graphics.redbox,graphics.blue,graphics.yellow,graphics.green,graphics.bluehome,graphics.yellowhome,graphics.greenhome)      #checks if a kill can be made.

                            graphics.red[i].x0 = graphics.redbox[bb].x
                            graphics.red[i].y0 = graphics.redbox[bb].y
                            graphics.red[i].x = graphics.redbox[bb].x + 25
                            graphics.red[i].y = graphics.redbox[bb].y + 25
                            graphics.red[i].swap()
                            graphics.red[i].num = bb
                            doublecheck(graphics.red)                           #checks if the gamepiece can be made as a double.

                            nc = nc + 1
                            if bb == 57:                              #checks if game has traversed all the blocks
                                # del graphics.red[i]
                                graphics.red.remove(graphics.red[i])

                            if nc > len(rolls) - 1:
                                BLUE = True                         #next players turn.
                                RED = False
                                clear()
                            break


                        # BLUES TURN!!!!!!!!!!!!!!!!!!!!

            if BLUE == True and TURN == False:                        #same as REDS CODE
                print("Blue's Turn")
                print("moves available: ", rolls)
                la="BLUE"
                if (movecheck(graphics.blue, graphics.bluehome, graphics.bluebox, la)) == False:
                    print("NO MOVES SIR JEE")
                    BLUE = False
                    YELLOW = True
                    clear()

                if BLUE == True:

                    for i in range(len(graphics.blue)):
                        if ((((cx > graphics.blue[i].x0 + 13) and (cx < graphics.blue[i].x + 13)) and (
                            (cy > graphics.blue[i].y0 + 14) and (cy < graphics.blue[i].y + 14)))
                            and (graphics.blue[i].x0 == graphics.bluehome[i].x) and (graphics.blue[i].y0 == graphics.bluehome[i].y)):
                            print("woila ")

                            if rolls[0 + nc] == 6:

                                graphics.blue[i].x0 = graphics.bluebox[0].x
                                graphics.blue[i].y0 = graphics.bluebox[0].y
                                graphics.blue[i].x = graphics.bluebox[0].x + 25
                                graphics.blue[i].y = graphics.bluebox[0].y + 25
                                graphics.blue[i].num = 0
                                graphics.blue[i].swap()
                                nc = nc + 1

                                if nc > len(rolls) - 1:
                                    YELLOW = True
                                    BLUE = False
                                    clear()
                                break

                        if ((((cx > graphics.blue[i].x0 + 13) and (cx < graphics.blue[i].x + 13)) and (
                            (cy > graphics.blue[i].y0 + 14) and (cy < graphics.blue[i].y + 14)))
                            and ((graphics.blue[i].x0 > 270) or (graphics.blue[i].y0 < 470))):
                            print("woila ")
                            bb = ((graphics.blue[i].num) + rolls[0 + nc])
                            if bb > 57:
                                break
                                # bb= ((graphics.blue[i].num) + rolls[0 + nc]) - 52

                            kill(graphics.bluebox,graphics.red,graphics.yellow,graphics.green,graphics.redhome,graphics.yellowhome,graphics.greenhome)

                            graphics.blue[i].x0 = graphics.bluebox[bb].x
                            graphics.blue[i].y0 = graphics.bluebox[bb].y
                            graphics.blue[i].x = graphics.bluebox[bb].x + 25
                            graphics.blue[i].y = graphics.bluebox[bb].y + 25
                            graphics.blue[i].swap()
                            graphics.blue[i].num = bb
                            doublecheck(graphics.blue)
                            nc = nc + 1
                            if bb == 57:
                                # del graphics.red[i]
                                graphics.blue.remove(graphics.blue[i])

                            if nc > len(rolls) - 1:
                                YELLOW = True
                                BLUE = False
                                clear()
                            break

                        # YELLOWS TURN!!!!!!!!!!!!!!!!!!!!

            if YELLOW == True and TURN == False:                     #Same as RED's code
                print("Yellows's Turn")
                print("moves available: ", rolls)
                la="YELLOW"
                if (movecheck(graphics.yellow, graphics.yellowhome, graphics.yellowbox,la)) == False:
                    print("NO MOVES SIR JEE")
                    YELLOW = False
                    GREEN = True
                    clear()

                if YELLOW == True:

                    for i in range(len(graphics.yellow)):
                        if ((((cx > graphics.yellow[i].x0 + 13) and (cx < graphics.yellow[i].x + 13)) and (
                                    (cy > graphics.yellow[i].y0 + 14) and (cy < graphics.yellow[i].y + 14)))
                            and (graphics.yellow[i].x0 == graphics.yellowhome[i].x) and (graphics.yellow[i].y0 == graphics.yellowhome[i].y)):
                            print("woila ")

                            if rolls[0 + nc] == 6:

                                graphics.yellow[i].x0 = graphics.yellowbox[0].x
                                graphics.yellow[i].y0 = graphics.yellowbox[0].y
                                graphics.yellow[i].x = graphics.yellowbox[0].x + 25
                                graphics.yellow[i].y = graphics.yellowbox[0].y + 25
                                graphics.yellow[i].num = 0
                                graphics.yellow[i].swap()
                                nc = nc + 1

                                if nc > len(rolls) - 1:
                                    YELLOW = False
                                    GREEN = True
                                    clear()
                                break

                        if ((((cx > graphics.yellow[i].x0 + 13) and (cx < graphics.yellow[i].x + 13)) and (
                                    (cy > graphics.yellow[i].y0 + 14) and (cy < graphics.yellow[i].y + 14)))
                            and ((graphics.yellow[i].x0 < 470) or (graphics.yellow[i].y0 < 470))):
                            print("woila ")
                            bb = ((graphics.yellow[i].num) + rolls[0 + nc])
                            if bb > 57:
                                break
                                #bb = ((graphics.yellow[i].num) + rolls[0 + nc]) - 52

                            kill(graphics.yellowbox,graphics.blue,graphics.red,graphics.green,graphics.bluehome,graphics.redhome,graphics.greenhome)

                            graphics.yellow[i].x0 = graphics.yellowbox[bb].x
                            graphics.yellow[i].y0 = graphics.yellowbox[bb].y
                            graphics.yellow[i].x = graphics.yellowbox[bb].x + 25
                            graphics.yellow[i].y = graphics.yellowbox[bb].y + 25
                            graphics.yellow[i].swap()
                            graphics.yellow[i].num = bb
                            doublecheck(graphics.yellow)
                            nc = nc + 1
                            if bb == 57:
                                # del graphics.red[i]
                                graphics.yellow.remove(graphics.yellow[i]);

                            if nc > len(rolls) - 1:
                                YELLOW = False
                                GREEN = True
                                clear()
                            break


                        # GREENS TURN!!!!!!!!!!!!!!!!!!!!

            if GREEN == True and TURN == False:                     #Same as RED's code
                print("Green's Turn")
                print("moves available: ", rolls)
                la="GREEN"
                if (movecheck(graphics.green, graphics.greenhome, graphics.greenbox,la)) == False:
                    print("NO MOVES SIR JEE")
                    GREEN = False
                    RED = True
                    clear()

                if GREEN == True:

                    for i in range(len(graphics.green)):
                        if ((((cx > graphics.green[i].x0 + 13) and (cx < graphics.green[i].x + 13)) and (
                                    (cy > graphics.green[i].y0 + 14) and (cy < graphics.green[i].y + 14)))
                            and (graphics.green[i].x0 == graphics.greenhome[i].x) and (graphics.green[i].y0 == graphics.greenhome[i].y)):
                            print("woila ")

                            if rolls[0 + nc] == 6:

                                graphics.green[i].x0 = graphics.greenbox[0].x
                                graphics.green[i].y0 = graphics.greenbox[0].y
                                graphics.green[i].x = graphics.greenbox[0].x + 25
                                graphics.green[i].y = graphics.greenbox[0].y + 25
                                graphics.green[i].num = 0
                                graphics.green[i].swap()
                                nc = nc + 1
                                print("graphics.green x.y: ", graphics.green[i].x0, graphics.green[i].y0)

                                if nc > len(rolls) - 1:
                                    GREEN = False
                                    RED = True
                                    clear()
                                break

                        if ((((cx > graphics.green[i].x0 + 13) and (cx < graphics.green[i].x + 13)) and (
                                    (cy > graphics.green[i].y0 + 14) and (cy < graphics.green[i].y + 14)))
                            and ((graphics.green[i].x0 < 470) or (graphics.green[i].y0 < 470))):
                            print("woila ")
                            bb = ((graphics.green[i].num) + rolls[0 + nc])
                            if bb > 57:
                                break
                                # bb = ((graphics.green[i].num) + rolls[0 + nc]) - 52

                            kill(graphics.greenbox,graphics.blue,graphics.yellow,graphics.red,graphics.bluehome,graphics.yellowhome,graphics.redhome)

                            graphics.green[i].x0 = graphics.greenbox[bb].x
                            graphics.green[i].y0 = graphics.greenbox[bb].y
                            graphics.green[i].x = graphics.greenbox[bb].x + 25
                            graphics.green[i].y = graphics.greenbox[bb].y + 25
                            graphics.green[i].swap()
                            graphics.green[i].num = bb
                            nc = nc + 1
                            doublecheck(graphics.green)
                            if bb == 57:
                                # del graphics.red[i]
                                graphics.green.remove(graphics.green[i])

                            if nc > len(rolls) - 1:
                                GREEN = False
                                RED = True
                                clear()
                            break


main()    #Main functin is called once when c==0 to intialize all the gamepieces.


def leftClick(event):  # Main play function is called on every left click.

    global c, cx, cy, RED, YELLOW
    c = c + 1
    cx = root.winfo_pointerx() - root.winfo_rootx()  # This formula returns the x,y co-ordinates of the mouse pointer relative to the board.
    cy = root.winfo_pointery() - root.winfo_rooty()

    print("Click at: ", cx, cy)

    main()           #Main function called on every click to progress the game


root.bind("<Button-1>", leftClick)


def turn():   #Prints whoose turn is it

    if RED == True:
        L2 = Label(root, text="   Red's Turn    ", fg='Black', background='red', font=("Arial", 24, "bold"))
        L2.place(x=770, y=50)

    if BLUE == True:
        L2 = Label(root, text="   Blue's Turn   ", fg='Black', background='blue', font=("Arial", 24, "bold"))
        L2.place(x=770, y=50)

    if GREEN == True:
        L2 = Label(root, text="Green's Turn  ", fg='Black', background='green', font=("Arial", 24, "bold"))
        L2.place(x=770, y=50)

    if YELLOW == True:
        L2 = Label(root, text="Yellow's Turn", fg='Black', background='yellow', font=("Arial", 24, "bold"))
        L2.place(x=770, y=50)


def roll():   #Rolling function that rolls a dice, goes again if its a six
    global rollc, dice, dice1, dice2, TURN, rolls

    if TURN == True:

        rollc = rollc + 1
        print("roll: ", rollc)

        if rollc == 1:
            dice = random.randint(1, 6)
            L1 = Label(root, text=dice, fg='Black', background='green', font=("Arial", 24, "bold"))
            L1.place(x=800, y=200)
            print("dice: ", dice)
            rolls.append(dice)
            if dice != 6:
                rollc = 0
                TURN = False

        if rollc == 2:
            if dice == 6:
                dice1 = random.randint(1, 6)
                L3 = Label(root, text=dice1, fg='Black', background='green', font=("Arial", 24, "bold"))
                L3.place(x=800, y=250)
                rolls.append(dice1)
                if dice1 != 6:
                    rollc = 0
                    TURN = False

        if rollc == 3:
            if dice1 == 6:
                dice2 = random.randint(1, 6)
                L4 = Label(root, text=dice2, fg='Black', background='green', font=("Arial", 24, "bold"))
                L4.place(x=800, y=300)
                rolls.append(dice2)
                rollc = 0
                TURN = False


def clear():        #clears all the variable prior to next player's turn
    global nc, rolls, TURN, L1, L3, L4
    nc = 0
    del rolls[:]
    TURN = True
    L1 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L1.place(x=800, y=200)
    L3 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L3.place(x=800, y=250)
    L4 = Label(root, text="        ", fg='Black', background='green', font=("Arial", 24, "bold"))
    L4.place(x=800, y=300)
    print("cleared")
    turn()


def movecheck(r, rh, rb, la):       #Check if the player can make a move

    if (dice == 6 and dice1 == 6 and dice2 == 6):
        return False

    win=True                                                  #Checking if the game is won or the player can make any moves.
    for j in range(4):
        if (r[j].x0 != rb[56].x) and (r[j].y0 != rb[56].y):
             win=False

    if win == True:                                         #If all gamepieces home, prints that the player has won
        print("YOU HAVE WON")
        L2 = Label(root, text=(la + "Wins"), fg='Black', background='green', font=("Arial", 24, "bold"))
        L2.place(x=770, y=500)
        return False

    if win == False and dice != 6:                    #if its not a 6 and all game pieces inside home, then next players turn
        for i in range(len(r)):
            if(r[i].num != -1):
                (print("good hai"))
                return True
        print("jani all in")
        return False

def kill(a,b,c,d,bh,ch,dh):   #function that determines if a gamepiece can be killed

    #if the game piece is not on a stop
    if ((a[bb].x0 != graphics.box[1].x and a[bb].y0 != graphics.box[1].y) and (a[bb].x0 != graphics.box[14].x and a[bb].y0 != graphics.box[14].y) and
        (a[bb].x0 != graphics.box[9].x and a[bb].y0 != graphics.box[9].y) and (a[bb].x0 != graphics.box[22].x and a[bb].y0 != graphics.box[22].y) and
        (a[bb].x0 != graphics.box[27].x and a[bb].y0 != graphics.box[27].y) and (a[bb].x0 != graphics.box[35].x and a[bb].y0 != graphics.box[35].y) and
        (a[bb].x0 != graphics.box[40].x and a[bb].y0 != graphics.box[40].y) and (a[bb].x0 != graphics.box[48].x and a[bb].y0 != graphics.box[48].y)):


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


turn()            #prints the "graphics.red player's turn" initially

button = Button(root, text="    Roll    ", relief="raised", font=("Arial", 20),  command=roll)  # call roll function evertime this button is clicked
button.place(x=805, y=120)

root.mainloop()