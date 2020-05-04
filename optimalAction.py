import numpy as np
import math as m
import random
from scipy._lib.six import xrange
import ludo_game
def maximax(nextStates, playerList, modifiedQtable, actionMaxAt, currentDepth = -1, maxDepth = 3, coinPositions = []):  
    # Q table is a nS*24*24*24*24 table 
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
    eachActionQMaxAt = []
    maxQ = -m.inf
    currentDepth += 1
    stateNum = 0
    if currentDepth == maxDepth+1:  # Base case
        return

################################### If Root Player #######################################################################        
    elif currentDepth == 0:
        print("We have reached the root! The root player is: ", playerList[currentDepth])
        validActions = ludo_game.getValidMoves()   # Get valid moves for the root player who just rolled the dice
        print("Valid actions for root are: ", validActions)
        nextStates = getNextStatesForActions(playerList[currentDepth], coinPositions, currentDepth)
        newactionMaxAt = []
        for state in nextStates:
            stateNum = ludo_game.getStateNumber(playerList[currentDepth], state)   # This is the function imported from ludo_game
            maximax(nextStates=nextStates,playerList= playerList,modifiedQtable= modifiedQtable,actionMaxAt= actionMaxAt,currentDepth= currentDepth,maxDepth= maxDepth,coinPositions= coinPositions)
            allActionsMaxQ = -m.inf
            # Checking if the current lvl corresponds to player 0
            if(playerList[currentDepth] == 0): 
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    if(actionMaxAt[aNum][0] in validActions):
                        eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, actionMaxAt[aNum][0], :, :, :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                        i = aNum    # Copying the index value of that action
                        j,k,l = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                        eachActionQMaxAt.append([i,j,k,l])
                        if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                            allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt 
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,newactionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else:
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,actionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass

            # Checking if the current lvl corresponds to player 1
            if(playerList[currentDepth] == 1):  
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    if(actionMaxAt[aNum][1] in validActions):
                        eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, :, actionMaxAt[aNum][1], :, :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                        j = aNum    # Copying the index value of that action
                        i,k,l = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                        eachActionQMaxAt.append([i,j,k,l])
                        if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                            allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,newactionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else:
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,actionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass
            
            # Checking if the current lvl corresponds to player 2
            if(playerList[currentDepth] == 2):  
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    if(actionMaxAt[aNum][2] in validActions):
                        eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, :, :, actionMaxAt[aNum][2], :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                        k = aNum    # Copying the index value of that action
                        i,j,l = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                        eachActionQMaxAt.append([i,j,k,l])
                        if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                            allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt 
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,newactionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else:
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,actionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass

            # Checking if the current lvl corresponds to player 3
            if(playerList[currentDepth] == 3):  
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    if(actionMaxAt[aNum][3] in validActions):
                        eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, :, :, :, actionMaxAt[aNum][3]] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                        l = aNum    # Copying the index value of that action
                        i,j,k = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                        eachActionQMaxAt.append([i,j,k,l])
                        if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                            allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt 
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,newactionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        print("This is the action player ",playerList[currentDepth]," should do: ", actionThePlayerShouldDo)
                        return actionThePlayerShouldDo   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else:
                        maxActionIndex = findMaxActionIndex(playerList[0],modifiedQtable,stateNum,actionMaxAt)
                        print("We are returning now")
                        actionThePlayerShouldDo = maxActionIndex[playerList[0]]
                        return actionThePlayerShouldDo    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass
