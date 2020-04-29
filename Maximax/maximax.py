import numpy as np
import math as m
def maximax(stateNum, nextStates, playerList, modifiedQtable, actionMaxAt, currentDepth = -1, maxDepth = 3):  # Q table is a nS*24*24*24*24 table 
    # Q[playerNumber, state, actions, reactions, reactions, reactions]
    ########################################################################################################
    # NOTE: 
    # There could be multiple max Q values for each action a player takes. 
    # This happens when the max Q value obtained by me doing a certain action wrt 
    # the opponent doing a certain action is the same for multiple actions of 
    # the opponent for my same action. 
    # 
    #               Q[myaction,opponentaction] == Q[myaction,differentopponentaction]
    # 
    # This means the i,j,k,l should instead be a list of values each and not the 
    # first out of the many max values that we have. By picking just one 
    # value, we narrow down the possible actions the next player has to pick 
    # from and possibly making him suboptimal inturn. 
    # IDK how to work this out right now. To be checked later.
    ########################################################################################################
    tempMaxAt = []
    
    currentDepth += 1
    if currentDepth == maxDepth+1:  # Base case
        return actionMaxAt
    else:
        nextStates = getNextStatesForActions(playerList[currentDepth], stateNum)
        for stateNum in nextStates:
            actionMaxAt = maximax(stateNum, nextStates, playerList, modifiedQtable, actionMaxAt, currentDepth, maxDepth)
            # Checking if the current lvl corresponds to player 0
            if(playerList[currentDepth] == 0): 
                for aNum in range(len(actionMaxAt)):
                    temp = modifiedQtable[playerList[currentDepth],stateNum, actionMaxAt[aNum][0], :, :, :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    i = aNum    # Copying the index value of that action
                    j,k,l = np.unravel_index(temp.argmax(), temp.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    tempMaxAt.append([i,j,k,l])
                actionMaxAt = tempMaxAt
                return actionMaxAt

            # Checking if the current lvl corresponds to player 1
            if(playerList[currentDepth] == 1):  
                for aNum in range(len(actionMaxAt)):
                    temp = modifiedQtable[playerList[currentDepth],stateNum, :, actionMaxAt[aNum][1], :, :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    j = aNum    # Copying the index value of that action
                    i,k,l = np.unravel_index(temp.argmax(), temp.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    tempMaxAt.append([i,j,k,l])
                actionMaxAt = tempMaxAt
                return actionMaxAt
            
            # Checking if the current lvl corresponds to player 2
            if(playerList[currentDepth] == 2):  
                for aNum in range(len(actionMaxAt)):
                    temp = modifiedQtable[playerList[currentDepth],stateNum, :, :, actionMaxAt[aNum][2], :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    k = aNum    # Copying the index value of that action
                    i,j,l = np.unravel_index(temp.argmax(), temp.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    tempMaxAt.append([i,j,k,l])
                actionMaxAt = tempMaxAt
                return actionMaxAt

            # Checking if the current lvl corresponds to player 3
            if(playerList[currentDepth] == 3):  
                for aNum in range(len(actionMaxAt)):
                    temp = modifiedQtable[playerList[currentDepth],stateNum, :, :, :, actionMaxAt[aNum][3]] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    l = aNum    # Copying the index value of that action
                    i,j,k = np.unravel_index(temp.argmax(), temp.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    tempMaxAt.append([i,j,k,l])
                actionMaxAt = tempMaxAt
                return actionMaxAt 

def getNextStatesForActions(currentPlayer, stateNum):
    return [0]

def modifiedQtable(Qtable, stateNum, totalActions, validActions, playerList):
    # Obtain original Q table, extract invalid actions from valid actions and mark all
    # fields corresponding to invalid actions in Q table as -inf
    currentPlayer = playerList[0]
    modifiedQtable = Qtable
    invalidActions =  set(totalActions) ^ set(validActions)
    for i in range(len(playerList)):
        for j in invalidActions:
            if currentPlayer == 0:
                modifiedQtable[playerList[i], stateNum, j, :, :, :] = -m.inf
            elif currentPlayer == 1:
                modifiedQtable[playerList[i], stateNum, :, j, :, :] = -m.inf
            elif currentPlayer == 2:
                modifiedQtable[playerList[i], stateNum, :, :, j, :] = -m.inf
            elif currentPlayer == 3:
                modifiedQtable[playerList[i], stateNum, :, :, :, j] = -m.inf
            else: print("Player number input is incorrect!")

    return modifiedQtable

if __name__ == "__main__":
    nStates = 1
    nPlayers = 4
    nActions = 24 
    Qtable = np.random.rand(nPlayers, nStates, nActions, nActions, nActions, nActions)
    playerList = [0,0,0,0]
    totalActions = [i for i in range(24)]
    currentDepth = -1
    maxDepth = 3
    currentPlayer = 0   # Player indices are 0,1,2,3 (A corresponding color for each index: to be assigned)
    # change current player value according to turn and playerList will populate players in the order of turns
    validActions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    for i in range(4):
        if currentPlayer + i < 4:
            playerList[i] = currentPlayer + i
        else:
            playerList[i] = (currentPlayer + i) - 4
    stateNum = 0
    modifiedQtable = modifiedQtable(Qtable, stateNum, totalActions, validActions, playerList)
    actionMaxAt = [[i,i,i,i] for i in range(24)]
    nextStates = [0]
    actionMaxAt = maximax(stateNum, nextStates, playerList, modifiedQtable, actionMaxAt, currentDepth, maxDepth)  # Returns a list of index values where that player has max Q value for that action
    print(modifiedQtable[0,0,actionMaxAt[0][0],actionMaxAt[0][1],actionMaxAt[0][2],actionMaxAt[0][3]])