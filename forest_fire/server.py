from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire
from .agent import TreeCell

COLORS = {"Fine": "#00AA00", "On Fire": "#880000", "Burned Out": "#000000"}


def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    #'sparse_ratio': UserSettableParameter('slider', 'Ratio of sparse vegetations', 0.5, 0, 1.0, 0.1),
    'random_fires': UserSettableParameter('checkbox', 'Spontaneous Fires (Temperature based)', value=False),
    'wind_strength': UserSettableParameter('slider', 'Wind strength', 10, 0, 80, 1),
    'wind_dir': UserSettableParameter('choice', 'Wind Direction', value=('\u2B07 South'),
                                      choices=["\u2B06  North", "\u2197 North/East", "\u27A1 East",
                                               "\u2198 South/East", "\u2B07 North",
                                               "\u2199 South/West", "\u2B05 West",
                                               "\u2196 North/West"]),
}
server = ModularServer(
    ForestFire, [canvas_element, tree_chart, pie_chart], "Forest Fire", model_params
)