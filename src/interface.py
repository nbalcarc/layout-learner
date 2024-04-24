from hands import Hands
import numpy as np
import numpy.typing as npt


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
    0 - bigram
    1 - trigram
    2 - quadgram
    3 - redirect
    4 - redirect stretch
    5 - stretch
    6 - alternation
    7 - repeats
    8 - skipgrams
    '''

    # constants (to be passed as multipliers)
    bigram_const = 10
    trigram_const = 15
    quadgram_const = 15
    redirect_const = -10
    stretch_const = -10
    alternation_const = 2
    repeat_const = -10
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


#def 


class Environment:
    """Bridge between reinforcement learning and the analyzer."""
    def __init__(self, keyboard_config: KeyboardConfig, max_iterations: int):
        self.keyboard_config = keyboard_config
        self.max_iterations = max_iterations
        self.iteration = 0


    def step(self, action: int) -> tuple[npt.NDArray, float, bool, tuple[npt.NDArray, float, npt.NDArray, float]]:
        """
        Apply an action

        Returns: (next state, reward, is done, (events, avg finger distance, avg finger time gaps, finger use std))
        """

        done = self.iteration >= self.max_iterations #set a cap
        self.iteration += 1

        new_state = self.keyboard_config.layout.copy()
        layout_swap(new_state, action) #apply action
        self.keyboard_config.layout = new_state

        events, avg_distance, time_gaps, use_deviation, reward = analyze(self.keyboard_config, [""])

        return new_state, reward, done, (events, avg_distance, time_gaps, use_deviation)


