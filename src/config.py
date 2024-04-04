import numpy as np


def setup():
    global layout, coordinate_grid, effort_grid, hand_placement
    class layout():
        qwerty = qwerty
        dvorak = dvorak
        colemak = colemak
        colemak_dh = colemak_dh
        workman = workman
        norman = norman
        semimak_jq = semimak_jq
        mtgap = mtgap
        alphabetical = alphabetical


    class coordinate_grid():
        standard = effort_grid_standard
        matrix = effort_grid_matrix


    class effort_grid():
        standard = effort_grid_standard
        matrix = effort_grid_matrix


    class hand_placement():
        home_row_us = home_row_us
        home_row_in = home_row_in
        augmented = augmented
        hunt_and_peck = hunt_and_peck
        gamer = gamer
        pinkyless = pinkyless



"""
##### EFFORT GRID #####


How difficult each key is to press, numbers taken from here:
    https://colemakmods.github.io/mod-dh/model.html

"""


# for a normal staggered keyboard (for actual project use)
effort_grid_standard = np.array([
    [3.0, 2.5, 2.1, 2.3, 2.6,   3.4, 2.2, 2.0, 2.4, 3.0],
    [1.6, 1.3, 1.1, 1.0, 2.9,   2.9, 1.0, 1.1, 1.3, 1.6],
    [3.5, 3.0, 2.7, 2.2, 3.7,   2.2, 1.8, 2.4, 2.7, 3.3],
])


# for a non-staggered keyboard (more for personal use)
effort_grid_matrix = np.array([
    [3.0, 2.4, 2.0, 2.2, 3.2,   3.2, 2.2, 2.0, 2.4, 3.0],
    [1.6, 1.3, 1.1, 1.0, 2.9,   2.9, 1.0, 1.1, 1.3, 1.6],
    [3.2, 2.6, 2.3, 1.6, 3.0,   3.0, 1.6, 2.3, 2.6, 3.2],
])



"""
##### COORDINATE GRID #####


The relative placement of keys.

"""


coordinate_grid_standard = np.array([
    [(0.0, 0.00), (0.0, 1.00), (0.0, 2.00), (0.0, 3.00), (0.0, 4.00),   (0.0, 5.00), (0.0, 6.00), (0.0, 7.00), (0.0, 8.00), (0.0, 9.00)],
    [(1.0, 0.25), (1.0, 1.25), (1.0, 2.25), (1.0, 3.25), (1.0, 4.25),   (1.0, 5.25), (1.0, 6.25), (1.0, 7.25), (1.0, 8.25), (1.0, 9.25)],
    [(2.0, 0.75), (2.0, 1.75), (2.0, 2.75), (2.0, 3.75), (2.0, 4.75),   (2.0, 5.75), (2.0, 6.75), (2.0, 7.75), (2.0, 8.75), (2.0, 9.75)],
])

coordinate_grid_matrix = np.array([
    [(0.0, 0.00), (0.0, 1.00), (0.0, 2.00), (0.0, 3.00), (0.0, 4.00),   (0.0, 5.00), (0.0, 6.00), (0.0, 7.00), (0.0, 8.00), (0.0, 9.00)],
    [(1.0, 0.00), (1.0, 1.00), (1.0, 2.00), (1.0, 3.00), (1.0, 4.00),   (1.0, 5.00), (1.0, 6.00), (1.0, 7.00), (1.0, 8.00), (1.0, 9.00)],
    [(2.0, 0.00), (2.0, 1.00), (2.0, 2.00), (2.0, 3.00), (2.0, 4.00),   (2.0, 5.00), (2.0, 6.00), (2.0, 7.00), (2.0, 8.00), (2.0, 9.00)],
])



"""
##### HAND PLACEMENT #####


What keys are assigned to what fingers.
"""


# standard home row finger placement (in the United States)
home_row_us = np.array([
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
])


# standard home row finger placement (in India)
home_row_in = np.array([
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [1, 2, 3, 3, 4,   4, 5, 6, 6, 7],
])


# augmented layout
augmented = np.array([
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [1, 2, 3, 3, 3,   4, 4, 5, 6, 7],
])


# just two index fingers
hunt_and_peck = np.array([
    [3, 3, 3, 3, 3,   4, 4, 4, 4, 4],
    [3, 3, 3, 3, 3,   4, 4, 4, 4, 4],
    [3, 3, 3, 3, 3,   4, 4, 4, 4, 4],
])


# left hand home row, right hand hunt and peck
gamer = np.array([
    [0, 1, 2, 3, 3,   4, 4, 4, 4, 4],
    [0, 1, 2, 3, 3,   4, 4, 4, 4, 4],
    [0, 1, 2, 3, 3,   4, 4, 4, 4, 4],
])


# standard home row but without pinkies, may not be accurate for testing
pinkyless = np.array([
    [1, 1, 2, 3, 3,   4, 4, 5, 6, 6],
    [1, 1, 2, 3, 3,   4, 4, 5, 6, 6],
    [1, 1, 2, 3, 3,   4, 4, 5, 6, 6],
])



"""
##### BUILT-IN LAYOUTS #####


Used to compare our learned layouts vs real existing layouts.
"""


qwerty = np.array([
    "qwertyuiop",
    "asdfghjkl;",
    "zxcvbnm,./",
])


# a little approximated, the symbols don't work the same as qwerty
dvorak = np.array([
    "/,.pyfgcrl",
    "aoeuidhtns",
    ";qjkxbmwvz",
])


colemak = np.array([
    "qwfpgjluy;",
    "arstdhneio",
    "zxcvbkh,./",
])


colemak_dh = np.array([
    "qwfpbjluy;",
    "arstgmneio",
    "zxcdvkh,./",
])


workman = np.array([
    "qdrwbjfup;",
    "ashtgyneoi",
    "zxmcvkl,./",
])


norman = np.array([
    "qwdfkjurl;",
    "asetgynioh",
    "zxcvbpm,./",
])


# approximation due to symbols
semimak_jq = np.array([
    "flhvz;wuoy",
    "srntkcdeai",
    "xjbmqpg,./",
])


# approximation due to symbols
mtgap = np.array([
    "ypoujkdlcw",
    "inea;mhtsr",
    "qz/.,bfgvx",
])


alphabetical = np.array([
    "abcdefghij",
    "klmnopqrs;",
    "tuvwxyz,./",
])



setup()


