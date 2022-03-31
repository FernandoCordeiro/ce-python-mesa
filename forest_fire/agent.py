from mesa import Agent
import random

class TreeCell(Agent):
    """
    A tree cell.
    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.
    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, model, unique_id, pos):
        '''
        Create a new tree.
        Args:
        pos: The tree's coordinates on the grid. Used as the unique_id
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.unique_id = unique_id
        self.condition = "Fine"
        self.life_bar = 100       # give the tree a life bar
        self.burning_rate = 20  # need to change that as well
        self.trees_claimed = 0
        self.fire_bar = 0

        self.veg_state = 0.4

        # assigning density with the given probability
        #if random.uniform(0, 1) < self.model.sparse_ratio:
        #    self.veg_density = -0.4
        #else:
        self.veg_density = 0.65

        self.fireinitstep = None

        #

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "On Fire":
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"