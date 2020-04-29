import numpy as np
from scipy.optimize import linprog

class MinimaxQPlayer:

    def __init__(self, numStates, numActionsA, numActionsB, decay, expl, gamma):
        self.decay = decay  # Learning rate decay
        self.expl = expl    # Epsilon (how often the agent takes a random action)
        self.gamma = gamma  # Discount factor
        self.alpha = 1      # Learning rate
        self.V = np.ones(numStates) # State value
        self.Q = np.ones((numStates, numActionsA, numActionsB)) # Q value
        self.pi = np.ones((numStates, numActionsA)) / numActionsA   # Policy
        self.numStates = numStates
        self.numActionsA = numActionsA
        self.numActionsB = numActionsB
        self.learning = True    # Stop learning or not

    def chooseAction(self, state, restrict=None):
        if self.learning and np.random.rand() < self.expl:  # Pick random action if learning is true and within epsilon prob
            action = np.random.randint(self.numActionsA)
        else:   # Else, go with the policy
            action = self.weightedActionChoice(state)
        return action

    def weightedActionChoice(self, state):  # Chooses random value that matches with an action from the policy
        rand = np.random.rand()             # As policy distb changes, we become more biased towards certain actions over others
        cumSumProb = np.cumsum(self.pi[state])
        action = 0
        while rand > cumSumProb[action]:
            action += 1
        return action

    def getReward(self, initialState, finalState, actions, reward, restrictActions=None):
        if not self.learning:   
            return
        actionA, actionB = actions
        self.Q[initialState, actionA, actionB] = (1 - self.alpha) * self.Q[initialState, actionA, actionB] + \
            self.alpha * (reward + self.gamma * self.V[finalState])
        self.V[initialState] = self.updatePolicy(initialState)  # EQUIVALENT TO : min(np.sum(self.Q[initialState].T * self.pi[initialState], axis=1))
        # self.V[initialState] = max(np.sum(self.Q[initialState].T * self.pi[initialState], axis=1))
        self.alpha *= self.decay

    def updatePolicy(self, state, retry=False):
        # c = np.zeros(self.numActionsA + 1)
        # c[0] = -1
        # # c = [-1,-1,-1]
        # A_ub = np.ones((self.numActionsB, self.numActionsA + 1))  # I believe this should be (numPlayers, numActionsA + 1)
        # A_ub[:, 1:] = -self.Q[state].T
        # b_ub = np.zeros(self.numActionsB)
        # A_eq = np.ones((1, self.numActionsA + 1))
        # A_eq[0, 0] = 0
        # b_eq = [1]
        # bounds = ((None, None),) + ((0, 1),) * self.numActionsA

        # res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

        if True:
            Qtranspose = self.Q[state].T
            newtemp = Qtranspose * self.pi[state]
            thissum = np.sum(newtemp, axis=1)
            minthissum = min(thissum)
            arr = [self.pi[state],minthissum]
            temp = np.argmax(arr)
            act = arr[temp]
            self.pi[state] = act    
        # if res.success:
        #     print("Policy updated with (state,action): ",state, ",", res.x[1:])
        #     self.pi[state] = res.x[1:]
        elif not retry:
            return self.updatePolicy(state, retry=True)
        # else:
        #     print("Alert : %s" % res.message)
        #     return self.V[state]
        # print("Returning state value: ", res.x[0])
        # return res.x[0]

    def policyForState(self, state):
        for i in range(self.numActionsA):
            print("Actions %d : %f" % (i, self.pi[state, i]))


if __name__ == '__main__':

    def testUpdatePolicy():
        m = MinimaxQPlayer(1, 2, 2, 1e-4, 0.2, 0.9)
        m.Q[0] = [[0, 1], [1, 0.5]]
        m.updatePolicy(0)
        print(m.pi)

    testUpdatePolicy()