####################################### If not Root Player ###########################################################################################################################                
    else:
        nextStates = getNextStatesForActions(playerList[currentDepth], coinPositions, currentDepth)
        newactionMaxAt = []
        for state in nextStates:
            stateNum = ludo_game.getStateNumber(playerList[currentDepth], state)   # This is the function imported from ludo_game
            maximax(nextStates=nextStates,playerList= playerList,modifiedQtable= modifiedQtable,actionMaxAt= actionMaxAt,currentDepth= currentDepth,maxDepth= maxDepth,coinPositions= coinPositions)
            allActionsMaxQ = -m.inf
            # Checking if the current lvl corresponds to player 0
            if(playerList[currentDepth] == 0): 
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, actionMaxAt[aNum][0], :, :, :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    i = aNum    # Copying the index value of that action
                    j,k,l = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    eachActionQMaxAt.append([i,j,k,l])
                    if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                        allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt 
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        return newactionMaxAt   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else: return actionMaxAt    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass

            # Checking if the current lvl corresponds to player 1
            if(playerList[currentDepth] == 1):  
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, :, actionMaxAt[aNum][1], :, :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    j = aNum    # Copying the index value of that action
                    i,k,l = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    eachActionQMaxAt.append([i,j,k,l])
                    if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                        allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        return newactionMaxAt   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else: return actionMaxAt    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass
            
            # Checking if the current lvl corresponds to player 2
            if(playerList[currentDepth] == 2):  
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, :, :, actionMaxAt[aNum][2], :] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    k = aNum    # Copying the index value of that action
                    i,j,l = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    eachActionQMaxAt.append([i,j,k,l])
                    if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                        allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt 
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        return newactionMaxAt   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else: return actionMaxAt    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass

            # Checking if the current lvl corresponds to player 3
            if(playerList[currentDepth] == 3):  
                print("Current Player: ", playerList[currentDepth])
                for aNum in range(len(actionMaxAt)):
                    eachActionQ = modifiedQtable[playerList[currentDepth],stateNum, :, :, :, actionMaxAt[aNum][3]] # Extracting all Q values I get wrt others' actions for one action (aNum) of mine
                    l = aNum    # Copying the index value of that action
                    i,j,k = np.unravel_index(eachActionQ.argmax(), eachActionQ.shape) # Getting the index of the max Q value out of all values corresponding to that action
                    eachActionQMaxAt.append([i,j,k,l])
                    if(eachActionQ.argmax() > allActionsMaxQ):     # If the max Q value from this action is the best among all the actions for this player 
                        allActionsMaxQ = eachActionQ.argmax()
                if(allActionsMaxQ > maxQ):
                    newactionMaxAt = eachActionQMaxAt    # I use a new var here to copy the max actionslist because I don't want to replace the actionsMaxAt 
                    maxQ = allActionsMaxQ                 # within the for loop which is being used as the modifiedQtable index before moving to the previous recursion level
                    if state == nextStates[-1]:     # Only return a value at the last state for that player so that the for loop doesn't exit before exploring all next states
                        return newactionMaxAt   # The returned newActionMaxAt was updated only in the states where it had a better q value than the already explored states, 
                                                # so we are only returning the best possible actions list for that player from all his states.
                    else: return actionMaxAt    # This is returned when none of the states for that player found a better Q value. This will not execute usually, it is a default condition.
                else: pass

######################################## End of Maximax ###############################################################################################


def findMaxActionIndex(rootPlayer, modifiedQtable, stateNum, actionMaxAt):
    maxAction = -m.inf
    maxActionIndex = -m.inf
    for act in actionMaxAt:
        print("Player: ", rootPlayer, "stateNum: ",stateNum, " Performing action: ", act[rootPlayer], " Corresponding Q value: ",modifiedQtable[rootPlayer,stateNum,act[0],act[1],act[2],act[3]])
        if(modifiedQtable[rootPlayer,stateNum,act[0],act[1],act[2],act[3]] > maxAction):
            maxAction = modifiedQtable[rootPlayer,stateNum,act[0],act[1],act[2],act[3]]
            maxActionIndex = act
    return maxActionIndex

################################### EVAN ###################################################
# Returns a list of lists (each valid state that can result from the valid actions)
def getNextStatesForActions(currentPlayer, coinPositions, currentDepth):
    nextStates = [] #The list of next states from the actions available, determined by the feature numbers.
    #If the player is the root player, the valid states are chosen from the valid moves that come from the actual roll.
    if currentDepth == 0: #0 is the root, isn't it? Even if it gets passed in as -1, it gets incremented before this call...
        validMoves = ludo_game.getValidMovesFromState(coinPositions, currentPlayer, ludo_game.rolls[ludo_game.nc])
        for move in validMoves:
            nextStates.append(ludo_game.getNewState(coinPositions, currentPlayer, move, ludo_game.rolls[ludo_game.nc]))
    #Otherwise, all possible rolls and their valid moves and states are calculated.
    else:
        for i in range(1, 7):
            validMoves = ludo_game.getValidMovesFromState(coinPositions, currentPlayer, i)
            for move in validMoves:
                nextStates.append(ludo_game.getNewState(coinPositions, currentPlayer, move, i))
        pass
    return nextStates
    # return [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]] # Each sublist is one state with 16 values one for each coin
############################################################################################

def modifiedQtable(Qtable, stateNum, totalActions, validActions, playerList):
    # Obtain original Q table, extract invalid actions from valid actions and mark all
    # fields corresponding to invalid actions in Q table as -inf
    currentPlayer = playerList[0]
    modifiedQtable = Qtable
    invalidActions =  set(totalActions) ^ set(validActions)
    print("Setting current player",  currentPlayer, "in state",stateNum, "invalid actions", invalidActions," to -inf")
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
    coinPositions = random.sample(xrange(57), 16)
    actionMaxAt = maximax(nextStates=nextStates,playerList= playerList,modifiedQtable= modifiedQtable,actionMaxAt= actionMaxAt,currentDepth= currentDepth,maxDepth= maxDepth,coinPositions= coinPositions)  # Returns a list of index values where that player has max Q value for that action
    print(modifiedQtable[0,0,actionMaxAt[0][0],actionMaxAt[0][1],actionMaxAt[0][2],actionMaxAt[0][3]])