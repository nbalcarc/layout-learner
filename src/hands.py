import numpy as np
import numpy.typing as npt
from functools import reduce


class Finger:
    """Handles finger location and timing."""
    def __init__(self):
        self.location: int = 0
        self.last_used: int = -1


class Hands:
    """Contains a set of fingers and their assigned keys on a keyboard."""
    def __init__(self, hand_placements: npt.NDArray, keyboard_layout: npt.NDArray, coordinate_grid: npt.NDArray):
        #fingers = dict(map(lambda x: (x, Finger()), set(hand_placements))) #assign a Finger to an ID
        #self.fingermap = {i: fingers[h] for (i, h) in enumerate(hand_placements)} #assign keys to Fingers
        #self.last_finger = None
        #print(self.fingermap)
        #print(fingers)

        
        self.coordinate_grid = coordinate_grid
        self.keymap = dict(map(lambda x: (x[1], x[0]), enumerate(reduce(lambda a, x: a + x, keyboard_layout))))
        finger_objs = [Finger() for _ in range(8)]
        self.fingermap: list[Finger] = list(map(lambda x: finger_objs[x], hand_placements))
        #self.hand_fingers = list(map(lambda x: x < 5, hand_placements))
        self.hand_fingers = hand_placements < 5
        self.last_key = -1
        self.roll_count = 0
        self.stats = np.zeros(7) #alternation index, repeats, stretches, bigram rolls, trigram rolls, redirects, distance
        self.time = 0

    def type_key(self, key: str) -> int:
        """Updates Hand to type the given key, returns last time finger was used."""
        cur_key = self.keymap[key]
        last_key = self.last_key
        finger = self.fingermap[cur_key]
        self.last_key = cur_key

        scores = np.zeros(5) #alternation +, repeat -, stretch -, rolling +-, distance -

        # constants (to be passed as variable later)
        bigram_const = 10
        trigram_const = 15
        quadgram_const = 15
        redirect_const = -10
        repeat_const = -10
        skipgram_const = -5
        stretch_const = -10
        alternation_const = 2

        # calculate some values
        same_hand_row = last_key // 5 == cur_key // 5
        same_hand = self.hand_fingers[last_key] == self.hand_fingers[cur_key]

        # cover rolling scores
        if self.roll_count == 0 and abs(last_key - cur_key) == 1 and same_hand_row: #start key roll
            self.roll_count = last_key - cur_key
            scores[3] = bigram_const
        elif self.roll_count != 0: #roll was happening
            if np.sign(last_key) == np.sign(cur_key) and same_hand_row: #continue roll
                self.roll_count = last_key - cur_key
                scores[3] = trigram_const if abs(self.roll_count) == 3 else quadgram_const
            elif abs(dif := (last_key + self.roll_count) - cur_key) == 1 and np.sign(dif) == np.sign(self.roll_count): #redirect
                scores[3] = redirect_const
                self.roll_count = 0 #reset rolling status
            else: #rolling ended without redirect
                self.roll_count = 0 #reset rolling status
        
        # check for repeats and skipgrams
        if finger.last_used == self.time - 1: #repeat finger bigram
            scores[1] = repeat_const
        elif finger.last_used == self.time - 2: #skipgram
            scores[1] = skipgram_const

        # check for stretches
        if (abs(last_key - cur_key) == 1 #adjacent fingers
                and same_hand
                and (last_key // 10) - (cur_key // 10)) == 2: #2 row stretch

            scores[2] = stretch_const

        # check for hand alternation
        if not same_hand:
            scores[0] = alternation_const

        # calculate distance penalty
        if self.time - finger.last_used < 3: #no penalty for a gap of two keys or more
            last: tuple[np.float64, np.float64] = self.coordinate_grid[finger.location]
            cur: tuple[np.float64, np.float64] = self.coordinate_grid[cur_key]
            dist = np.sqrt((last[0] - cur[0]) ** 2 + (last[1] - cur[1]) ** 2)
            scores[4] = dist

        # update time
        finger.last_used = self.time
        finger.location = cur_key

        return 0


