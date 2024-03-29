# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        
        '''
        print "Legal moves: ", legalMoves
        print "Best score: ", bestScore
        print "Best indices: ", bestIndices
        print "Chosen index: ", chosenIndex
        
        print legalMoves[chosenIndex], "\n"
        '''
        
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        #########
        
        # Returns info about entire game state, including pellets (small dots when printed), 
        # pacman ('v' when printed, but pointing in direction of travel), ghost ('G' when printed),
        # and big food ('o' when printed)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        # Returns coordinates of pacman's position
        newPos = successorGameState.getPacmanPosition()
        # Returns a grid of boolean (T/F) food indicator variables
        newFood = successorGameState.getFood()
        # Returns agentState of all ghosts (agent state looks like it includes position and direction, as well scared timer, and some other things,
        # shown in game.py)
        newGhostStates = successorGameState.getGhostStates()
        # Returns array of how long each ghost is scared for. Is 0 when ghost is not scared
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        '''
        print "Successor game state: ", successorGameState
        print "New position: ", newPos
        print "New food: ", newFood
        print "New ghost states: ", newGhostStates
        print "New scared times: ", newScaredTimes
        '''
        
        # Real meat and potatoes of my evaluation function
        #########
        
        # If the new position is the same as a ghost position, DO NOT allow the move to be made
        for ghostState in newGhostStates:
            '''
            print "Ghost's position: ", ghostState.getPosition()
            print "Pacman's position: ", newPos
            '''
            if newPos == ghostState.getPosition():
                return -1
            # If pacman is 2 manhattan distance from a ghost, don't allow the action
            if util.manhattanDistance(newPos, ghostState.getPosition()) <= 2:
                return -1
        
        # Return the reciprocal of the closest food + if the you will grab food,
        # this way we use next closest food distance (as well as if the position contains food) as our eval function
        # First check if the position we go to is food
        if newPos in currentGameState.getFood().asList():
            isFood = 1.0
        else:
            isFood = 0.0
        #Then calculate distance to nearest food
        closestFoodDist = 1000       #initial distance in case food is not found
        for foodPos in newFood.asList():
            foodDist = util.manhattanDistance(newPos, foodPos)
            if foodDist < closestFoodDist:
                closestFoodDist = foodDist
        '''
        print "closest food: ", closestFoodDist
        print "reciprocal: ", float(1.0 / closestFoodDist)
        print "Is the next action food: ", isFood
        '''
        return float(1.0 / closestFoodDist) + isFood
        
        
        ''' #THIS DOESN'T WORK
        # Return the reciprocal of the amount of food left
        return 1 / newFood.count()
        '''

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        #Wikipedia has pseudocode: https://en.wikipedia.org/wiki/Minimax
        '''
        #Algorithm from AI - A Modern Approach, 3rd Edition, pg. 166
        function MINIMAX-DECISION(state) returns an action
            return argmax a in ACTIONS(s) MIN-VALUE(RESULT(state, a))
        --------
        function MAX-VALUE(state) returns a utility value
            if TERMINAL-TEST(state) then return UTILITY(state)
            v <- -infinity
            for each a in ACTIONS(state) do
                v <- MAX(v, MIN-VALUE(RESULT(s, a)))
            return v
        --------
        function MIN-VALUE(state) returns a utility value
            if TERMINAL-TEST(state) then return UTILITY(state)
            v <- infinity
            for each a in ACTIONS(state) do
                v <- MIN(v, MAX-VALUE(RESULT(s, a)))
            return v
        '''
        "*** YOUR CODE HERE ***"
        ###As a note, I am returning [action, scoreTheActionWillEarn] for my functions
        
        def minmaxDecision(state, depth, agentIndex):
            #print "Current depth: ", depth     #Used for DEBUGGING
            #If we look one past the total # of agents, then it is time to restart the tree and look at pacman's action
            #This means we will have to increase the depth as well
            if agentIndex >= state.getNumAgents():
                depth = depth + 1
                agentIndex = 0
            #print "New depth: ", depth     #Used for DEBUGGING
            
            #If we are looking at pacman
            if agentIndex == 0:
                return maxValue(state, depth, agentIndex)
            #If we are looking at any of the ghosts
            else:
                return minValue(state, depth, agentIndex)
                
        def maxValue(state, depth, agentIndex):
            moves = state.getLegalActions()
            #print "Max moves: ", moves     #Used for DEBUGGING
            #First check terminal test, i.e. are there no moves to make OR we have reached the end depth
            #If we are at the terminal test, we return just the utility value (which is just score) 
            if len(moves) == 0 or depth == self.depth:
                return self.evaluationFunction(state)
                
            #v will hold our [action, score]
            v = ["", -float('inf')]
            
            #Then we go through all possible moves and find the max value it can give us
            for m in moves:
                result = minValue(state.generateSuccessor(0, m), depth, agentIndex + 1)
                #check if result's utility value (i.e. score) is larger than current v (i.e. check for max among all moves)
                if not isinstance(result, list):        #since we can be given [action, score] or just score, I check first which is being passed in
                    competingScore = result
                else:
                    competingScore = result[1]
                    
                if competingScore > v[1]:
                    v[0] = m
                    v[1] = competingScore
            return v
            
        def minValue(state, depth, agentIndex):
            moves = state.getLegalActions(agentIndex)
            #print "Min moves: ", moves     #Used for DEBUGGING
            #First check terminal test, i.e. are there no moves to make OR we have reached the end depth
            #If we are at the terminal test, we return just the utility value (which is just score) 
            if len(moves) == 0 or depth == self.depth:
                return self.evaluationFunction(state)
                
            #v will hold our [action, score]
            v = ["", float('inf')]
            
            #Then we go through all possible moves and find the min value it can give us
            for m in moves:
                #note that I call minmaxDecision instead of maxValue b/c I may have to iterate through multiple ghosts
                result = minmaxDecision(state.generateSuccessor(agentIndex, m), depth, agentIndex + 1)
                #check if result's utility value (i.e. score) is smaller than current v (i.e. check for min among all moves)
                if not isinstance(result, list):        #since we can be given [action, score] or just score, I check first which is being passed in
                    competingScore = result
                else:
                    competingScore = result[1]
                
                #print "The competing score is: ", competingScore       #Used for DEBUGGING
                if competingScore < v[1]:
                    v[0] = m
                    v[1] = competingScore
            return v
        
        #print "Intial depth: ", self.depth     #Used for DEBUGGING
        return minmaxDecision(gameState, 0, 0)[0]
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        #Algorithm from AI - A Modern Approach, 3rd Edition, pg. 170
        '''
        function ALPHA-BETA-SEARCH(state) returns an action
            v <- MAX-VALUE(state, -infinity, +infinity)
            return the action in ACTIONS(state) with value v
        ----------
        function MAX-VALUE(state, alpha, beta) returns a utility value
            if TERMINAL-TEST(state) then return UTILITY(state)
            v <- -infinity
            for each a in ACTIONS(state) do
                v <- MAX(v, MIN-VALUE(RESULT(s,a),alpha, beta))
                if v >= beta then return v
                alpha <- MAX(alpha, v)
            return v
        ----------
        function MIN-VALUE(state, alpha, beta) returns a utility value
            if TERMINAL-TEST(state) then return UTILITY(state)
            v <- +infinity
            for each a in ACTIONS(state) do
                v <- MIN(v, MAX-VALUE(RESULT(s,a) ,alpha, beta))
                if v <= alpha then return v
                beta <- MIN(beta, v)
            return v
        '''
        "*** YOUR CODE HERE ***"
        def alphaBetaSearch(state, depth, agentIndex, alpha, beta):
            #If we look one past the total # of agents, then it is time to restart the tree and look at pacman's action
            #This means we will have to increase the depth as well
            if agentIndex >= state.getNumAgents():
                depth = depth + 1
                agentIndex = 0
            
            #If we are looking at pacman
            if agentIndex == 0:
                return maxValue(state, depth, agentIndex, alpha, beta)
            #If we are looking at any of the ghosts
            else:
                return minValue(state, depth, agentIndex, alpha, beta)
                
        def maxValue(state, depth, agentIndex, alpha, beta):
            moves = state.getLegalActions()
            #First check terminal test, i.e. are there no moves to make OR we have reached the end depth
            #If we are at the terminal test, we return just the utility value (which is just score) 
            if len(moves) == 0 or depth == self.depth:
                return self.evaluationFunction(state)
                
            #v will hold our [action, score]
            v = ["", -float('inf')]
            
            #Then we go through all possible moves and find the max value it can give us
            for m in moves:
                result = minValue(state.generateSuccessor(0, m), depth, agentIndex + 1, alpha, beta)
                #check if result's utility value (i.e. score) is larger than current v (i.e. check for max among all moves)
                if not isinstance(result, list):        #since we can be given [action, score] or just score, I check first which is being passed in
                    competingScore = result
                else:
                    competingScore = result[1]
                    
                if competingScore > v[1]:
                    v[0] = m
                    v[1] = competingScore
                #check if result's utility value (i.e. score) is larger than beta
                if v[1] > beta:
                    return v
                #set alpha to be the maximum value of all moves
                if alpha < v[1]:
                    alpha = v[1]
            return v
            
        def minValue(state, depth, agentIndex, alpha, beta):
            moves = state.getLegalActions(agentIndex)
            #First check terminal test, i.e. are there no moves to make OR we have reached the end depth
            #If we are at the terminal test, we return just the utility value (which is just score) 
            if len(moves) == 0 or depth == self.depth:
                return self.evaluationFunction(state)
                
            #v will hold our [action, score]
            v = ["", float('inf')]
            
            #Then we go through all possible moves and find the min value it can give us
            for m in moves:
                #note that I call alphaBetaSearch instead of maxValue b/c I may have to iterate through multiple ghosts
                result = alphaBetaSearch(state.generateSuccessor(agentIndex, m), depth, agentIndex + 1, alpha, beta)
                #check if result's utility value (i.e. score) is smaller than current v (i.e. check for min among all moves)
                if not isinstance(result, list):        #since we can be given [action, score] or just score, I check first which is being passed in
                    competingScore = result
                else:
                    competingScore = result[1]
                
                if competingScore < v[1]:
                    v[0] = m
                    v[1] = competingScore
                #check if result's utility value (i.e. score) is smaller than alpha
                if v[1] < alpha:
                    return v
                #set beta to be the minimum value of all moves
                if beta > v[1]:
                    beta = v[1]
            return v
        
        # when calling the function for the first time, alpha should be - infinity, beta shuold be + infinity, referenced from: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
        return alphaBetaSearch(gameState, 0, 0, -float('inf'), float('inf'))[0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        #Pseudocode according to Berkely AI Lecture 7
            #Note that my implementation differs b/c I check for terminal state within the MAX and EXP functions (much like above)
        '''
        def value(state):
            if the state is a terminal state: return the state's utility
            if the next agent is MAX: return max-value(state)
            if the next agent is EXP: return exp-value(state)
        def max-value(state):
            initialize v = -infinity
            for each successor of state:
                v = max(v, value(successor))
            return v
        def exp-value(state):
            initialize v = 0
            for each successor of state:
                p = probability(successor)
                v += p * value(successor)
            return v
        '''
        
        "*** YOUR CODE HERE ***"
        def expectiMax(state, depth, agentIndex):
            #If we look one past the total # of agents, then it is time to restart the tree and look at pacman's action
            #This means we will have to increase the depth as well
            if agentIndex >= state.getNumAgents():
                depth = depth + 1
                agentIndex = 0
            
            #If we are looking at pacman
            if agentIndex == 0:
                return maxValue(state, depth, agentIndex)
            #If we are looking at any of the ghosts
            else:
                return expValue(state, depth, agentIndex)
                
        def maxValue(state, depth, agentIndex):
            moves = state.getLegalActions()
            #First check terminal test, i.e. are there no moves to make OR we have reached the end depth
            #If we are at the terminal test, we return just the utility value (which is just score) 
            if len(moves) == 0 or depth == self.depth:
                return self.evaluationFunction(state)
                
            #v will hold our [action, score]
            v = ["", -float('inf')]
            
            #Then we go through all possible moves and find the max value it can give us
            for m in moves:
                result = expValue(state.generateSuccessor(0, m), depth, agentIndex + 1)
                #check if result's utility value (i.e. score) is larger than current v (i.e. check for max among all moves)
                if not isinstance(result, list):        #since we can be given [action, score] or just score, I check first which is being passed in
                    competingScore = result
                else:
                    competingScore = result[1]
                    
                if competingScore > v[1]:
                    v[0] = m
                    v[1] = competingScore
            return v
            
        def expValue(state, depth, agentIndex):
            moves = state.getLegalActions(agentIndex)
            #First check terminal test, i.e. are there no moves to make OR we have reached the end depth
            #If we are at the terminal test, we return just the utility value (which is just score) 
            if len(moves) == 0 or depth == self.depth:
                return self.evaluationFunction(state)
                
            #v will hold our [action, score]
            v = ["", 0.0]
            #Here I randomly select one of the ghost's legal moves and predict that the ghost will choose this random move
            v[0] = random.choice(moves)
            #p will hold the probabilty a move is chosen, which is just 1/(# of moves) since each move has the same probabilty of being chosen
            p = 1.0 / float(len(moves))
            
            #Then we go through all possible moves and compute the expected score (which is prob(move) * score(move), summed over all moves)
            for m in moves:
                #note that I call expectiMax instead of maxValue b/c I may have to iterate through multiple ghosts
                result = expectiMax(state.generateSuccessor(agentIndex, m), depth, agentIndex + 1)
                if not isinstance(result, list):        #since we can be given [action, score] or just score, I check first which is being passed in
                    value = float(result)
                else:
                    value = float(result[1])
                #Adding expected value for one particular move to total expected value
                v[1] = v[1] + (p * value)
            return v
        
        return expectiMax(gameState, 0, 0)[0]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

