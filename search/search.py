# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

from util import *
import copy

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState() - Coordinate tuple (5, 5)
  print "Is the start a goal?", problem.isGoalState(problem.getStartState()) - boolean
  print "Start's successors:", problem.getSuccessors(problem.getStartState()) - [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
  """
  "*** YOUR CODE HERE ***"
  curState = problem.getStartState()
  visited = set()
  toDo = Stack()
  result = []
  if problem.isGoalState(curState):
    return result

  while True:
    visited.add(curState)
    # Get Successors
    successors = problem.getSuccessors(curState)
    for successor in successors:
      if successor[0] not in visited:
        newResult = list(result)
        newResult.append(successor[1])
        if problem.isGoalState(successor[0]):
          return newResult
        else:
          toDo.push((successor[0], newResult))
    if toDo.isEmpty(): # No available paths found
      break

    next = toDo.pop()
    curState = next[0]
    if curState in visited:
      continue
    result = next[1]

  raise Exception("No valid path found")
  
def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  curState = problem.getStartState()
  visited = set()
  toDo = Queue()
  result = []
  if problem.isGoalState(curState):
    return result

  while True:
    visited.add(curState)
    # Get Successors
    successors = problem.getSuccessors(curState)
    for successor in successors:
      if successor[0] not in visited:
        newResult = list(result)
        newResult.append(successor[1])
        if problem.isGoalState(successor[0]):
          return newResult
        else:
          toDo.push((successor[0], newResult))
    if toDo.isEmpty(): # No available paths found
      break

    next = toDo.pop()
    curState = next[0]
    if curState in visited:
      continue
    result = next[1]

  raise Exception("No valid path found")
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  curState = problem.getStartState()

  visited = set()
  toDo = PriorityQueue()
  result = []

  toDo.push((curState, result, 0), 0)
  if problem.isGoalState(curState):
    return result

  while not toDo.isEmpty():
    # Grab next node off PriorityQueue
    next = toDo.pop()
    curState = next[0]
    if curState in visited:
      continue
    else:
      visited.add(curState)
    result = next[1]
    costSoFar = next[2]

    # Get Successors
    successors = problem.getSuccessors(curState)
    for successor in successors:
      if successor[0] not in visited:
        totCost = costSoFar + successor[2]
        newResult = list(result)
        newResult.append(successor[1])
        if problem.isGoalState(successor[0]):
          return newResult
        else:
          toDo.push((successor[0], newResult, totCost), totCost)

  raise Exception("No valid path found")

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  curState = problem.getStartState()
  visited = set()
  toDo = PriorityQueue()
  result = []

  toDo.push((curState, result, 0), 0)
  if problem.isGoalState(curState):
    return result

  while not toDo.isEmpty():
    # Grab next node off PriorityQueue
    next = toDo.pop()
    curState = next[0]
    if curState in visited:
      continue
    else:
      visited.add(curState)
    result = next[1]
    costSoFar = next[2]

    # Get Successors
    successors = problem.getSuccessors(curState)
    for successor in successors:
      if successor[0] not in visited:
        totCost = costSoFar + successor[2] + heuristic(successor[0], problem)
        newResult = list(result)
        newResult.append(successor[1])
        if problem.isGoalState(successor[0]):
          return newResult
        else:
          toDo.push((successor[0], newResult, totCost), totCost)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
