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
from copy import deepcopy

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


# Create a node class type that will hold node data and the node previous to it
class StateNode:
    def __init__(self, coord, direction, cost, prevstate):
        # Deepcopy is needed for tuple objects
        self.coord = deepcopy(coord)
        self.direction = direction
        self.cost = cost
        self.prevstate = deepcopy(prevstate)
    def next(self):
        return self.prevstate


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    QUESTION 1: Depth first search
    Frontier is a LIFO Queue, or Stack, successors will be in front.
    """
    "*** YOUR CODE HERE ***"
    # Create a start node
    originstate = problem.getStartState()
    node = StateNode(originstate, None, 0, None)
    # Initialize data objects, Queue for Frontier, set for explored, and dictionary to check for duplicate nodes
    frontier = util.Stack()
    frontier.push(node)
    explored = set()
    directions = []
    # Holds all nodes in either the frontier or explored, key - coord, value - cost
    nodedict = {node.coord: node.cost}

    # While loop until frontier is empty
    while True:
        # Testing show the top node

        # Check if the frontier is empty, it is error
        if frontier.isEmpty() is True:
            return
        else:
            # Pop the top node off of the frontier stack
            node = frontier.pop()
            explored.add(node.coord)
            # Add only those that move from the frontier to explored into the dictionary
            nodedict[node.coord] = node.cost
            # print("Currently explored node: ", node.coord)
            # Check if the current node is the solution
            if problem.isGoalState(node.coord) is True:
                # directions.append(node.direction)
                # Run through all nested objects in the matching node variable
                while node.coord != originstate:
                    # print("Directions from final node to start: ", node.direction)
                    directions.append(node.direction)
                    node = node.next()
                # This will create a path from end to start, reverse for answer
                directions.reverse()
                return directions

            else:
                # If it is not the solution, create nodes for all of it's children and add them to the frontier
                # print("Parent coordinates: ", node.coord)
                successorlist = problem.getSuccessors(node.coord)
                # print("Successors: ", successorlist)
                for i in range(len(successorlist)):
                    # Create a child node from the successorlist
                    # Successors contain coordinates[0], directions[1], and cost [2], and the parent node (node)
                    childnode = StateNode(successorlist[i][0], successorlist[i][1], successorlist[i][2], node)
                    # print("Child node of ", childnode.prevstate.coord, " is ", childnode.coord)
                    # Check if the coordinate has already been explored or is waiting in frontier
                    # print("Dictionary keys so far or coordinates accessed: ", nodedict.keys())
                    if nodedict.__contains__(childnode.coord) is True:
                        # print("Node", childnode.coord, "has already been explored or waits in frontier, ignoring")
                        continue
                    else:
                        # Add the newly verified node onto the frontier and to the dictionary
                        frontier.push(childnode)
                        # nodedict[childnode.coord] = childnode.cost


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    """
    QUESTION 2: BFS is identical to DFS with the exception of the frontier is now a FIFO queue instead of LIFO
    and elements are added to the dictionary as they are explored.
    """
    # Create a start node
    originstate = problem.getStartState()
    node = StateNode(originstate, None, 0, None)
    # Initialize data objects, Queue for Frontier, set for explored, and dictionary to check for duplicate nodes
    frontier = util.Queue()
    frontier.push(node)
    explored = set()
    directions = []
    # Holds all nodes in either the frontier or explored, key - coord, value - cost
    nodedict = {node.coord: node.cost}

    # While loop until frontier is empty
    while True:
        # Testing show the top node

        # Check if the frontier is empty, it is error
        if frontier.isEmpty() is True:
            return
        else:
            # Pop the top node off of the frontier stack
            node = frontier.pop()
            explored.add(node.coord)
            # Add only those that move from the frontier to explored into the dictionary
            # nodedict[node.coord] = node.cost
            # print("Currently explored node: ", node.coord)
            # Check if the current node is the solution
            if problem.isGoalState(node.coord) is True:
                # directions.append(node.direction)
                # Run through all nested objects in the matching node variable
                while node.coord != originstate:
                    # print("Directions from final node to start: ", node.direction)
                    directions.append(node.direction)
                    node = node.next()
                # This will create a path from end to start, reverse for answer
                directions.reverse()
                return directions

            else:
                # If it is not the solution, create nodes for all of it's children and add them to the frontier
                # print("Parent coordinates: ", node.coord)
                successorlist = problem.getSuccessors(node.coord)
                # print("Successors: ", successorlist)
                for i in range(len(successorlist)):
                    # Create a child node from the successorlist
                    # Successors contain coordinates[0], directions[1], and cost [2], and the parent node (node)
                    childnode = StateNode(successorlist[i][0], successorlist[i][1], successorlist[i][2], node)
                    # print("Child node of ", childnode.prevstate.coord, " is ", childnode.coord)
                    # Check if the coordinate has already been explored or is waiting in frontier
                    # print("Dictionary keys so far or coordinates accessed: ", nodedict.keys())
                    if nodedict.__contains__(childnode.coord) is True:
                        # print("Node", childnode.coord, "has already been explored or waits in frontier, ignoring")
                        continue
                    else:
                        # Add the newly verified node onto the frontier and to the dictionary
                        frontier.push(childnode)
                        nodedict[childnode.coord] = childnode.cost


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    """
    QUESTION 3: UFS, uses a priority queue for frontier
    """
    # Create a start node
    originstate = problem.getStartState()
    node = StateNode(originstate, None, 0, None)
    # Initialize data objects, Queue for Frontier, set for explored, and dictionary to check for duplicate nodes
    frontier = util.PriorityQueue()
    frontier.update(node, node.cost)
    explored = set()
    directions = []
    # Holds all nodes in either the frontier or explored, key - coord, value - cost
    nodefront = {node.coord: node.cost}
    nodeexpl = {}
    # Houses elements within frontier

    # While loop until frontier is empty
    while True:
        # Testing show the top node

        # Check if the frontier is empty, it is error
        if frontier.isEmpty() is True:
            return
        else:
            # Pop the top node off of the frontier stack
            # Remove the value from the frontier tracking dictionary and add it to the explored one
            node = frontier.pop()
            del nodefront[node.coord]
            explored.add(node.coord)
            nodeexpl[node.coord] = node.cost
            # Add only those that move from the frontier to explored into the dictionary
            # nodedict[node.coord] = node.cost
            # print("Currently explored node: ", node.coord)
            # Check if the current node is the solution
            if problem.isGoalState(node.coord) is True:
                # directions.append(node.direction)
                # Run through all nested objects in the matching node variable
                while node.coord != originstate:
                    # print("Directions from final node to start: ", node.direction)
                    directions.append(node.direction)
                    node = node.next()
                # This will create a path from end to start, reverse for answer
                directions.reverse()
                return directions

            else:
                # If it is not the solution, create nodes for all of it's children and add them to the frontier
                # print("Parent coordinates: ", node.coord)
                successorlist = problem.getSuccessors(node.coord)
                # print("Successors: ", successorlist)
                for i in range(len(successorlist)):
                    # Create a child node from the successorlist
                    # Successors contain coordinates[0], directions[1], and cost [2], and the parent node (node)
                    # UCS - node cost is equal to the cost of the path used to get to it.
                    childnode = StateNode(successorlist[i][0], successorlist[i][1], successorlist[i][2] + node.cost, node)
                    # print("Child node of ", childnode.prevstate.coord, " is ", childnode.coord)
                    # Check if the coordinate has already been explored or is waiting in frontier
                    # print("Dictionary keys so far or coordinates accessed: ", nodedict.keys())
                    # Check if the child node only goes back to the parent node, add it into the queue with double cost

                    if nodefront.__contains__(childnode.coord) is False and \
                            nodeexpl.__contains__(childnode.coord) is False:
                        # Child state is not within explored or frontier
                        frontier.update(childnode, childnode.cost)
                        nodefront[childnode.coord] = childnode.cost
                    # Check if the frontier contains the same node
                    elif nodefront.__contains__(childnode.coord) is True:
                        # If the frontier contains the current child node but with a higher path cost
                        childcost = childnode.cost
                        existingcost = nodefront[childnode.coord]
                        # print(childcost, existingcost)
                        if childcost < existingcost:
                            # replace the higher cost node with the current child node
                            # print(nodefront)
                            frontier.update(childnode, childnode.cost)
                            nodefront[childnode.coord] = childnode.cost
                            # print(nodefront)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    QUESTION 4: ASTAR search algorithm
    Based off of UCS algorithm
    """
    # Create a start node
    originstate = problem.getStartState()
    node = StateNode(originstate, None, heuristic(originstate, problem), None)

    # Initialize data objects, Queue for Frontier, set for explored, and dictionary to check for duplicate nodes
    frontier = util.PriorityQueue()
    frontier.update(node, node.cost)
    explored = set()
    directions = []
    visited = []
    # Holds all nodes in either the frontier or explored, key - coord, value - cost
    nodefront = {node.coord: node.cost}
    nodeexpl = {}
    # Houses elements within frontier
    # explored.add(node.coord)
    # nodeexpl[node.coord] = node.cost
    # print("Size of explored: ", explored.__len__(), " ", nodeexpl.__len__())
    # While loop until frontier is empty
    while True:
        # print("Frontier Dictionary: ", nodefront.__len__(), " frontier queue: ", frontier.heap.__len__())
        # Testing show the top node

        # Check if the frontier is empty, it is error
        if frontier.isEmpty() is True:
            return
        else:
            # Pop the top node off of the frontier stack
            # Remove the value from the frontier tracking dictionary and add it to the explored one
            node = frontier.pop()
            # print("Current node's", node.coord, "cost:", node.cost)
            # print("Removing ", node.coord)
            del nodefront[node.coord]
            # Add node to explored
            explored.add(node.coord)
            nodeexpl[node.coord] = node.cost
            # print("Size of explored: ", explored.__len__(), " ", nodeexpl.__len__())
            # Add only those that move from the frontier to explored into the dictionary
            # nodedict[node.coord] = node.cost
            # print("Currently explored node: ", node.coord)
            # Check if the current node is the solution
            if problem.isGoalState(node.coord) is True:
                # directions.append(node.direction)
                # Run through all nested objects in the matching node variable
                while node.coord != originstate:
                    # print("Directions from final node to start: ", node.direction)
                    # print("Finishing node backtrack: ", node.coord)
                    directions.append(node.direction)
                    node = node.next()
                # This will create a path from end to start, reverse for answer
                directions.reverse()
                return directions

            else:
                # If it is not the solution, create nodes for all of it's children and add them to the frontier
                # print("Parent coordinates: ", node.coord)
                successorlist = problem.getSuccessors(node.coord)
                # print("Successors: ", successorlist)
                for i in range(len(successorlist)):
                    # Create a child node from the successorlist
                    # Successors contain coordinates[0], directions[1], and cost [2], and the parent node (node)
                    # UCS - node cost is equal to the cost of the path used to get to it.
                    childnode = StateNode(successorlist[i][0], successorlist[i][1], successorlist[i][2] + node.cost, node)
                    # print("Child node of ", childnode.prevstate.coord, " is ", childnode.coord, " with cost", childnode.cost)
                    # Check if the coordinate has already been explored or is waiting in frontier
                    # print("Dictionary keys so far or coordinates accessed: ", nodedict.keys())
                    # Check if the node does not exist at all within the graph

                    if nodefront.__contains__(childnode.coord) is False and nodeexpl.__contains__(childnode.coord) is False:
                        # Child state is not within explored or frontier
                        frontier.update(childnode, childnode.cost + heuristic(childnode.coord, problem))
                        nodefront[childnode.coord] = childnode.cost
                        # print("Adding: ", childnode.coord)
                        # print("Frontier Dictionary: ", nodefront.__len__(), " frontier queue: ", frontier.heap.__len__())
                        continue
                    # Check if the frontier contains the same node and check that explored does not have it already
                    elif nodefront.__contains__(childnode.coord) is True and nodeexpl.__contains__(childnode.coord) is False:

                        # If the frontier contains the current child node but with a higher path cost
                        childcost = childnode.cost
                        existingcost = nodefront[childnode.coord]

                        # print("Frontier Dictionary: ", nodefront.__len__(), " frontier queue: ", frontier.heap.__len__())

                        # print(childcost, existingcost)
                        if childcost < existingcost:
                            # replace the higher cost node with the current child node
                            # print("child cost: ", childcost, " Pre existing node cost: ", existingcost)
                            # Weed out old matching node
                            temppop = frontier.pop()
                            tempholder = []
                            while temppop.coord != childnode.coord:
                                # print("Next ", temppop.coord)
                                tempholder.append(temppop)
                                temppop = frontier.pop()
                            # print(tempholder.__len__())
                            # Add in the replacement node
                            frontier.update(childnode, childnode.cost + heuristic(childnode.coord, problem))
                            # Add back all elements that were popped to find matching node
                            for i in range(tempholder.__len__()):
                                frontier.update(tempholder[i], tempholder[i].cost + heuristic(tempholder[i].coord, problem))
                            # frontier.update(childnode, childnode.cost)
                            nodefront[childnode.coord] = childnode.cost
                            # print("Replacing: ", childnode.coord, "With cost: ", childnode.cost, " and parent ", childnode.prevstate.coord)
                            # print("Frontier Dictionary: ", nodefront.__len__(), " frontier queue: ", frontier.heap.__len__())
                            continue
                        else:
                            # print("A duplicate of ", childnode.coord, " exists in the frontier but is higher than child")
                            continue
                    else:
                        # print("Node ", childnode.coord, "Cannot replace or be added onto the frontier")
                        continue
                #print("End Frontier Dictionary: ", nodefront.__len__(), " frontier queue: ", frontier.heap.__len__())

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
