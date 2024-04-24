from hands import Hands
import numpy as np
import numpy.typing as npt
import config


class KeyboardConfig:
    """Contains important info about a keyboard."""
    def __init__(self, layout: npt.NDArray, coordinate_grid: npt.NDArray, hand_placements: npt.NDArray):
        self.layout = layout
        self.coordinate_grid = coordinate_grid
        self.hand_placements = hand_placements


actions = [(x, y) for x in range(30) for y in range(x)]
def layout_swap(layout: npt.NDArray, action: int):
    """Edits a layout inplace, given the provided swap action."""
    if action < 0 or action >= 435:
        raise Exception("layout_swap function received an action outside of [0, 869]!")

    x, y = actions[action]
    c = layout[x]
    layout[x] = layout[y]
    layout[y] = c


def analyze(keyboard_config: KeyboardConfig, dataset: list[str]) -> tuple[npt.NDArray, float, npt.NDArray, float, float]:
    """
    Analyze a complete keyboard config without considering comfort.

    Returns: (counts of events, avg finger distance, time gaps, use std, reward)
    """

    hands = Hands(keyboard_config.hand_placements, keyboard_config.layout, keyboard_config.coordinate_grid)
    events, avg_distance, time_gaps, use_deviation = hands.type_data(dataset)


    '''
    Events:
    0 - bigram - Eg: ER, AS, OP
    1 - trigram - Eg: WER, RTY
    2 - quadgram - EG: ASDF
    3 - redirect - Bigram and opp. direction (Can be both ways) - Eg: ERW, IOPU, IUO, UIU, DFS 
    4 - redirect stretch - Eg: ERC, ERX (Combination of redirect & stretch)
    5 - stretch - Eg: RX (2 rows apart, stretch 2 immediate fingers)
    6 - alternation - Switching hands b/w each letter
    7 - repeats - Same finger twice - Eg: ED, FT
    8 - skipgrams - eg: ETD, ETE, SOW - Same finger used twice, with in-b/w 1 any character but not the same finger and character
    '''

    # constants (to be passed as multipliers)
    bigram_const = 8
    trigram_const = 15
    quadgram_const = 50
    redirect_const = -10
    stretch_const = -12
    alternation_const = 2
    repeat_const = -12
    skipgram_const = -5
    distance_const = 1

    points = (
        events[0] * bigram_const +
        events[1] * trigram_const +
        events[2] * quadgram_const +
        (events[3] + events[4]) * redirect_const +
        (events[4] + events[5]) * stretch_const +
        events[6] + alternation_const +
        events[7] * repeat_const +
        events[8] * skipgram_const +
        avg_distance * distance_const #may be unnecessary because we already account for repeats and skipgrams
    )

    return (events, avg_distance, time_gaps, use_deviation, points)


def collect_data() -> list[str]:
    with open("../data/processed/.compiled.txt") as file:
        return file.read().splitlines()


def to_ints(layout: npt.NDArray) -> npt.NDArray:
    """Convert a layout to ints."""
    return np.array([x for x in range(layout.size)])


def to_keys(layout: npt.NDArray) -> npt.NDArray:
    """Convert ints to a layout."""
    return np.array(list(map(lambda x: config.layout.alphabetical[x], layout)))


def save_data(data: list[tuple[npt.NDArray, float, npt.NDArray, float, float]]):
    pass


class Environment:
    """Bridge between reinforcement learning and the analyzer."""
    def __init__(self, keyboard_config: KeyboardConfig, max_iterations: int, data: list[str]):
        self.keyboard_config = keyboard_config
        self.max_iterations = max_iterations
        self.iteration = 0
        self.data = data


    def step(self, action: int) -> tuple[npt.NDArray, float, bool, tuple[npt.NDArray, float, npt.NDArray, float]]:
        """
        Apply an action

        Returns: (next state, reward, is done, (events, avg finger distance, avg finger time gaps, finger use std))
        """

        done = self.iteration >= self.max_iterations #set a cap
        self.iteration += 1

        new_state = self.keyboard_config.layout.copy()
        #print(new_state)
        layout_swap(new_state, action) #apply action
        self.keyboard_config.layout = to_keys(new_state)

        events, avg_distance, time_gaps, use_deviation, reward = analyze(self.keyboard_config, self.data)
        self.keyboard_config.layout = new_state

        return new_state, reward, done, (events, avg_distance, time_gaps, use_deviation)


