from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation

from .agent import TreeCell
import random

class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, 
                width=100, 
                height=100, 
                density=0.65, 
                wind_strength=8, 
                wind_dir="N",
                random_fires=1
                #sparse_ratio
                ):
        """
        Create a new forest fire model.
        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.height = height
        self.width = width
        self.density = density
        self.n_agents = 0
        self.agents = []

        wind_vector = {"\u2B06  North": (0, 1), "\u2197 North/East": (1, 1), "\u27A1 East": (1, 0),
                       "\u2198 South/East": (1, -1), "\u2B07 South": (0, -1), "\u2199 South/West": (-1, -1),
                       "\u2B05 West": (-1, 0), "\u2196 North/West": (-1, 1)}
        self.wind_dir = wind_vector[wind_dir]
        self.wind_strength = wind_strength

        self.random_fires = random_fires
        self.initial_tree = height * width * density
        #self.sparse_ratio = sparse_ratio

        # Create the vegetation agents
        self.init_vegetation(TreeCell, self.initial_tree)

        # Create a data collection
        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
            }
        )
        '''
        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
        '''
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # if spontaneous fires are turned on, check whether one ignites in this step
        if self.random_fires:
            randtree = int(random.random() * len(self.agents))
            if self.agents[randtree].condition == "Fine":
                self.randomfire(self, randtree)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

    def init_vegetation(self, agent_type, n):
        '''
        Creating trees
        '''
        x = random.randrange(self.width)
        y = random.randrange(self.height)

        # initiating vegetation in the centre if possible, otherwise random position
        self.new_agent(agent_type, (int(self.width / 2), int(self.height / 2)))

        # Placing all other vegetation
        for i in range(int(n - 1)):
            while not self.grid.is_cell_empty((x, y)):
                x = random.randrange(self.width)
                y = random.randrange(self.height)
            self.new_agent(agent_type, (x, y))
    
    def new_agent(self, agent_type, pos):
        '''
        Method that enables us to add agents of a given type.
        '''
        self.n_agents += 1

        # Create a new agent of the given type
        new_agent = agent_type(self, self.n_agents, pos)

        # Place the agent on the grid
        self.grid.place_agent(new_agent, pos)

        # And add the agent to the model so we can track it
        self.agents.append(new_agent)

        return new_agent
    