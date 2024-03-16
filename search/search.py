# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    currentState = problem.getStartState()
    path = list()
    explored = set()
    frontier = util.Stack()
    if problem.isGoalState(currentState):
        return path
    frontier.push((currentState, path))
    while not frontier.isEmpty():
        (currentState, path) = frontier.pop()
        explored.add(currentState)
        if problem.isGoalState(currentState):
            return path
        for successor, action, _ in problem.getSuccessors(currentState):
            if successor not in explored:
                frontier.push((successor, path + [action]))
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    currentState = problem.getStartState()
    path = list()
    explored = set()
    frontier = util.Queue()
    if problem.isGoalState(currentState):
        return path
    frontier.push((currentState, path))
    while not frontier.isEmpty():
        (currentState, path) = frontier.pop()
        explored.add(currentState)
        if problem.isGoalState(currentState):
            return path
        for successor, action, _ in problem.getSuccessors(currentState):
            if successor not in explored and successor not in [s[0] for s in frontier.list]:
                frontier.push((successor, path + [action]))
    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    currentState = problem.getStartState()
    path = list()
    frontier = util.PriorityQueue()
    explored = set()
    """bfs dar cu cozi de prioritate basically"""
    if problem.isGoalState(currentState):
        return path
    frontier.push((currentState,path), 0)
    while not frontier.isEmpty():
        currentState, path = frontier.pop()
        explored.add(currentState)
        if problem.isGoalState(currentState):
            return path
        statesInFrontier = [entry[2] for entry in frontier.heap]
        for successor, action, cost in problem.getSuccessors(currentState):
            successorPath = path + [action]
            newPotentialCost = problem.getCostOfActions(successorPath)
            if successor not in explored and successor not in [s for s, v in statesInFrontier]:
                frontier.push((successor, successorPath), newPotentialCost)
            else:
                # basically trebuie sa vedem daca nu cumva am putea gasi un drum mai ieftin pentru starea unde am ajuns care deja e in frontiera lord
                for index, existingState in enumerate(statesInFrontier):
                    if existingState[0] == successor:
                        currentCost = frontier.heap[index][0]   # in tupla din heap pe pozitia 0 e costul
                        if currentCost > newPotentialCost:
                            frontier.heap[index] = (currentCost, frontier.heap[index][1], (successor, successorPath))
                            frontier.update((successor, successorPath), newPotentialCost)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    currentState = problem.getStartState()
    path = list()
    frontier = util.PriorityQueue()
    explored = set()
    """bfs dar cu cozi de prioritate basically"""
    if problem.isGoalState(currentState):
        return path
    frontier.push((currentState, path), heuristic(currentState, problem))
    while not frontier.isEmpty():
        currentState, path = frontier.pop()
        explored.add(currentState)
        if problem.isGoalState(currentState):
            return path
        statesInFrontier = [entry[2] for entry in frontier.heap]
        for successor, action, cost in problem.getSuccessors(currentState):
            successorPath = path + [action]
            newPotentialCost = problem.getCostOfActions(successorPath) + heuristic(successor, problem)
            if successor not in explored and successor not in [s for s, v in statesInFrontier]:
                frontier.push((successor, successorPath), newPotentialCost)
            else:
                # basically trebuie sa vedem daca nu cumva am putea gasi un drum mai ieftin pentru starea unde am ajuns care deja e in frontiera lord
                for index, existingState in enumerate(statesInFrontier):
                    if existingState[0] == successor:
                        currentCost = frontier.heap[index][0]  # in tupla din heap pe pozitia 0 e costul
                        if currentCost > newPotentialCost:
                            frontier.heap[index] = (currentCost, frontier.heap[index][1], (successor, successorPath))
                            frontier.update((successor, successorPath), newPotentialCost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
