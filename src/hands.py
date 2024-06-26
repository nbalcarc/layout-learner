import numpy as np
import numpy.typing as npt
from functools import reduce


class Finger:
    """Handles finger location and timing."""
    def __init__(self, id: int):
        self.id = id
        self.location: int = -1
        self.last_used: int = -1


class Hands:
    """Contains a set of fingers and their assigned keys on a keyboard."""
    def __init__(self, hand_placements: npt.NDArray, keyboard_layout: npt.NDArray, coordinate_grid: npt.NDArray):
        self.coordinate_grid = coordinate_grid
        print(keyboard_layout)
        self.keymap = dict(map(lambda x: (x[1], x[0]), enumerate(reduce(lambda a, x: a + x, keyboard_layout)))) #key to index
        finger_objs = [Finger(i) for i in range(8)]
        self.fingermap: list[Finger] = list(map(lambda x: finger_objs[x], hand_placements)) #index to Finger

        self.reset()


    def reset(self):
        """Prepare for a clean run."""
        self.last_key = -1
        self.roll = 0 #negative is left, positive is right
        self.time = 0 #current time


    def type_key(self, key: str) -> tuple[int, int, float]:
        """Updates Hand to type the given key, returns score for this character."""
        
        # handle gaps/spacers first
        if key == "-":
            self.roll = 0
            self.time += 1
            self.last_key = -1
            return (-2, -1, -1)

        cur_key = self.keymap[key]
        last_key = self.last_key
        finger = self.fingermap[cur_key]

        '''
        Events:
        -2 - spacer (DEPRECATED)
        -1 - nothing
        0 - bigram
        1 - trigram
        2 - quadgram
        3 - redirect
        4 - redirect stretch
        5 - stretch
        6 - alternation
        '''

        # decide on the event
        if last_key == -1: #if very first press
            event = -1 #nothing

        elif (self.fingermap[last_key].id // 4) == (self.fingermap[cur_key].id // 4): #same hand
            if (abs(self.fingermap[last_key].id - self.fingermap[cur_key].id) == 1 #adjacent fingers
                and abs(last_key - cur_key) == 1 #adjacent keys
                and self.time - self.fingermap[last_key].last_used == 1 #contiguous (no gaps)
            ): #using same-row adjacent fingers, could be a roll
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

            elif self.fingermap[last_key] is self.fingermap[cur_key]: #using same finger
                self.roll = 0
                event = -1

            elif abs(last_key // 10 - cur_key // 10) == 2: #2 rows away, stretch
                #if (self.roll > 0 and cur_key < last_key) or (self.roll < 0 and cur_key > last_key): #redirect stretch
                if (self.roll > 0 and (cur_key % 5) < (last_key % 5)) or (self.roll < 0 and (cur_key % 5) > (last_key % 5)): #redirect stretch
                    event = 4 #redirect stretch
                else:
                    event = 5 #stretch
                self.roll = 0

            elif self.roll != 0 and np.sign(self.roll) and abs(cur_key - last_key) in [2, 3]: #redirect (bigram or trigram redirected)
                self.roll = 0
                event = 3

            else: #same hand but not a stretch, roll, or redirect
                self.roll = 0
                event = -1

        else: #different hand
            self.roll = 0
            event = 6 #alternation

        # grab time_gap
        if finger.last_used == -1:
            time_gap = -1 #if never pressed before, don't enact penalty
        else:
            time_gap = self.time - finger.last_used

        # calculate distance penalty
        if time_gap == 1 or time_gap == 2:
            last: tuple[np.float64, np.float64] = self.coordinate_grid[finger.location]
            cur: tuple[np.float64, np.float64] = self.coordinate_grid[cur_key]
            dist = np.sqrt((last[0] - cur[0]) ** 2 + (last[1] - cur[1]) ** 2)
            distance = dist / time_gap #cut penalty in half if time_gap is 2
        else:
            distance = 0 #no penalty for a gap of two keys or more (or never pressed)

        # update time and other vars
        finger.last_used = self.time
        finger.location = cur_key
        self.time += 1
        self.last_key = cur_key

        #return scores
        return (event, time_gap, distance)


    def type_data(self, data: list[str]) -> tuple[npt.NDArray, float, npt.NDArray, float]:
        """
        Run a full dataset on the Hands. Returns statistics.

        Return: (all events, avg overall distance, avg time gap per finger, std of finger usage)
        """

        events = np.zeros(9) #count of all events (7 from typing a key)
        time_gap_totals = np.zeros(8) #total gaps
        time_gap_counts = np.zeros(8) #numbers of occurences
        distance_totals = 0.0 #total distance
        distance_counts = 0 #number of keys pressed

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

        for phrase in data:
            self.reset()
            for c in phrase:

                if c == "-": #spacer, there are no pluses
                    self.roll = 0
                    self.time += 1

                else: #normal key press

                    # run type_key() and update stats
                    event, time_gap, distance = self.type_key(c)

                    # update events array
                    if event == -1: #nothing
                        pass
                    #elif event == -2: #spacer
                    #    continue #don't save the stats
                    else: #update events array
                        events[event] += 1

                    # count repeats and skipgrams
                    if time_gap == 1:
                        events[7] += 1
                    elif time_gap == 2:
                        events[8] += 1

                    distance_counts += 1
                    distance_totals += distance

                    if time_gap > 0:
                        time_gap_counts[self.fingermap[self.keymap[c]].id] += 1 #increase count of this finger
                        time_gap_totals[self.fingermap[self.keymap[c]].id] += time_gap #add the time gap for this finger
                    else:
                        pass #don't consider time gaps for unpressed keys

        # remove double/triple counting of bigrams and trigrams
        events[1] -= events[2] #remove quadgrams from trigrams
        events[0] -= events[2] #remove quadgrams from bigrams
        events[0] -= events[1] #remove trigrams from bigrams

        # calculate finger use factor
        time_gap_averages = time_gap_totals / time_gap_counts
        time_gap_normalized = time_gap_averages / time_gap_averages.sum()
        time_gap_deviation = float(np.std(time_gap_normalized))

        return (events, distance_totals / distance_counts, time_gap_averages, time_gap_deviation)


