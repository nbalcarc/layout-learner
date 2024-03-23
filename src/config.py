import numpy as np



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
##### HAND PLACEMENT #####


What keys are assigned to what fingers.
"""


# standard home row finger placement
home_row = np.array([
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
    [0, 1, 2, 3, 3,   4, 4, 5, 6, 7],
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
pinky_less = np.array([
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


all_layouts = {
    "qwerty": qwerty,
    "dvorak": dvorak,
    "colemak": colemak,
    "colemak-dh": colemak_dh,
    "workman": workman,
    "norman": norman,
    "semimak-jq": semimak_jq,
    "mtgap": mtgap,
    "alphabetical": alphabetical,
}


