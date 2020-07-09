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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    start = problem.getStartState()
    stack = util.Stack()
    parent = {}
    explored = set()
    stack.push(start)
    parent[start] = None
    while not stack.isEmpty():
        x = stack.pop()
        explored.add(x)
        if problem.isGoalState(x): 
            path = []
            while(parent[x] != None):
                x, action = parent[x]
                path.append(action)
            return path[::-1]
        successors = problem.getSuccessors(x)
        for (next_state, next_action, _) in successors:
            if next_state not in explored:
                stack.push(next_state)
                parent[next_state] = (x, next_action)
    print("No path found")
    return None


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    q = util.Queue()
    parent = {}
    explored = set()
    q.push(start)
    parent[start] = None
    while not q.isEmpty():
        x = q.pop()
        explored.add(x)
        if problem.isGoalState(x): 
            path = []
            while(parent[x] != None):
                x, action = parent[x]
                path.append(action)
            return path[::-1]
        successors = problem.getSuccessors(x)
        for (next_state, next_action, _) in successors:
            if next_state not in explored:
                q.push(next_state)
                parent[next_state] = (x, next_action)
                explored.add(next_state)
    print("No path found")
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    
    pq = util.PriorityQueue()
    parent = {}
    explored = set()
    
    pq.push(start, 0)
    parent[start] = (None, None, 0)

    while not pq.isEmpty():
    
        x= pq.pop()
        explored.add(x)
    
        if problem.isGoalState(x): 
            path = []
            while(parent[x][0] != None):
                x, action, _ = parent[x]
                path.append(action)
            return path[::-1]
    
        cost = parent[x][2]
        successors = problem.getSuccessors(x)
        for (next_state, next_action, next_cost) in successors:
            new_cost = cost+next_cost
            if next_state not in explored :
                if next_state not in parent or new_cost < parent[next_state][2]:
                    pq.update(next_state, new_cost)            
                    parent[next_state] = (x, next_action, new_cost)
    print("No path found")
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start = problem.getStartState()
    
    pq = util.PriorityQueue()
    parent = {}
    explored = set()
    
    pq.push(start, heuristic(start, problem))
    parent[start] = (None, None, 0)

    while not pq.isEmpty():
        x= pq.pop()
        explored.add(x)

        if problem.isGoalState(x): 
            path = []
            while(parent[x][0] != None):
                x, action, _ = parent[x]
                path.append(action)
            return path[::-1]
    
        cost = parent[x][2]
        successors = problem.getSuccessors(x)
        for (next_state, next_action, next_cost) in successors:
            new_cost = cost+next_cost
            f = new_cost + heuristic(next_state, problem)
            old_f = None
            if next_state in parent and parent[next_state][0] != None:
                old_f = (parent[next_state][2] + heuristic(next_state, problem))
            if next_state not in explored :
                if next_state not in parent or f  < old_f:
                    pq.update(next_state, f)            
                    parent[next_state] = (x, next_action, new_cost)
    print("No path found")
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
