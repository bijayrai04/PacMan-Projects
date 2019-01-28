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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print newPos
        # print newFood
        # print newScaredTimes
        score = 0
        listFoodRemaining = newFood.asList()
        capsules = successorGameState.getCapsules()
        if successorGameState.isWin():
            return 100000
        score += successorGameState.getScore()- currentGameState.getScore()
        if action == Directions.STOP:
            score -= 20
        score -= len(listFoodRemaining)* 20
        if newPos in currentGameState.getCapsules():
            score += 2000
        foodDistance = [0]
        for food in listFoodRemaining:
            foodDistance.append(manhattanDistance(food, newPos))
        foodDistanceSum = 0

        for distance in foodDistance:
            foodDistanceSum += distance
        if foodDistanceSum > 0:
            score += 1/foodDistanceSum
        if min(foodDistance):
            score += 1/min(foodDistance)

        score -= 5 * len(listFoodRemaining)

        ghostPosition = []
        for ghost in newGhostStates:
            ghostPosition.append(ghost.getPosition())

        ghostDistance = [0]
        for ghostPos in ghostPosition:
            ghostDistance.append(manhattanDistance(ghostPos, newPos))

        currGhostPosition = []
        for ghost in currentGameState.getGhostStates():
            currGhostPosition.append(ghost.getPosition())

        currGhostDistance = [0]
        for ghostPos in currGhostPosition:
            currGhostDistance.append(manhattanDistance(ghostPos, newPos))

        if newPos == min(ghostDistance):
            score += 1000

        scaredTimeSum = 0
        for time in newScaredTimes:
            scaredTimeSum += time

        if scaredTimeSum > 0 and min(currGhostDistance) < min(ghostDistance):
            score += 300
        else:
            score -= 100

        if scaredTimeSum <= 0 and min(currGhostDistance) < min(ghostDistance):
            score -= 300
        else:
            score += 100

        return score
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
        "*** YOUR CODE HERE ***"
        #Ghosts are always trying to minimize the score it gives
        def minValue(gameState, depth, agentIndex):
            scoreMin = 1000000
            if gameState.isWin() or gameState.isLose(): #Cutoff Test
                return self.evaluationFunction(gameState)
            possibleActionsMin = gameState.getLegalActions(agentIndex)
            for action in possibleActionsMin:
                successorMin = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:
                    scoreMin = min (scoreMin, maxValue(successorMin, depth))
                else:
                    scoreMin = min (scoreMin, minValue(successorMin, depth, agentIndex+1))
            return scoreMin

        #Pacman is always trying to maximize the score it receives
        def maxValue(gameState, depth, agentIndex = 0): #Pacman always has agentIndex = 0
            updatedDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or updatedDepth == self.depth: #Cutoff test
                return self.evaluationFunction(gameState)
            scoreMax = -1000000
            possibleActionsMax = gameState.getLegalActions(0)
            for action in possibleActionsMax:
                successorMax = gameState.generateSuccessor(0, action)
                scoreMax = max(scoreMax, minValue(successorMax, updatedDepth, agentIndex+1))
            return scoreMax

        # MiniMax Strategy
        possibleActions = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        possibleActions = gameState.getLegalActions(0)
        comparableScore = -100000000
        bestAction = ''
        for action in possibleActions:
            successor = gameState.generateSuccessor(0, action)
            score = minValue(successor, 0, 1) #Looking at the first Ghost Nodes
            if score > comparableScore:
                comparableScore = score
                bestAction = action
        return bestAction
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #Ghosts are always trying to minimize the score it gives
        def minValue(gameState, depth, agentIndex, alphaVal, betaVal):
            scoreMin = 1000000
            if gameState.isWin() or gameState.isLose(): #Cutoff Test
                return self.evaluationFunction(gameState)
            possibleActionsMin = gameState.getLegalActions(agentIndex)
            betaNew = betaVal
            for action in possibleActionsMin:
                successorMin = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:
                    scoreMin = min (scoreMin, maxValue(successorMin, depth, alphaVal, betaNew))
                    if scoreMin < alphaVal:
                        return scoreMin
                    betaNew = min(betaNew, scoreMin)
                else:
                    scoreMin = min (scoreMin, minValue(successorMin, depth, agentIndex+1, alphaVal, betaNew))
                    if scoreMin < alphaVal:
                        return scoreMin
                    betaNew = min(betaNew, scoreMin)
            return scoreMin

        #Pacman is always trying to maximize the score it receives
        def maxValue(gameState, depth, alphaVal, betaVal, agentIndex = 0): #Pacman always has agentIndex = 0
            updatedDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or updatedDepth == self.depth: #Cutoff test
                return self.evaluationFunction(gameState)
            scoreMax = -1000000
            possibleActionsMax = gameState.getLegalActions(0)
            alphaNew = alphaVal
            for action in possibleActionsMax:
                successorMax = gameState.generateSuccessor(0, action)
                scoreMax = max(scoreMax, minValue(successorMax, updatedDepth, agentIndex+1, alphaNew, betaVal))
                if scoreMax > betaVal:
                    return scoreMax
                alphaNew = max (alphaNew, scoreMax)
            return scoreMax

        # Alpha-beta Pruning (Not visiting useless nodes while using Minimax)
        possibleActions = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        possibleActions = gameState.getLegalActions(0)
        comparableScore = -100000000
        bestAction = ''
        alphaVal = -10000000 # Worst Case scenario for Pacman(receive)
        betaVal = 100000000 # Worst Case scenario for Ghosts(give)
        for action in possibleActions:
            successor = gameState.generateSuccessor(0, action)
            score = minValue(successor, 0, 1, alphaVal, betaVal) #Looking at the first Ghost Nodes
            if score > comparableScore:
                comparableScore = score
                bestAction = action
            # Alpha value update at the node
            if score > betaVal:
                return bestAction
            alphaVal = max(alphaVal, score)
        return bestAction

        #util.raiseNotDefined()

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
        "*** YOUR CODE HERE ***"
                #Ghosts are always trying to minimize the score it gives
        def expectedValue(gameState, depth, agentIndex):
            totExpedtedVal = 0
            if gameState.isWin() or gameState.isLose(): #Cutoff Test
                return self.evaluationFunction(gameState)
            possibleActionsMin = gameState.getLegalActions(agentIndex)
            for action in possibleActionsMin:
                successorMin = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:
                    expedtedVal = maxValue(successorMin, depth)
                else:
                    expedtedVal = expectedValue(successorMin, depth, agentIndex+1)
                totExpedtedVal += expedtedVal
            return float(totExpedtedVal)/float(len(possibleActionsMin))

        #Pacman is always trying to maximize the score it receives
        def maxValue(gameState, depth, agentIndex = 0): #Pacman always has agentIndex = 0
            updatedDepth = depth + 1
            if gameState.isWin() or gameState.isLose() or updatedDepth == self.depth: #Cutoff test
                return self.evaluationFunction(gameState)
            scoreMax = -1000000
            possibleActionsMax = gameState.getLegalActions(0)
            for action in possibleActionsMax:
                successorMax = gameState.generateSuccessor(0, action)
                scoreMax = max(scoreMax, expectedValue(successorMax, updatedDepth, agentIndex+1))
            return scoreMax

        # Expectimax Strategy (MiniMax assuming ghosts are suboptimal)
        possibleActions = gameState.getLegalActions(0)
        numAgents = gameState.getNumAgents()
        possibleActions = gameState.getLegalActions(0)
        comparableScore = -100000000
        bestAction = ''
        for action in possibleActions:
            successor = gameState.generateSuccessor(0, action)
            score = expectedValue(successor, 0, 1) #Looking at the first Ghost Nodes
            if score > comparableScore:
                comparableScore = score
                bestAction = action
        return bestAction

        #util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Scores are updated based the distance between the ghosts, food pellets,
      powercapsules and the current position of the player.

      Since the time ghosts are scared is beneficial to Pacman's movement, and the
      opposite harmful scores are updated accordingly. Most codes from Problem 1
      are reused to see their usefulness.

    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = 0
    score += currentGameState.getScore()
    capsules = currentGameState.getCapsules()

    listFood = newFood.asList()
    # score -= len(listFood)
    foodDistance = [0]
    for food in listFood:
        foodDistance.append(manhattanDistance(food, newPos))

    foodDistanceSum = 0
    for food in foodDistance:
        foodDistanceSum += food

    if foodDistanceSum > 0:
        score += 1/foodDistanceSum

    ghostPosition = []
    for ghost in newGhostStates:
        ghostPosition.append(ghost.getPosition())

    ghostDistance = [0]
    for ghostPos in ghostPosition:
        ghostDistance.append(manhattanDistance(ghostPos, newPos))

    sumGhostDistance = 0
    for ghostD in ghostDistance:
        sumGhostDistance += ghostD

    #if min(ghostDistance):
    #   score += ghostDistance 
    scaredTimeSum = 0
    for time in newScaredTimes:
        scaredTimeSum += time
    if newPos in capsules:
        score += 2000
    if scaredTimeSum > 0:
        score -= sumGhostDistance
        score += scaredTimeSum*2
        score -= len(capsules)
    else:
        score += len(capsules)
        score += sumGhostDistance
    return score

    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

