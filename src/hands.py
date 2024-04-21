import numpy as np
import numpy.typing as npt
from functools import reduce


class Finger:
    """Handles finger location and timing."""
    def __init__(self, id: int):
        self.id = id
        self.location: int = 0
        self.last_used: int = -1


class Hands:
    """Contains a set of fingers and their assigned keys on a keyboard."""
    def __init__(self, hand_placements: npt.NDArray, keyboard_layout: npt.NDArray, coordinate_grid: npt.NDArray):
        self.coordinate_grid = coordinate_grid
        self.keymap = dict(map(lambda x: (x[1], x[0]), enumerate(reduce(lambda a, x: a + x, keyboard_layout)))) #key to index
        finger_objs = [Finger(i) for i in range(8)]
        self.fingermap: list[Finger] = list(map(lambda x: finger_objs[x], hand_placements)) #index to Finger
        #self.hand_fingers = hand_placements < 5 #bool saying whether each index is on the left (True) or right (False) hand

        self.reset()


    def reset(self):
        """Prepare for a clean run."""
        self.last_key = -1
        self.roll = 0 #negative is left, positive is right
        self.time = 0 #current time


    def type_key(self, key: str) -> tuple[int, int, float]:
        """Updates Hand to type the given key, returns score for this character."""
        cur_key = self.keymap[key]
        last_key = self.last_key
        finger = self.fingermap[cur_key]

        #scores = np.zeros(5) #alternation +, repeat -, stretch -, rolling +-, distance -

        event: int = -1
        time_gap: int = -1 #for repeats/skipgrams
        distance: float = -1 #for repeats/skipgrams

        '''
        Events:
        -1 - nothing
        0 - bigram
        1 - trigram
        2 - quadgram
        3 - redirect
        4 - redirect stretch
        5 - stretch
        6 - alternation
        '''

        ## constants (to be passed as variable later)
        #bigram_const = 10
        #trigram_const = 15
        #quadgram_const = 15
        #redirect_const = -10
        #repeat_const = -10
        #skipgram_const = -5 
        #stretch_const = -10
        #alternation_const = 2

        ## account for not having typed yet
        #if last_key == -1:
        #    last_key = cur_key

        # calculate some values
        #same_hand_row = last_key // 5 == cur_key // 5
        #same_hand = self.hand_fingers[last_key] == self.hand_fingers[cur_key]

        # decide on the event
        if last_key == -1: #if very first press
            event = -1 #nothing

        elif (self.fingermap[last_key].id // 5) == (self.fingermap[cur_key].id // 5): #same hand
            if abs(self.fingermap[last_key].id - self.fingermap[cur_key].id) == 1 and abs(last_key - cur_key) == 1: #using same-row adjacent fingers, could be a roll
                if cur_key > last_key and self.roll >= 0: #right-wise roll
                    if self.roll == 0:
                        self.roll = 1
                        event = 0 #bigram
                    elif self.roll == 1:
                        self.roll = 2
                        event = 1 #trigram
                    else:
                        self.roll = 0
                        event = 2 #quadgram
                        # pentagrams are impossible assuming you don't use your thumbs like a sane human
                        # and redirects are impossible off of a quadgram, so we don't need to remember the roll
                elif last_key > cur_key and self.roll <= 0: #left-wise roll
                    if self.roll == 0:
                        self.roll = -1
                        event = 0 #bigram
                    elif self.roll == -1:
                        self.roll = -2
                        event = 1 #trigram
                    else:
                        self.roll = 0
                        event = 2 #quadgram
                else: #redirect (current "roll" doesn't match with the roll that was taking place)
                    self.roll = 0
                    event = 3 #redirect

                #event = abs(self.roll)
                #if abs(self.roll) < 2: #increase roll
                #    self.roll += 1 * (1 if cur_key > last_key else -1)
                #else:
                #    self.roll = 0
                #    # pentagrams are impossible assuming you don't use your thumbs like a sane human
                #    # and redirects are impossible off of a quadgram, so we don't need to remember the roll

            elif self.fingermap[last_key] is self.fingermap[cur_key]: #using same finger
                self.roll = 0
                event = -1

            elif abs(last_key // 10 - cur_key // 10) == 2: #2 rows away, stretch
                self.roll = 0
                if (self.roll > 0 and cur_key < last_key) or (self.roll < 0 and cur_key > last_key): #redirect stretch
                    event = 4 #redirect stretch
                else:
                    event = 5 #stretch

            else: #same hand but not a stretch, roll, or redirect
                self.roll = 0
                event = -1

        else: #different hand
            self.roll = 0
            event = 6 #alternation

        ## cover rolling scores
        #if self.roll_count == 0 and abs(last_key - cur_key) == 1 and same_hand_row: #start key roll
        #    self.roll_count = last_key - cur_key
        #    scores[3] = bigram_const
        #elif self.roll_count != 0: #roll was happening
        #    if np.sign(last_key) == np.sign(cur_key) and same_hand_row: #continue roll
        #        self.roll_count = last_key - cur_key
        #        scores[3] = trigram_const if abs(self.roll_count) == 3 else quadgram_const
        #    elif abs(dif := (last_key + self.roll_count) - cur_key) == 1 and np.sign(dif) == np.sign(self.roll_count): #redirect
        #        scores[3] = redirect_const
        #        self.roll_count = 0 #reset rolling status
        #    else: #rolling ended without redirect
        #        self.roll_count = 0 #reset rolling status
        #
        ## check for repeats and skipgrams
        #if finger.last_used == self.time - 1: #repeat finger bigram
        #    scores[1] = repeat_const
        #elif finger.last_used == self.time - 2: #skipgram
        #    scores[1] = skipgram_const

        ## check for stretches
        #if (abs(last_key - cur_key) == 1 #adjacent fingers
        #        and same_hand
        #        and ((last_key // 10) - (cur_key // 10)) == 2 #2 row stretch
        #        ):
        #    scores[2] = stretch_const

        ## check for hand alternation
        #if not same_hand:
        #    scores[0] = alternation_const

        # calculate distance penalty
        if self.time - finger.last_used < 3: #no penalty for a gap of two keys or more
            last: tuple[np.float64, np.float64] = self.coordinate_grid[finger.location]
            cur: tuple[np.float64, np.float64] = self.coordinate_grid[cur_key]
            distance = np.sqrt((last[0] - cur[0]) ** 2 + (last[1] - cur[1]) ** 2)

        # update time and other vars
        finger.last_used = self.time
        finger.location = cur_key
        self.time += 1
        self.last_key = cur_key

        #return scores
        return (event, time_gap, distance)


    def type_data(self, data: list[str]):
        """Run a full dataset on the Hands."""

        for phrase in data:
            for c in phrase:
                scores = self.type_key(c)


