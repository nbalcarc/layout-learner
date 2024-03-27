import numpy as np
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


def main():
    """Main entry point."""

    Hands(config.home_row)


if __name__ == "__main__":
    main()


