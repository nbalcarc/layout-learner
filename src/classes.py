import numpy.typing as npt
from functools import reduce

import config


class Finger:
    """Handles finger location and timing."""
    def __init__(self):
        self.location: int = 0
        self.last_used: int = 0


class Hands:
    """Contains a set of fingers and their assigned keys on a keyboard."""
    def __init__(self, hand_placements: npt.NDArray):
        flattened = reduce(lambda a, x: a + list(x), hand_placements, []) #2D -> 1D
        uniques = set(list(flattened)) #which fingers there are
        fingers = dict(map(lambda x: (x, Finger()), uniques)) #assign a Finger to an ID
        self.fingermap = {i: fingers[h] for (i, h) in enumerate(flattened)} #assign keys to Fingers


class KeyboardConfig:
    """Contains important info about a keyboard."""
    def __init__(self, layout: npt.NDArray, coordinate_grid: npt.NDArray, effort_grid: npt.NDArray, hand_placements: npt.NDArray = config.hand_placement.home_row):
        self.layout = layout
        self.coordinate_grid = coordinate_grid
        self.effort_grid = effort_grid
        self.hand_placements = hand_placements


class Analyzer:
    """Runs analytics on a hand and layout."""
    def __init__(self, keyboard_config: KeyboardConfig):
        self.keyboard_config = keyboard_config
        self.hands = Hands(keyboard_config.hand_placements)


