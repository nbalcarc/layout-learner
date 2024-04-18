import config
from hands import Hands


class Roll:
    def __init__(self):
        self.direction = -1
        self.row = -1
        self.finger = -1


class AnalyzerResults:
    """Contains the results of running the analyzer on a KeyboardConfig."""
    def __init__(self, speed: float, comfort: float):
        self.speed = speed
        self.comfort = comfort
    

def analyze_without_comfort(keyboard_config: config.KeyboardConfig, dataset: str) -> AnalyzerResults:
    """Analyze a complete keyboard config without considering comfort."""
    '''
    consider these:
        same finger bigrams (same finger types two different consecutive letters)
        same finger skipgrams (same finger types two different letters with a gap of 1)
        rolled bi/trigrams (a string of consecutive fingers on the same row)
        redirects (a bigram roll followed by a letter on a finger behind the roll)
        lateral stretch bigrams (next consecutive finger types on a column 2 away from last finger)
    '''

    hands = Hands(keyboard_config.hand_placements, keyboard_config.layout)



    return AnalyzerResults(0.0, 0.0)


