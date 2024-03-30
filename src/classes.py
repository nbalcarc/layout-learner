import numpy.typing as npt
from functools import reduce


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
    def __init__(self, effort_grid: npt.NDArray, coordinate_grid: npt.NDArray, layout: npt.NDArray):
        self.effort_grid = effort_grid
        self.coordinate_grid = coordinate_grid
        self.layout = layout


class Analyzer:
    """Runs analytics on a hand and layout."""
    def __init__(self, hand_placements: npt.NDArray, keyboard_config: KeyboardConfig):
        self.keyboard_config = keyboard_config
        self.hands = Hands(hand_placements)


