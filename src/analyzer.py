import config
from hands import Hands
import numpy.typing as npt


#class Roll:
#    def __init__(self):
#        self.direction = -1
#        self.row = -1
#        self.finger = -1


#class AnalyzerResults:
#    """Contains the results of running the analyzer on a KeyboardConfig."""
#    def __init__(self, speed: float, comfort: float):
#        self.speed = speed
#        self.comfort = comfort
    

def analyze_without_comfort(keyboard_config: config.KeyboardConfig, dataset: list[str]) -> tuple[npt.NDArray, float]:
    """Analyze a complete keyboard config without considering comfort."""
    '''
    consider these:
        same finger bigrams (same finger types two different consecutive letters)
        same finger skipgrams (same finger types two different letters with a gap of 1)
        rolled bi/trigrams (a string of consecutive fingers on the same row)
        redirects (a bigram roll followed by a letter on a finger behind the roll)
        lateral stretch bigrams (next consecutive finger types on a column 2 away from last finger)
    '''

    hands = Hands(keyboard_config.hand_placements, keyboard_config.layout, keyboard_config.coordinate_grid)
    events, time_gaps, distance = hands.type_data(dataset)

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
    #repeat_const = -10 #will be halved in two for a skipgram
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
        distance * distance_const #may be unnecessary because we already account for repeats and skipgrams
    )

    #return AnalyzerResults(0.0, 0.0)
    return (events, points)


