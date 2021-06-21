from definitions import Agent
import numpy as np
from scipy.spatial import distance
import random

class RandAgent(Agent):
    """
    This class implements an agent that explores the environmente randomly
    until it reaches the target
    """

    def __init__(self, env, bound=100):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)
        
        
        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path} 
        # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment
        # Select a random neighbor that has not been visited yet
            
        viable_neighbors =  self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:              
            random.shuffle(viable_neighbors)
            for n in viable_neighbors:
                # Append neighbor to the path and add it to the frontier
                self.frontier = [path + [n]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])





















class BFSAgent(Agent):
    """
    This class implements an agent that explores the environment using the Breadth First Search method
    until it reaches the target
    """

    def __init__(self, env, bound=100):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)
        
        
        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path} 
        # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment select the first neighbor that was added to the frontier that haven't been visited
            
        viable_neighbors =  self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:              
            for n in viable_neighbors:
                cycle = False
                # Poda de ciclos
                for e in path: 
                    if (n==e).all():
                        cycle = True 
                        break
                if not cycle: 
                    # Append neighbor to the path and add it to the end of the frontier
                    self.frontier = self.frontier + [path + [n]]

                

    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])



















class DFSAgent(Agent):
    """
    This class implements an agent that explores the environment using the Depth First Search method
    until it reaches the target
    """

    def __init__(self, env, bound=100):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select the last path from the frontier
        path = self.frontier.pop(0)
        
        
        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path} 
        # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment 
        # select the first neighbor that was added to the frontier that hasn't been visited
            
        viable_neighbors =  self.percepts['neighbors']

        # If the agent is not stuck
        if viable_neighbors:              
            for n in viable_neighbors:
                cycle = False
                # Cycle Pruning
                for e in path: 
                    if (n==e).all():
                        cycle = True 
                        break
                # Multiple Path Pruning
                visited = False
                for e in self.visited: 
                    if (n==e).all():
                        visited = True 
                        break
                if not cycle and not visited:
                    # Append neighbor to the path and add it to the start of the frontier 
                    self.frontier = [path + [n]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])

















class GreedyAgent(Agent):
    """
    This class implements an agent that explores the environment using the Greedy Best First Search method
    until it reaches the target
    """

    def __init__(self, env, bound=100):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

        self.cost =[0]

    def act(self):
        """Implements the agent action
        """

        # Select the lowest heuristic value path from the frontier
        hcost = []
        for path in self.frontier: 
            hcost.append(distance.euclidean(path[-1],self.percepts['target']))
        i = hcost.index(min(hcost))
        path = self.frontier.pop(i)
        
        # Visit the last node in the path
        action = {'visit_position': path[-1], 'path': path} 
        # The agent sends a position and the full path to the environment, the environment can plot the path in the room 
        self.percepts = self.env.signal(action)

        # Add visited node
        self.visited.append(path[-1])

        # From the list of viable neighbors given by the environment 
        # select the viable neighbors and add them to the frontier

        viable_neighbors =  self.percepts['neighbors']
        

        # If the agent is not stuck
        if viable_neighbors:              
            for n in viable_neighbors:
                cycle = False
                # Cycle Pruning
                for e in path: 
                    if (n==e).all():
                        cycle = True 
                        break
                # Multiple Path Pruning
                visited = False
                for e in self.visited: 
                    if (n==e).all():
                        visited = True 
                        break
                if not cycle and not visited:
                    # Append neighbor to the path and add it to the start of the frontier 
                    self.frontier = [path + [n]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while (self.percepts['current_position'] != self.percepts['target']).any() and self.frontier:
            self.act()
        print(self.percepts['current_position'])




















class BBAgent(Agent):
    """
    This class implements an agent that finds the minimum distance path using branch and bound

    """

    def __init__(self, env, bound=100):
        """Connects to the next available port.

        Args:
            env: A reference to an environment.

        """

        # Make a connection to the environment using the superclass constructor
        Agent.__init__(self,env)
        
        # Get initial percepts
        self.percepts = env.initial_percepts()
        
        # Initializes the frontier with the initial postion 
        self.frontier = [[self.percepts['current_position']]]
        self.cost = [0]
        self.bound = bound
        self.path_path = []
        
        # Initializes list of visited nodes for multiple path prunning
        self.visited = []

    def act(self):
        """Implements the agent action
        """

        # Select a path from the frontier
        path = self.frontier.pop(0)
        cost = self.cost.pop(0)
        
        if cost + distance.euclidean(path[-1],self.percepts['target']) < self.bound:
            # Visit the last node in the path
            action = {'visit_position': path[-1], 'path': path} 
            # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
            self.percepts = self.env.signal(action)

            # Add visited node
            self.visited.append(path[-1])

            if (self.percepts['current_position'] == self.percepts['target']).all():
                self.best_path = path
                self.bound = cost
                print(self.bound)

            # From the list of viable neighbors given by the environment
            # Select a random neighbor that has not been visited yet
            
            viable_neighbors =  self.percepts['neighbors']

            # If the agent is not stuck
            if viable_neighbors:              
                for n in viable_neighbors:
                    # Append neighbor to the path and add it to the frontier
                    self.frontier = [path + [n]] + self.frontier

    def run(self):
        """Keeps the agent acting until it finds the target
        """
        # Run agent
        while self.frontier:
            self.act()
        print(self.percepts['current_position'])

        for i in range(1000):
            action = {'visit_position': self.best_path[-1], 'path': self.best_path} 
            # The agente sends a position and the full path to the environment, the environment can plot the path in the room 
            self.percepts = self.env.signal(action)