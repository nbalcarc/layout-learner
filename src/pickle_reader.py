import pickle
import numpy as np
import numpy.typing as npt
from typing import Any
import matplotlib.pyplot as plt
import os


all_stats = []
layouts = []

pickle_files = sorted(filter(lambda x: x.startswith("output_"), os.listdir("./pickles")))
print(list(pickle_files))
for pickle_file in pickle_files:

    with open(f"pickles/{pickle_file}", "rb") as file:
        dumped: tuple[list[dict[str, Any]], npt.NDArray] = pickle.load(file)

    stats, layout = dumped
    all_stats.extend(stats)
    layouts.append(layout)



rewards = list(map(lambda x: x["reward"], all_stats))

print(len(all_stats))
print(np.array(layouts))


plt.close()
plt.clf()
plt.figure(figsize = (6.4, 4.8), dpi = 100)
plt.plot(list(range(len(rewards))), rewards, label = "Rewards")
#plt.plot(range(smallest), season[3][0:smallest], label = "Predicted")
plt.legend(loc = "lower right")
plt.title("Rewards Over Time")
plt.savefig(f"output_graphs/rewards.png")


