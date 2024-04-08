import classes


class Roll:
    def __init__(self):
        self.direction = -1
        self.row = -1
        self.finger = -1


def analyze_without_comfort(keyboard_config: classes.KeyboardConfig, dataset: str) -> classes.AnalyzerResults:
    
    '''
    consider these:
        same finger bigrams (same finger types two different consecutive letters)
        same finger skipgrams (same finger types two different letters with a gap of 1)
        rolled bi/trigrams (a string of consecutive fingers on the same row)
        redirects (a bigram roll followed by a letter on a finger behind the roll)
        lateral stretch bigrams (next consecutive finger types on a column 2 away from last finger)
    '''



    return  classes.AnalyzerResults(0.0, 0.0)


