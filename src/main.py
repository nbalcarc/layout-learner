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
        flattened = reduce(lambda a, x: a + list(x), hand_placements, [])
        uniques = set(list(flattened)) #which fingers there are
        fingers = dict(map(lambda x: (x, Finger()), uniques))

        self.fingermap = dict()
        for i, h in enumerate(flattened):
            self.fingermap[i] = fingers[h]


def thing(layout: np.chararray):
    pass


def main():
    """Main entry point."""

    layout = np.chararray((3, 10))

    Hands(config.home_row)


    


if __name__ == "__main__":
    main()



