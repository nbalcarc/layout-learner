import numpy as np


# for a non-staggered keyboard
effort_grid_matrix = np.array([
    [3.0, 2.4, 2.0, 2.2, 3.2,   3.2, 2.2, 2.0, 2.4, 3.0],
    [1.6, 1.3, 1.1, 1.0, 2.9,   2.9, 1.0, 1.1, 1.3, 1.6],
    [3.2, 2.6, 2.3, 1.6, 3.0,   3.0, 1.6, 2.3, 2.6, 3.2],
])


# for a normal staggered keyboard
effort_grid_standard = np.array([
    [3.0, 2.5, 2.1, 2.3, 2.6,   3.4, 2.2, 2.0, 2.4, 3.0],
    [1.6, 1.3, 1.1, 1.0, 2.9,   2.9, 1.0, 1.1, 1.3, 1.6],
    [3.5, 3.0, 2.7, 2.2, 3.7,   2.2, 1.8, 2.4, 2.7, 3.3],
])


def thing(layout: np.chararray):
    pass


def main():
    """Main entry point."""

    layout = np.chararray((3, 10))

    


if __name__ == "__main__":
    main()



