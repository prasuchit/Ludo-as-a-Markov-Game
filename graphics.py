import tkinter.messagebox as tkmb
from tkinter import *  # Tkinter is used as the GUI.
root = Tk()
logodict = {}
box = 0
cboxes = 0
# redbox = 0
# bluebox = 0
# greenbox = 0
# yellowbox = 0
homes = 0
# redhome = 0
# bluehome = 0
# yellowhome = 0
# greenhome = 0
players = 0
# red =0 
# blue = 0
# yellow = 0
# green = 0
rap = 0

RED=0
BLUE=1
YELLOW=2
GREEN=3

#############################################################################################################################
def initBoard(width = None, height = None, geometry = None, background = None, title = None, filename = None):
    root.resizable(width=width, height=height)  # The window size of the game.
    root.geometry(geometry)
    root.configure(background=background)
    root.title(title)
    with open(filename) as f:
        logo = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        logo = [x.strip() for x in logo]

    for l in logo:
        temp = (str(l)+".gif")
        logodict[l] = PhotoImage(file=temp)

    # print(logodict)
    Label(image= logodict.get("redside"), width=298, height=298).place(x=-1, y=-1)               #setting up board images
    Label(image= logodict.get("blueside"), width=300, height=300).place(x=(-2), y=(448))
    Label(image= logodict.get("greenside"), width=296, height=296).place(x=(450), y=(0))
    Label(image= logodict.get("yellowside"), width=294, height=294).place(x=(450), y=(450))
    Label(image= logodict.get("center"), width=150, height=150).place(x=(298), y=(298))
    
    tkmb.showinfo(title=None, message="TO START GAME PRESS OKAY & TO EXIT PRESS CROSS UP IN THE WINDOW")
    v = 0
    z = 0
    # start = [0,50,100,250,300,350,400,450,600,650]
    while (v != 300):           #Drawing White boxes
        z = 0
        while (z != 150):
            Label(image= logodict.get("whitebox"), width=46, height=46).place(x=(300 + z), y=(0 + v))
            Label(image= logodict.get("whitebox"), width=46, height=46).place(x=(0 + v), y=(300 + z))
            Label(image= logodict.get("whitebox"), width=46, height=46).place(x=(300 + z), y=(450 + v))
            Label(image= logodict.get("whitebox"), width=46, height=46).place(x=(450 + v), y=(300 + z))
            z = z + 50
        v = v + 50
    v = 0
    while (v != 250):     #Drawing other color boxes
        Label(image= logodict.get("redbox"), width=46, height=46).place(x=(50 + v), y=(350))
        Label(image= logodict.get("greenbox"), width=46, height=46).place(x=(350), y=(50 + v))
        Label(image= logodict.get("yellowbox"), width=46, height=46).place(x=(450 + v), y=(350))
        Label(image= logodict.get("bluebox"), width=46, height=46).place(x=(350), y=(450 + v))
        v = v + 50

    Label(image= logodict.get("redbox"), width=46, height=46).place(x=(100), y=(400))
    Label(image= logodict.get("greenbox"), width=46, height=46).place(x=(300), y=(100))
    Label(image= logodict.get("yellowbox"), width=46, height=46).place(x=(600), y=(300))
    Label(image= logodict.get("bluebox"), width=46, height=46).place(x=(400), y=(600))
    Label(image= logodict.get("redstop"), width=46, height=46).place(x=(50), y=(300))
    Label(image= logodict.get("greenstop"), width=46, height=46).place(x=(400), y=(50))
    Label(image= logodict.get("yellowstop"), width=46, height=46).place(x=(650), y=(400))
    Label(image= logodict.get("bluestop"), width=46, height=46).place(x=(300), y=(650))
    Label(image= logodict.get("head"), width=46, height=46).place(x=250, y=400)        #Drawing arrows
    Label(image= logodict.get("tail"), width=46, height=46).place(x=300, y=450)
    Label(image= logodict.get("head1"), width=46, height=46).place(x=400, y=450)
    Label(image= logodict.get("tail1"), width=46, height=46).place(x=450, y=400)
    Label(image= logodict.get("head2"), width=46, height=46).place(x=450, y=300)
    Label(image= logodict.get("tail2"), width=46, height=46).place(x=400, y=250)
    Label(image= logodict.get("head3"), width=46, height=46).place(x=300, y=250)
    Label(image= logodict.get("tail3"), width=46, height=46).place(x=250, y=300)
###########################################################################################################################
class Box: 
    global rap
    rap = None

    def __init__(self, num=-1, x=0, y=0, x0=0, y0=0, double=False, box_color="red"): #Changed default to "red."
        self.num = num                #no of gamepiece acc to box
        self.x = x                    #initial and final co-ordinates of the boxes
        self.y = y
        self.x0 = x0
        self.y0 = y0
        self.rap = Label(image= logodict.get(box_color), width=20, height=20)        #image of game piece.
        self.double = double                                       #if one game piece on top of another.

    def swap(self):                     #Swaps the position of gamepiece according to the number on dice.
        self.rap.place(x=self.x0 + 13, y=self.y0 + 14)
############################################################################################################################

def drawBoard():
    global box, cboxes, homes, players
    
    #All colors can be condensed to lists; this is necessary for shortening the handling of turn-taking.
    #The order for the lists will always be red -> blue -> yellow -> green.
    box = [Box() for i in range(52)]  #List the outer box coordinates.
    cboxes = [[Box() for i in range(57)] for j in range(4)] #Coordinates for all colored boxes, home/stop excluded.
    homes = [[Box() for i in range(4)] for j in range(4)] #Coordinates for the home positions.
    players = [[0 for i in range (4)] for j in range(4)] #Coordinates for the players' pieces.
    for j in range(0, len(players[0])): #The logos mean these need to be implemented individually.
            players[RED][j] = Box()
            players[BLUE][j] = Box(box_color="blue")
            players[YELLOW][j] = Box(box_color="yellow")
            players[GREEN][j] = Box(box_color="green")

    #Population code must also change, but fortunately it can be shortened a great deal.
    for j in range(4):                        #Populates list of homeboxes, colored boxes, gamepieces and white boxes
            #The home piece logic must remain the same, but pay respect to the new naming conventions.
            homes[RED][j].x = (100 + ((100 * j) if j < 2 else (100 * (j - 2)))) #Red. (Did he know about ternary operators?)
            homes[RED][j].y = (100 if j < 2 else 200) #(Seriously, ternary operators are the best.)
            homes[BLUE][j].x = (100 + ((100 * j) if j < 2 else (100 * (j - 2)))) #Blue.
            homes[BLUE][j].y = (550 if j < 2 else 650)
            homes[YELLOW][j].x = (550 + ((100 * j) if j < 2 else (100 * (j - 2)))) #Yellow.
            homes[YELLOW][j].y = (550 if j < 2 else 650)
            homes[GREEN][j].x = (550 + ((100 * j) if j < 2 else (100 * (j - 2)))) #Green.
            homes[GREEN][j].y = (100 if j < 2 else 200)
            
            #The rest, though, can be condensed...
            for i in range(4):
                players[i][j].x0 = homes[i][j].x
                players[i][j].y0 = homes[i][j].y
                players[i][j].x = (players[i][j].x0) + 25
                players[i][j].y = (players[i][j].y0) + 25

    #This was not explained originally, but here he is configuring the coordinates for each of the outer boxes.
    #Starting at the bottom left square next to blue, and working clockwise...
    #Blue's left column.
    for i in range(6):
        box[i].x = 300
        box[i].y = (700 - (50 * i))

    #Red's bottom row.
    for i in range(6, 12):
        box[i].x = (250 - (50 * (i - 6)))
        box[i].y = (400)

    #Red's middle square.
    box[12].x = 0
    box[12].y = 350

    #Red's top row.
    for i in range(13, 19):
        box[i].x = (0 + (50 * (i - 13)))
        box[i].y = (300)

    #Green's left column.
    for i in range(19, 25):
        box[i].x = (300)
        box[i].y = (250 - (50 * (i - 19)))

    #Green's middle square.
    box[25].x = 350
    box[25].y = 0

    #Green's right column.
    for i in range(26, 32):
        box[i].x = (400)
        box[i].y = (0 + (50 * (i - 26)))

    #Yellow's top row.
    for i in range(32, 38):
        box[i].x = (450 + (50 * (i - 32)))
        box[i].y = (300)

    #Yellow's middle square.
    box[38].x = 700
    box[38].y = 350

    #Yellow's bottom row.
    for i in range(39, 45):
        box[i].x = (700 - (50 * (i - 39)))
        box[i].y = (400)

    #Blue's right column.
    for i in range(45, 51):
        box[i].x = (400)
        box[i].y = (450 + (50 * (i - 45)))

    #Blue's middle square.
    box[51].x = 350
    box[51].y = 700
    
    #This part also has to be changed to match the new notation.
    #Red.
    lx = 14 #This index pulls double duty. For this half of each player, it's the outer boxes indices
            #relative to the indices of the player. Also, the value of lx here is determined by
            #its "offset" from the first box--the bottom left spot for the blue squares.
            #Blue -> Red -> Green -> Yellow, in ascending order of offset.
    for i in range(52):
        cboxes[RED][i].x = box[lx].x
        cboxes[RED][i].y = box[lx].y
        lx = lx + 1
        if lx > 51:
            lx = 0

    lx = 50 #Here, it instead is to fill out the final, colored squares that lead to each player's goal.
    for i in range(7):
        cboxes[RED][lx].x = (0 + (50 * i))
        cboxes[RED][lx].y = 350
        lx = lx + 1
        
    #Blue.
    lx = 1
    for i in range(52):
        cboxes[BLUE][i].x = box[lx].x
        cboxes[BLUE][i].y = box[lx].y
        lx = lx + 1
        if lx > 51:
            lx = 0

    lx = 50
    for i in range(7):
        cboxes[BLUE][lx].x = 350
        cboxes[BLUE][lx].y = (700 - (50 * i))
        lx = lx + 1
        
    #Yellow.
    lx = 40
    for i in range(52):
        cboxes[YELLOW][i].x = box[lx].x
        cboxes[YELLOW][i].y = box[lx].y
        lx = lx + 1
        if lx > 51:
            lx = 0

    lx = 50
    for i in range(7):
        cboxes[YELLOW][lx].x = (700 - (50 * i))
        cboxes[YELLOW][lx].y = (350)
        lx = lx + 1
        
    #Green.
    lx = 27
    for i in range(52):

        cboxes[GREEN][i].x = box[lx].x
        cboxes[GREEN][i].y = box[lx].y

        lx = lx + 1
        if lx > 51:
            lx = 0

    lx = 50
    for i in range(7):
        cboxes[GREEN][lx].x = 350
        cboxes[GREEN][lx].y = (0 + (50 * i))
        lx = lx + 1
    
    #With the placement determined, actually draw the pieces on the board.
    for i in range(4):
        players[RED][i].swap()
        players[BLUE][i].swap()
        players[GREEN][i].swap()
        players[YELLOW][i].swap()
    #################################################### THE END ##########################################################